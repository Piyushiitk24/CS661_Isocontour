**README.md**  
# CS661 Assignment Submission  

---

## **Part 1: 2D Isocontour Extraction (80 Points)**  
### Script: `extract_isocontour.py`  

#### **Requirements**  
- Input: 2D VTKImageData (e.g., `Isabel_2D.vti`).  
- Output: VTKPolyData (.vtp file) readable in ParaView.  
- Isovalue Range: `-1438 < isovalue < 630`.  

#### **How to Run**  
```bash  
python extract_isocontour.py \  
    --input <path/to/input.vti> \  
    --isovalue <VALUE> \  
    --output <path/to/output.vtp>  
```  

#### **Example**  
```bash  
python extract_isocontour.py \  
    --input Isabel_2D.vti \  
    --isovalue 100 \  
    --output contour.vtp  
```  

#### **Parameters**  
- `--input`: Path to the 2D `.vti` file (e.g., `Isabel_2D.vti`).  
- `--isovalue`: Scalar value for contour extraction (**must be in (-1438, 630)**).  
- `--output`: Path to save the output `.vtp` file.  

#### **Key Implementation Notes**  
1. **Algorithm**:  
   - Traverses cell edges **counterclockwise** (right → top → left → bottom).  
   - Uses **linear interpolation** to compute intersections.  
   - Ignores ambiguous cells (only processes cells with **exactly two intersections**).  
2. **VTK Usage**:  
   - No VTK filters (e.g., `vtkContourFilter`) are used.  
   - Only `vtkXMLImageDataReader` and `vtkXMLPolyDataWriter` for I/O.  
3. **Output**:  
   - `.vtp` file contains line segments stored in a `vtkCellArray`.  

---

## **Part 2: Volume Rendering (20 Points)**  
### Script: `volume_render.py`  

#### **Requirements**  
- Input: 3D VTKImageData (e.g., `Isabel_3D.vti`).  
- Phong Shading: Toggleable via command-line argument.  
- Render Window: Fixed size `1000x1000`.  

#### **How to Run**  
```bash  
python volume_render.py \  
    --input <path/to/input.vti> \  
    --phong <0|1>  
```  

#### **Example**  
```bash  
python volume_render.py \  
    --input Isabel_3D.vti \  
    --phong 1  
```  

#### **Parameters**  
- `--input`: Path to the 3D `.vti` file (e.g., `Isabel_3D.vti`).  
- `--phong`: Enable Phong shading:  
  - `1`: Enable (ambient/diffuse/specular = 0.5).  
  - `0`: Disable.  

#### **Key Implementation Notes**  
1. **Transfer Functions**:  
   - **Color**:  
     ```python  
     color_tf.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)  # Cyan  
     color_tf.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)  # Blue  
     color_tf.AddRGBPoint(-1873.9,  0.0, 0.0, 0.5)  # Dark Blue  
     color_tf.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)  # Red  
     color_tf.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)  # Orange  
     color_tf.AddRGBPoint(2594.97,  1.0, 1.0, 0.0)  # Yellow  
     ```  
   - **Opacity**:  
     ```python  
     opacity_tf.AddPoint(-4931.54, 1.0)  
     opacity_tf.AddPoint(101.815,  0.002)  
     opacity_tf.AddPoint(2594.97,  0.0)  
     ```  
2. **Volume Rendering**:  
   - Uses `vtkSmartVolumeMapper` for ray casting.  
   - Adds a white outline via `vtkOutlineFilter`.  
3. **Interaction**:  
   - Rotate: Left-click + drag.  
   - Zoom: Right-click + drag.  
   - Pan: Middle-click + drag.  

---

## **General Instructions**  
### **Prerequisites**  
1. Install VTK:  
   ```bash  
   pip install vtk  
   ```  
2. Datasets:  
   - Ensure `Isabel_2D.vti` and `Isabel_3D.vti` are in the working directory or provide full paths.  

### **Dataset Details**  
- **Source**: [VIS 2004 Contest Data](http://vis.computer.org/vis2004contest/index.html).  
- **Variable**: Pressure.  

### **Visualization in ParaView**  
1. **Isocontour (.vtp)**:  
   - Open in ParaView.  
   - Adjust line color and thickness under *Properties* → *Styling*.  
2. **Volume Rendering**:  
   - The script opens an interactive window automatically.  

### **Common Issues**  
- **File Not Found**: Use absolute paths if files are not in the working directory.  
- **VTK Errors**: Reinstall VTK with `pip install --force-reinstall vtk`.  

--- 

**Submitted By**: Lt Cdr Piyush Tiwari
**Student ID**: 241040099