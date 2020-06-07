from typing import Dict


def generate_base_filter(initial_filter: Dict, times: Dict) -> Dict:
    base_filter: Dict = initial_filter
    if times:
        base_filter["time"] = times
    return base_filter
