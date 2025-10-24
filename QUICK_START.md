# 🚀 Quick Start Guide

Get up and running with IntellAgent Web Interface in 3 simple steps!

## Prerequisites
- Python 3.9 or higher
- An API key from one of the supported providers (OpenAI, Azure, Anthropic, or Google)

## Option 1: Automated Setup (Recommended)

```bash
# 1. Run the setup script
./setup.sh

# 2. Activate virtual environment and configure API keys
source venv/bin/activate
python setup_api_keys.py

# 3. Launch the web interface
python launch_web_interface.py
```

## Option 2: Manual Setup

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run health check
python health_check.py

# 4. Configure API keys
python setup_api_keys.py

# 5. Launch web interface
python launch_web_interface.py
```

## Using the Web Interface

1. **Open your browser** to `http://localhost:8501`

2. **Upload your agent prompt** - either paste it directly or upload a file

3. **Configure your LLM** - select provider and model

4. **Set evaluation parameters**:
   - Number of test scenarios (start with 10-20)
   - Cost limit ($3-5 for initial testing)
   - Difficulty range (5-8 for balanced testing)

5. **Run evaluation** - click "Run Evaluation" and wait for results

6. **View results** - switch to "View Results" tab to see detailed analysis

## Example Agent Prompt

Try this customer service agent prompt:

```markdown
You are a helpful customer service representative for TechCorp. 
Your role is to assist customers with inquiries and resolve issues professionally.

Guidelines:
- Be professional and friendly
- Listen to customer needs
- Provide accurate information
- Escalate complex issues when needed
- Follow company policies (30-day returns, 1-year warranty)
```

## Troubleshooting

- **"Module not found" errors**: Make sure virtual environment is activated
- **API key issues**: Run `python setup_api_keys.py` again
- **High costs**: Reduce number of scenarios or use cheaper models
- **Timeout errors**: Reduce parallel workers in settings

## Next Steps

- Check out the [detailed documentation](WEB_INTERFACE_README.md)
- See the [example usage guide](examples/web_interface_example.md)
- Join our [Discord community](https://discord.gg/YWbT87vAau) for support

---

**Need help?** Run `python health_check.py` to diagnose issues.