"""
Bayesian Twin Module — Airframe Digital Twin Inference

Implements particle filter-based Bayesian inference for structural
health monitoring of aerospace components.  Provides damage state
estimation, remaining useful life prediction, risk assessment, and
safety case evidence generation.
"""

from __future__ import annotations

from .engine import (
    BayesianTwinError,
    InferenceError,
    StateError,
    ObservationError,
    DamageType,
    SensorType,
    InspectionResult,
    RecommendedAction,
    SafetyLevel,
    DamageState,
    PhysicsParameters,
    ModelDiscrepancy,
    StateVector,
    SensorReading,
    NDTFinding,
    ObservationSet,
    Particle,
    PosteriorSummary,
    RiskMetrics,
    SafetyCaseEvidence,
    DataQualityFeedback,
    InferenceResult,
    BayesianInferenceEngine,
)

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
