import torch
from rl_model import RLModel
from stable_baselines3 import PPO

def analyze_ppo_model(model_path):
    """
    Analyzes a PPO model from Stable Baselines 3
    """
    # Load the model
    model = RLModel.load(model_path)
    policy = model.policy
    
    print("=" * 60)
    print("PPO MODEL ANALYSIS")
    print("=" * 60)
    
    # 1. General information
    print("\n1. GENERAL INFORMATION:")
    print(f"Observation space: {model.observation_space}")
    print(f"Action space: {model.action_space}")
    print(f"Device: {model.device}")
    
    # 2. General architecture
    print("\n2. GENERAL ARCHITECTURE:")
    print(policy)
    
    # 3. Parameter count
    total_params = sum(p.numel() for p in policy.parameters())
    trainable_params = sum(p.numel() for p in policy.parameters() if p.requires_grad)
    
    print(f"\n3. PARAMETERS:")
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    
    # 4. Neural network details
    print("\n4. NEURAL NETWORK DETAILS:")
    
    # Features extractor
    if hasattr(policy, 'features_extractor'):
        print("\nFeatures Extractor:")
        print(policy.features_extractor)
        features_params = sum(p.numel() for p in policy.features_extractor.parameters())
        print(f"Features extractor parameters: {features_params:,}")
    
    # MLP extractor (for policy and value)
    if hasattr(policy, 'mlp_extractor'):
        print("\nMLP Extractor:")
        print(policy.mlp_extractor)
        mlp_params = sum(p.numel() for p in policy.mlp_extractor.parameters())
        print(f"MLP extractor parameters: {mlp_params:,}")
        
        # Separate policy and value networks
        if hasattr(policy.mlp_extractor, 'policy_net'):
            policy_net_params = sum(p.numel() for p in policy.mlp_extractor.policy_net.parameters())
            print(f"Policy network parameters: {policy_net_params:,}")
            
        if hasattr(policy.mlp_extractor, 'value_net'):
            value_net_params = sum(p.numel() for p in policy.mlp_extractor.value_net.parameters())
            print(f"Value network parameters: {value_net_params:,}")
    
    # Action network
    if hasattr(policy, 'action_net'):
        print("\nAction Network:")
        print(policy.action_net)
        action_params = sum(p.numel() for p in policy.action_net.parameters())
        print(f"Action network parameters: {action_params:,}")
    
    # Value network
    if hasattr(policy, 'value_net'):
        print("\nValue Network:")
        print(policy.value_net)
        value_params = sum(p.numel() for p in policy.value_net.parameters())
        print(f"Value network parameters: {value_params:,}")
    
    # 5. Detailed network structure
    print("\n5. DETAILED STRUCTURE:")
    
    # Analyze structure more cleanly
    if hasattr(policy, 'mlp_extractor'):
        mlp = policy.mlp_extractor
        if hasattr(mlp, 'policy_net'):
            print("\nPolicy Network Structure:")
            for i, layer in enumerate(mlp.policy_net):
                if hasattr(layer, 'in_features') and hasattr(layer, 'out_features'):
                    print(f"  Layer {i}: {layer.in_features} → {layer.out_features} ({type(layer).__name__})")
                else:
                    print(f"  Layer {i}: {type(layer).__name__}")
        
        if hasattr(mlp, 'value_net'):
            print("\nValue Network Structure:")
            for i, layer in enumerate(mlp.value_net):
                if hasattr(layer, 'in_features') and hasattr(layer, 'out_features'):
                    print(f"  Layer {i}: {layer.in_features} → {layer.out_features} ({type(layer).__name__})")
                else:
                    print(f"  Layer {i}: {type(layer).__name__}")
    
    # 6. Main Hyperparameters
    print("\n6. MAIN HYPERPARAMETERS:")
    print(f"Gamma (discount factor): {model.gamma}")
    print(f"Learning Rate: {model.learning_rate}")
    print(f"N Steps: {model.n_steps}")
    print(f"Batch Size: {model.batch_size}")
    print(f"N Epochs: {model.n_epochs}")
    print(f"GAE Lambda: {model.gae_lambda}")
    print(f"Clip Range: {model.clip_range}")
    print(f"VF Coef: {model.vf_coef}")
    print(f"Ent Coef: {model.ent_coef}")
    
    # 7. Architectural information
    print("\n7. ARCHITECTURAL INFORMATION:")
    if hasattr(policy, 'features_dim'):
        print(f"Features dimension: {policy.features_dim}")
    
    if hasattr(policy, 'net_arch'):
        print(f"Network architecture: {policy.net_arch}")
    
    # Calculate effective time horizon
    effective_horizon = 1 / (1 - model.gamma) if model.gamma < 1.0 else float('inf')
    print(f"Effective time horizon: {effective_horizon:.1f} steps")
    
    # Gamma interpretation
    if model.gamma >= 0.99:
        sight = "very long-sighted"
    elif model.gamma >= 0.95:
        sight = "long-sighted"
    elif model.gamma >= 0.9:
        sight = "moderately long-sighted"
    else:
        sight = "short-sighted"
    print(f"The model is {sight}")
    
    print("\n" + "=" * 60)
    return model

# Usage example
if __name__ == "__main__":
    # Replace with your model path
    model_path = "ppo_pikavolley_iter.zip"
    
    try:
        analyze_ppo_model(model_path)
    except Exception as e:
        print(f"Error loading the model: {e}")
        print("Make sure the path is correct and the file exists.")
