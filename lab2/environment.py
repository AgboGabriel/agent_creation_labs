"""
LAB 2: Environment Modeling
Simulates a disaster environment with different zones and conditions
"""

import random
import asyncio
from datetime import datetime
from enum import Enum

class DisasterType(Enum):
    EARTHQUAKE = "earthquake"
    FLOOD = "flood"
    FIRE = "fire"
    NONE = "none"

class ZoneSeverity(Enum):
    NORMAL = "normal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EnvironmentZone:
    """Represents a zone in the environment with conditions"""
    
    def __init__(self, zone_id, name, base_risk=0.1):
        self.zone_id = zone_id
        self.name = name
        self.base_risk = base_risk
        self.current_disaster = DisasterType.NONE
        self.severity = ZoneSeverity.NORMAL
        self.temperature = 25.0  # Celsius
        self.humidity = 50.0     # Percentage
        self.wind_speed = 10.0   # 
        self.last_update = datetime.now()
    
    def update_conditions(self):
        """Update environmental conditions with some randomness"""
        self.temperature += random.uniform(-2, 2)
        self.humidity += random.uniform(-10, 10)
        self.wind_speed += random.uniform(-5, 5)
        
        # Clamp values to reasonable ranges
        self.temperature = max(-10, min(50, self.temperature))
        self.humidity = max(0, min(100, self.humidity))
        self.wind_speed = max(0, min(150, self.wind_speed))
        
        # Randomly trigger disasters based on conditions
        self._check_disaster_trigger()
        
        self.last_update = datetime.now()
        return self.get_status()
    
    def _check_disaster_trigger(self):
        """Check if conditions warrant a disaster event"""
        # Reset disaster if it was NONE
        if self.current_disaster == DisasterType.NONE:
            disaster_chance = self.base_risk
            
            # Increase chances based on conditions
            if self.temperature > 35:
                disaster_chance += 0.1
                if random.random() < disaster_chance:
                    self.current_disaster = DisasterType.FIRE
                    self.severity = ZoneSeverity.MEDIUM
            
            elif self.humidity > 80 and self.wind_speed > 30:
                disaster_chance += 0.15
                if random.random() < disaster_chance:
                    self.current_disaster = DisasterType.FLOOD
                    self.severity = ZoneSeverity.HIGH
            
            elif random.random() < disaster_chance:
                self.current_disaster = DisasterType.EARTHQUAKE
                self.severity = ZoneSeverity.LOW
        
        # If there's already a disaster, it might worsen or improve
        elif self.current_disaster != DisasterType.NONE:
            if random.random() < 0.3:  # 30% chance disaster escalates
                severity_levels = list(ZoneSeverity)
                current_idx = severity_levels.index(self.severity)
                if current_idx < len(severity_levels) - 1 and random.random() < 0.5:
                    self.severity = severity_levels[current_idx + 1]
            
            elif random.random() < 0.2:  # 20% chance disaster ends
                self.current_disaster = DisasterType.NONE
                self.severity = ZoneSeverity.NORMAL
    
    def get_status(self):
        """Get current zone status as dictionary"""
        return {
            'zone_id': self.zone_id,
            'name': self.name,
            'disaster': self.current_disaster.value,
            'severity': self.severity.value,
            'temperature': round(self.temperature, 1),
            'humidity': round(self.humidity, 1),
            'wind_speed': round(self.wind_speed, 1),
            'last_update': self.last_update.strftime("%H:%M:%S"),
            'risk_level': self._calculate_risk_level()
        }
    
    def _calculate_risk_level(self):
        """Calculate overall risk level"""
        risk_score = self.base_risk
        
        if self.current_disaster != DisasterType.NONE:
            severity_multiplier = {
                ZoneSeverity.LOW: 1.5,
                ZoneSeverity.MEDIUM: 2.0,
                ZoneSeverity.HIGH: 3.0,
                ZoneSeverity.CRITICAL: 5.0
            }
            risk_score *= severity_multiplier.get(self.severity, 1.0)
        
        if self.temperature > 40:
            risk_score += 0.2
        if self.humidity > 90:
            risk_score += 0.15
        if self.wind_speed > 60:
            risk_score += 0.25
        
        return min(1.0, risk_score)

class DisasterEnvironment:
    """Main environment with multiple zones"""
    
    def __init__(self):
        self.zones = {}
        self._initialize_zones()
        self.event_history = []
    
    def _initialize_zones(self):
        """Create initial zones"""
        zones_data = [
            (1, "Downtown", 0.15),
            (2, "Residential", 0.08),
            (3, "Industrial", 0.25),
            (4, "Coastal", 0.20),
            (5, "Rural", 0.05)
        ]
        
        for zone_id, name, risk in zones_data:
            self.zones[zone_id] = EnvironmentZone(zone_id, name, risk)
    
    async def run_simulation(self, duration_seconds=60):
        """Run environment simulation"""
        print("Starting environment simulation...")
        start_time = datetime.now()
        
        while (datetime.now() - start_time).seconds < duration_seconds:
            for zone in self.zones.values():
                status = zone.update_conditions()
                
                # Log significant events
                if zone.current_disaster != DisasterType.NONE:
                    event = {
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'zone': zone.name,
                        'event': f"{zone.current_disaster.value}_{zone.severity.value}",
                        'details': status
                    }
                    self.event_history.append(event)
                    
                    if zone.severity in [ZoneSeverity.HIGH, ZoneSeverity.CRITICAL]:
                        print(f" ALERT: {zone.name} - {zone.current_disaster.value} "
                              f"({zone.severity.value})")
            
            await asyncio.sleep(5)  # Update every 5 seconds
        
        print(f"Simulation complete. Events recorded: {len(self.event_history)}")
    
    def get_all_status(self):
        """Get status of all zones"""
        return [zone.get_status() for zone in self.zones.values()]