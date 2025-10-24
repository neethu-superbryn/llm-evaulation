#!/usr/bin/env python3
"""
Health check script for IntellAgent Web Interface
Verifies that all dependencies and configurations are properly set up.
"""

import sys
import os
import importlib
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML"])
    import yaml

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requires Python 3.9+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas', 
        'yaml',
        'langchain',
        'langchain_openai',
        'langchain_core',
        'langchain_community',
        'networkx'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'yaml':
                import yaml
            else:
                importlib.import_module(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   To install missing packages, run:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_file_structure():
    """Check if required files and directories exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'web_interface.py',
        'launch_web_interface.py',
        'setup_api_keys.py',
        'run.py',
        'requirements.txt',
        'simulator/__init__.py',
        'simulator/simulator_executor.py',
        'simulator/env.py'
    ]
    
    required_dirs = [
        'config',
        'simulator',
        'examples'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (missing)")
            all_good = False
    
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ (missing)")
            all_good = False
    
    return all_good

def check_config_files():
    """Check configuration files"""
    print("\n⚙️  Checking configuration files...")
    
    config_files = [
        'config/config_default.yml',
        'config/llm_env.yml'
    ]
    
    all_good = True
    
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    yaml.safe_load(f)
                print(f"   ✅ {config_file} (valid YAML)")
            except yaml.YAMLError as e:
                print(f"   ❌ {config_file} (invalid YAML: {e})")
                all_good = False
        else:
            print(f"   ❌ {config_file} (missing)")
            all_good = False
    
    return all_good

def check_api_keys():
    """Check if API keys are configured"""
    print("\n🔑 Checking API key configuration...")
    
    env_file = "config/llm_env.yml"
    if not os.path.exists(env_file):
        print(f"   ❌ {env_file} not found")
        print("   Run: python setup_api_keys.py")
        return False
    
    try:
        with open(env_file, 'r') as f:
            config = yaml.safe_load(f)
        
        providers_configured = []
        
        # Check each provider
        providers = {
            'openai': 'OPENAI_API_KEY',
            'azure': 'AZURE_OPENAI_API_KEY', 
            'anthropic': 'ANTHROPIC_KEY',
            'google': 'GOOGLE_API_KEY'
        }
        
        for provider, key_field in providers.items():
            if provider in config and config[provider].get(key_field):
                print(f"   ✅ {provider.title()} API key configured")
                providers_configured.append(provider)
            else:
                print(f"   ⚠️  {provider.title()} API key not configured")
        
        if providers_configured:
            print(f"   ✅ {len(providers_configured)} provider(s) configured")
            return True
        else:
            print("   ❌ No API keys configured")
            print("   Run: python setup_api_keys.py")
            return False
            
    except Exception as e:
        print(f"   ❌ Error reading config: {e}")
        return False

def check_write_permissions():
    """Check if we can write to required directories"""
    print("\n✍️  Checking write permissions...")
    
    test_dirs = ['results', 'config']
    all_good = True
    
    for test_dir in test_dirs:
        try:
            os.makedirs(test_dir, exist_ok=True)
            test_file = os.path.join(test_dir, '.write_test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print(f"   ✅ {test_dir}/ (writable)")
        except Exception as e:
            print(f"   ❌ {test_dir}/ (not writable: {e})")
            all_good = False
    
    return all_good

def main():
    """Run all health checks"""
    print("🏥 IntellAgent Web Interface Health Check")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Configuration Files", check_config_files),
        ("API Keys", check_api_keys),
        ("Write Permissions", check_write_permissions)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Health Check Summary")
    print("=" * 50)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} {name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} checks passed")
    
    if passed == len(results):
        print("\n🎉 All checks passed! You're ready to use the web interface.")
        print("   Run: python launch_web_interface.py")
    else:
        print(f"\n⚠️  {len(results) - passed} check(s) failed. Please fix the issues above.")
        
        # Provide specific guidance
        failed_checks = [name for name, result in results if not result]
        
        if "Dependencies" in failed_checks:
            print("\n💡 To install dependencies:")
            print("   pip install -r requirements.txt")
        
        if "API Keys" in failed_checks:
            print("\n💡 To configure API keys:")
            print("   python setup_api_keys.py")
        
        if "File Structure" in failed_checks:
            print("\n💡 Make sure you're running this from the IntellAgent root directory")

if __name__ == "__main__":
    main()