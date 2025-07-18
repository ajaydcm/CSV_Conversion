# Log to CSV Converter

This tool allows you to convert `.bin` or `.ulg` log files from PX4 or ArduPilot into CSV format using a graphical file picker.

## Clone the Repository to Your Local System
```bash
    git clone https://github.com/ajaydcm/CSV_Conversion.git
    cd CSV_Conversion
```
## 🛠️ Requirements

- Python 3.x
- `requirements.txt` includes:
  - `pyulog`
  - `pymavlink`
  - `pandas`
  - `tkinter` (install separately if on Linux)

### 📦 Install Requirements

```bash
pip install -r requirements.txt
```
### ▶️ Run the Script
```bash 
python CSV_Conversion.py 
```

## 🪟 What Happens After Running
- A file picker will open — select your .bin or .ulg log file.

- Another dialog will appear — select the folder where you want the CSV files to be saved.

- The script will automatically convert the log file into multiple CSVs and store them in a subfolder named after the log file.