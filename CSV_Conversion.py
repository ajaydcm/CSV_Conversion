import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from pyulog import ULog
import pandas as pd
from pymavlink import mavutil

# Initialize Tkinter GUI
root = tk.Tk()
root.withdraw()

# Select log file
log_file = filedialog.askopenfilename(
    title="Select Log File (.bin or .ulg)",
    filetypes=[("BIN or ULog files", "*.bin *.ulg"), ("All files", "*.*")]
)

if not log_file:
    messagebox.showinfo("No File Selected", "No log file selected. Exiting.")
    sys.exit(0)

# Determine file type
ext = os.path.splitext(log_file)[1].lower()
if ext not in [".bin", ".ulg"]:
    messagebox.showerror("Unsupported Format", f"Unsupported file extension: {ext}")
    sys.exit(1)

# Select output folder
parent_folder = filedialog.askdirectory(title="Select Folder to Save CSV Logs")
if not parent_folder:
    messagebox.showinfo("No Folder Selected", "No output folder selected. Exiting.")
    sys.exit(0)

# Prepare output directory
basename = os.path.basename(log_file)
filename_no_ext = os.path.splitext(basename)[0]
output_dir = os.path.join(parent_folder, filename_no_ext)
os.makedirs(output_dir, exist_ok=True)

print(f"Selected log file: {log_file}")
print(f"CSV files will be saved to: {output_dir}")

# --------------------------------------
# Handler: ArduPilot BIN Log
# --------------------------------------
if ext == ".bin":
    print("Processing ArduPilot BIN log...")
    try:
        mav = mavutil.mavlink_connection(log_file, dialect="ardupilotmega")
        msg_types = set()

        while True:
            msg = mav.recv_match()
            if msg is None:
                break
            msg_types.add(msg.get_type())

        print(f"Found {len(msg_types)} message types.")
        for mtype in sorted(msg_types):
            csv_file = os.path.join(output_dir, f"{mtype}.csv")
            cmd = ["mavlogdump.py", log_file, "--types", mtype, "--format", "csv"]
            try:
                with open(csv_file, "w") as f:
                    subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)
                print(f"Saved {mtype} → {csv_file}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to export {mtype}")
                print(e.stderr.decode())
    except Exception as e:
        messagebox.showerror("BIN Parsing Failed", f"Failed to process BIN file:\n{e}")
        sys.exit(1)

# --------------------------------------
# Handler: PX4 ULog
# --------------------------------------
elif ext == ".ulg":
    print("Processing PX4 ULog...")
    try:
        ulog = ULog(log_file)
        print("Found the following topics in the log:")
        for data in ulog.data_list:
            print(f"- {data.name} (msg_id: {data.msg_id})")

        for data in ulog.data_list:
            topic_name = data.name
            msg_id = data.msg_id
            field_data = data.data

            if not field_data:
                print(f"Skipping topic {topic_name} (no data)")
                continue

            df = pd.DataFrame(field_data)
            safe_topic = topic_name.replace("/", "_")
            csv_path = os.path.join(output_dir, f"{safe_topic}_msgid_{msg_id}.csv")
            df.to_csv(csv_path, index=False)
            print(f"Saved topic {topic_name} → {csv_path}")
    except Exception as e:
        messagebox.showerror("ULog Parsing Failed", f"Failed to process ULog file:\n{e}")
        sys.exit(1)

# Final info
messagebox.showinfo("Export Complete", f"CSV files saved to:\n{output_dir}")
