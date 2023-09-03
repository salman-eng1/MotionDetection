 Install Python Dependencies:

➢ Install python 3.11 using Microsoft Store & https://www.python.org/downloads/ 
• make sure you’re able to run python commands globally
• press windows +R
• enter “systempropertiesadvanced”
• click on environment variables
• find “path” in system variables then press “Add New”
• Add the required path as example:
• C:\Users\ABOHADI\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_
qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts
Note: the path will be the same on all windows machines but you have to change the highlighted 
words according to your username and Python version 
 
 
➢ Execute the following commands: 
powershell$ pip install opencv-python
powershell$ pip install pyinstaller
powershell$ pip install pygetwindow
 
 
 
 Setup and Run 
➢ Download Nssm: 
• Follow the link https://nssm.cc/download and download nssm 2.24
• Unzip the folder to the destination path as example “D:/zeour/detection”
• Add the following path to the environment variables the same way as above
“D:\detection\nssm-2.24\win64”
• Put the script “motiondet.py” in path “D:/detection” 
 
➢ Create Motion Detector as Windows Service 
powershell$ cd D:/detection
powershell$ pyinstaller --onefile motiondet.py
//file named dist will be created and inside of it, you will find motiondet.exe
powershell$ mv dist/motiondet.exe .
powershell$ nssm install "MotionDetection" "D:/detection/motiondet.exe"
powershell$ nssm start MotionDetection
powershell$ nssm status MotionDetection // it should return “Running”
 
Now you’re free to control the script as Windows service, you can check services and search 
for MotionDetection
