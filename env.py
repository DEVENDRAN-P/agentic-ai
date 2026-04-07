"""
Emergency Response Environment for Smart Emergency Response Systems
Implements OpenEnv framework with realistic constraints and reward shaping
"""

import numpy as np
import gymnasium as gym
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Emergency severity levels"""
    LOW = 1
    MEDIUM = 5
    HIGH = 8
    CRITICAL = 10


@dataclass
class Emergency:
    """Emergency case data structure"""
    id: int
    severity: int  # 1-10 scale
    location: Tuple[float, float]  # (latitude, longitude)
    waiting_time: int  # seconds since reported
    time_to_live: int  # max response time before critical


@dataclass
class Ambulance:
    """Ambulance resource data structure"""
    id: int
    location: Tuple[float, float]
    status: str  # 'available', 'on_route', 'at_hospital'
    response_time: int  # seconds to reach emergency
    capacity: int  # number of patients it can carry


@dataclass
class Hospital:
    """Hospital resource data structure"""
    id: int
    location: Tuple[float, float]
    capacity: int  # total beds
    available_beds: int
    specialization: List[str]  # medical specializations


@dataclass
class Traffic:
    """Traffic condition data structure"""
    road_id: int
    congestion_level: float  # 0.0 (clear) to 1.0 (gridlock)
    travel_time_multiplier: float  # multiplier for base travel time


class EmergencyResponseEnv(gym.Env):
    """
    OpenEnv-compliant emergency response environment
    State: emergencies, ambulances, hospitals, traffic conditions
    Action: {ambulance_id, emergency_id, hospital_id}
    Reward: priority_handling + response_speed + resource_usage
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__()
        
        # Configuration
        self.config = {
            'num_ambulances': 5,
            'num_hospitals': 3,
            'num_emergencies': 10,
            'map_size': (100.0, 100.0),  # 100x100 km area
            'max_response_time': 1800,  # 30 minutes in seconds
            'traffic_density': 0.3,
            'seed': None
        }
        if config:
            self.config.update(config)
        
        # Random number generator
        self.rng = np.random.default_rng(self.config['seed'])
        
        # Environment state
        self.emergencies: List[Emergency] = []
        self.ambulances: List[Ambulance] = []
        self.hospitals: List[Hospital] = []
        self.traffic: List[Traffic] = []
        
        # Episode tracking
        self.current_step = 0
        self.total_response_time = 0
        self.successful_responses = 0
        self.failed_responses = 0
        
        # Action and observation space
        self.action_space = gym.spaces.Dict({
            'ambulance_id': gym.spaces.Discrete(self.config['num_ambulances']),
            'emergency_id': gym.spaces.Discrete(self.config['num_emergencies']),
            'hospital_id': gym.spaces.Discrete(self.config['num_hospitals'])
        })
        
        # Enhanced observation space with more detailed state information
        self.observation_space = gym.spaces.Dict({
            'emergencies': gym.spaces.Box(low=0, high=1, shape=(self.config['num_emergencies'], 7)),  # severity, waiting, ttl, x, y, priority_score, urgency
            'ambulances': gym.spaces.Box(low=0, high=1, shape=(self.config['num_ambulances'], 6)),  # status, x, y, response_time, distance_to_nearest, availability_score
            'hospitals': gym.spaces.Box(low=0, high=1, shape=(self.config['num_hospitals'], 5)),  # capacity, x, y, specialization_match, distance_score
            'traffic': gym.spaces.Box(low=0, high=1, shape=(self.config['num_emergencies'] * self.config['num_ambulances'], 2)),  # congestion, travel_multiplier
            'metrics': gym.spaces.Box(low=0, high=1, shape=(1, 4))  # avg_response_time, success_rate, resource_utilization, priority_handling
        })
        
        # Action validation constraints
        self.action_constraints = {
            'max_response_time': self.config['max_response_time'],
            'min_severity_priority': 7,  # Minimum severity for priority handling
            'max_waiting_time': 600,  # 10 minutes
            'min_hospital_capacity': 0.2  # 20% capacity threshold
        }
    
    def reset(self, seed: int = None, options: Dict = None) -> Tuple[Dict[str, np.ndarray], Dict]:
        """Reset environment to initial state"""
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        
        # Generate new emergencies
        self.emergencies = self._generate_emergencies()
        
        # Generate ambulances
        self.ambulances = self._generate_ambulances()
        
        # Generate hospitals
        self.hospitals = self._generate_hospitals()
        
        # Generate traffic conditions
        self.traffic = self._generate_traffic()
        
        # Reset episode tracking
        self.current_step = 0
        self.total_response_time = 0
        self.successful_responses = 0
        self.failed_responses = 0
        
        return self._get_observation(), {}
    
    def step(self, action: Dict[str, int]) -> Tuple[Dict[str, np.ndarray], float, bool, Dict]:
        """Execute one step in the environment"""
        ambulance_id = action['ambulance_id']
        emergency_id = action['emergency_id']
        hospital_id = action['hospital_id']
        
        # Validate action
        reward = 0.0
        done = False
        info = {}
        
        # Check if ambulance is available
        ambulance = self.ambulances[ambulance_id]
        if ambulance.status != 'available':
            reward -= 0.5  # Penalty for using busy ambulance
            info['reason'] = 'ambulance_busy'
        else:
            # Check if emergency exists
            if emergency_id >= len(self.emergencies) or self.emergencies[emergency_id] is None:
                reward -= 1.0  # Penalty for invalid emergency
                info['reason'] = 'invalid_emergency'
            else:
                emergency = self.emergencies[emergency_id]
                
                # Check if hospital has capacity
                hospital = self.hospitals[hospital_id]
                if hospital.available_beds <= 0:
                    reward -= 0.8  # Penalty for full hospital
                    info['reason'] = 'hospital_full'
                else:
                    # Calculate response time
                    response_time = self._calculate_response_time(ambulance, emergency)
                    
                    # Check if response is within acceptable time
                    if response_time > self.config['max_response_time']:
                        reward -= 0.6  # Penalty for slow response
                        info['reason'] = 'slow_response'
                    else:
                        # Successful response
                        reward += self._calculate_reward(emergency, response_time)
                        self.successful_responses += 1
                        self.total_response_time += response_time
                        
                        # Update ambulance status
                        ambulance.status = 'on_route'
                        ambulance.response_time = response_time
                        
                        # Update hospital capacity
                        hospital.available_beds -= 1
                        
                        # Remove emergency from active list
                        self.emergencies[emergency_id] = None
                        
                        info['reason'] = 'successful_response'
        
        # Update traffic conditions
        self._update_traffic()
        
        # Check if episode is done (all emergencies handled or max steps reached)
        active_emergencies = sum(1 for e in self.emergencies if e is not None)
        self.current_step += 1
        
        if active_emergencies == 0 or self.current_step >= 100:
            done = True
            info['total_response_time'] = self.total_response_time
            info['successful_responses'] = self.successful_responses
            info['failed_responses'] = self.failed_responses
        
        return self._get_observation(), reward, done, info
    
    def _generate_emergencies(self) -> List[Emergency]:
        """Generate random emergencies with varying severity and locations"""
        emergencies = []
        for i in range(self.config['num_emergencies']):
            severity = self.rng.choice([1, 5, 8, 10], p=[0.4, 0.3, 0.2, 0.1])
            location = (
                self.rng.uniform(0, self.config['map_size'][0]),
                self.rng.uniform(0, self.config['map_size'][1])
            )
            waiting_time = self.rng.integers(0, 300)  # 0-5 minutes
            time_to_live = self.rng.integers(600, 1800)  # 10-30 minutes
            
            emergencies.append(Emergency(
                id=i,
                severity=severity,
                location=location,
                waiting_time=waiting_time,
                time_to_live=time_to_live
            ))
        
        return emergencies
    
    def _generate_ambulances(self) -> List[Ambulance]:
        """Generate ambulances with random locations"""
        ambulances = []
        for i in range(self.config['num_ambulances']):
            location = (
                self.rng.uniform(0, self.config['map_size'][0]),
                self.rng.uniform(0, self.config['map_size'][1])
            )
            
            ambulances.append(Ambulance(
                id=i,
                location=location,
                status='available',
                response_time=0,
                capacity=2  # Can carry 2 patients
            ))
        
        return ambulances
    
    def _generate_hospitals(self) -> List[Hospital]:
        """Generate hospitals with varying capacities"""
        hospitals = []
        for i in range(self.config['num_hospitals']):
            location = (
                self.rng.uniform(0, self.config['map_size'][0]),
                self.rng.uniform(0, self.config['map_size'][1])
            )
            capacity = self.rng.integers(50, 200)
            specialization = self.rng.choice([
                ['trauma', 'cardiology'],
                ['pediatrics', 'emergency'],
                ['general', 'surgery']
            ], p=[0.4, 0.3, 0.3])
            
            hospitals.append(Hospital(
                id=i,
                location=location,
                capacity=capacity,
                available_beds=capacity,
                specialization=specialization
            ))
        
        return hospitals
    
    def _generate_traffic(self) -> List[Traffic]:
        """Generate traffic conditions between all locations"""
        traffic = []
        for i in range(self.config['num_emergencies'] * self.config['num_ambulances']):
            congestion_level = self.rng.beta(2, 5)  # Skewed toward lower congestion
            travel_time_multiplier = 1.0 + congestion_level * 2.0
            
            traffic.append(Traffic(
                road_id=i,
                congestion_level=congestion_level,
                travel_time_multiplier=travel_time_multiplier
            ))
        
        return traffic
    
    def _calculate_response_time(self, ambulance: Ambulance, emergency: Emergency) -> int:
        """Calculate response time based on distance and traffic"""
        distance = np.linalg.norm(np.array(ambulance.location) - np.array(emergency.location))
        base_time = distance / 60.0 * 3600  # 60 km/h speed
        
        # Apply traffic multiplier
        traffic_index = (ambulance.id * len(self.emergencies) + emergency.id) % len(self.traffic)
        traffic = self.traffic[traffic_index]
        
        return int(base_time * traffic.travel_time_multiplier)
    
    def _calculate_reward(self, emergency: Emergency, response_time: int) -> float:
        """Calculate reward based on priority handling and efficiency"""
        # Base reward for successful response
        base_reward = 1.0
        
        # Priority bonus for high severity cases
        severity_bonus = emergency.severity / 10.0 * 0.5
        
        # Response time penalty (faster is better)
        max_time = self.config['max_response_time']
        time_penalty = max(0, (response_time / max_time) - 0.5) * -0.3
        
        # Waiting time consideration
        waiting_bonus = min(emergency.waiting_time / 300.0, 0.2) * -0.2
        
        return base_reward + severity_bonus + time_penalty + waiting_bonus
    
    def _update_traffic(self):
        """Update traffic conditions over time"""
        for traffic in self.traffic:
            # Traffic gradually changes over time
            change = self.rng.normal(0, 0.05)
            traffic.congestion_level = np.clip(traffic.congestion_level + change, 0.0, 1.0)
            traffic.travel_time_multiplier = 1.0 + traffic.congestion_level * 2.0
    
    def _get_observation(self) -> Dict[str, np.ndarray]:
        """Get current observation of the environment"""
        emergencies_obs = []
        for emergency in self.emergencies:
            if emergency is None:
                emergencies_obs.append([0.0, 0.0, 0.0, 0.0, 0.0])
            else:
                # Normalize values to 0-1 range
                severity_norm = emergency.severity / 10.0
                waiting_norm = min(emergency.waiting_time / 300.0, 1.0)
                ttl_norm = min(emergency.time_to_live / 1800.0, 1.0)
                x_norm = emergency.location[0] / self.config['map_size'][0]
                y_norm = emergency.location[1] / self.config['map_size'][1]
                
                emergencies_obs.append([
                    severity_norm,
                    waiting_norm,
                    ttl_norm,
                    x_norm,
                    y_norm
                ])
        
        ambulances_obs = []
        for ambulance in self.ambulances:
            status_norm = 1.0 if ambulance.status == 'available' else 0.0
            x_norm = ambulance.location[0] / self.config['map_size'][0]
            y_norm = ambulance.location[1] / self.config['map_size'][1]
            response_norm = min(ambulance.response_time / self.config['max_response_time'], 1.0)
            
            ambulances_obs.append([
                status_norm,
                x_norm,
                y_norm,
                response_norm
            ])
        
        hospitals_obs = []
        for hospital in self.hospitals:
            capacity_norm = hospital.available_beds / hospital.capacity
            x_norm = hospital.location[0] / self.config['map_size'][0]
            y_norm = hospital.location[1] / self.config['map_size'][1]
            
            hospitals_obs.append([
                capacity_norm,
                x_norm,
                y_norm
            ])
        
        traffic_obs = []
        for traffic in self.traffic:
            traffic_obs.append([traffic.congestion_level])
        
        return {
            'emergencies': np.array(emergencies_obs),
            'ambulances': np.array(ambulances_obs),
            'hospitals': np.array(hospitals_obs),
            'traffic': np.array(traffic_obs)
        }


# Example usage
if __name__ == "__main__":
    env = EmergencyResponseEnv()
    
    print("Emergency Response Environment")
    print("=" * 50)
    
    # Test reset
    obs, info = env.reset()
    print(f"Initial observation keys: {obs.keys()}")
    
    # Test step
    action = {
        'ambulance_id': 0,
        'emergency_id': 0,
        'hospital_id': 0
    }
    obs, reward, done, info = env.step(action)
    
    print(f"Action: {action}")
    print(f"Reward: {reward:.2f}")
    print(f"Done: {done}")
    print(f"Info: {info}")
    
    print(f"\nEnvironment summary:")
    print(f"  Successful responses: {env.successful_responses}")
    print(f"  Failed responses: {env.failed_responses}")
    print(f"  Total response time: {env.total_response_time} seconds")