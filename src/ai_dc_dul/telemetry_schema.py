from dataclasses import dataclass
from typing import Literal, Optional, Dict, Any
from datetime import datetime

ComponentType = Literal[
    "psu",
    "fan",
    "ssd",
    "cpu",
    "gpu",
    "memory",
    "nic",
    "rack_env",
]

@dataclass
class TelemetryRecord:
    """Unified telemetry record for one component at one timestamp."""
    ts: datetime
    asset_id: str
    component_id: str
    component_type: ComponentType
    vendor: Optional[str] = None
    model: Optional[str] = None
    metrics: Dict[str, float] = None
    target_dul_days: Optional[float] = None
    failed: Optional[int] = None
    meta: Dict[str, Any] = None

def normalize_ocp_metric_name(raw_name: str) -> str:
    name = raw_name.strip().lower()
    mapping = {
        "inputpower": "psu_input_power_w",
        "outputpower": "psu_output_power_w",
        "efficiency": "psu_efficiency_pct",
        "lineinputvoltage": "psu_voltage_v",
        "outputcurrent": "psu_current_a",
        "temperature": "temp_c",
        "temperature1": "temp_c",
        "fanrpm": "fan_rpm",
        "rpm": "fan_rpm",
        "wearlevel": "ssd_wear_pct",
        "percentused": "ssd_wear_pct",
        "ecc_correctable": "ecc_correctable",
        "ecc_uncorrectable": "ecc_uncorrectable",
        # GPU-ish names
        "gputemp": "gpu_temp_c",
        "gpupower": "gpu_power_w",
        "gpumemoryeccerrors": "gpu_mem_err",
        # NIC-ish names
        "rxerrors": "nic_rx_err",
        "txerrors": "nic_tx_err",
        "pciecorrectableerrors": "nic_pcie_ce",
        "pcieuncorrectableerrors": "nic_pcie_ue",
    }
    return mapping.get(name, name)
