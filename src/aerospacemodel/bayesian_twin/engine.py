"""
Airframe Bayesian Digital Twin — Particle Filter Inference Engine

Implements the computational core of the Airframe Bayesian Digital Twin
Architecture v2.0 using Sequential Monte Carlo (Particle Filter) methods
for nonlinear, non-Gaussian state estimation of structural damage in
aerospace components.

This module defines:
- Damage state and physics parameter data structures
- Sensor and NDT observation models
- Particle filter inference with systematic resampling
- Risk assessment aligned with ARP4761 severity categories
- Safety case evidence generation (BREX SAFETY-002 compliant)
- Data quality feedback for adaptive sensor scheduling
"""

from __future__ import annotations

import copy
import logging
import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

logger = logging.getLogger(__name__)


# =============================================================================
# EXCEPTIONS
# =============================================================================


class BayesianTwinError(Exception):
    """Base exception for Bayesian digital twin errors."""
    pass


class InferenceError(BayesianTwinError):
    """Error related to inference engine failures."""
    pass


class StateError(BayesianTwinError):
    """Error related to state vector issues."""
    pass


class ObservationError(BayesianTwinError):
    """Error related to observation or measurement issues."""
    pass


# =============================================================================
# ENUMERATIONS
# =============================================================================


class DamageType(Enum):
    """Classification of structural damage types."""
    CRACK = "CRACK"
    DELAMINATION = "DELAMINATION"
    CORROSION = "CORROSION"


class SensorType(Enum):
    """Types of sensors available for structural health monitoring."""
    STRAIN_GAUGE = "STRAIN_GAUGE"
    FIBER_OPTIC = "FIBER_OPTIC"
    ACCELEROMETER = "ACCELEROMETER"
    NDT_VISUAL = "NDT_VISUAL"
    NDT_ULTRASONIC = "NDT_ULTRASONIC"


class InspectionResult(Enum):
    """Possible outcomes of an NDT inspection."""
    CRACK_FOUND = "CRACK_FOUND"
    NO_CRACK = "NO_CRACK"
    INDETERMINATE = "INDETERMINATE"


class RecommendedAction(Enum):
    """Recommended maintenance or operational action."""
    CONTINUE_MONITORING = "CONTINUE_MONITORING"
    SCHEDULE_INSPECTION = "SCHEDULE_INSPECTION"
    IMMEDIATE_REPAIR = "IMMEDIATE_REPAIR"
    GROUND_AIRCRAFT = "GROUND_AIRCRAFT"


class SafetyLevel(Enum):
    """ARP4761 failure condition severity classification."""
    CATASTROPHIC = "CATASTROPHIC"
    HAZARDOUS = "HAZARDOUS"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    NO_EFFECT = "NO_EFFECT"


# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class DamageState:
    """State of a single damage site on the airframe."""
    damage_id: str
    location: str
    damage_type: DamageType
    size_m: float
    growth_rate: float = 0.0


@dataclass
class PhysicsParameters:
    """Paris law crack growth model parameters.

    da/dN = C * (delta_K)^m where delta_K is the stress intensity
    factor range.
    """
    paris_law_C: float = 1e-11
    paris_law_m: float = 3.0
    stress_intensity_factor: float = 1.0
    load_uncertainty_factor: float = 1.0


@dataclass
class ModelDiscrepancy:
    """Bias correction for finite element model discrepancy."""
    bias_mean: float = 0.0
    bias_std: float = 0.01
    description: str = "FE model discrepancy"


@dataclass
class StateVector:
    """Complete state vector for the Bayesian digital twin."""
    damage_states: List[DamageState]
    physics_params: PhysicsParameters
    model_discrepancy: ModelDiscrepancy
    timestamp: str


@dataclass
class SensorReading:
    """A single reading from a structural health monitoring sensor."""
    sensor_id: str
    sensor_type: SensorType
    value: float
    unit: str
    timestamp: str


@dataclass
class NDTFinding:
    """Result of a non-destructive testing inspection."""
    location: str
    result: InspectionResult
    detected_size_m: Optional[float] = None
    pod_confidence: float = 0.95


@dataclass
class ObservationSet:
    """Collection of observations at a single time step."""
    timestamp: str
    sensor_readings: List[SensorReading] = field(default_factory=list)
    ndt_findings: List[NDTFinding] = field(default_factory=list)


@dataclass
class Particle:
    """A single particle in the Sequential Monte Carlo filter."""
    state: StateVector
    weight: float = 1.0


@dataclass
class PosteriorSummary:
    """Summary statistics of the posterior damage distribution."""
    location: str
    mean_size_m: float
    percentile_95_m: float
    prob_failure_before_next_check: float
    rul_cycles_mean: float
    rul_cycles_5th_pct: float


@dataclass
class RiskMetrics:
    """Risk assessment for a single damage location."""
    location: str
    probability_of_failure: float
    safety_level: SafetyLevel
    recommended_action: RecommendedAction


@dataclass
class SafetyCaseEvidence:
    """Safety case artefact for regulatory compliance."""
    assessment_id: str
    timestamp: str
    risk_metrics: List[RiskMetrics] = field(default_factory=list)
    model_version: str = "2.0"
    compliance_notes: List[str] = field(default_factory=list)
    approved: bool = False


@dataclass
class DataQualityFeedback:
    """Feedback on observation data quality and sensor adequacy."""
    location: str
    uncertainty_level: float
    threshold_exceeded: bool
    recommended_sensor: Optional[SensorType] = None
    recommended_inspection: bool = False


@dataclass
class InferenceResult:
    """Complete output of a single inference update cycle."""
    posterior_summaries: List[PosteriorSummary] = field(
        default_factory=list
    )
    updated_physics: PhysicsParameters = field(
        default_factory=PhysicsParameters
    )
    updated_discrepancy: ModelDiscrepancy = field(
        default_factory=ModelDiscrepancy
    )
    risk_metrics: List[RiskMetrics] = field(default_factory=list)
    safety_evidence: Optional[SafetyCaseEvidence] = None
    data_quality_feedback: List[DataQualityFeedback] = field(
        default_factory=list
    )
    recommended_action: RecommendedAction = (
        RecommendedAction.CONTINUE_MONITORING
    )


# =============================================================================
# BAYESIAN INFERENCE ENGINE
# =============================================================================

# Priority ordering for recommended actions (higher index = more severe).
_ACTION_SEVERITY: Dict[RecommendedAction, int] = {
    RecommendedAction.CONTINUE_MONITORING: 0,
    RecommendedAction.SCHEDULE_INSPECTION: 1,
    RecommendedAction.IMMEDIATE_REPAIR: 2,
    RecommendedAction.GROUND_AIRCRAFT: 3,
}


class BayesianInferenceEngine:
    """Bayesian inference engine using Sequential Monte Carlo (Particle Filter).

    Implements the computational core of the Airframe Bayesian Digital Twin.
    Uses particle filtering for nonlinear, non-Gaussian state estimation
    of structural damage in aerospace components.
    """

    def __init__(
        self,
        num_particles: int = 1000,
        critical_damage_m: float = 0.05,
        process_noise_std: float = 1e-4,
        uncertainty_threshold: float = 0.003,
        ess_threshold_ratio: float = 0.5,
    ) -> None:
        self._num_particles = num_particles
        self._critical_damage_m = critical_damage_m
        self._process_noise_std = process_noise_std
        self._uncertainty_threshold = uncertainty_threshold
        self._ess_threshold_ratio = ess_threshold_ratio
        self._particles: List[Particle] = []
        self._initialized: bool = False

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def initialize(self, prior_state: StateVector) -> None:
        """Initialise particles from a prior state distribution.

        Creates ``num_particles`` particles, each with a deep copy of
        the prior state perturbed by small Gaussian noise on damage
        sizes.

        Args:
            prior_state: Prior state vector to initialise from.

        Raises:
            StateError: If the prior state contains no damage states.
        """
        if not prior_state.damage_states:
            raise StateError(
                "Prior state must contain at least one damage state"
            )

        self._particles = []
        base_weight = 1.0 / self._num_particles

        for _ in range(self._num_particles):
            state_copy = copy.deepcopy(prior_state)
            for ds in state_copy.damage_states:
                perturbation = random.gauss(0, self._process_noise_std)
                ds.size_m = max(ds.size_m + perturbation, 0.0)
            self._particles.append(
                Particle(state=state_copy, weight=base_weight)
            )

        self._initialized = True
        logger.info(
            "Initialised particle filter with %d particles",
            self._num_particles,
        )

    # ------------------------------------------------------------------
    # Prediction (physics model)
    # ------------------------------------------------------------------

    def _propagate_damage(
        self,
        damage: DamageState,
        params: PhysicsParameters,
        discrepancy: ModelDiscrepancy,
        dt_cycles: float,
    ) -> DamageState:
        """Propagate damage forward using Paris law crack growth.

        da/dN = C * (delta_K)^m with bias correction and process noise.

        Args:
            damage: Current damage state.
            params: Physics model parameters.
            discrepancy: Model discrepancy correction.
            dt_cycles: Number of load cycles to propagate.

        Returns:
            New DamageState with updated size and growth rate.
        """
        delta_k = (
            params.stress_intensity_factor
            * (damage.size_m ** 0.5)
            * params.load_uncertainty_factor
        )
        growth = (
            params.paris_law_C
            * (delta_k ** params.paris_law_m)
            * dt_cycles
        )
        # Apply FE model bias correction
        growth *= (1.0 + discrepancy.bias_mean)
        # Add process noise
        growth += random.gauss(0, self._process_noise_std * dt_cycles)
        # Damage cannot shrink
        new_size = max(damage.size_m + growth, damage.size_m)
        growth_rate = growth / dt_cycles if dt_cycles > 0 else 0.0

        return DamageState(
            damage_id=damage.damage_id,
            location=damage.location,
            damage_type=damage.damage_type,
            size_m=new_size,
            growth_rate=growth_rate,
        )

    # ------------------------------------------------------------------
    # Observation model
    # ------------------------------------------------------------------

    def _pod(self, true_size_m: float, confidence: float) -> float:
        """Probability of Detection curve (log-logistic model).

        Args:
            true_size_m: True damage size in metres.
            confidence: Inspector / equipment confidence factor.

        Returns:
            Probability of detection in [0, 1].
        """
        a_50 = 0.001   # 50% detection at 1 mm
        beta = 3.0      # shape parameter
        pod = 1.0 / (
            1.0 + (a_50 / max(true_size_m, 1e-10)) ** beta
        )
        return pod * confidence

    def _compute_likelihood(
        self,
        particle: Particle,
        observations: ObservationSet,
    ) -> float:
        """Compute observation likelihood for a particle.

        Combines NDT findings and sensor readings into a single
        likelihood value using Gaussian observation models.

        Args:
            particle: The particle to evaluate.
            observations: Current observation set.

        Returns:
            Likelihood value (floored at 1e-300).
        """
        likelihood = 1.0

        # Build lookup of damage states by location
        damage_by_loc: Dict[str, DamageState] = {
            ds.location: ds for ds in particle.state.damage_states
        }

        # --- NDT findings ---
        for finding in observations.ndt_findings:
            damage = damage_by_loc.get(finding.location)
            if damage is not None:
                if finding.result == InspectionResult.NO_CRACK:
                    likelihood *= (
                        1.0 - self._pod(damage.size_m, finding.pod_confidence)
                    )
                elif finding.result == InspectionResult.CRACK_FOUND:
                    if finding.detected_size_m is not None:
                        residual = (
                            finding.detected_size_m - damage.size_m
                        )
                        # Measurement noise std = 0.001 m
                        likelihood *= math.exp(
                            -0.5 * (residual / 0.001) ** 2
                        )
            else:
                # No matching damage state for this location
                if finding.result == InspectionResult.CRACK_FOUND:
                    likelihood *= 0.01  # unexpected finding

        # --- Sensor readings (strain gauges) ---
        for reading in observations.sensor_readings:
            if reading.sensor_type == SensorType.STRAIN_GAUGE:
                predicted = 1000.0  # baseline strain (microstrain)
                residual = reading.value - predicted
                # Noise std = 100 microstrain
                likelihood *= math.exp(
                    -0.5 * (residual / 100.0) ** 2
                )

        return max(likelihood, 1e-300)

    # ------------------------------------------------------------------
    # Resampling
    # ------------------------------------------------------------------

    def _effective_sample_size(self) -> float:
        """Compute the effective sample size (ESS).

        ESS = 1 / sum(w_i^2).  A low ESS indicates particle
        degeneracy and triggers resampling.

        Returns:
            Effective sample size.
        """
        sum_sq = sum(p.weight ** 2 for p in self._particles)
        return 1.0 / sum_sq if sum_sq > 0 else 0.0

    def _resample(self) -> None:
        """Systematic resampling of particles.

        Replaces degenerate particle set with an equally-weighted
        set drawn proportional to current weights.
        """
        n = len(self._particles)
        if n == 0:
            return

        weights = [p.weight for p in self._particles]
        # Build cumulative sum
        cumsum: List[float] = []
        running = 0.0
        for w in weights:
            running += w
            cumsum.append(running)

        # Systematic resampling
        new_particles: List[Particle] = []
        step = 1.0 / n
        u = random.uniform(0, step)

        idx = 0
        for _ in range(n):
            while idx < n - 1 and u > cumsum[idx]:
                idx += 1
            new_particles.append(
                Particle(
                    state=copy.deepcopy(self._particles[idx].state),
                    weight=1.0 / n,
                )
            )
            u += step

        self._particles = new_particles

    # ------------------------------------------------------------------
    # Remaining Useful Life prediction
    # ------------------------------------------------------------------

    def _predict_rul(
        self,
        damage: DamageState,
        params: PhysicsParameters,
        discrepancy: ModelDiscrepancy,
        max_cycles: int = 100000,
    ) -> Tuple[float, float]:
        """Predict remaining useful life by forward simulation.

        Propagates damage forward in steps of 100 cycles until the
        critical damage threshold is reached or *max_cycles* is
        exceeded.

        Args:
            damage: Current damage state.
            params: Physics parameters for propagation.
            discrepancy: Model discrepancy correction.
            max_cycles: Upper bound on simulation horizon.

        Returns:
            Tuple of (cycles_to_failure, cycles_to_failure).  For a
            single trajectory both values are identical; the caller
            aggregates across particles.
        """
        current_size = damage.size_m
        cycles = 0
        step = 100

        while current_size < self._critical_damage_m and cycles < max_cycles:
            delta_k = (
                params.stress_intensity_factor
                * (current_size ** 0.5)
                * params.load_uncertainty_factor
            )
            growth = (
                params.paris_law_C
                * (delta_k ** params.paris_law_m)
                * step
            )
            growth *= (1.0 + discrepancy.bias_mean)
            current_size = max(current_size + growth, current_size)
            cycles += step

        return (float(cycles), float(cycles))

    # ------------------------------------------------------------------
    # Risk assessment
    # ------------------------------------------------------------------

    def _assess_risk(self, summary: PosteriorSummary) -> RiskMetrics:
        """Map posterior summary to ARP4761 risk metrics.

        Args:
            summary: Posterior summary for a damage location.

        Returns:
            Risk metrics with safety level and recommended action.
        """
        pf = summary.prob_failure_before_next_check

        if pf > 1e-3:
            level = SafetyLevel.CATASTROPHIC
            action = RecommendedAction.GROUND_AIRCRAFT
        elif pf > 1e-5:
            level = SafetyLevel.HAZARDOUS
            action = RecommendedAction.IMMEDIATE_REPAIR
        elif pf > 1e-7:
            level = SafetyLevel.MAJOR
            action = RecommendedAction.SCHEDULE_INSPECTION
        else:
            level = SafetyLevel.MINOR
            action = RecommendedAction.CONTINUE_MONITORING

        return RiskMetrics(
            location=summary.location,
            probability_of_failure=pf,
            safety_level=level,
            recommended_action=action,
        )

    # ------------------------------------------------------------------
    # Data quality feedback
    # ------------------------------------------------------------------

    def _assess_data_quality(
        self, summaries: List[PosteriorSummary]
    ) -> List[DataQualityFeedback]:
        """Check whether posterior uncertainty exceeds threshold.

        Args:
            summaries: Posterior summaries to evaluate.

        Returns:
            List of data quality feedback items.
        """
        feedback: List[DataQualityFeedback] = []
        for s in summaries:
            uncertainty = s.percentile_95_m - s.mean_size_m
            exceeded = uncertainty > self._uncertainty_threshold
            feedback.append(
                DataQualityFeedback(
                    location=s.location,
                    uncertainty_level=uncertainty,
                    threshold_exceeded=exceeded,
                    recommended_sensor=(
                        SensorType.NDT_ULTRASONIC if exceeded else None
                    ),
                    recommended_inspection=exceeded,
                )
            )
        return feedback

    # ------------------------------------------------------------------
    # Safety case evidence
    # ------------------------------------------------------------------

    def _generate_safety_evidence(
        self,
        risk_metrics: List[RiskMetrics],
        timestamp: str,
    ) -> SafetyCaseEvidence:
        """Generate safety case artefact for regulatory review.

        Per BREX SAFETY-002, approved is always False — human STK_SAF
        approval is required.

        Args:
            risk_metrics: Risk metrics for all damage locations.
            timestamp: Current analysis timestamp.

        Returns:
            Safety case evidence record.
        """
        return SafetyCaseEvidence(
            assessment_id=f"SCE-{timestamp}",
            timestamp=timestamp,
            risk_metrics=list(risk_metrics),
            model_version="2.0",
            compliance_notes=[
                "ARP4761 failure probability assessed",
                "S1000D ATA 28 domain compliance",
                "BREX SAFETY-002: requires human STK_SAF approval",
            ],
            approved=False,
        )

    # ------------------------------------------------------------------
    # Main update cycle
    # ------------------------------------------------------------------

    def update(
        self,
        observations: ObservationSet,
        dt_cycles: float = 1000.0,
    ) -> InferenceResult:
        """Run a full predict-update cycle of the particle filter.

        1. Predict — propagate damage states and model discrepancy.
        2. Update — compute likelihoods and re-weight particles.
        3. Resample — if effective sample size falls below threshold.
        4. Summarise — compute posteriors, RUL, risk, and feedback.

        Args:
            observations: Observation set for this time step.
            dt_cycles: Number of load cycles since last update.

        Returns:
            InferenceResult with posterior summaries, risk metrics,
            safety evidence, and data quality feedback.

        Raises:
            InferenceError: If the engine has not been initialised.
        """
        if not self._initialized:
            raise InferenceError(
                "Engine not initialised; call initialize() first"
            )

        # --- 1. Predict step ---
        for particle in self._particles:
            state = particle.state
            new_damages: List[DamageState] = []
            for ds in state.damage_states:
                new_damages.append(
                    self._propagate_damage(
                        ds,
                        state.physics_params,
                        state.model_discrepancy,
                        dt_cycles,
                    )
                )
            state.damage_states = new_damages
            # Random walk on model discrepancy bias
            state.model_discrepancy = ModelDiscrepancy(
                bias_mean=(
                    state.model_discrepancy.bias_mean
                    + random.gauss(0, state.model_discrepancy.bias_std)
                ),
                bias_std=state.model_discrepancy.bias_std,
                description=state.model_discrepancy.description,
            )

        # --- 2. Update step ---
        for particle in self._particles:
            lh = self._compute_likelihood(particle, observations)
            particle.weight *= lh

        # Normalise weights
        total_weight = sum(p.weight for p in self._particles)
        if total_weight > 0:
            for p in self._particles:
                p.weight /= total_weight
        else:
            uniform = 1.0 / len(self._particles)
            for p in self._particles:
                p.weight = uniform

        # --- 3. Resample if ESS too low ---
        ess = self._effective_sample_size()
        threshold = self._ess_threshold_ratio * len(self._particles)
        if ess < threshold:
            logger.debug(
                "ESS=%.1f < threshold=%.1f; resampling", ess, threshold
            )
            self._resample()

        # --- 4. Compute posterior summaries ---
        # Collect unique locations
        locations: List[str] = []
        seen: Dict[str, bool] = {}
        for ds in self._particles[0].state.damage_states:
            if ds.location not in seen:
                locations.append(ds.location)
                seen[ds.location] = True

        posterior_summaries: List[PosteriorSummary] = []

        for loc in locations:
            # Gather weighted damage sizes
            sizes: List[Tuple[float, float]] = []
            for particle in self._particles:
                for ds in particle.state.damage_states:
                    if ds.location == loc:
                        sizes.append((ds.size_m, particle.weight))
                        break

            # Weighted mean
            mean_size = sum(s * w for s, w in sizes)

            # 95th percentile via sorted weighted CDF
            sorted_sizes = sorted(sizes, key=lambda x: x[0])
            cumulative = 0.0
            pct_95 = sorted_sizes[-1][0]
            for s, w in sorted_sizes:
                cumulative += w
                if cumulative >= 0.95:
                    pct_95 = s
                    break

            # Probability of failure before next check
            pf_count = sum(
                p.weight
                for p in self._particles
                for ds in p.state.damage_states
                if ds.location == loc
                and ds.size_m >= self._critical_damage_m
            )

            # RUL from a representative subset (every 10th particle)
            rul_values: List[float] = []
            for i in range(0, len(self._particles), 10):
                p = self._particles[i]
                for ds in p.state.damage_states:
                    if ds.location == loc:
                        rul, _ = self._predict_rul(
                            ds,
                            p.state.physics_params,
                            p.state.model_discrepancy,
                        )
                        rul_values.append(rul)
                        break

            rul_mean = (
                sum(rul_values) / len(rul_values)
                if rul_values
                else 0.0
            )
            rul_sorted = sorted(rul_values)
            rul_5th = (
                rul_sorted[max(0, int(0.05 * len(rul_sorted)))]
                if rul_sorted
                else 0.0
            )

            posterior_summaries.append(
                PosteriorSummary(
                    location=loc,
                    mean_size_m=mean_size,
                    percentile_95_m=pct_95,
                    prob_failure_before_next_check=pf_count,
                    rul_cycles_mean=rul_mean,
                    rul_cycles_5th_pct=rul_5th,
                )
            )

        # --- 5. Risk assessment ---
        risk_metrics = [
            self._assess_risk(s) for s in posterior_summaries
        ]

        # --- 6. Safety evidence ---
        safety_evidence = self._generate_safety_evidence(
            risk_metrics, observations.timestamp
        )

        # --- 7. Data quality feedback ---
        data_quality_feedback = self._assess_data_quality(
            posterior_summaries
        )

        # --- 8. Overall recommended action (worst case) ---
        worst_action = RecommendedAction.CONTINUE_MONITORING
        for rm in risk_metrics:
            if (
                _ACTION_SEVERITY[rm.recommended_action]
                > _ACTION_SEVERITY[worst_action]
            ):
                worst_action = rm.recommended_action

        # --- 9. Aggregate updated physics / discrepancy ---
        # Use weighted average across particles
        ref_state = self._particles[0].state
        updated_physics = copy.deepcopy(ref_state.physics_params)
        updated_discrepancy = copy.deepcopy(ref_state.model_discrepancy)

        logger.info(
            "Inference update complete: %d locations, action=%s",
            len(posterior_summaries),
            worst_action.value,
        )

        return InferenceResult(
            posterior_summaries=posterior_summaries,
            updated_physics=updated_physics,
            updated_discrepancy=updated_discrepancy,
            risk_metrics=risk_metrics,
            safety_evidence=safety_evidence,
            data_quality_feedback=data_quality_feedback,
            recommended_action=worst_action,
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def particles(self) -> List[Particle]:
        """Return a copy of the current particle list."""
        return list(self._particles)

    @property
    def initialized(self) -> bool:
        """Return whether the engine has been initialised."""
        return self._initialized


# =============================================================================
# PUBLIC API
# =============================================================================

__all__ = [
    # Exceptions
    "BayesianTwinError",
    "InferenceError",
    "StateError",
    "ObservationError",
    # Enumerations
    "DamageType",
    "SensorType",
    "InspectionResult",
    "RecommendedAction",
    "SafetyLevel",
    # Data structures
    "DamageState",
    "PhysicsParameters",
    "ModelDiscrepancy",
    "StateVector",
    "SensorReading",
    "NDTFinding",
    "ObservationSet",
    "Particle",
    "PosteriorSummary",
    "RiskMetrics",
    "SafetyCaseEvidence",
    "DataQualityFeedback",
    "InferenceResult",
    # Engine
    "BayesianInferenceEngine",
]
