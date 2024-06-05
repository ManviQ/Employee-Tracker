# Employee-Tracker
This is an ongoing Project on Employee Performance Tracker for a Coffee Shop, that is to be presented in an upcoming Hackathon.  
Project Start Date: 29/05/2024

# Goal
To track the Employee Performance in a Coffee Shop by tracking their actions using a live camera tracking system.

# Features
- Uniquely identifies each person in the shop, staff will be distinct from the customers (Staff Facial Recognition yet to be implemented)
- Identifies and tracks the position of objects such as cups
- Counts the number of cups served by each staff member
- Tracks the Customer's waiting time (currently being worked on)
- Tracking additional statistics such as: Number of customers that enter the shop, Busy Hours, etc... (being worked on - at a low priority)
- Detecting Employee actions (to track employee idle time - yet to be implemented)

# Made with
- Python 3.10
- Ultralytics 8.2.16 (using Yolov8x pre-trained model)
- PyTorch 2.3.0 (with CUDA Acceleration)
- OpenCV (4.9.0 - Custom Wheel with CUDA acceleration)

# Watch the Demo
[![YouTube Video Thumbnail](https://img.youtube.com/vi/Unz3vQvvyyA/0.jpg)](https://www.youtube.com/watch?v=Unz3vQvvyyA)

# Want to run it on your system?
**Step 1:** CLONE THE REPOSITORY    

**Step 2:** Importing Environment via Anaconda  
In your anaconda prompt:
> conda env create -f C:\{path-to-folder}\environment.yml

**Step 3:** Once the environment is activated and all the packages have been installed
> python run.py
