# Parking Space Counter (OpenCV)

This project uses **OpenCV** to detect free and occupied parking spaces from a video or webcam feed.  
It works in two main steps:  
1. **Mark Parking Spots** – select the exact parking space positions using a simple mouse picker tool.  
2. **Count Occupancy** – process each frame to detect whether each spot is free or occupied in real-time.

---

## Features
- Real-time parking space counting
- Green/Red overlay for free/occupied spots
- Mouse tool for marking parking spaces
- Works with both video files and live webcam
- Adjustable detection threshold for better accuracy

---

## Installation

```bash
# Clone the repository
git clone https://github.com/HeerRana/Parking-space-counter-opencv.git
cd parking-space-counter-opencv
```

```bash
# (Optional) Create and activate a virtual environment
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\\Scripts\\activate
```

```bash
# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### **1. Mark Parking Spaces**
```bash
python parking_space_picker.py
```
- **Left Click** – Add a parking spot (top-left corner of the rectangle)  
- **Right Click** – Remove a parking spot  
- Spots are saved in `car_park_pos` for later use.  

> **Note:** Use `image.png` (a still frame of your parking lot) when picking spots.

---

### **2. Run the Parking Counter**
```bash
python main.py
```
- **ESC** – Quit program  
- **S** – Save snapshot to `output.png`  

---

### **Webcam vs Video**
By default, `main.py` uses `video.mp4`.  
To use your webcam, change:
```python
cap = cv2.VideoCapture(0)  # Change 0 or 1 depending on your camera index
```

---

## Output Example (Video)
[![Watch the output](https://img.youtube.com/vi/QD38b_hHwAE/hqdefault.jpg)](https://youtu.be/QD38b_hHwAE?feature=shared)

---

## Project Structure
```
parking-space-counter-opencv/
│
├── main.py                    # Parking detection & counting
├── parking_space_picker.py    # Mouse-based parking spot picker
├── utils.py                   # Helper functions
├── car_park_pos               # Saved parking spot coordinates
├── image.png                  # Image used for picking spots
├── video.mp4                  # Parking lot video
├── output.png                 # Example output snapshot
├── README.md                  # Documentation
└── requirements.txt           # Dependencies
```

---

## Tech Stack
- Python 3.11.5
- OpenCV
- NumPy
- Pickle

---

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Install dependencies
```bash
pip install -r requirements.txt
```
