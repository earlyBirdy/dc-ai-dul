# Telemetry Schema

The central object is `TelemetryRecord`, which represents one component at one timestamp.

Key fields:
- `ts`: datetime
- `asset_id`: server or rack identifier
- `component_id`: PSU1, FAN3, GPU0, etc.
- `component_type`: one of:
  - psu, fan, ssd, cpu, gpu, memory, nic, rack_env
- `metrics`: dict[str, float]
  - Examples:
    - psu_input_power_w
    - psu_output_power_w
    - psu_efficiency_pct
    - fan_rpm
    - ssd_wear_pct
    - ecc_correctable
    - ecc_uncorrectable
    - gpu_temp_c
    - gpu_power_w
    - gpu_mem_err
- `target_dul_days`: optional training label
- `failed`: optional event indicator for survival models
