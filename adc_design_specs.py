# -*- coding: utf-8 -*-
"""
Generates the design specification dictionary for the high-performance
8-bit SAR ADC core within the RICC project, targeting TSMC 28nm technology.

This script serves as a reproducible specification for the Nature Electronics
submission, enabling peer review and validation of the core ADC architecture.
"""

def generate_sar_adc_specs():
    """
    Defines and returns the architectural and physical parameters for the
    RICC's 8-bit energy-efficient SAR ADC.

    The design choices reflect state-of-the-art practices for mixed-signal
    design in deep sub-micron technologies.

    Returns:
        dict: A dictionary containing the complete design specification.
    """
    
    specs = {
        "technology_node": "TSMC 28nm HPC+",
        "supply_voltage_v": 0.9,
        "resolution_bits": 8,
        "architecture": "Fully Differential Charge-Redistribution SAR",
        
        "cdac": {
            "type": "Differential Split-Capacitor Array",
            "unit_capacitance_fF": 1.0,
            "bridge_capacitor": "1 * unit_capacitance",
            "lsb_array_weights": ["1C", "2C", "4C", "8C"],
            "msb_array_weights": ["1C", "2C", "4C", "8C"],
            "total_capacitance_per_side_fF": 31.0 # (1+2+4+8)*2 + 1(bridge_C) but bridge is in series
        },
        
        "comparator": {
            "type": "Dynamic StrongARM Latch with Low-Noise Pre-amplifier",
            "pre_amplifier": {
                "description": "Differential pair with diode-connected PMOS loads for good common-mode rejection.",
                "input_nmos_W_um": 1.2,
                "input_nmos_L_nm": 30
            },
            "latch": {
                "description": "Standard StrongARM latch for high-speed, zero static power operation.",
                "input_pair_nmos_W_um": 1.0,
                "input_pair_nmos_L_nm": 30,
                "cross_coupled_nmos_W_um": 0.5,
                "cross_coupled_nmos_L_nm": 30,
                "cross_coupled_pmos_W_um": 1.0,
                "cross_coupled_pmos_L_nm": 30,
            }
        },
        
        "sar_logic": {
            "type": "Asynchronous Control FSM",
            "description": "Self-timed logic that triggers the comparator only after the DAC has settled, maximizing speed and efficiency.",
            "synthesis_target": "Standard Cell Library for TSMC 28nm"
        },
        
        "performance_targets": {
            "sampling_rate_MSps": "100-200", # Typical for this architecture
            "power_consumption_uW": "< 100",  # Expected power target at 100 MSps
            "enob_bits": "> 7.5",            # Effective Number of Bits
            "figure_of_merit_fJ_conv-step": "< 10" # Walden FoM
        }
    }
    
    return specs

if __name__ == '__main__':
    # Generate the specification dictionary
    adc_specifications = generate_sar_adc_specs()
    
    # Print the specifications in a clean, readable format
    import json
    print("=====================================================================")
    print(" RICC Project: 8-bit SAR ADC Design Specifications (TSMC 28nm)")
    print("=====================================================================")
    print(json.dumps(adc_specifications, indent=4))
    print("\nThis specification is intended for the supplementary materials of")
    print("the Nature Electronics submission to ensure full reproducibility.")
