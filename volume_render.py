# volume_render.py
# CS661 Assignment - Volume Rendering with VTK
# -----------------------------------------------------------------------------
# This script renders a 3D volume dataset with color/opacity transfer functions
# and optional Phong shading for realistic lighting effects.
# -----------------------------------------------------------------------------

import vtk
import argparse
import os

def render_volume(input_file, use_phong):
    """
    Renders a 3D volume dataset with customizable transfer functions and lighting.
    
    Steps:
      1. Read 3D volume data
      2. Configure color/opacity transfer functions
      3. Set up volume rendering properties
      4. Add bounding box outline
      5. Create render window and display results
    """
    
    # =========================================================================
    # Step 1: Read Input Data
    # =========================================================================
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Error: Input file '{input_file}' not found.")

    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)  # Load 3D hurricane data
    reader.Update()

    # =========================================================================
    # Step 2: Configure Color Transfer Function
    # =========================================================================
    color_tf = vtk.vtkColorTransferFunction()
    
    # Add RGB control points (Data Value, Red, Green, Blue)
    color_tf.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)   # Cyan
    color_tf.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)   # Blue
    color_tf.AddRGBPoint(-1873.9,  0.0, 0.0, 0.5)   # Dark Blue
    color_tf.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)   # Red
    color_tf.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)   # Orange
    color_tf.AddRGBPoint(2594.97,  1.0, 1.0, 0.0)   # Yellow

    # =========================================================================
    # Step 3: Configure Opacity Transfer Function
    # =========================================================================
    opacity_tf = vtk.vtkPiecewiseFunction()
    
    # Add opacity control points (Data Value, Opacity)
    opacity_tf.AddPoint(-4931.54, 1.0)    # Fully opaque
    opacity_tf.AddPoint(101.815,  0.002)  # Nearly transparent
    opacity_tf.AddPoint(2594.97,  0.0)    # Fully transparent

    # =========================================================================
    # Step 4: Set Up Volume Properties
    # =========================================================================
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color_tf)          # Connect color function
    volume_property.SetScalarOpacity(opacity_tf) # Connect opacity function
    volume_property.SetInterpolationTypeToLinear() # Smooth rendering

    # Configure Phong shading if enabled
    if use_phong:
        volume_property.ShadeOn()                # Enable lighting
        volume_property.SetAmbient(0.5)          # Ambient light contribution
        volume_property.SetDiffuse(0.5)          # Diffuse light contribution
        volume_property.SetSpecular(0.5)         # Specular highlights

    # =========================================================================
    # Step 5: Create Volume Mapper
    # =========================================================================
    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputConnection(reader.GetOutputPort())  # Connect to data

    # =========================================================================
    # Step 6: Create Volume Actor
    # =========================================================================
    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)            # Connect mapper
    volume.SetProperty(volume_property) # Apply visual properties

    # =========================================================================
    # Step 7: Add Bounding Box Outline
    # =========================================================================
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort()) # Same data as volume

    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())

    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(1, 1, 1)  # White outline

    # =========================================================================
    # Step 8: Set Up Rendering Window
    # =========================================================================
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)          # Add volume to scene
    renderer.AddActor(outline_actor)    # Add outline to scene
    renderer.SetBackground(0.2, 0.3, 0.4)  # Dark blue background

    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)   # Fixed window size as per requirements
    render_window.AddRenderer(renderer)

    # =========================================================================
    # Step 9: Enable Interaction
    # =========================================================================
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()  # Prepare for user interaction
    interactor.Start()

def main():
    """Handles command-line arguments and starts rendering."""
    
    parser = argparse.ArgumentParser(
        description="Render 3D Hurricane Volume Data with VTK",
        epilog="Example: python volume_render.py --input Isabel_3D.vti --phong 1"
    )
    parser.add_argument("--input", type=str, required=True,
                       help="Path to 3D .vti file (e.g., Isabel_3D.vti)")
    parser.add_argument("--phong", type=int, choices=[0, 1], required=True,
                       help="Enable Phong shading (1=Yes, 0=No)")
    args = parser.parse_args()

    render_volume(args.input, args.phong)

if __name__ == "__main__":
    main()