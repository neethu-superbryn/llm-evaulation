#!/usr/bin/env python3
"""
Helper script to set up API keys for IntellAgent
"""

import yaml
import os
from pathlib import Path

def setup_api_keys():
    """Interactive setup for API keys"""
    print("🔧 IntellAgent API Key Setup")
    print("=" * 40)
    
    # Load existing config or create new one
    config_path = "config/llm_env.yml"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {
            'openai': {
                'OPENAI_API_KEY': '',
                'OPENAI_API_BASE': '',
                'OPENAI_ORGANIZATION': ''
            },
            'azure': {
                'AZURE_OPENAI_API_KEY': '',
                'AZURE_OPENAI_ENDPOINT': '',
                'OPENAI_API_VERSION': ''
            },
            'google': {
                'GOOGLE_API_KEY': ''
            },
            'anthropic_vertex': {
                'PROJECT_ID': '',
                'REGION': ''
            },
            'anthropic': {
                'ANTHROPIC_KEY': ''
            },
            'oracle': {
                'SERVICE_ENDPOINT': '',
                'COMPARTMENT_ID': ''
            }
        }
    
    print("Which LLM provider would you like to configure?")
    print("1. OpenAI")
    print("2. Azure OpenAI")
    print("3. Anthropic")
    print("4. Google (Gemini)")
    print("5. Skip setup")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        print("\n📝 OpenAI Configuration")
        api_key = input("Enter your OpenAI API key: ").strip()
        if api_key:
            config['openai']['OPENAI_API_KEY'] = api_key
            print("✅ OpenAI API key configured")
    
    elif choice == "2":
        print("\n📝 Azure OpenAI Configuration")
        api_key = input("Enter your Azure OpenAI API key: ").strip()
        endpoint = input("Enter your Azure OpenAI endpoint: ").strip()
        version = input("Enter API version (default: 2024-02-15-preview): ").strip() or "2024-02-15-preview"
        
        if api_key and endpoint:
            config['azure']['AZURE_OPENAI_API_KEY'] = api_key
            config['azure']['AZURE_OPENAI_ENDPOINT'] = endpoint
            config['azure']['OPENAI_API_VERSION'] = version
            print("✅ Azure OpenAI configuration saved")
    
    elif choice == "3":
        print("\n📝 Anthropic Configuration")
        api_key = input("Enter your Anthropic API key: ").strip()
        if api_key:
            config['anthropic']['ANTHROPIC_KEY'] = api_key
            print("✅ Anthropic API key configured")
    
    elif choice == "4":
        print("\n📝 Google (Gemini) Configuration")
        api_key = input("Enter your Google API key: ").strip()
        if api_key:
            config['google']['GOOGLE_API_KEY'] = api_key
            print("✅ Google API key configured")
    
    elif choice == "5":
        print("⏭️  Skipping API key setup")
        return
    
    else:
        print("❌ Invalid choice")
        return
    
    # Save configuration
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"\n✅ Configuration saved to {config_path}")
    print("🚀 You can now run the web interface with: python launch_web_interface.py")

if __name__ == "__main__":
    setup_api_keys()