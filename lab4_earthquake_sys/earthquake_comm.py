import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from datetime import datetime

# Simple mock earthquake environment
class EarthquakeEnvironment:
    def __init__(self):
        self.locations = ["San Francisco", "Tokyo", "Los Angeles", "Mexico City", "Jakarta"]
        self.severities = ["Low", "Moderate", "High", "Critical"]
        
    def get_reading(self):
        """Generate a mock earthquake reading"""
        magnitude = round(random.uniform(2.0, 7.5), 1)
        severity_index = min(int(magnitude / 2), 3)
        
        return {
            'location': random.choice(self.locations),
            'magnitude': magnitude,
            'severity': self.severities[severity_index],
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }

# Simple goals
def define_goals():
    class Goal:
        def __init__(self, name, priority, condition_func, action):
            self.name = name
            self.priority = priority
            self.condition = condition_func
            self.action = action
    
    return [
        Goal("Evacuate Area", 10, lambda r: r['magnitude'] >= 5.0, "Send evacuation alert"),
        Goal("Deploy Rescue", 8, lambda r: r['magnitude'] >= 4.5, "Deploy rescue teams"),
        Goal("Alert Hospitals", 6, lambda r: r['magnitude'] >= 4.0, "Notify medical facilities"),
        Goal("Monitor Aftershocks", 4, lambda r: r['magnitude'] >= 3.0, "Increase monitoring frequency")
    ]

# ── Sensor Agent ───────────────────────────────────────────────────────────
class SensorAgent(Agent):
    class MonitorBehaviour(CyclicBehaviour):
        async def run(self):
            # Get earthquake reading
            reading = self.agent.environment.get_reading()
            
            print(f"\n[SENSOR]  Earthquake detected!")
            print(f"  Location  : {reading['location']}")
            print(f"  Magnitude : {reading['magnitude']} ML")
            print(f"  Severity  : {reading['severity']}")
            
            # Send INFORM to Coordinator
            msg = Message(to="coordinator@localhost")
            msg.body = f"Earthquake:{reading['location']}|Mag:{reading['magnitude']}|Severity:{reading['severity']}"
            msg.set_metadata("performative", "INFORM")
            msg.set_metadata("ontology", "earthquake_detection")
            await self.send(msg)
            print(f"  [SENSOR] Sent INFORM to coordinator")
            
            # If significant earthquake, send REQUEST for resources
            if reading["magnitude"] >= 4.0:
                goals = define_goals()
                triggered = [g for g in goals if g.condition(reading)]
                
                if triggered:
                    msg2 = Message(to="responder@localhost")
                    msg2.body = f"Request:{reading['location']}|Mag:{reading['magnitude']}|Severity:{reading['severity']}"
                    msg2.set_metadata("performative", "REQUEST")
                    msg2.set_metadata("ontology", "resource_request")
                    await self.send(msg2)
                    print(f"  [SENSOR] Sent REQUEST to responder")
            
            await asyncio.sleep(8)
    
    async def setup(self):
        self.environment = EarthquakeEnvironment()
        print(f"\nSensorAgent {self.jid} started - Monitoring for earthquakes...")
        self.add_behaviour(self.MonitorBehaviour())

# ── Coordinator Agent ─────────────────────────────────────────────────────
class CoordinatorAgent(Agent):
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=2)
            if msg:
                performative = msg.get_metadata("performative")
                
                print(f"\n[COORDINATOR] Received from {msg.sender}")
                print(f"  Performative: {performative}")
                print(f"  Body: {msg.body}")
                
                if performative == "INFORM":
                    # Parse the earthquake data
                    parts = msg.body.split('|')
                    location = parts[0].split(':')[1]
                    magnitude = parts[1].split(':')[1]
                    
                    print(f"  Logging earthquake: {location} - Magnitude {magnitude}")
                    
                    # Send acknowledgment
                    reply = msg.make_reply()
                    reply.body = f"Earthquake in {location} logged"
                    reply.set_metadata("performative", "INFORM")
                    await self.send(reply)
                    print(f"   Sent acknowledgment")
    
    async def setup(self):
        print(f" CoordinatorAgent {self.jid} started - Ready to receive alerts")
        self.add_behaviour(self.ReceiveBehaviour())

# ── Responder Agent ───────────────────────────────────────────────────────
class ResponderAgent(Agent):
    class ResponderBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=2)
            if msg:
                performative = msg.get_metadata("performative")
                
                print(f"\n[RESPONDER] Received from {msg.sender}")
                print(f"  Performative: {performative}")
                print(f"  Body: {msg.body}")
                
                if performative == "REQUEST":
                    # Parse the request
                    parts = msg.body.split('|')
                    location = parts[0].split(':')[1]
                    magnitude = parts[1].split(':')[1]
                    
                    print(f"   RESOURCE REQUEST for {location} (Mag: {magnitude})")
                    
                    # Send AGREE
                    agree = msg.make_reply()
                    agree.body = f"Resources mobilized for {location}"
                    agree.set_metadata("performative", "AGREE")
                    await self.send(agree)
                    print(f"  Sent AGREE")
                    
                    # Simulate work
                    await asyncio.sleep(2)
                    
                    # Send INFORM with status
                    status = msg.make_reply()
                    status.body = f"Rescue teams dispatched to {location}"
                    status.set_metadata("performative", "INFORM")
                    await self.send(status)
                    print(f"  Sent INFORM (dispatched)")
    
    async def setup(self):
        print(f"ResponderAgent {self.jid} started - Ready for resource requests")
        self.add_behaviour(self.ResponderBehaviour())

# ── Logger Agent ───────────────────────────────────────────────────────────
class LoggerAgent(Agent):
    class LoggerBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=2)
            if msg:
                performative = msg.get_metadata("performative")
                print(f"\n[LOGGER]  {msg.sender} - {performative}: {msg.body}")
    
    async def setup(self):
        print(f" LoggerAgent {self.jid} started - Logging all messages")
        self.add_behaviour(self.LoggerBehaviour())