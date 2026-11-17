"""ARINC 615A dual-role conformance simulation package (Track A).

The public package does not export evaluator truth.  Independent IF-EXP-TRUTH
records live under ``a615a_sim.evaluator`` and fail closed to algorithm/arm
importers.  Bound-model FIND/SEND/ABORT/INFORMATION behaviour is SIMULATED-IUT
only and is not a conformance result.
"""

__version__ = "0.0.1"
