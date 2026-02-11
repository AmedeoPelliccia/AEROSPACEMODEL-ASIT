# ASIGT Pipeline Implementation

- Core implementation: `src/aerospacemodel/asigt/pipeline.py` (five-stage AMM pipeline).
- Convenience entry points: `execute_pipeline()` and `create_amm_pipeline()` in the same module.
- Demo run: `examples/run_amm_pipeline_demo.py` shows end-to-end execution from KDB creation through DM/PM/DML generation and CSDB assembly.
- Tests: `tests/test_content_pipeline.py` covers config loading, each stage, and full pipeline behavior.
