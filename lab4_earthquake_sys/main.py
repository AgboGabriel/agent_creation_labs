import asyncio
import spade
from earthquake_comm import SensorAgent, CoordinatorAgent, ResponderAgent, LoggerAgent

async def main():
    print("=" * 60)
    print("EARTHQUAKE MONITORING SYSTEM - FIPA-ACL COMMUNICATION")
    print("=" * 60)
    
    # Create agents - passwords can be anything for local server
    sensor = SensorAgent("sensor@localhost", "123")
    coordinator = CoordinatorAgent("coordinator@localhost", "123")
    responder = ResponderAgent("responder@localhost", "123")
    logger = LoggerAgent("logger@localhost", "123")
    
    print("\nStarting agents...")
    
    # Start receiver agents first
    await coordinator.start()
    await responder.start()
    await logger.start()
    await asyncio.sleep(1)
    
    # Start sender agent
    await sensor.start()
    
    print("\nALL AGENTS STARTED!")
    print("\nCommunication Flow:")
    print("   INFORM: Sensor → Coordinator (earthquake alert)")
    print("   REQUEST: Sensor → Responder (resource request when M≥4.0)")
    print("   AGREE: Responder → Sensor (acknowledgment)")
    print("   INFORM: Responder → Sensor (resources dispatched)")
    print("\nRunning... Press Ctrl+C to stop\n")
    print("=" * 60)
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping agents...")
    
    await sensor.stop()
    await coordinator.stop()
    await responder.stop()
    await logger.stop()
    print("System stopped.")

if __name__ == "__main__":
    spade.run(main())