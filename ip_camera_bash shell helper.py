import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import tempfile

# HQ recording script as a string
hq_script = """#!/bin/sh
STARTTIME=$1
HQDIR=$2
HQLENGTH=$3
CAM1_IP=$4
CAM2_IP=$5
CAM3_IP=$6
CAM4_IP=$7
CAM5_IP=$8

ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM1_IP:554/Streaming/Channels/1" -vcodec copy -an -t $HQLENGTH $HQDIR/CAM1D_$STARTTIME.mkv &
ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM2_IP:554/Streaming/Channels/1" -vcodec copy -an -t $HQLENGTH $HQDIR/CAM2D_$STARTTIME.mkv &
ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM3_IP:554/Streaming/Channels/1" -vcodec copy -an -t $HQLENGTH $HQDIR/CAM3D_$STARTTIME.mkv &
ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM4_IP:554/Streaming/Channels/1" -vcodec copy -an -t $HQLENGTH $HQDIR/CAM4D_$STARTTIME.mkv &
ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM5_IP:554/Streaming/Channels/1" -vcodec copy -an -t $HQLENGTH $HQDIR/CAM5D_$STARTTIME.mkv &
"""

# LQ recording script as a string
lq_script = """#!/bin/sh
STARTTIME=$1
LQDIR=$2
LQLENGTH=$3
LOCALSTORE=$4
CAM1_IP=$5
CAM2_IP=$6
CAM3_IP=$7
CAM4_IP=$8
CAM5_IP=$9

find $LOCALSTORE -maxdepth 1 -type f -mmin +190 -exec mv '{}' $LQDIR \\;

ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM1_IP:554/Streaming/Channels/2" -vcodec copy -an -t $LQLENGTH $LOCALSTORE/CAM1D_$STARTTIME.mkv &
ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM2_IP:554/Streaming/Channels/2" -vcodec copy -an -t $LQLENGTH $LOCALSTORE/CAM2D_$STARTTIME.mkv &
ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM3_IP:554/Streaming/Channels/2" -vcodec copy -an -t $LQLENGTH $LOCALSTORE/CAM3D_$STARTTIME.mkv &
ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM4_IP:554/Streaming/Channels/2" -vcodec copy -an -t $LQLENGTH $LOCALSTORE/CAM4D_$STARTTIME.mkv &
ffmpeg -v 0 -rtsp_transport tcp -i "rtsp://CAM_USERNAME:CAM_PASSWORD@$CAM5_IP:554/Streaming/Channels/2" -vcodec copy -an -t $LQLENGTH $LOCALSTORE/CAM5D_$STARTTIME.mkv &
"""

# Delete old files script as a string
delete_script = """#!/bin/sh
LQDIR=$1
HQDIR=$2
LOCALSTOREF=$3

find $LQDIR -maxdepth 1 -type f -mtime +90 -exec rm {} \\;
find $HQDIR -maxdepth 1 -type f -mtime +3 -exec rm {} \\;
find $LOCALSTOREF -maxdepth 1 -type f -mmin +240 -exec rm {} \\;
"""

# Function to execute a script from a string
def execute_script(script, *args):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.sh') as temp_script:
        temp_script.write(script)
        temp_script_path = temp_script.name

    try:
        # Make the temporary script executable
        subprocess.run(['chmod', '+x', temp_script_path], check=True)
        # Execute the script with arguments
        command = [temp_script_path] + list(args)
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "Script executed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Script execution failed:\n{e}")
    finally:
        subprocess.run(['rm', '-f', temp_script_path])

# Main Tkinter window
root = tk.Tk()
root.title("IP Camera Bash Script Helper")

# Frame for inputs
frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky="NSEW")

# Variables for user input
start_time_var = tk.StringVar()
hq_dir_var = tk.StringVar()
lq_dir_var = tk.StringVar()
local_store_var = tk.StringVar()
hq_length_var = tk.StringVar(value="900")
lq_length_var = tk.StringVar(value="10800")
cam_ips = [tk.StringVar() for _ in range(5)]

# Helper function to create labels and entry widgets
def create_label_entry(frame, text, var, row, suggestion=""):
    ttk.Label(frame, text=text).grid(row=row, column=0, sticky="W")
    entry = ttk.Entry(frame, textvariable=var, width=30)
    entry.grid(row=row, column=1, padx=5, pady=2, sticky="EW")
    if suggestion:
        ttk.Label(frame, text=suggestion).grid(row=row, column=2, sticky="W")

# Create input fields
create_label_entry(frame, "Start Time Format", start_time_var, 0, "MM.DD.YYYY_[HHh_MMm_SSs]")
create_label_entry(frame, "HQ Directory", hq_dir_var, 1, "Path for HQ recordings")
create_label_entry(frame, "LQ Directory", lq_dir_var, 2, "Path for LQ recordings")
create_label_entry(frame, "Local Storage", local_store_var, 3, "Path for local storage")
create_label_entry(frame, "HQ Length (seconds)", hq_length_var, 4, "Recording time for HQ")
create_label_entry(frame, "LQ Length (seconds)", lq_length_var, 5, "Recording time for LQ")

# Camera IP inputs
for i, cam_ip in enumerate(cam_ips):
    create_label_entry(frame, f"Camera {i+1} IP", cam_ip, 6 + i, "IP address of camera")

# Functions to run the scripts
def run_hq_script():
    args = [start_time_var.get(), hq_dir_var.get(), hq_length_var.get()]
    args += [cam_ip.get() for cam_ip in cam_ips]
    execute_script(hq_script, *args)

def run_lq_script():
    args = [start_time_var.get(), lq_dir_var.get(), lq_length_var.get(), local_store_var.get()]
    args += [cam_ip.get() for cam_ip in cam_ips]
    execute_script(lq_script, *args)

def run_delete_script():
    args = [lq_dir_var.get(), hq_dir_var.get(), local_store_var.get()]
    execute_script(delete_script, *args)

# Buttons for running scripts
ttk.Button(frame, text="Run HQ Script", command=run_hq_script).grid(row=11, column=0, pady=10, sticky="EW")
ttk.Button(frame, text="Run LQ Script", command=run_lq_script).grid(row=11, column=1, pady=10, sticky="EW")
ttk.Button(frame, text="Run Delete Script", command=run_delete_script).grid(row=11, column=2, pady=10, sticky="EW")

# Main loop
root.mainloop()
