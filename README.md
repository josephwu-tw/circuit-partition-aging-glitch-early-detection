# ⚡ Circuit Partition Aging Glitch Early Detection

## 🚀 Overview
This project develops an LSTM-based anomaly detection system to identify circuit aging glitches at an early stage, enabling detection 5+ cycles before failure.

It combines circuit simulation, synthetic data generation, and deep learning to improve reliability analysis in digital systems.

---

## 🎯 Problem
Circuit aging effects (e.g., NBTI, HCI) introduce timing degradation and intermittent glitches that are difficult to detect using traditional methods.

This project aims to:
- Detect aging-induced glitches earlier than conventional approaches
- Simulate circuit behavior under aging conditions
- Build a scalable ML pipeline for reliability analysis

---

## 🧠 Approach

### 1. Data Generation & Simulation
- Parsed and processed circuit benchmark files
- Connected multiple circuit partitions to simulate complex systems
- Generated synthetic datasets using MISR-based error signatures

### 2. Feature Engineering
- Extracted time-series features representing circuit degradation
- Encoded glitch patterns across simulation cycles

### 3. Model Design
- Built an LSTM-based sequence model for anomaly detection
- Captured temporal dependencies in circuit aging behavior

### 4. Evaluation
- Compared predicted glitch patterns with ground truth
- Achieved early detection 5+ cycles ahead of actual failure

---

## 🏗️ Pipeline

```
Circuit Benchmarks → Simulation → Data Generation → Feature Engineering → LSTM Model → Early Glitch Detection
```

---

## ⚙️ Tech Stack

- Python  
- TensorFlow / Keras  
- NumPy / Pandas  
- Custom simulation tools  

---

## 📊 Results

- Detected aging-related glitches 5+ cycles earlier than baseline  
- Enabled early-stage failure prediction for circuit reliability analysis  
- Demonstrated effectiveness of sequence models for time-dependent hardware degradation  

---

## 🧪 Usage

### Install dependencies
```bash
pip install -r requirements.txt
```

### Generate data
```bash
python data_generator.py
```

### Train model
```bash
python model.py
```

### Evaluate model
```bash
python evaluation.py
```

---

## 📁 Project Structure

```
.
├── bench_file/        # Circuit benchmark files
├── data/              # Generated datasets
├── models/            # Trained models
├── data_generator.py  # Data generation pipeline
├── model.py           # LSTM model
├── evaluation.py      # Evaluation scripts
```

---

## 🔮 Future Improvements

- Extend to transformer-based sequence models  
- Integrate with real hardware measurement data  
- Build visualization dashboard for glitch detection  
- Deploy as API service for automated reliability analysis  

---

## 💡 Key Takeaways

- Combines simulation, machine learning, and system design  
- Demonstrates ability to build end-to-end pipelines for complex engineering problems  
- Applies deep learning to hardware reliability and time-series anomaly detection  
