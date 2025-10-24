import streamlit as st
import os
import yaml
import tempfile
import shutil
from datetime import datetime
import pandas as pd
import json
from pathlib import Path
import base64

# Import the existing simulator components
from simulator.utils.file_reading import override_config
from simulator.simulator_executor import SimulatorExecutor

# Set page config
st.set_page_config(
    page_title="IntellAgent - Agent Evaluator",
    page_icon="🤖",
    layout="wide"
)

def load_css():
    """Load custom CSS for better styling"""
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .config-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .results-section {
        background-color: #e8f5e8;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .stButton > button {
        background-color: #2E86AB;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #1a5f7a;
    }
    </style>
    """, unsafe_allow_html=True)

def create_config_from_inputs(prompt_text, llm_config, evaluation_config):
    """Create a configuration dictionary from user inputs"""
    
    # Base configuration template
    config = {
        'environment': {
            'prompt': prompt_text,
            'tools_file': '',
            'database_folder': '',
            'database_validators': '',
            'task_description': {
                'llm': llm_config,
                'extraction_prompt': {
                    'prompt_hub_name': 'eladlev/task_extraction'
                }
            }
        },
        'description_generator': {
            'flow_config': {
                'prompt': {
                    'prompt_hub_name': 'eladlev/flows_extraction'
                }
            },
            'policies_config': {
                'prompt': {
                    'prompt_hub_name': 'eladlev/policies_extraction'
                },
                'num_workers': 3,
                'timeout': 20
            },
            'edge_config': {
                'prompt': {
                    'prompt_hub_name': 'eladlev/policies_graph'
                },
                'num_workers': 5,
                'timeout': 20
            },
            'description_config': {
                'prompt': {
                    'prompt_hub_name': 'eladlev/description_generation:c7ecf9ea'
                },
                'num_workers': 3,
                'timeout': 40
            },
            'refinement_config': {
                'do_refinement': False,
                'prompt_feedback': {
                    'prompt_hub_name': 'eladlev/description_refinement'
                },
                'prompt_refinement': {
                    'prompt_hub_name': 'eladlev/refined_description2'
                },
                'num_workers': 3,
                'timeout': 20
            },
            'llm_policy': llm_config,
            'llm_edge': llm_config,
            'llm_description': llm_config,
            'llm_refinement': llm_config
        },
        'event_generator': {
            'symbolic_enrichment_config': {
                'prompt': {
                    'prompt_hub_name': 'eladlev/event_symbolic'
                },
                'num_workers': 3,
                'timeout': 40
            },
            'symbolic_constraints_config': {
                'prompt': {
                    'prompt_hub_name': 'eladlev/symbolic_prompt_constraints'
                },
                'num_workers': 3,
                'timeout': 40
            },
            'event_graph': {
                'llm': llm_config,
                'prompt_restrictions': {
                    'prompt_hub_name': 'eladlev/filter_restrictions'
                },
                'prompt_final_res': {
                    'prompt_hub_name': 'eladlev/event_final'
                },
                'prompt_executors': {
                    'prompt_hub_name': 'eladlev/event_executor'
                },
                'num_workers': 3,
                'timeout': 180
            }
        },
        'dialog_manager': {
            'user_parsing_mode': 'thought',
            'memory_path': "memory.db",
            'user_prompt': {
                'prompt_hub_name': 'eladlev/user_sim'
            },
            'critique_config': {
                'prompt': {
                    'prompt_hub_name': 'eladlev/end_critique'
                },
                'llm': llm_config
            },
            'llm_user': llm_config,
            'llm_chat': llm_config,
            'num_workers': evaluation_config['num_workers'],
            'timeout': 200,
            'mini_batch_size': 10,
            'cost_limit': evaluation_config['cost_limit'],
            'recursion_limit': 35
        },
        'analysis': {
            'prompt': {
                'prompt_hub_name': 'eladlev/analysis_info'
            },
            'llm': llm_config,
            'num_workers': 3,
            'timeout': 20
        },
        'dataset': {
            'name': 'dataset',
            'min_difficult_level': evaluation_config['min_difficulty'],
            'max_difficult_level': evaluation_config['max_difficulty'],
            'num_samples': evaluation_config['num_samples'],
            'mini_batch_size': 10,
            'max_iterations': 100,
            'cost_limit': evaluation_config['cost_limit']
        }
    }
    
    return config

def display_results(results_path):
    """Display the evaluation results"""
    st.markdown('<div class="results-section">', unsafe_allow_html=True)
    st.subheader("📊 Evaluation Results")
    
    # Look for results files
    results_csv = os.path.join(results_path, 'results.csv')
    config_yaml = os.path.join(results_path, 'config.yaml')
    
    if os.path.exists(results_csv):
        # Load and display results
        df = pd.read_csv(results_csv)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Scenarios", len(df))
        
        with col2:
            success_rate = (df['score'] == 1).mean() * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        with col3:
            failure_rate = (df['score'] == 0).mean() * 100
            st.metric("Failure Rate", f"{failure_rate:.1f}%")
        
        with col4:
            avg_challenge = df['challenge_level'].mean()
            st.metric("Avg Challenge Level", f"{avg_challenge:.1f}")
        
        # Detailed results
        st.subheader("Detailed Results")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            score_filter = st.selectbox("Filter by Result", ["All", "Success", "Failure", "Error"])
        with col2:
            challenge_filter = st.slider("Min Challenge Level", 
                                       int(df['challenge_level'].min()), 
                                       int(df['challenge_level'].max()), 
                                       int(df['challenge_level'].min()))
        
        # Apply filters
        filtered_df = df.copy()
        if score_filter == "Success":
            filtered_df = filtered_df[filtered_df['score'] == 1]
        elif score_filter == "Failure":
            filtered_df = filtered_df[filtered_df['score'] == 0]
        elif score_filter == "Error":
            filtered_df = filtered_df[filtered_df['score'] == -1]
        
        filtered_df = filtered_df[filtered_df['challenge_level'] >= challenge_filter]
        
        # Display filtered results
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download results
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name=f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
    else:
        st.warning("No results found. The evaluation may still be running or may have failed.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    load_css()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 IntellAgent - Conversational AI Evaluator</h1>', unsafe_allow_html=True)
    st.markdown("Upload your agent's prompt and configuration to run comprehensive evaluation scenarios")
    
    # Initialize session state
    if 'evaluation_complete' not in st.session_state:
        st.session_state.evaluation_complete = False
    if 'results_path' not in st.session_state:
        st.session_state.results_path = None
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Setup & Run", "View Results"])
    
    if page == "Setup & Run":
        # Agent Prompt Upload Section
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("📝 Agent Prompt")
        
        prompt_input_method = st.radio("How would you like to provide your agent prompt?", 
                                     ["Upload file", "Paste text"])
        
        prompt_text = ""
        if prompt_input_method == "Upload file":
            uploaded_file = st.file_uploader("Upload your agent prompt file", 
                                           type=['txt', 'md'], 
                                           help="Upload a text or markdown file containing your agent's system prompt")
            if uploaded_file is not None:
                prompt_text = str(uploaded_file.read(), "utf-8")
                st.text_area("Preview of uploaded prompt:", prompt_text, height=200, disabled=True)
        else:
            prompt_text = st.text_area("Paste your agent prompt here:", 
                                     height=200,
                                     placeholder="Enter your conversational agent's system prompt...")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # LLM Configuration Section
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.subheader("🔧 LLM Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            llm_provider = st.selectbox("LLM Provider", 
                                      ["openai", "azure", "anthropic", "google"])
            
            if llm_provider == "openai":
                model_name = st.selectbox("Model", 
                                        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"])
            elif llm_provider == "azure":
                model_name = st.text_input("Azure Model Deployment Name", "gpt-4o")
            elif llm_provider == "anthropic":
                model_name = st.selectbox("Model", 
                                        ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"])
            else:  # google
                model_name = st.selectbox("Model", 
                                        ["gemini-1.5-pro", "gemini-1.5-flash"])
        
        with col2:
            st.subheader("API Configuration")
            st.info("Make sure your API keys are set in config/llm_env.yml")
            
            # Show current API key status (without revealing the key)
            env_file = "config/llm_env.yml"
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    env_config = yaml.safe_load(f)
                    
                if llm_provider in env_config:
                    key_field = f"{llm_provider.upper()}_API_KEY" if llm_provider != "anthropic" else "ANTHROPIC_KEY"
                    if llm_provider == "azure":
                        key_field = "AZURE_OPENAI_API_KEY"
                    
                    if key_field in env_config[llm_provider] and env_config[llm_provider][key_field]:
                        st.success(f"✅ {llm_provider.title()} API key configured")
                    else:
                        st.error(f"❌ {llm_provider.title()} API key not found")
                else:
                    st.error(f"❌ {llm_provider.title()} configuration not found")
            else:
                st.error("❌ llm_env.yml not found")
        
        llm_config = {
            'type': llm_provider,
            'name': model_name
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Evaluation Configuration Section
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.subheader("⚙️ Evaluation Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num_samples = st.number_input("Number of Test Scenarios", 
                                        min_value=5, max_value=200, value=20,
                                        help="Number of scenarios to generate and test")
        
        with col2:
            cost_limit = st.number_input("Cost Limit ($)", 
                                       min_value=1.0, max_value=50.0, value=5.0, step=0.5,
                                       help="Maximum cost for the evaluation")
        
        with col3:
            num_workers = st.number_input("Parallel Workers", 
                                        min_value=1, max_value=10, value=3,
                                        help="Number of parallel workers for faster processing")
        
        col1, col2 = st.columns(2)
        with col1:
            min_difficulty = st.slider("Minimum Difficulty Level", 1, 10, 5)
        with col2:
            max_difficulty = st.slider("Maximum Difficulty Level", 1, 10, 10)
        
        evaluation_config = {
            'num_samples': num_samples,
            'cost_limit': cost_limit,
            'num_workers': num_workers,
            'min_difficulty': min_difficulty,
            'max_difficulty': max_difficulty
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Run Evaluation Button
        if st.button("🚀 Run Evaluation", type="primary", use_container_width=True):
            if not prompt_text.strip():
                st.error("Please provide an agent prompt before running the evaluation.")
            else:
                with st.spinner("Running evaluation... This may take several minutes."):
                    try:
                        # Create temporary config
                        config = create_config_from_inputs(prompt_text, llm_config, evaluation_config)
                        
                        # Create output directory
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_path = f"results/web_evaluation_{timestamp}"
                        
                        # Run the evaluation
                        executor = SimulatorExecutor(config, output_path)
                        executor.load_dataset()
                        executor.run_simulation()
                        
                        # Store results path in session state
                        st.session_state.results_path = output_path
                        st.session_state.evaluation_complete = True
                        
                        st.success("✅ Evaluation completed successfully!")
                        st.info("Switch to 'View Results' tab to see the detailed analysis.")
                        
                    except Exception as e:
                        st.error(f"❌ Evaluation failed: {str(e)}")
                        st.exception(e)
    
    elif page == "View Results":
        st.subheader("📊 Evaluation Results")
        
        if st.session_state.evaluation_complete and st.session_state.results_path:
            # Find the latest experiment
            experiments_dir = os.path.join(st.session_state.results_path, 'experiments')
            if os.path.exists(experiments_dir):
                experiments = [d for d in os.listdir(experiments_dir) 
                             if os.path.isdir(os.path.join(experiments_dir, d))]
                if experiments:
                    latest_experiment = sorted(experiments)[-1]
                    experiment_path = os.path.join(experiments_dir, latest_experiment)
                    display_results(experiment_path)
                else:
                    st.warning("No experiment results found.")
            else:
                st.warning("No results directory found.")
        else:
            st.info("No evaluation results available. Please run an evaluation first.")
            
            # Option to load existing results
            st.subheader("Load Existing Results")
            results_dir = st.text_input("Enter path to existing results directory:")
            if st.button("Load Results") and results_dir:
                if os.path.exists(results_dir):
                    st.session_state.results_path = results_dir
                    st.session_state.evaluation_complete = True
                    st.rerun()
                else:
                    st.error("Directory not found.")

if __name__ == "__main__":
    main()