# src/hat_framework.py
# (Version 2.0 - Final, Modular, and Manuscript-Consistent)
"""
Defines the physically-grounded noise models for the Hardware-Aware
Training (HAT) framework, as described in our paper "Resilience that Learns."

This module provides the `stochastic_forward_pass` function, which serves as a
PyTorch-based implementation of the "f_physical" model discussed in
Supplementary Note S1.3.
"""

import torch
import torch.nn as nn
import numpy as np

def _apply_reram_conductance_variation(weights, device):
    """Models device-to-device variability based on log-normal distribution.
    See Supplementary Note S1.3, S8.5, and Table S7 for empirical basis."""
    # Sigma values are derived from measured Cell-to-Cell variation in Table S7
    # For simplicity, we use an average sigma. In a full model, this could vary per layer.
    sigma_lognormal = 0.185 # Matches the measured LRS variation
    g_variation = torch.from_numpy(
        np.random.lognormal(mean=0, sigma=sigma_lognormal, size=weights.shape)
    ).float().to(device)
    return weights * g_variation

def _apply_interconnect_parasitics(x):
    """Applies a simplified non-linear model for IR drop on word lines.
    See Supplementary Note S7.4 (Kelvin Sense) for layout-level mitigation."""
    r_line_effect = 0.05 # Effective non-linearity after mitigation
    v_drop_factor = torch.tanh(x * r_line_effect) / (r_line_effect + 1e-9)
    return x * (1 - v_drop_factor)

def _apply_readout_noise_and_quantization(output):
    """Models thermal noise from TIA/ADC and 8-bit quantization.
    See Supplementary Note S7.1-S7.3 for circuit details."""
    # Thermal noise, scaled to typical neural network activation ranges
    thermal_noise_std = 0.001
    thermal_noise = torch.randn_like(output) * thermal_noise_std
    
    # 8-bit ADC quantization
    quant_levels = 2**8
    scaled_output = torch.clamp(output + thermal_noise, -1.0, 1.0)
    quantized_output = torch.round(scaled_output * (quant_levels / 2 - 1)) / (quant_levels / 2 - 1)
    
    return quantized_output

def stochastic_forward_pass(linear_layer, x, is_aged=False):
    """
    Applies a stochastic, hardware-aware forward pass to a linear layer.

    This function serves as the "f_physical" model, combining multiple
    empirically-grounded non-idealities.

    Args:
        linear_layer (nn.Linear): The PyTorch linear layer.
        x (torch.Tensor): The input tensor.
        is_aged (bool): If True, applies additional degradation effects.

    Returns:
        torch.Tensor: The output tensor after applying hardware non-idealities.
    """
    weights = linear_layer.weight
    bias = linear_layer.bias

    # 1. Apply baseline device variations
    noisy_weights = _apply_reram_conductance_variation(weights, x.device)
    effective_inputs = _apply_interconnect_parasitics(x)

    # 2. Simulate hardware aging if specified
    if is_aged:
        # Aging can cause systematic resistance drift and increased noise
        drift_factor = 1.05 # 5% systematic drift
        noise_increase_factor = 1.5
        noisy_weights *= drift_factor
        effective_inputs *= (1/noise_increase_factor) # Simulate SNR degradation

    # 3. Perform the core linear operation
    output = nn.functional.linear(effective_inputs, noisy_weights, bias)
    
    # 4. Apply readout-chain non-idealities
    final_output = _apply_readout_noise_and_quantization(output)
    
    return final_output
