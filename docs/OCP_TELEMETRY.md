# OCP Telemetry Mapping

This document describes how common OCP / Redfish fields map into internal metrics.

Examples:

- PSU (PowerSupplies):
  - `InputPower` -> `psu_input_power_w`
  - `OutputPower` -> `psu_output_power_w`
  - `Efficiency` -> `psu_efficiency_pct`
  - `LineInputVoltage` -> `psu_voltage_v`

- Fans (Thermal / Sensors):
  - `Reading` -> `fan_rpm`
  - `UpperThresholdNonCritical` -> `fan_upper_warn`
  - `LowerThresholdCritical` -> `fan_lower_crit`

- NIC 3.0:
  - `RxErrors` -> `nic_rx_err`
  - `TxErrors` -> `nic_tx_err`
  - `PcieCorrectableErrors` -> `nic_pcie_ce`
  - `PcieUncorrectableErrors` -> `nic_pcie_ue`

- Cloud SSD:
  - `PercentUsed` -> `ssd_wear_pct`
  - `MediaErrors` -> `ssd_media_err`
  - `PowerOnHours` -> `ssd_poh`
  - `UnsafeShutdowns` -> `ssd_unsafe_shutdowns`

- GPU:
  - `Temperature` -> `gpu_temp_c`
  - `PowerWatts` -> `gpu_power_w`
  - `MemoryECCErrors` -> `gpu_mem_err`
