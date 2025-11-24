# Quick Start Guide 🚀

## ⚡ 30-Second Demo

Want to see it work **right now**? Run this:

```powershell
python simulation\war_generator_standalone.py
```

**What you'll see:**
- ⚔️ 100 soldiers in a battlefield simulation
- 💓 Real-time heart rate monitoring
- 🚨 Anomaly alerts when soldiers are "poisoned"
- ⏱️ Runs for 60 seconds

---

## 📋 Prerequisites

Before you start, make sure you have:

- ✅ **Python 3.9+** installed
- ✅ **Docker Desktop** running
- ✅ **Minikube** installed (for full setup)
- ✅ **Git** (to clone the project)

---

## 🎯 Three Ways to Run This Project

### Option 1: Standalone Demo (Easiest) ⭐

**Time:** 1 minute  
**Requirements:** Just Python

```powershell
# Install dependencies
pip install simpy

# Run the demo
python simulation\war_generator_standalone.py
```

**Perfect for:**
- Quick demonstration
- Understanding the simulation logic
- Testing without infrastructure

---

### Option 2: With API Server (Intermediate) 🌐

**Time:** 5 minutes  
**Requirements:** Python + dependencies

```powershell
# Step 1: Install all dependencies
pip install -r requirements.txt

# Step 2: Start the API server
uvicorn serving.app:app --reload

# Step 3: In another terminal, test the API
curl -X POST "http://localhost:8000/predict" `
  -H "Content-Type: application/json" `
  -d '{
    "soldier_id": 1,
    "heart_rate": 190,
    "stamina": 100,
    "timestamp": 1234567890
  }'
```

**Expected Response:**
```json
{
  "soldier_id": 1,
  "anomaly_score": 0.95,
  "is_anomalous": true,
  "status": "BREACH"
}
```

**Perfect for:**
- Testing the API
- Understanding anomaly detection logic
- Integration testing

---

### Option 3: Full Production Setup (Advanced) 🏗️

**Time:** 15-20 minutes  
**Requirements:** Python + Docker + Minikube

#### Step 1: Start Minikube

```powershell
minikube start --memory 3500 --cpus 2 --driver=docker
```

#### Step 2: Deploy Infrastructure

```powershell
# Deploy Redis (Feature Store)
powershell -ExecutionPolicy Bypass -File deploy_minimal.ps1
```

#### Step 3: Port Forward Services

**Terminal 1:**
```powershell
kubectl port-forward -n feast svc/redis-master 6379:6379
```

Keep this running!

#### Step 4: Run Full Simulation

**Terminal 2:**
```powershell
# For Kafka-enabled version (requires Kafka running)
python simulation\war_generator.py

# OR use standalone version
python simulation\war_generator_standalone.py
```

#### Step 5: Train ML Model (Optional)

**Terminal 3:**
```powershell
python ml\train_model.py
```

This will:
- Generate synthetic training data
- Train a Temporal Fusion Transformer model
- Save the model checkpoint

#### Step 6: Start API Server

**Terminal 4:**
```powershell
uvicorn serving.app:app --reload
```

API will be available at: `http://localhost:8000`

**Perfect for:**
- Full MLOps pipeline demonstration
- Production-like environment
- Resume/portfolio showcase

---

## 🧪 Verify Everything Works

Run the comprehensive test suite:

```powershell
powershell -ExecutionPolicy Bypass -File test_all_components.ps1
```

**Expected Output:**
```
Tests Passed: 6
Tests Failed: 0
🎉 ALL TESTS PASSED! Project is fully functional!
```

---

## 📊 What Each Component Does

### 1. Simulation (`simulation/war_generator_standalone.py`)
- Creates 100 virtual soldiers
- Simulates heart rate and stamina
- Randomly injects anomalies (poison attacks)
- Prints events to console

### 2. API Server (`serving/app.py`)
- FastAPI REST API
- `/predict` endpoint for anomaly detection
- `/health` endpoint for health checks
- Returns JSON responses

### 3. ML Model (`ml/train_model.py`)
- Temporal Fusion Transformer (TFT)
- Learns normal patterns from historical data
- Predicts expected heart rate
- Detects anomalies when actual differs from expected

### 4. Infrastructure
- **Minikube**: Local Kubernetes cluster
- **Redis**: Feature store (online storage)
- **Kafka**: Message queue (optional)

---

## 🎬 Demo Script (For Presentations)

### 1. Introduction (30 seconds)
> "This is Chakravyuha - a real-time anomaly detection system for battlefield monitoring. It uses the same technology stack as Netflix, Uber, and Airbnb."

### 2. Show Simulation (1 minute)
```powershell
python simulation\war_generator_standalone.py
```

> "Here you can see 100 soldiers being monitored. Watch for the red alerts - those are anomalies being detected in real-time."

### 3. Show API (1 minute)
```powershell
# Start API
uvicorn serving.app:app --reload

# Test with normal heart rate
curl -X POST "http://localhost:8000/predict" `
  -H "Content-Type: application/json" `
  -d '{"soldier_id": 1, "heart_rate": 75, "stamina": 100, "timestamp": 1234567890}'

# Test with anomalous heart rate
curl -X POST "http://localhost:8000/predict" `
  -H "Content-Type: application/json" `
  -d '{"soldier_id": 1, "heart_rate": 195, "stamina": 100, "timestamp": 1234567890}'
```

> "The API returns 'SECURE' for normal readings and 'BREACH' for anomalies. This same pattern is used in fraud detection, IoT monitoring, and cybersecurity."

### 4. Show Infrastructure (30 seconds)
```powershell
kubectl get pods --all-namespaces
```

> "Everything runs on Kubernetes - the same platform used by Google, Amazon, and Microsoft for production workloads."

---

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution:**
```powershell
pip install -r requirements.txt
```

### Issue: "Minikube won't start"
**Solution:**
```powershell
# Check Docker is running
docker ps

# Reduce memory if needed
minikube start --memory 3000 --cpus 2 --driver=docker
```

### Issue: "Port already in use"
**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue: "Redis pod not running"
**Solution:**
```powershell
# Check pod status
kubectl get pods -n feast

# Restart if needed
kubectl delete pod -n feast -l app.kubernetes.io/name=redis
```

---

## 📚 Next Steps

Once you have everything running:

1. ✅ **Read the README.md** for detailed architecture explanation
2. ✅ **Check WORKLOG.md** for development history
3. ✅ **Explore the code** in `simulation/`, `ml/`, and `serving/`
4. ✅ **Modify parameters** (number of soldiers, anomaly rate, etc.)
5. ✅ **Add to your resume/portfolio**

---

## 🎯 Key Files

| File | Purpose |
|------|---------|
| `README.md` | Complete project documentation |
| `QUICKSTART.md` | This file - quick start guide |
| `WORKLOG.md` | Development log and status |
| `test_all_components.ps1` | Comprehensive test suite |
| `simulation/war_generator_standalone.py` | Standalone demo |
| `serving/app.py` | FastAPI server |
| `ml/train_model.py` | Model training script |

---

## 💡 Pro Tips

1. **For Demos:** Use the standalone version - it works immediately
2. **For Learning:** Read the code comments - they explain everything
3. **For Resume:** Focus on the technology stack (Kubernetes, Kafka, TFT)
4. **For Interviews:** Be ready to explain the architecture diagram

---

**Need Help?** Check the README.md for detailed explanations!

**Ready to Impress?** Run the demo and show it off! 🚀
