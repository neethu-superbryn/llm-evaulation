# Web Interface Example

This example shows how to use the IntellAgent web interface to evaluate a customer service chatbot.

## Example Agent Prompt

Here's a sample customer service agent prompt you can use to test the web interface:

```markdown
You are a helpful customer service representative for TechCorp, a technology company that sells laptops, smartphones, and accessories. Your role is to assist customers with their inquiries, resolve issues, and provide excellent service.

## Guidelines:
1. **Be Professional and Friendly**: Always maintain a courteous and helpful tone
2. **Listen Actively**: Understand the customer's needs before providing solutions
3. **Provide Accurate Information**: Only give information you're certain about
4. **Escalate When Needed**: If you cannot resolve an issue, escalate to a human agent
5. **Follow Up**: Ensure the customer's issue is fully resolved before ending the conversation

## Available Actions:
- Check order status
- Process returns and exchanges
- Provide product information
- Troubleshoot technical issues
- Schedule service appointments
- Apply discounts or credits when appropriate

## Company Policies:
- 30-day return policy for all products
- 1-year warranty on all devices
- Free shipping on orders over $100
- Price matching within 14 days of purchase

## Tone:
- Professional but warm
- Patient and understanding
- Solution-oriented
- Empathetic to customer concerns

Remember: Your goal is to turn every customer interaction into a positive experience that builds loyalty and trust in the TechCorp brand.
```

## Step-by-Step Evaluation

### 1. Launch the Interface
```bash
python launch_web_interface.py
```

### 2. Configure Your Setup
- **Prompt**: Copy the example prompt above or upload it as a file
- **LLM Provider**: Choose OpenAI (recommended for beginners)
- **Model**: Select `gpt-4o-mini` for cost-effective evaluation
- **Scenarios**: Start with 15-20 scenarios
- **Cost Limit**: Set to $3-5 for initial testing
- **Difficulty**: Use range 5-8 for balanced testing

### 3. Expected Results
With this customer service prompt, you should expect:
- **Success Rate**: 70-85% (good customer service agents handle most scenarios well)
- **Common Failure Points**: 
  - Complex technical issues requiring specialized knowledge
  - Policy edge cases not covered in the prompt
  - Situations requiring human judgment
- **Challenge Areas**: 
  - Angry or frustrated customers
  - Multiple interconnected issues
  - Requests outside company policy

### 4. Analyzing Results
Look for patterns in the failures:
- **Policy Gaps**: Are there policies missing from your prompt?
- **Tone Issues**: Is the agent maintaining professionalism under pressure?
- **Escalation**: Is the agent appropriately escalating complex issues?
- **Information Accuracy**: Is the agent providing correct information?

### 5. Iterating and Improving
Based on results, you might:
- Add more specific policy guidelines
- Include examples of difficult customer interactions
- Clarify escalation procedures
- Add more product-specific information

## Advanced Configuration Example

For more comprehensive testing:

```yaml
# Evaluation Settings
num_samples: 50
cost_limit: 10.0
min_difficulty: 3
max_difficulty: 10
num_workers: 5

# This will generate scenarios covering:
# - Basic inquiries (difficulty 3-5)
# - Complex problems (difficulty 6-8)  
# - Edge cases and stress tests (difficulty 9-10)
```

## Sample Scenarios Generated

The system might generate scenarios like:
- "Customer wants to return a laptop after 35 days"
- "Customer received damaged product and is very upset"
- "Customer asking about a product that doesn't exist"
- "Customer wants price match for competitor's sale price"
- "Customer has multiple issues: billing, shipping, and technical"

## Tips for Better Results

1. **Be Specific**: Include specific policies, procedures, and examples
2. **Cover Edge Cases**: Think about unusual situations your agent might encounter
3. **Define Boundaries**: Clearly state what the agent can and cannot do
4. **Include Examples**: Show the agent how to handle difficult situations
5. **Test Iteratively**: Start small, analyze results, improve, and test again

---

This example demonstrates how the web interface can help you systematically improve your conversational AI agents through comprehensive scenario testing.