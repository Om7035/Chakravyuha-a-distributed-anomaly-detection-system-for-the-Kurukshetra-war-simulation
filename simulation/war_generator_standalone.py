# simulation/war_generator_standalone.py
# Standalone version that doesn't require Kafka - just prints events
import simpy
import json
import time
import random

# Configuration
NUM_SOLDIERS = 100
SIMULATION_DURATION = 60  # 1 minute for testing

class Soldier:
    def __init__(self, env, soldier_id):
        self.env = env
        self.id = soldier_id
        self.heart_rate = 60 + random.randint(-5, 5)
        self.stamina = 100
        self.process = env.process(self.run())

    def run(self):
        while True:
            # Simulate "Action" every 1 second
            yield self.env.timeout(1)
            
            # Anomaly Injection: Randomly poison units
            if random.random() < 0.05: 
                self.heart_rate = 180 + random.randint(0, 20)
                print(f"🚨 ANOMALY: Soldier {self.id} - Heart Rate: {self.heart_rate} (POISONED!)")
            else:
                self.heart_rate = max(40, min(200, self.heart_rate + random.randint(-2, 2)))

            event = {
                "soldier_id": self.id,
                "timestamp": time.time(),
                "heart_rate": self.heart_rate,
                "stamina": self.stamina
            }
            
            # Print event instead of sending to Kafka
            if self.env.now % 10 == 0:  # Print every 10 seconds
                print(f"[{int(self.env.now)}s] Soldier {self.id}: HR={self.heart_rate}, Stamina={self.stamina}")

def run_simulation():
    print("⚔️  Starting Kurukshetra Simulation (Standalone Mode)...")
    print(f"Simulating {NUM_SOLDIERS} soldiers for {SIMULATION_DURATION} seconds")
    print("=" * 60)
    
    env = simpy.Environment()
    
    # Create 100 Soldiers
    for i in range(NUM_SOLDIERS):
        Soldier(env, i)
        
    env.run(until=SIMULATION_DURATION)
    
    print("=" * 60)
    print("✅ Simulation complete!")

if __name__ == "__main__":
    run_simulation()
