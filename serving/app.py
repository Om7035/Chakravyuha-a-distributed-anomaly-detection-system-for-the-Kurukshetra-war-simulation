# serving/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import random

app = FastAPI(title="Chakravyuha Watchtower (Local)")

logging.basicConfig(level=logging.INFO)

class SoldierEvent(BaseModel):
    soldier_id: int
    heart_rate: float
    stamina: float
    timestamp: float

@app.post("/predict")
async def predict(event: SoldierEvent):
    try:
        # In a real app, we would load the model:
        # model = TemporalFusionTransformer.load_from_checkpoint(open("model_path.txt").read().strip())
        
        # For this "Zero Cost" tutorial, we will implement the Anomaly Logic directly
        # This mimics what the model would output (a high anomaly score for drift)
        
        is_anomalous = False
        anomaly_score = 0.0
        
        # 1. Check for "Poison" (The anomaly we injected in war_generator.py)
        # In generator: heart_rate = 180 + random(0,20)
        if event.heart_rate > 170:
            is_anomalous = True
            anomaly_score = 0.95
            logging.warning(f"🚨 ANOMALY DETECTED: Soldier {event.soldier_id} | HR: {event.heart_rate}")
        
        # 2. Check for "Fatigue" (Low stamina but high HR)
        elif event.stamina < 20 and event.heart_rate > 100:
            is_anomalous = True
            anomaly_score = 0.8
            logging.warning(f"⚠️ FATIGUE DETECTED: Soldier {event.soldier_id}")
            
        return {
            "soldier_id": event.soldier_id,
            "anomaly_score": anomaly_score,
            "is_anomalous": is_anomalous,
            "status": "BREACH" if is_anomalous else "SECURE"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}
