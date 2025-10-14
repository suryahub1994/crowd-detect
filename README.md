# 🧠 Crowd Density Estimation Prototype

A computer vision prototype that estimates **crowd density in video feeds** using YOLO-based person detection and dynamic heatmap visualization.  
Developed as an early experiment toward intelligent public-space monitoring and analytics — useful in contexts like **event management**, **safety compliance**, and **urban crowd control**.

---

## 🎯 Problem Statement

Large gatherings and public areas require constant situational awareness.  
Traditional surveillance offers only visual data — not actionable insights like *how dense* a crowd is at any given time.

This project aims to:
- Detect people in each video frame using a pretrained **YOLOv8 model**  
- Estimate **local crowd density** using clustering (K-Means)  
- Visualize the density distribution through an evolving **heatmap overlay**  
- Maintain *temporal smoothness* via **age-based blending** between frames

---

## 🧩 Key Features

- ✅ **YOLOv8-based person detection** for robust performance across scenes  
- 🎨 **Adaptive heatmap** that persists and smoothens over time  
- 🧮 **K-Means clustering** to group spatially close detections  
 - ⚙️ Simple configuration through code constants — no external dependencies beyond OpenCV & Ultralytics  

---

## 📊 Example Use-Cases

| Scenario | Goal |
|-----------|------|
| Event venues | Monitor crowd hotspots in real-time |
| Malls / stations | Detect over-crowding or bottlenecks |
| Public protests | Study density trends without identity tracking |
| Smart cities | Feed data to safety and planning dashboards |

---

## 🧠 Algorithm Overview

1. **Input Video** → Read each frame via OpenCV  
2. **Person Detection** → Use YOLOv8 to get bounding boxes  
3. **Centroid Extraction** → Compute center points of each person  
4. **Spatial Clustering** → Apply K-Means to group people by proximity  
5. **Density Scoring** → Estimate crowd density per cluster  
6. **Heatmap Blending** → Maintain an *ageing* heatmap that gradually decays instead of flickering  
7. **Visualization** → Overlay colored ellipses (smoother than circles) onto the frame  

---

## 📸 Example Output

<img width="1427" height="761" alt="Screenshot 2025-10-14 at 9 16 22 PM" src="https://github.com/user-attachments/assets/1931fd21-2e27-4583-b146-eb47b6295617" />

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/crowd-density-estimation.git
cd crowd-density-estimation

# Install dependencies
pip install ultralytics opencv-python numpy
