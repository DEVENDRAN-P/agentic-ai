#!/usr/bin/env python3
"""
Gradio Web Interface for OpenEnv Inference
"""

import os
import json
from typing import Tuple
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.env import EmergencyResponseEnv
from src.inference import RandomBaselineAgent, SmartHeuristicAgent
from src.graders import create_grader_for_task

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

TASKS = ["easy", "medium", "hard"]
MODELS = ["random", "heuristic"]
MAX_EPISODES = 10


def run_inference(task: str, model: str, episodes: int) -> Tuple[str, str]:
    """Run inference and return results"""
    try:
        # Validate inputs
        episodes = min(max(int(episodes), 1), MAX_EPISODES)
        
        if task not in TASKS:
            return "Error", f"Invalid task. Choose from: {', '.join(TASKS)}"
        
        if model not in MODELS:
            return "Error", f"Invalid model. Choose from: {', '.join(MODELS)}"
        
        # Initialize environment
        env = EmergencyResponseEnv()
        
        # Initialize agent
        if model == "random":
            agent = RandomBaselineAgent(env.action_space)
        else:
            agent = SmartHeuristicAgent(env.action_space, env.observation_space)
        
        # Initialize grader
        grader = create_grader_for_task(task)
        
        # Run episodes
        results = {
            "task": task,
            "model": model,
            "episodes_run": episodes,
            "episode_scores": [],
            "total_reward": 0.0,
            "average_score": 0.0
        }
        
        for episode in range(episodes):
            obs, info = env.reset(seed=episode)
            episode_reward = 0.0
            done = False
            step_count = 0
            
            while not done and step_count < 100:
                action = agent.act(obs)
                obs, reward, terminated, truncated, info = env.step(action)
                episode_reward += reward
                done = terminated or truncated
                step_count += 1
            
            # Grade episode
            score = grader.grade(episode_reward, step_count)
            results["episode_scores"].append({
                "episode": episode + 1,
                "reward": float(episode_reward),
                "steps": step_count,
                "score": float(score)
            })
            results["total_reward"] += episode_reward
        
        # Calculate averages
        results["average_score"] = sum(e["score"] for e in results["episode_scores"]) / episodes
        results["average_reward"] = results["total_reward"] / episodes
        
        # Format output
        output_text = f"""
✅ Inference Complete

Task: {task}
Model: {model}
Episodes: {episodes}

Results:
- Average Reward: {results['average_reward']:.3f}
- Average Score: {results['average_score']:.3f}
- Total Reward: {results['total_reward']:.3f}

Episode Details:
"""
        for ep in results["episode_scores"]:
            output_text += f"\n  Episode {ep['episode']}: Reward={ep['reward']:.2f}, Steps={ep['steps']}, Score={ep['score']:.3f}"
        
        json_output = json.dumps(results, indent=2)
        
        return output_text, json_output
        
    except Exception as e:
        error_msg = f"Error during inference: {str(e)}"
        return error_msg, json.dumps({"error": str(e)})


# Create Gradio interface
def create_interface():
    with gr.Blocks(title="OpenEnv Inference") as interface:
        gr.Markdown("# OpenEnv Emergency Response Inference")
        gr.Markdown("Run inference on the Emergency Response environment with different models and difficulty levels.")
        
        with gr.Row():
            with gr.Column():
                task_selector = gr.Radio(
                    choices=TASKS,
                    value="easy",
                    label="Task Difficulty",
                    info="Select the difficulty level"
                )
                model_selector = gr.Radio(
                    choices=MODELS,
                    value="random",
                    label="Model",
                    info="Select the agent model"
                )
                episodes_slider = gr.Slider(
                    minimum=1,
                    maximum=MAX_EPISODES,
                    value=5,
                    step=1,
                    label="Number of Episodes",
                    info="How many episodes to run"
                )
                run_button = gr.Button("Run Inference", variant="primary", size="lg")
        
        with gr.Row():
            with gr.Column():
                output_text = gr.Textbox(
                    label="Results",
                    interactive=False,
                    lines=15
                )
            with gr.Column():
                json_output = gr.JSON(
                    label="Detailed Results (JSON)"
                )
        
        # Connect button to function
        run_button.click(
            fn=run_inference,
            inputs=[task_selector, model_selector, episodes_slider],
            outputs=[output_text, json_output]
        )
    
    return interface


if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_name="0.0.0.0", server_port=7860, share=False)
