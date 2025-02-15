CS661 Assignment 1 Submission
============================
Name: Lt Cdr Piyush Tiwari
Student ID: 241040099

Required Setup
-------------
- Python 3.6 or higher
- VTK 9.0 or higher (installed via: pip install vtk)
- Isabel_2D.vti and Isabel_3D.vti files in the working directory

================================================================================
1. Isocontour Extraction Script (Part 1)
================================================================================
My script extract_isocontour.py generates isocontours from the Isabel_2D.vti 
hurricane pressure data. 

To run my script:
----------------
python extract_isocontour.py --input Isabel_2D.vti --isovalue 100 --output contour.vtp

Required parameters:
--input    : Isabel_2D.vti file
--isovalue : Any value between -1438 and 630 (Note: isovalue=100 produces a clear 
            cyclone contour pattern)
--output   : Name of output .vtp file (e.g., contour.vtp)

To view the results:
-------------------
1. Open the output .vtp file in ParaView
2. Important: Change ParaView's background to white for better contour visibility
3. The contour should appear as continuous lines showing the hurricane structure
4. Adjust contour color if needed for better contrast against white background

================================================================================
2. Volume Rendering Script (Part 2)
================================================================================
My script volume_render.py visualizes the Isabel_3D.vti hurricane data with 
configurable Phong shading.

To run my script:
----------------
With Phong shading:
python volume_render.py --input Isabel_3D.vti --phong 1

Without Phong shading:
python volume_render.py --input Isabel_3D.vti --phong 0

Required parameters:
--input : Isabel_3D.vti file
--phong : 1 for Phong shading enabled, 0 for disabled

The script will open a 1000x1000 window showing the volume rendering. You can:
- Rotate the volume: Left mouse button + drag
- Zoom: Right mouse button + drag
- Pan: Middle mouse button + drag

================================================================================
Troubleshooting
================================================================================
If you encounter any issues running my scripts:

1. File errors:
   - Ensure Isabel_2D.vti and Isabel_3D.vti are in the same directory as the scripts
   - Or provide complete paths to the files

2. VTK issues:
   - Try reinstalling VTK: pip install --force-reinstall vtk

3. Visualization:
   - Part 1: Make sure to set white background in ParaView
   - Part 2: If display is blank, try rotating the volume

Contact: 241040099@iitk.ac.in if you need any clarification about running my scripts.