"""
Advanced Agent Implementations

This module provides sophisticated agent implementations ranging from
heuristic-based to LLM-ready architectures.
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from abc import ABC, abstractmethod
from .env import EmergencyResponseEnv


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, env: EmergencyResponseEnv, name: str = "Agent"):
        self.env = env
        self.name = name
        self.episode_memory = []
    
    @abstractmethod
    def get_action(self, state: Dict[str, Any]) -> Dict[str, int]:
        """Get action from state."""
        pass
    
    def reset_episode(self):
        """Reset episode memory."""
        self.episode_memory = []


class PriorityHeuristicAgent(BaseAgent):
    """
    Advanced heuristic agent with multi-factor decision making.
    
    Decision factors:
    1. Severity-weighted prioritization
    2. Distance-optimized ambulance selection
    3. Capacity-aware hospital selection
    4. Wait-time penalties
    """
    
    def __init__(self, env: EmergencyResponseEnv):
        super().__init__(env, name="PriorityHeuristic")
    
    def get_action(self, state: Dict[str, Any]) -> Dict[str, int]:
        """Generate intelligent action with advanced heuristics."""
        # Get available resources
        available_ambulances = [a for a in state["ambulances"] if a["available"]]
        unassigned_emergencies = [e for e in state["emergencies"] if not e["assigned"]]
        available_hospitals = [h for h in state["hospitals"] if h["capacity"] > 0]
        
        if not available_ambulances or not unassigned_emergencies or not available_hospitals:
            return {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
        
        # Score emergencies: severity + wait time penalty
        scored_emergencies = []
        for e in unassigned_emergencies:
            score = (
                e["severity"] * 0.7 +  # 70% weight on severity
                e["time_waiting"] * 0.3  # 30% weight on wait time
            )
            scored_emergencies.append((score, e))
        
        target_emergency = max(scored_emergencies, key=lambda x: x[0])[1]
        
        # Select closest ambulance
        closest_ambulance = min(
            available_ambulances,
            key=lambda a: abs(a["location"] - target_emergency["location"])
        )
        
        # Select best hospital (balance capacity and distance)
        best_hospital = None
        best_score = -float('inf')
        
        for h in available_hospitals:
            capacity_score = h["capacity"] / self.env.hospital_capacity
            distance_score = 1.0 - (abs(h["location"] - target_emergency["location"]) / self.env.grid_size)
            combined_score = 0.6 * capacity_score + 0.4 * distance_score
            
            if combined_score > best_score:
                best_score = combined_score
                best_hospital = h
        
        action = {
            "ambulance_id": closest_ambulance["id"],
            "emergency_id": target_emergency["id"],
            "hospital_id": best_hospital["id"]
        }
        
        self.episode_memory.append(action)
        return action


class ResourceOptimizationAgent(BaseAgent):
    """
    Agent optimized for resource efficiency and load balancing.
    
    Focus: Maximize ambulance utilization and even hospital distribution
    """
    
    def __init__(self, env: EmergencyResponseEnv):
        super().__init__(env, name="ResourceOptimization")
    
    def get_action(self, state: Dict[str, Any]) -> Dict[str, int]:
        """Generate action optimizing for resource efficiency."""
        available_ambulances = [a for a in state["ambulances"] if a["available"]]
        unassigned_emergencies = [e for e in state["emergencies"] if not e["assigned"]]
        available_hospitals = [h for h in state["hospitals"] if h["capacity"] > 0]
        
        if not available_ambulances or not unassigned_emergencies or not available_hospitals:
            return {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
        
        # Select emergency (with severity bias to prevent starvation)
        unassigned_emergencies.sort(key=lambda e: -e["severity"])
        target_emergency = unassigned_emergencies[0]
        
        # Select ambulance (prefer least busy ones for future availability)
        closest_ambulance = min(
            available_ambulances,
            key=lambda a: abs(a["location"] - target_emergency["location"])
        )
        
        # Select hospital with most available capacity (load balancing)
        best_hospital = max(
            available_hospitals,
            key=lambda h: h["capacity"]
        )
        
        action = {
            "ambulance_id": closest_ambulance["id"],
            "emergency_id": target_emergency["id"],
            "hospital_id": best_hospital["id"]
        }
        
        self.episode_memory.append(action)
        return action


class AdaptiveAgent(BaseAgent):
    """
    Adaptive agent that learns from episode feedback and adjusts strategy.
    
    Maintains internal state about:
    - Success rates of decisions
    - Emergency patterns
    - Resource availability trends
    """
    
    def __init__(self, env: EmergencyResponseEnv, learning_rate: float = 0.1):
        super().__init__(env, name="Adaptive")
        self.learning_rate = learning_rate
        self.strategy_weights = {
            "severity": 0.7,
            "distance": 0.2,
            "wait_time": 0.1
        }
        self.success_history = []
    
    def get_action(self, state: Dict[str, Any]) -> Dict[str, int]:
        """Generate action using adaptive weights."""
        available_ambulances = [a for a in state["ambulances"] if a["available"]]
        unassigned_emergencies = [e for e in state["emergencies"] if not e["assigned"]]
        available_hospitals = [h for h in state["hospitals"] if h["capacity"] > 0]
        
        if not available_ambulances or not unassigned_emergencies or not available_hospitals:
            return {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
        
        # Score emergencies with adaptive weights
        scored_emergencies = []
        for e in unassigned_emergencies:
            score = (
                self.strategy_weights["severity"] * (e["severity"] / 10.0) +
                self.strategy_weights["wait_time"] * min(e["time_waiting"] / 20.0, 1.0)
            )
            scored_emergencies.append((score, e))
        
        target_emergency = max(scored_emergencies, key=lambda x: x[0])[1]
        
        # Select closest ambulance
        closest_ambulance = min(
            available_ambulances,
            key=lambda a: abs(a["location"] - target_emergency["location"])
        )
        
        # Select hospital with best balance
        best_hospital = max(
            available_hospitals,
            key=lambda h: h["capacity"]
        )
        
        action = {
            "ambulance_id": closest_ambulance["id"],
            "emergency_id": target_emergency["id"],
            "hospital_id": best_hospital["id"]
        }
        
        self.episode_memory.append(action)
        return action
    
    def update_from_reward(self, reward: float, action_info: Dict[str, Any]):
        """Update strategy based on reward signal."""
        self.success_history.append(reward)
        
        # Adapt weights based on recent performance
        if len(self.success_history) > 10:
            recent_avg = np.mean(self.success_history[-10:])
            if recent_avg > 0.5:
                # Good performance - increase severity weight
                self.strategy_weights["severity"] *= (1 + self.learning_rate)
            else:
                # Poor performance - increase distance weight
                self.strategy_weights["distance"] *= (1 + self.learning_rate)
            
            # Normalize weights
            total = sum(self.strategy_weights.values())
            self.strategy_weights = {k: v/total for k, v in self.strategy_weights.items()}


class LLMReadyAgent(BaseAgent):
    """
    Agent designed to interface with LLM APIs (OpenAI, Claude, etc.).
    
    This agent:
    1. Formats state as natural language
    2. Queries LLM for decision
    3. Parses LLM response into valid action
    
    Example LLM prompt:
    "Given state: 3 emergencies (severity 8,5,3), 2 available ambulances at locations 1,4,
     and 2 hospitals (capacity 2,1), what is the best action?"
    """
    
    def __init__(self, env: EmergencyResponseEnv, llm_client=None):
        super().__init__(env, name="LLMReady")
        self.llm_client = llm_client  # e.g., OpenAI client
        self.fallback_agent = PriorityHeuristicAgent(env)
    
    def state_to_prompt(self, state: Dict[str, Any]) -> str:
        """Convert state to natural language prompt for LLM."""
        prompt = f"""Emergency Response Coordination Task

Current State:
- Active Emergencies: {len(state['emergencies'])}
  {', '.join([f"E{e['id']} (severity {e['severity']}, waiting {e['time_waiting']}s)" 
              for e in state['emergencies'][:5]])}

- Available Ambulances: {sum(1 for a in state['ambulances'] if a['available'])}/{len(state['ambulances'])}
  Locations: {', '.join([f"A{a['id']}@L{a['location']}" for a in state['ambulances'] if a['available']])}

- Hospitals capacity: {', '.join([f"H{h['id']}({h['capacity']}/{self.env.hospital_capacity})" 
                                   for h in state['hospitals']])}

- Traffic level: {state['traffic_level']}/5

Decision: Select which ambulance should respond to which emergency and which hospital to use.
Format: ambulance_id, emergency_id, hospital_id

Choose the assignment that:
1. Prioritizes high-severity cases first
2. Minimizes response time
3. Balances hospital load

Your decision:"""
        return prompt
    
    def parse_llm_response(self, response: str) -> Dict[str, int]:
        """Parse LLM response into action."""
        try:
            # Try to extract numbers from response
            import re
            numbers = re.findall(r'\d+', response)
            if len(numbers) >= 3:
                return {
                    "ambulance_id": int(numbers[0]),
                    "emergency_id": int(numbers[1]),
                    "hospital_id": int(numbers[2])
                }
        except:
            pass
        
        # Fallback to heuristic
        return self.fallback_agent.get_action(self._get_current_state())
    
    def get_action(self, state: Dict[str, Any]) -> Dict[str, int]:
        """Get action from LLM or fallback to heuristic."""
        if self.llm_client is None:
            # No LLM available - use fallback
            return self.fallback_agent.get_action(state)
        
        try:
            # Format state and query LLM
            prompt = self.state_to_prompt(state)
            response = self.llm_client.query(prompt)
            action = self.parse_llm_response(response)
        except Exception as e:
            # Fallback on error
            action = self.fallback_agent.get_action(state)
        
        self.episode_memory.append(action)
        return action


class EnsembleAgent(BaseAgent):
    """
    Ensemble agent that combines multiple agent strategies.
    
    Votes on actions and selects majority or weighted choice.
    """
    
    def __init__(self, env: EmergencyResponseEnv):
        super().__init__(env, name="Ensemble")
        self.agents = [
            PriorityHeuristicAgent(env),
            ResourceOptimizationAgent(env),
            AdaptiveAgent(env)
        ]
        self.weights = [0.4, 0.35, 0.25]  # Agent weights
    
    def get_action(self, state: Dict[str, Any]) -> Dict[str, int]:
        """Get actions from all agents and vote."""
        actions = [agent.get_action(state) for agent in self.agents]
        
        # Simple voting: most common action
        action_counts = {}
        for action in actions:
            key = (action["ambulance_id"], 
                  action["emergency_id"], 
                  action["hospital_id"])
            action_counts[key] = action_counts.get(key, 0) + 1
        
        # Select most voted action
        best_action_tuple = max(action_counts.items(), key=lambda x: x[1])[0]
        
        action = {
            "ambulance_id": best_action_tuple[0],
            "emergency_id": best_action_tuple[1],
            "hospital_id": best_action_tuple[2]
        }
        
        self.episode_memory.append(action)
        return action


def create_agent(env: EmergencyResponseEnv, agent_type: str = "priority") -> BaseAgent:
    """Factory function to create agents."""
    agent_map = {
        "priority": PriorityHeuristicAgent,
        "resource": ResourceOptimizationAgent,
        "adaptive": AdaptiveAgent,
        "ensemble": EnsembleAgent,
        "llm": LLMReadyAgent
    }
    
    if agent_type not in agent_map:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    return agent_map[agent_type](env)
