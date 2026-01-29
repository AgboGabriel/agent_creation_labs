import asyncio
import json
from datetime import datetime

class SensorAgent:
    
    def __init__(self, agent_id, environment):
        self.agent_id = agent_id
        self.environment = environment
        self.readings_log = []
        self.alert_count = 0
        self.is_running = False
        
    async def start(self):
        
        print(f"SensorAgent {self.agent_id} initializing...")
        self.is_running = True
        
        self.sensing_task = asyncio.create_task(self._sensing_loop())
        self.alert_task = asyncio.create_task(self._alert_loop())
        self.logging_task = asyncio.create_task(self._logging_loop())
        
        print(f"SensorAgent {self.agent_id} started successfully")
        
    async def stop(self):
        print(f"Stopping SensorAgent {self.agent_id}...")
        self.is_running = False
        
       
        self.sensing_task.cancel()
        self.alert_task.cancel()
        self.logging_task.cancel()
        
        
        try:
            await self.sensing_task
            await self.alert_task
            await self.logging_task
        except asyncio.CancelledError:
            pass
            
        print(f"SensorAgent {self.agent_id} stopped")
    
    async def _sensing_loop(self):
        """Continuously sense environment conditions"""
        while self.is_running:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
           
            status = self.environment.get_all_status()
            
       
            reading = {
                'timestamp': timestamp,
                'sensor_id': self.agent_id,
                'readings': status
            }
            
            self.readings_log.append(reading)
            
          
            alerts = [zone for zone in status if zone['disaster'] != 'none']
            
            if alerts:
                print(f"[{timestamp}] Sensor {self.agent_id}: Detected {len(alerts)} issues")
            else:
                print(f"[{timestamp}] Sensor {self.agent_id}: All zones normal")
            
            await asyncio.sleep(3) 
    
    async def _alert_loop(self):
        while self.is_running:
            status = self.environment.get_all_status()
            
            for zone in status:
                if zone['severity'] in ['high', 'critical']:
                    self.alert_count += 1
                    
                    alert_msg = f"CRITICAL ALERT #{self.alert_count}\nZone: {zone['name']}\nDisaster: {zone['disaster']}\nSeverity: {zone['severity']}\nRisk Level: {zone['risk_level']:.2f}"
                    
                    print("\n" + "="*50)
                    print(alert_msg)
                    print("="*50 + "\n")
                    
                   
                    with open(f"alert_{self.alert_count}.log", "w") as f:
                        f.write(alert_msg)
            
            await asyncio.sleep(5)  
    
    async def _logging_loop(self):
      
        log_count = 0
        while self.is_running:
            if self.readings_log:
                log_count += 1
                
                filename = f"sensor_data_{log_count}.json"
                with open(filename, "w") as f:
                    json.dump(self.readings_log[-5:], f, indent=2)
                
                print(f"Sensor {self.agent_id}: Saved readings to {filename}")
               
                if self.environment.event_history:
                    event_file = f"events_{log_count}.json"
                    with open(event_file, "w") as f:
                        json.dump(self.environment.event_history[-3:], f, indent=2)
            
            await asyncio.sleep(10)  