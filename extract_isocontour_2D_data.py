import vtk
import argparse
import os

def extract_isocontour(input_file, isovalue, output_file):
    """
    Reads a 2D uniform grid dataset from a VTK ImageData (.vti) file, extracts isocontour
    segments based on a given isovalue, and saves the resulting contour as a VTK PolyData (.vtp) file.

    - The script **does not use VTK's built-in contour filter**, as per assignment requirements.
    - Instead, it **manually computes intersections** along cell edges using linear interpolation.
    - **Only handles simple cases** (no ambiguity resolution), following counterclockwise traversal.
    
    Parameters:
        input_file (str): Filename of the input .vti file (assumed to be in the same directory).
        isovalue (float): Scalar value for contour extraction.
        output_file (str): Filename of the output .vtp file (saved in the same directory).
    """

    # Ensure input file exists in the current directory
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Error: Input file '{input_file}' not found in the current directory.")

    # Read the 2D dataset from the input .vti file
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    image_data = reader.GetOutput()

    # Ensure the dataset is truly 2D (third dimension should be 1)
    dims = image_data.GetDimensions()  # (width, height, depth)
    if dims[2] != 1:
        raise ValueError("Error: The input dataset is not 2D. Expected depth = 1.")

    # Get dataset properties: origin, spacing, and scalar values
    origin = image_data.GetOrigin()  # (x0, y0, z0)
    spacing = image_data.GetSpacing()  # (dx, dy, dz)
    scalars = image_data.GetPointData().GetScalars()  # Extract scalar field values

    # Initialize VTK structures for storing extracted contour points and line segments
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    # Iterate over each cell in the grid
    for j in range(dims[1] - 1):  # Row-wise traversal
        for i in range(dims[0] - 1):  # Column-wise traversal

            # Identify the four corner indices of the cell (bottom-left, bottom-right, top-right, top-left)
            idx00 = j * dims[0] + i       # (i, j)
            idx10 = idx00 + 1             # (i+1, j)
            idx11 = idx10 + dims[0]       # (i+1, j+1)
            idx01 = idx00 + dims[0]       # (i, j+1)

            # Retrieve scalar values at these corners
            s00 = scalars.GetTuple1(idx00)
            s10 = scalars.GetTuple1(idx10)
            s11 = scalars.GetTuple1(idx11)
            s01 = scalars.GetTuple1(idx01)

            # Store the intersection points for this cell
            intersections = []

            # -- Edge 0: Bottom edge (left to right)
            if (s00 <= isovalue) != (s10 <= isovalue):  # Opposite sides of isovalue
                t = (isovalue - s00) / (s10 - s00) if s10 != s00 else 0.0
                x = origin[0] + (i + t) * spacing[0]
                y = origin[1] + j * spacing[1]
                intersections.append((x, y))

            # -- Edge 1: Right edge (bottom to top)
            if (s10 <= isovalue) != (s11 <= isovalue):
                t = (isovalue - s10) / (s11 - s10) if s11 != s10 else 0.0
                x = origin[0] + (i + 1) * spacing[0]
                y = origin[1] + (j + t) * spacing[1]
                intersections.append((x, y))

            # -- Edge 2: Top edge (right to left)
            if (s11 <= isovalue) != (s01 <= isovalue):
                t = (isovalue - s11) / (s01 - s11) if s01 != s11 else 0.0
                x = origin[0] + (i + 1 - t) * spacing[0]
                y = origin[1] + (j + 1) * spacing[1]
                intersections.append((x, y))

            # -- Edge 3: Left edge (top to bottom)
            if (s01 <= isovalue) != (s00 <= isovalue):
                t = (isovalue - s01) / (s00 - s01) if s00 != s01 else 0.0
                x = origin[0] + i * spacing[0]
                y = origin[1] + (j + 1 - t) * spacing[1]
                intersections.append((x, y))

            # If exactly two intersection points exist, add a line segment
            if len(intersections) == 2:
                pid0 = points.InsertNextPoint(intersections[0][0], intersections[0][1], 0.0)
                pid1 = points.InsertNextPoint(intersections[1][0], intersections[1][1], 0.0)
                lines.InsertNextCell(2)
                lines.InsertCellPoint(pid0)
                lines.InsertCellPoint(pid1)

    # Store the computed contour as VTK PolyData
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)

    # Write the extracted isocontour to a .vtp file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)
    writer.SetInputData(polydata)
    writer.Write()

def main():
    """
    Parses command-line arguments, validates input values, and calls the isocontour extraction function.
    """
    parser = argparse.ArgumentParser(description="Extract a 2D isocontour from a VTK image dataset.")
    parser.add_argument("--input", type=str, required=True, help="Filename of the input .vti file (should be in the same directory).")
    parser.add_argument("--isovalue", type=float, required=True, help="Isovalue for contour extraction (-1438 to 630).")
    parser.add_argument("--output", type=str, required=True, help="Filename to save the output .vtp file (saved in the same directory).")
    args = parser.parse_args()

    # Validate isovalue range
    if not (-1438 < args.isovalue < 630):
        raise ValueError("Error: Isovalue must be within the range (-1438, 630).")

    # Ensure input filename is correct (no paths, just filenames)
    input_file = os.path.basename(args.input)
    output_file = os.path.basename(args.output)  # Extract only filename

    # Call extraction function
    extract_isocontour(input_file, args.isovalue, output_file)

if __name__ == "__main__":
    main()
