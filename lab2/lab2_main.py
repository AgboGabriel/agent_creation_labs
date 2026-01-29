
import asyncio
import json
from environment import DisasterEnvironment
from sensor_agent import SensorAgent

def print_header():
    print("\n" + "="*70)
    print("LAB 2: PERCEPTION AND ENVIRONMENT MODELING")
    print("="*70)
    print("Objective: Implement agent perception of environmental events")
    print("="*70)

async def main():
    print_header()
    
    print("\nCreating disaster environment with 5 zones...")
    environment = DisasterEnvironment()
    
    
    print("\nINITIAL ZONE STATUS:")
    print("-" * 50)
    for zone in environment.zones.values():
        status = zone.get_status()
        print(f"Zone {zone.zone_id}: {zone.name}")
        print(f"  Base Risk: {zone.base_risk:.2f}")
        print(f"  Current: {status['disaster']} ({status['severity']})")
        print(f"  Conditions: {status['temperature']}C, {status['humidity']}% humidity")
        print()
    
    
    print("Creating SensorAgent...")
    sensor_agent = SensorAgent("Sensor-001", environment)
    
    
    print("Starting SensorAgent (will run for 30 seconds)...")
    await sensor_agent.start()
    
    
    print("Starting environment simulation...")
    simulation_task = asyncio.create_task(
        environment.run_simulation(duration_seconds=30)
    )
    
    
    await simulation_task
    

    print("\nStopping SensorAgent...")
    await sensor_agent.stop()
    
    
    print("\n" + "="*70)
    print("LAB 2 RESULTS")
    print("="*70)
    
    print("\nSaving final logs...")
    
    
    with open("final_events_log.json", "w") as f:
        json.dump(environment.event_history, f, indent=2)
    
    
    with open("final_sensor_readings.json", "w") as f:
        json.dump(sensor_agent.readings_log, f, indent=2)
    
    print("\nLogs saved:")
    print("  final_events_log.json")
    print("  final_sensor_readings.json")
    
    
    print(f"\nTotal events recorded: {len(environment.event_history)}")
    print(f"Total sensor readings: {len(sensor_agent.readings_log)}")
    print(f"Total alerts detected: {sensor_agent.alert_count}")
    
    print("\n" + "="*70)
    print("\n" + "="*70)
    print("LAB 2 COMPLETE")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())