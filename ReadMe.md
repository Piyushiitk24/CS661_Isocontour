# README.txt - CS661 Assignment 1  
## Isocontour and Volume Visualization  
### Course: CS661 - Big Data Visual Analytics  
### Submitted By:  
- Group Number: `28`  
- Roll Numbers: `241040099, 242110601`  

---

## Requirements  
Before running the scripts, ensure the following are installed:  

### 1. Required Software
- Python 3.x  
- VTK (Python module)  

### 2. Install VTK if Not Installed
Run the following command in the terminal or command prompt:  
```bash
pip install vtk
```
(*If working in a virtual environment, activate it first using `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows) before running the above command.*)  

---

## Project Files
```
CS661_Isocontour/
│── extract_isocontour_2D_data.py
│── volume_rendering_3D_data.py
│── README.txt
│── Isabel_2D.vti   <-- Data file for isocontour extraction
│── Isabel_3D.vti   <-- Data file for volume rendering
│── extracted_isocontour.vtp  <-- Example output file
```

### Files in This Project
| File | Description |
|------|-------------|
| `extract_isocontour_2D_data.py` | Extracts a 2D isocontour from a `.vti` file and saves it as a `.vtp` file for visualization in ParaView. |
| `volume_rendering_3D_data.py` | Performs 3D volume rendering of a `.vti` dataset and opens an interactive window for visualization. |

---

## 1. Running the 2D Isocontour Extraction Script  
This script extracts **isocontours from a 2D `.vti` dataset** and saves the result in a **`.vtp` file** for visualization in ParaView.

### Command to Run:
```bash
python extract_isocontour_2D_data.py --input Isabel_2D.vti --isovalue -500 --output extracted_isocontour.vtp
```

### Arguments Explained:
| Argument | Description |
|----------|-------------|
| `--input` | Filename of the 2D `.vti` file (should be `Isabel_2D.vti` in the same folder). |
| `--isovalue` | A floating-point value for contour extraction (e.g., `-500`). |
| `--output` | Filename to save the output `.vtp` file (saved in the same folder). |

### Output File
- The extracted isocontour will be saved as `extracted_isocontour.vtp` in the **same directory as the script**.
- To specify a different name, modify the `--output` argument.

### Viewing the Output in ParaView
1. Open **ParaView**.
2. Click **File → Open** and select `extracted_isocontour.vtp`.
3. Click **Apply** to visualize the isocontour.
4. Change the **coloring settings** in **Properties Panel → Coloring** to **"Solid Color"** for better visibility.

---

## 2. Running the 3D Volume Rendering Script  
This script performs **3D volume rendering** using VTK.

### Command to Run:
```bash
python volume_rendering_3D_data.py --input Isabel_3D.vti --phong 1
```
For **Phong shading off**:
```bash
python volume_rendering_3D_data.py --input Isabel_3D.vti --phong 0
```

### Arguments Explained:
| Argument | Description |
|----------|-------------|
| `--input` | Filename of the 3D `.vti` file (should be `Isabel_3D.vti` in the same folder). |
| `--phong` | Set `1` to enable Phong shading, `0` to disable it. |

### What Happens Next?
- A **1000×1000 render window** will open showing the **3D volume rendering**.
- If **Phong shading is enabled (`--phong 1`)**, lighting effects will be applied.
- You can **rotate, zoom, and explore** the visualization interactively.
- **Close the window** when done.

---

## Important Notes
✅ **Keep all files in the same directory.**  
✅ **No additional folders (`data/`, `results/`) are required.**  
✅ **Copy-paste the above commands directly into the terminal to run the scripts.**  
✅ **Make sure you have `VTK` installed using:**
```bash
pip install vtk
```

---

## ParaView Visualization Settings
- **For Isocontour Visualization** (`.vtp` files):
  - Open in **ParaView** and set **"Solid Color"** for better visibility.
  - Change the background color for contrast if needed.
- **For Volume Rendering**:
  - If exporting manually to ParaView, use **Jet or CoolWarm colormap** for better contrast.

---

## Running Inside a Virtual Environment
- If using a Python virtual environment, activate it before running the scripts:
  ```bash
  source venv/bin/activate  # macOS/Linux
  venv\Scripts\activate     # Windows
  ```
- The scripts **will work without a virtual environment** as long as Python and VTK are installed.

---

## ✅ Final Commands to Run
```bash
# Extract 2D isocontour
python extract_isocontour_2D_data.py --input Isabel_2D.vti --isovalue 100 --output extracted_isocontour.vtp

# Run 3D volume rendering
python volume_rendering_3D_data.py --input Isabel_3D.vti --phong 1
```