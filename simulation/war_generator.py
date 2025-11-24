# simulation/war_generator.py
import simpy
import json
import time
import random
from confluent_kafka import Producer

# Configuration
KAFKA_TOPIC = "soldier_telemetry"
KAFKA_CONF = {
    'bootstrap.servers': 'localhost:31092', 
    'client.id': 'war-simulator'
}

class Soldier:
    def __init__(self, env, soldier_id, producer):
        self.env = env
        self.id = soldier_id
        self.producer = producer
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
            else:
                self.heart_rate = max(40, min(200, self.heart_rate + random.randint(-2, 2)))

            event = {
                "soldier_id": self.id,
                "timestamp": time.time(),
                "heart_rate": self.heart_rate,
                "stamina": self.stamina
            }
            
            # Push to Kafka
            # Note: In a real app, we'd handle buffer errors here
            try:
                self.producer.produce(KAFKA_TOPIC, key=str(self.id), value=json.dumps(event))
                self.producer.poll(0)
            except Exception as e:
                print(f"Queue full or error: {e}")

def run_simulation():
    print("⚔️  Starting Kurukshetra Simulation...")
    p = Producer(KAFKA_CONF)
    env = simpy.Environment()
    
    # Create 100 Soldiers
    for i in range(100):
        Soldier(env, i, p)
        
    env.run(until=1000) 
    p.flush()

if __name__ == "__main__":
    run_simulation()
