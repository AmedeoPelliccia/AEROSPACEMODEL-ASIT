# =============================================================================
# ASIGT Quantum Module
# Quantum-Accelerated Optimization for Aerospace Design
# =============================================================================
"""
Quantum Module for ASIGT (Aerospace System Information Generation Tool)

Provides quantum computing algorithms for aerospace optimization:
    - QAOA: Quantum Approximate Optimization Algorithm
    - VQE: Variational Quantum Eigensolver
    - QML: Quantum Machine Learning (future)

Example:
    >>> from ASIGT.quantum import create_aerospace_quantum_optimizer
    >>> optimizer = create_aerospace_quantum_optimizer(
    ...     contract_id="KITDM-CTR-QUANTUM-001"
    ... )
    >>> problem = optimizer.formulate_config_selection_problem(
    ...     configurations=pareto_front,
    ...     selection_count=10,
    ...     objective_weights={"fuel_burn": 0.3, "weight": 0.3, "cost": 0.4}
    ... )
    >>> result = optimizer.optimize(problem)
"""

from .quantum_optimizer import (
    # Enumerations
    QuantumAlgorithm,
    QuantumBackendType,
    ProblemType,
    OptimizationStatus,

    # Configurations
    QuantumCircuitConfig,
    QAOAConfig,
    VQEConfig,

    # Data classes
    QUBOProblem,
    QuantumOptimizationResult,

    # Optimizers
    QuantumOptimizer,
    QAOAOptimizer,
    VQEOptimizer,

    # Manager
    QuantumOptimizationManager,

    # Factory functions
    create_aerospace_quantum_optimizer,
    create_fleet_optimization_qubo,
)

__all__ = [
    # Enumerations
    "QuantumAlgorithm",
    "QuantumBackendType",
    "ProblemType",
    "OptimizationStatus",

    # Configurations
    "QuantumCircuitConfig",
    "QAOAConfig",
    "VQEConfig",

    # Data classes
    "QUBOProblem",
    "QuantumOptimizationResult",

    # Optimizers
    "QuantumOptimizer",
    "QAOAOptimizer",
    "VQEOptimizer",

    # Manager
    "QuantumOptimizationManager",

    # Factory functions
    "create_aerospace_quantum_optimizer",
    "create_fleet_optimization_qubo",
]
