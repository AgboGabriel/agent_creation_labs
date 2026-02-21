import random


# ==============================
# 1. ACL Message Structure
# ==============================

class ACLMessage:
    def __init__(self, performative, sender, receiver, content):
        self.performative = performative
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def __str__(self):
        return f"[{self.performative}] From: {self.sender} To: {self.receiver} | Content: {self.content}"


# ==============================
# 2. Disaster Environment
# ==============================

class DisasterEnvironment:
    def generate_event(self):
        severities = ["LOW", "MEDIUM", "HIGH"]
        return {
            "severity": random.choice(severities),
            "location": f"Zone-{random.randint(1,5)}"
        }


# ==============================
# 3. Sensor Agent
# ==============================

class SensorAgent:
    def __init__(self, name, coordinator):
        self.name = name
        self.coordinator = coordinator

    def detect_event(self, environment):
        event = environment.generate_event()
        print("\n[Sensor] Detected:", event)

        # Send INFORM message
        message = ACLMessage(
            performative="INFORM",
            sender=self.name,
            receiver="Coordinator",
            content=event
        )

        print("Message Sent:", message)
        self.coordinator.receive_message(message)


# ==============================
# 4. Coordinator Agent
# ==============================

class CoordinatorAgent:
    def __init__(self, name, rescue_agent):
        self.name = name
        self.rescue_agent = rescue_agent

    def receive_message(self, message):
        print("\n[Coordinator] Message Received:", message)

        if message.performative == "INFORM":
            self.handle_inform(message)

    def handle_inform(self, message):
        event = message.content
        severity = event["severity"]

        print("[Coordinator] Processing severity:", severity)

        if severity == "HIGH":
            self.send_request(event)
        else:
            print("[Coordinator] Monitoring situation. No major action required.")

    def send_request(self, event):
        request_message = ACLMessage(
            performative="REQUEST",
            sender=self.name,
            receiver="RescueTeam",
            content=f"Dispatch team to {event['location']} immediately!"
        )

        print("Message Sent:", request_message)
        self.rescue_agent.receive_message(request_message)


# ==============================
# 5. Rescue Agent
# ==============================

class RescueAgent:
    def __init__(self, name):
        self.name = name

    def receive_message(self, message):
        print("\n[RescueAgent] Message Received:", message)

        if message.performative == "REQUEST":
            self.execute_action(message.content)

    def execute_action(self, instruction):
        print("[RescueAgent] Executing Action:", instruction)


# ==============================
# 6. Main Simulation
# ==============================

if __name__ == "__main__":

    environment = DisasterEnvironment()
    rescue_agent = RescueAgent("RescueTeam")
    coordinator = CoordinatorAgent("Coordinator", rescue_agent)
    sensor = SensorAgent("SensorUnit", coordinator)

    # Run simulation
    for i in range(3):
        sensor.detect_event(environment)