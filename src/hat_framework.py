# src/hat_framework.py
# Defines the hardware non-idealities for the RICC's AIMC core.

import torch
import torch.nn as nn
import numpy as np

# This is the heart of the HAT methodology.
# It models the physical computation y = f_physical(x, W, P_noise)
def stochastic_forward_pass(linear_layer, x):
    """
    Applies a stochastic, hardware-aware forward pass to a linear layer.

    Args:
        linear_layer (nn.Linear): The PyTorch linear layer.
        x (torch.Tensor): The input tensor.

    Returns:
        torch.Tensor: The output tensor after applying hardware noise.
    """
    weights = linear_layer.weight
    bias = linear_layer.bias

    # 1. ReRAM Conductance Variation (Log-Normal Distribution)
    # Mean=0, Sigma=0.12 (in log-space) models physical variability.
    g_variation = torch.from_numpy(
        np.random.lognormal(mean=0, sigma=0.12, size=weights.shape)
    ).float().to(x.device)
    noisy_weights = weights * g_variation

    # 2. Interconnect Parasitics (IR Drop Model) - Simplified
    # A simple non-linear scaling simulates voltage drop. A real model is more complex.
    r_line_effect = 0.05 
    v_drop_factor = torch.tanh(x * r_line_effect) / (r_line_effect + 1e-9)
    effective_inputs = x * (1 - v_drop_factor)
    
    # 3. Perform the core operation
    output = nn.functional.linear(effective_inputs, noisy_weights, bias)
    
    # 4. Readout Noise and Quantization
    # Add thermal noise and simulate 8-bit ADC quantization
    thermal_noise_std = 0.8e-3 # Scaled for typical NN outputs
    thermal_noise = torch.randn_like(output) * thermal_noise_std
    
    # Quantization
    output_with_noise = output + thermal_noise
    quant_levels = 2**8
    scaled_output = torch.clamp(output_with_noise, -1.0, 1.0) # Assume output range [-1, 1]
    quantized_output = torch.round(scaled_output * (quant_levels / 2)) / (quant_levels / 2)
    
    return quantized_output
