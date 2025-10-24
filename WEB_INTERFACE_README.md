# IntellAgent Web Interface

A user-friendly web interface for evaluating conversational AI agents using the IntellAgent framework.

## 🚀 Quick Start

### 1. Set up API Keys
```bash
python setup_api_keys.py
```
This will guide you through configuring your LLM provider API keys.

### 2. Launch the Web Interface
```bash
python launch_web_interface.py
```
This will start the Streamlit web interface at `http://localhost:8501`

## 📋 Features

### Agent Prompt Upload
- **File Upload**: Upload your agent's system prompt as a `.txt` or `.md` file
- **Text Input**: Paste your prompt directly into the text area
- **Preview**: See a preview of your uploaded prompt before evaluation

### LLM Configuration
- **Multiple Providers**: Support for OpenAI, Azure OpenAI, Anthropic, and Google Gemini
- **Model Selection**: Choose from available models for each provider
- **API Status**: Visual indicators showing if your API keys are properly configured

### Evaluation Settings
- **Number of Scenarios**: Control how many test scenarios to generate (5-200)
- **Cost Limit**: Set a maximum cost limit for the evaluation ($1-$50)
- **Difficulty Range**: Set minimum and maximum difficulty levels (1-10)
- **Parallel Processing**: Configure number of workers for faster processing

### Results Dashboard
- **Summary Metrics**: Success rate, failure rate, average challenge level
- **Detailed Results**: Filterable table with all scenario results
- **Export Options**: Download results as CSV
- **Interactive Filters**: Filter by result type and challenge level

## 🔧 Configuration

### Supported LLM Providers

#### OpenAI
- Models: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-3.5-turbo`
- Required: `OPENAI_API_KEY`

#### Azure OpenAI
- Models: Custom deployment names
- Required: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `OPENAI_API_VERSION`

#### Anthropic
- Models: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`, `claude-3-haiku-20240307`
- Required: `ANTHROPIC_KEY`

#### Google Gemini
- Models: `gemini-1.5-pro`, `gemini-1.5-flash`
- Required: `GOOGLE_API_KEY`

### Manual API Key Configuration

If you prefer to manually configure API keys, edit `config/llm_env.yml`:

```yaml
openai:
  OPENAI_API_KEY: "your-api-key-here"
  OPENAI_API_BASE: ""
  OPENAI_ORGANIZATION: ""

azure:
  AZURE_OPENAI_API_KEY: "your-azure-key"
  AZURE_OPENAI_ENDPOINT: "https://your-resource.openai.azure.com/"
  OPENAI_API_VERSION: "2024-02-15-preview"

anthropic:
  ANTHROPIC_KEY: "your-anthropic-key"

google:
  GOOGLE_API_KEY: "your-google-key"
```

## 📊 Understanding Results

### Metrics Explained

- **Success Rate**: Percentage of scenarios where the agent performed as expected
- **Failure Rate**: Percentage of scenarios where the agent failed to meet expectations
- **Challenge Level**: Average difficulty of the test scenarios (1-10 scale)

### Result Codes
- `1`: Success - Agent handled the scenario correctly
- `0`: Failure - Agent failed to handle the scenario properly
- `-1`: Error - Technical error during evaluation

### Filtering Results
- **By Result Type**: View only successes, failures, or errors
- **By Challenge Level**: Focus on scenarios above a certain difficulty threshold

## 🛠️ Troubleshooting

### Common Issues

#### "API key not found" Error
- Run `python setup_api_keys.py` to configure your API keys
- Verify the `config/llm_env.yml` file contains your keys

#### "Rate limit messages"
- Reduce the number of parallel workers in evaluation settings
- Increase cost limit if using a pay-per-use API

#### "Timeout errors"
- Check your internet connection
- Verify API endpoints are accessible
- Try reducing the number of parallel workers

#### High Costs
- Reduce the number of test scenarios
- Use smaller/cheaper models (e.g., `gpt-4o-mini` instead of `gpt-4o`)
- Set a lower cost limit

### Performance Tips

1. **Start Small**: Begin with 10-20 scenarios to test your setup
2. **Use Appropriate Models**: `gpt-4o-mini` is often sufficient for evaluation tasks
3. **Monitor Costs**: Keep an eye on the cost limit setting
4. **Parallel Processing**: Adjust workers based on your API rate limits

## 📁 File Structure

```
results/
└── web_evaluation_YYYYMMDD_HHMMSS/
    ├── policies_graph/
    │   └── descriptions_generator.pickle
    ├── datasets/
    │   └── dataset__YYYYMMDD_HHMMSS.pickle
    └── experiments/
        └── dataset__exp_1/
            ├── results.csv          # Main results file
            ├── config.yaml          # Evaluation configuration
            ├── prompt.txt           # Agent prompt used
            └── policies_info.json   # Extracted policies
```

## 🔄 Integration with Existing Workflow

The web interface generates the same output format as the command-line version, so you can:

1. Use the existing visualization tools:
   ```bash
   streamlit run simulator/visualization/Simulator_Visualizer.py
   ```

2. Process results with custom scripts using the CSV output

3. Compare results across different agent versions

## 🆘 Support

If you encounter issues:

1. Check the [main README](README.md) for general troubleshooting
2. Verify your API keys are correctly configured
3. Review the console output for detailed error messages
4. Join the [Discord community](https://discord.gg/YWbT87vAau) for support

## 🎯 Next Steps

After running your evaluation:

1. **Analyze Results**: Look for patterns in failures and successes
2. **Iterate on Prompts**: Use insights to improve your agent's prompt
3. **Compare Versions**: Run evaluations on different prompt versions
4. **Scale Up**: Increase scenario count for more comprehensive testing

---

*For more information about the IntellAgent framework, see the [main documentation](README.md).*