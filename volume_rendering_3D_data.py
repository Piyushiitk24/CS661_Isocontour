import vtk
import argparse
import os

def main():
    """
    Main function to perform 3D volume rendering of a .vti dataset using VTK.
    
    - Supports **interactive visualization** with user-defined Phong shading.
    - Uses **vtkSmartVolumeMapper()** for optimized volume rendering.
    - Applies **color and opacity transfer functions** to highlight volume details.
    - Includes **vtkOutlineFilter** to display a bounding box.

    Command-line Arguments:
        --input  : Filename of the 3D .vti dataset (assumed to be in the same directory).
        --phong  : Enable (1) or disable (0) Phong shading.
    """

    # Command-line argument parsing to allow user input
    parser = argparse.ArgumentParser(description="VTK Volume Rendering with Optional Phong Shading")
    parser.add_argument("--input", type=str, required=True,
                        help="Path (absolute or relative) to the 3D .vti file.")
    parser.add_argument("--phong", type=int, choices=[0, 1], required=True,
                        help="Enable Phong shading (1=Yes, 0=No)")
    args = parser.parse_args()

    # Ensure input file exists in the current directory
    input_file = os.path.basename(args.input)  # Extract only filename
    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"Error: Input file '{args.input}' not found or path is invalid.")

    # Load the 3D dataset from the input .vti file using vtkXMLImageDataReader
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()  # Ensure the file is fully read

    # ------------------------------
    # Define Transfer Functions
    # ------------------------------

    # Color Transfer Function: Maps scalar values to RGB colors
    color_tf = vtk.vtkColorTransferFunction()
    color_tf.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)  # Cyan
    color_tf.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)  # Blue
    color_tf.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)   # Dark Blue
    color_tf.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)  # Red
    color_tf.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)  # Orange
    color_tf.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)   # Yellow

    # Opacity Transfer Function: Controls transparency at different scalar values
    opacity_tf = vtk.vtkPiecewiseFunction()
    opacity_tf.AddPoint(-4931.54, 1.0)    # Fully opaque at lowest value
    opacity_tf.AddPoint(101.815, 0.002)   # Nearly transparent at intermediate value
    opacity_tf.AddPoint(2594.97, 0.0)     # Fully transparent at highest value

    # ------------------------------
    # Configure Volume Properties
    # ------------------------------

    # vtkVolumeProperty ties together:
    # - Color Transfer Function
    # - Opacity Transfer Function
    # - Interpolation type (Linear)
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color_tf)
    volume_property.SetScalarOpacity(opacity_tf)
    volume_property.SetInterpolationTypeToLinear()

    # If Phong shading is enabled, set shading coefficients
    if args.phong == 1:
        volume_property.ShadeOn()
        volume_property.SetAmbient(0.5)
        volume_property.SetDiffuse(0.5)
        volume_property.SetSpecular(0.5)

    # ------------------------------
    # Setup Volume Rendering
    # ------------------------------

    # vtkSmartVolumeMapper automatically selects the best volume rendering technique
    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create a vtkVolume object (actor) and assign the mapper and properties
    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volume_property)

    # ------------------------------
    # Add Outline for Context
    # ------------------------------

    # vtkOutlineFilter generates a bounding box around the dataset
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())
    
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)

    # ------------------------------
    # Setup Renderer and Window
    # ------------------------------

    # Create a vtkRenderer to display the volume and outline
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.AddActor(outline_actor)  # Add the bounding box
    renderer.SetBackground(1.0, 1.0, 1.0)  # Set background color to white

    # Create a vtkRenderWindow and add the renderer
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)  # Set the window size
    render_window.AddRenderer(renderer)

    # ------------------------------
    # Setup User Interaction
    # ------------------------------

    # Create an interactor to allow interactive exploration of the volume
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Initialize and start the rendering loop
    interactor.Initialize()
    interactor.Start()

if __name__ == "__main__":
    main()
