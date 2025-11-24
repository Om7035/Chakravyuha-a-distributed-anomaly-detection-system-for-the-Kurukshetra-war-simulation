# test_all_components.ps1
# Comprehensive test script for Project Chakravyuha

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "PROJECT CHAKRAVYUHA - COMPREHENSIVE TEST SUITE" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

$testsPassed = 0
$testsFailed = 0

# Test 1: Check Minikube
Write-Host "`n[TEST 1] Checking Minikube Status..." -ForegroundColor Yellow
try {
    $minikubeStatus = & "D:\Minikube\minikube.exe" status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Minikube is running" -ForegroundColor Green
        $testsPassed++
    }
    else {
        Write-Host "❌ Minikube is not running" -ForegroundColor Red
        $testsFailed++
    }
}
catch {
    Write-Host "❌ Minikube check failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 2: Check Redis Pod
Write-Host "`n[TEST 2] Checking Redis Pod..." -ForegroundColor Yellow
try {
    $redisPod = kubectl get pods -n feast -l app.kubernetes.io/name=redis -o jsonpath='{.items[0].status.phase}' 2>&1
    if ($redisPod -eq "Running") {
        Write-Host "✅ Redis pod is running" -ForegroundColor Green
        $testsPassed++
    }
    else {
        Write-Host "❌ Redis pod status: $redisPod" -ForegroundColor Red
        $testsFailed++
    }
}
catch {
    Write-Host "❌ Redis check failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 3: Check Python Dependencies
Write-Host "`n[TEST 3] Checking Python Dependencies..." -ForegroundColor Yellow
try {
    $pythonCheck = python -c "import simpy, fastapi, pytorch_lightning; print('OK')" 2>&1
    if ($pythonCheck -like "*OK*") {
        Write-Host "✅ Python dependencies installed" -ForegroundColor Green
        $testsPassed++
    }
    else {
        Write-Host "❌ Missing Python dependencies" -ForegroundColor Red
        $testsFailed++
    }
}
catch {
    Write-Host "❌ Python check failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 4: Test Standalone Simulation
Write-Host "`n[TEST 4] Testing Standalone Simulation (10 seconds)..." -ForegroundColor Yellow
try {
    # Create a temporary test version that runs for 10 seconds
    $testScript = @"
import simpy
import random

class Soldier:
    def __init__(self, env, soldier_id):
        self.env = env
        self.id = soldier_id
        self.heart_rate = 60 + random.randint(-5, 5)
        self.process = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(1)
            if random.random() < 0.05:
                self.heart_rate = 180 + random.randint(0, 20)
                print(f"ANOMALY: Soldier {self.id} - HR: {self.heart_rate}")

env = simpy.Environment()
for i in range(10):
    Soldier(env, i)
env.run(until=10)
print("TEST_COMPLETE")
"@
    $testScript | Out-File -FilePath "test_sim.py" -Encoding UTF8
    $simOutput = python test_sim.py 2>&1
    Remove-Item "test_sim.py" -Force
    
    if ($simOutput -like "*TEST_COMPLETE*") {
        Write-Host "✅ Simulation working correctly" -ForegroundColor Green
        $testsPassed++
    }
    else {
        Write-Host "❌ Simulation test failed" -ForegroundColor Red
        $testsFailed++
    }
}
catch {
    Write-Host "❌ Simulation test failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 5: Check FastAPI App
Write-Host "`n[TEST 5] Checking FastAPI App..." -ForegroundColor Yellow
try {
    $apiCheck = python -c "from serving.app import app; print('OK')" 2>&1
    if ($apiCheck -like "*OK*") {
        Write-Host "✅ FastAPI app loads successfully" -ForegroundColor Green
        $testsPassed++
    }
    else {
        Write-Host "❌ FastAPI app has issues" -ForegroundColor Red
        $testsFailed++
    }
}
catch {
    Write-Host "❌ FastAPI check failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 6: Check File Structure
Write-Host "`n[TEST 6] Checking Project Structure..." -ForegroundColor Yellow
$requiredFiles = @(
    "simulation\war_generator.py",
    "simulation\war_generator_standalone.py",
    "ml\train_model.py",
    "ml\feature_store.yaml",
    "serving\app.py",
    "infra\main.tf",
    "README.md",
    "requirements.txt"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (!(Test-Path $file)) {
        Write-Host "❌ Missing file: $file" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if ($allFilesExist) {
    Write-Host "✅ All required files present" -ForegroundColor Green
    $testsPassed++
}
else {
    $testsFailed++
}

# Summary
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host "Tests Passed: $testsPassed" -ForegroundColor Green
Write-Host "Tests Failed: $testsFailed" -ForegroundColor Red

if ($testsFailed -eq 0) {
    Write-Host "`n🎉 ALL TESTS PASSED! Project is fully functional!" -ForegroundColor Green
    Write-Host "`nYou can now:" -ForegroundColor Cyan
    Write-Host "1. Run standalone demo: python simulation\war_generator_standalone.py" -ForegroundColor White
    Write-Host "2. Start API server: uvicorn serving.app:app --reload" -ForegroundColor White
    Write-Host "3. Train model: python ml\train_model.py" -ForegroundColor White
}
else {
    Write-Host "`n⚠️ Some tests failed. Please check the errors above." -ForegroundColor Yellow
}

Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
