import vtk
import argparse
import os

def extract_isocontour(input_file, isovalue, output_file):
    # Read input data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    image_data = reader.GetOutput()

    # Validate dataset is 2D
    dims = image_data.GetDimensions()
    if dims[2] != 1:
        raise ValueError("Input data must be a 2D grid.")

    origin = image_data.GetOrigin()
    spacing = image_data.GetSpacing()
    scalars = image_data.GetPointData().GetScalars()

    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()
    point_ids = {}  # Track unique points using rounded coordinates

    # Iterate over each cell (counterclockwise edge checks)
    for j in range(dims[1] - 1):
        for i in range(dims[0] - 1):
            # Cell indices
            idx00 = j * dims[0] + i
            idx10 = idx00 + 1
            idx11 = idx10 + dims[0]
            idx01 = idx00 + dims[0]

            s00 = scalars.GetTuple1(idx00)
            s10 = scalars.GetTuple1(idx10)
            s11 = scalars.GetTuple1(idx11)
            s01 = scalars.GetTuple1(idx01)

            intersections = []

            # Edge 0: (i,j) to (i+1,j) - right edge
            if (s00 <= isovalue) != (s10 <= isovalue):
                t = (isovalue - s00) / (s10 - s00) if (s10 - s00) != 0 else 0.0
                x = origin[0] + (i + t) * spacing[0]
                y = origin[1] + j * spacing[1]
                intersections.append((x, y))

            # Edge 1: (i+1,j) to (i+1,j+1) - top edge
            if (s10 <= isovalue) != (s11 <= isovalue):
                t = (isovalue - s10) / (s11 - s10) if (s11 - s10) != 0 else 0.0
                x = origin[0] + (i + 1) * spacing[0]
                y = origin[1] + (j + t) * spacing[1]
                intersections.append((x, y))

            # Edge 2: (i+1,j+1) to (i,j+1) - left edge
            if (s11 <= isovalue) != (s01 <= isovalue):
                t = (isovalue - s11) / (s01 - s11) if (s01 - s11) != 0 else 0.0
                x = origin[0] + (i + 1 - t) * spacing[0]
                y = origin[1] + (j + 1) * spacing[1]
                intersections.append((x, y))

            # Edge 3: (i,j+1) to (i,j) - bottom edge
            if (s01 <= isovalue) != (s00 <= isovalue):
                t = (isovalue - s01) / (s00 - s01) if (s00 - s01) != 0 else 0.0
                x = origin[0] + i * spacing[0]
                y = origin[1] + (j + 1 - t) * spacing[1]
                intersections.append((x, y))

            # Add line segment if exactly two intersections (non-ambiguous)
            if len(intersections) == 2:
                pid0 = points.InsertNextPoint(intersections[0][0], intersections[0][1], 0.0)
                pid1 = points.InsertNextPoint(intersections[1][0], intersections[1][1], 0.0)
                lines.InsertNextCell(2)
                lines.InsertCellPoint(pid0)
                lines.InsertCellPoint(pid1)

    # Save output
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)
    writer.SetInputData(polydata)
    writer.Write()

def main():
    parser = argparse.ArgumentParser(description="Extract 2D isocontour from VTKImageData.")
    parser.add_argument("--input", type=str, required=True, help="Path to input .vti file")
    parser.add_argument("--isovalue", type=float, required=True, help="Isovalue in range (-1438, 630)")
    parser.add_argument("--output", type=str, required=True, help="Path to output .vtp file")
    args = parser.parse_args()

    if not (-1438 < args.isovalue < 630):
        raise ValueError("Isovalue must be in (-1438, 630)")

    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extract_isocontour(args.input, args.isovalue, args.output)

if __name__ == "__main__":
    main()