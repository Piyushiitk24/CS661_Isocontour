CS661 Assignment - Volume Rendering Instructions

1. Requirements:
   - Python 3.x
   - VTK library (install via: pip install vtk)

2. Usage:
   python scripts/volume_render.py --input <path/to/3D.vti> --phong <0|1>

   Example:
   python scripts/volume_render.py --input data/Isabel_3D.vti --phong 1

3. Parameters:
   --input: Path to 3D VTKImageData file (e.g., Isabel_3D.vti)
   --phong: 1 to enable Phong shading, 0 to disable

4. Expected Output:
   - A 1000x1000 window showing volume rendering with outline.
   - Use mouse to rotate/zoom.