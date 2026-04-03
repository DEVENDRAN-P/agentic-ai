"""
Event System for Dynamic Environment Behavior

Generates random events that create realistic emergency scenarios
and adds complexity to decision-making.
"""

import random
from typing import Dict, List, Any
from enum import Enum
from dataclasses import dataclass


class EventType(Enum):
    """Types of events that can occur."""
    MAJOR_INCIDENT = "major_incident"
    HOSPITAL_REDUCED_CAPACITY = "hospital_reduced_capacity"
    TRAFFIC_INCIDENT = "traffic_incident"
    AMBULANCE_BREAKDOWN = "ambulance_breakdown"
    AMBULANCE_AVAILABLE = "ambulance_available"
    HOSPITAL_CAPACITY_RESTORED = "hospital_capacity_restored"


@dataclass
class Event:
    """Represents a dynamic event."""
    type: EventType
    step: int
    description: str
    impact: Dict[str, Any]


class EventGenerator:
    """Generates random events during simulation."""
    
    def __init__(self, base_probability: float = 0.05):
        """
        Initialize event generator.
        
        Args:
            base_probability: Base probability of event occurring each step
        """
        self.base_probability = base_probability
        self.event_history: List[Event] = []
    
    def generate_events(self, env, step: int) -> List[Event]:
        """
        Generate events for current step.
        
        Args:
            env: EmergencyResponseEnv instance
            step: Current step number
        
        Returns:
            List of events that occur
        """
        events = []
        
        if random.random() < self.base_probability:
            # Major incident
            if random.random() < 0.3:
                event = self._create_major_incident_event(env, step)
                events.append(event)
            
            # Traffic incident
            elif random.random() < 0.25:
                event = self._create_traffic_incident_event(env, step)
                events.append(event)
            
            # Hospital capacity issue
            elif random.random() < 0.2:
                event = self._create_hospital_event(env, step)
                events.append(event)
            
            # Ambulance breakdown
            elif random.random() < 0.15:
                event = self._create_ambulance_breakdown_event(env, step)
                events.append(event)
        
        self.event_history.extend(events)
        return events
    
    def _create_major_incident_event(self, env, step: int) -> Event:
        """Create a major incident (multiple high-severity emergencies)."""
        num_new_emergencies = random.randint(2, 4)
        new_emergencies = []
        
        for _ in range(num_new_emergencies):
            new_emergencies.append({
                "severity": random.randint(7, 10),
                "location": random.randint(0, env.grid_size - 1)
            })
        
        return Event(
            type=EventType.MAJOR_INCIDENT,
            step=step,
            description=f"Major incident: {num_new_emergencies} high-severity emergencies spawned",
            impact={
                "new_emergencies": new_emergencies,
                "difficulty_multiplier": 1.5
            }
        )
    
    def _create_traffic_incident_event(self, env, step: int) -> Event:
        """Create traffic incident increasing travel times."""
        duration = random.randint(5, 15)
        traffic_increase = random.randint(1, 3)
        
        return Event(
            type=EventType.TRAFFIC_INCIDENT,
            step=step,
            description=f"Traffic incident: travel times increased by {traffic_increase}x for {duration} steps",
            impact={
                "traffic_factor_increase": traffic_increase,
                "duration": duration
            }
        )
    
    def _create_hospital_event(self, env, step: int) -> Event:
        """Create hospital capacity reduction event."""
        hospital_id = random.randint(1, len(env.hospitals))
        reduction = random.randint(1, 3)
        
        return Event(
            type=EventType.HOSPITAL_REDUCED_CAPACITY,
            step=step,
            description=f"Hospital {hospital_id} capacity reduced by {reduction} beds",
            impact={
                "hospital_id": hospital_id,
                "capacity_reduction": reduction
            }
        )
    
    def _create_ambulance_breakdown_event(self, env, step: int) -> Event:
        """Create ambulance breakdown event."""
        ambulance_id = random.randint(1, len(env.ambulances))
        repair_time = random.randint(10, 30)
        
        return Event(
            type=EventType.AMBULANCE_BREAKDOWN,
            step=step,
            description=f"Ambulance {ambulance_id} broken down, repair time: {repair_time} steps",
            impact={
                "ambulance_id": ambulance_id,
                "repair_time": repair_time
            }
        )
    
    def apply_event(self, env, event: Event):
        """Apply event effects to environment."""
        if event.type == EventType.MAJOR_INCIDENT:
            for new_emergency in event.impact["new_emergencies"]:
                emergency = {
                    "id": len(env.emergencies) + 1,
                    "severity": new_emergency["severity"],
                    "location": new_emergency["location"],
                    "time_waiting": 0,
                    "assigned_ambulance": None,
                    "assigned_hospital": None
                }
                env.emergencies.append(emergency)
        
        elif event.type == EventType.HOSPITAL_REDUCED_CAPACITY:
            hospital_id = event.impact["hospital_id"]
            if 1 <= hospital_id <= len(env.hospitals):
                hospital = env.hospitals[hospital_id - 1]
                reduction = event.impact["capacity_reduction"]
                hospital["current_capacity"] = max(0, hospital["current_capacity"] - reduction)
                hospital["max_capacity"] = max(1, hospital["max_capacity"] - reduction)
        
        elif event.type == EventType.TRAFFIC_INCIDENT:
            original_traffic = env.traffic_level
            env.traffic_level = min(5, env.traffic_level + event.impact["traffic_factor_increase"])
        
        elif event.type == EventType.AMBULANCE_BREAKDOWN:
            ambulance_id = event.impact["ambulance_id"]
            if 1 <= ambulance_id <= len(env.ambulances):
                ambulance = env.ambulances[ambulance_id - 1]
                ambulance["available"] = False
                ambulance["busy_until"] = event.impact["repair_time"]


class EventScheduler:
    """Manages scheduled and random events during simulation."""
    
    def __init__(self, generator: EventGenerator):
        self.generator = generator
        self.scheduled_events: Dict[int, List[Event]] = {}
    
    def schedule_event(self, step: int, event: Event):
        """Schedule event for specific step."""
        if step not in self.scheduled_events:
            self.scheduled_events[step] = []
        self.scheduled_events[step].append(event)
    
    def process_events(self, env, step: int) -> List[Event]:
        """Process all events for current step."""
        events = []
        
        # Scheduled events
        if step in self.scheduled_events:
            events.extend(self.scheduled_events[step])
        
        # Random events
        events.extend(self.generator.generate_events(env, step))
        
        # Apply events
        for event in events:
            self.generator.apply_event(env, event)
        
        return events
