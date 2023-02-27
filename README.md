# Assistive-Robot

Development of 2WD Assistive Robot using Raspberry Pi for Biomedical Engineering Final Project 

## Installation
On Windows 10 (for Development)
```bash
# Install Visual Studio Code 
https://update.code.visualstudio.com/1.74.3/win32-x64/stable
# Install Python 3 Compiler
https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe
# Install Git
https://github.com/git-for-windows/git/releases/download/v2.39.2.windows.1/Git-2.39.2-64-bit.exe
# Install OpenCV with Community Contrib 
pip install opencv-contrib-python
# Clone Assistive Robot Workspace
git clone https://github.com/ardhimaulidani/Assistive-Robot.git
```

On Ubuntu 20.04 (Raspberry Pi)
```bash
# Install OpenCV Dependencies
sudo apt-get update
sudo apt install python3-pip
sudo apt install build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev libopenexr-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
#Install OpenCV with Community Contrib 
pip install opencv-contrib-python
# Clone Assistive Robot Workspace
cd
git clone https://github.com/ardhimaulidani/Assistive-Robot.git
```

## Usage
```bash
# Run Motor with Controller
cd Assistive_Robot/robot_base
sudo python3 move.py

# Run Aruco Detection Camera
cd Assistive_Robot/qrcode
python3 aruco_read.py
```
