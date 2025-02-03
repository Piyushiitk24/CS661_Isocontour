import vtk
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="VTK Volume Rendering with Phong Shading")
    parser.add_argument("--input", type=str, required=True, help="Path to 3D .vti file")
    parser.add_argument("--phong", type=int, choices=[0, 1], required=True, 
                       help="Enable Phong shading (1=Yes, 0=No)")
    args = parser.parse_args()

    # Load 3D data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(args.input)
    reader.Update()

    # Color Transfer Function
    color_tf = vtk.vtkColorTransferFunction()
    color_tf.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)    # Cyan
    color_tf.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)    # Blue
    color_tf.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)     # Dark Blue
    color_tf.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)    # Red
    color_tf.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)    # Orange
    color_tf.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)     # Yellow

    # Opacity Transfer Function
    opacity_tf = vtk.vtkPiecewiseFunction()
    opacity_tf.AddPoint(-4931.54, 1.0)
    opacity_tf.AddPoint(101.815, 0.002)
    opacity_tf.AddPoint(2594.97, 0.0)

    # Volume Properties
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color_tf)
    volume_property.SetScalarOpacity(opacity_tf)
    volume_property.SetInterpolationTypeToLinear()

    # Phong Shading (if enabled)
    if args.phong == 1:
        volume_property.ShadeOn()
        volume_property.SetAmbient(0.5)
        volume_property.SetDiffuse(0.5)
        volume_property.SetSpecular(0.5)

    # Volume Mapper
    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Volume Actor
    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volume_property)

    # Outline
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)

    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.AddActor(outline_actor)
    renderer.SetBackground(0.2, 0.3, 0.4)  # Dark blue background

    # Render Window
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)       # Fixed 1000x1000 window
    render_window.AddRenderer(renderer)

    # Interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()
    interactor.Start()

if __name__ == "__main__":
    main()