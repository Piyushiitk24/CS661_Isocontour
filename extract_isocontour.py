# extract_isocontour.py
# CS661 Assignment - 2D Isocontour Extraction
# -----------------------------------------------------------------------------
# This script extracts an isocontour from a 2D grid using a simplified method.
# Key requirements met:
# - No VTK filters used (written from scratch)
# - Counterclockwise edge traversal
# - Handles non-ambiguous cases only
# - Works for any isovalue in (-1438, 630)
# -----------------------------------------------------------------------------

import vtk
import argparse
import os

def extract_isocontour(input_file, isovalue, output_file):
    """
    Extracts isocontour segments from a 2D grid and saves them as a .vtp file.
    
    Steps:
      1. Read input .vti file
      2. Check each cell's edges for intersections with the isovalue
      3. Store intersection points and create line segments
      4. Save results as a VTKPolyData (.vtp) file
    """
    
    # =========================================================================
    # Step 1: Read Input Data
    # =========================================================================
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)   # Load the input file
    reader.Update()
    image_data = reader.GetOutput()  # Get the 2D grid data

    # Basic validation: Ensure the dataset is 2D (depth = 1)
    dims = image_data.GetDimensions()  # Format: (width, height, depth)
    if dims[2] != 1:
        raise ValueError("Error: Input must be a 2D dataset (depth=1).")

    # Grid properties
    origin = image_data.GetOrigin()   # Starting point (x0, y0, z0)
    spacing = image_data.GetSpacing() # Distance between grid points (dx, dy, dz)
    scalars = image_data.GetPointData().GetScalars()  # Scalar values at each point

    # =========================================================================
    # Step 2: Prepare Output Structures
    # =========================================================================
    points = vtk.vtkPoints()    # Stores (x,y) coordinates of intersection points
    lines = vtk.vtkCellArray()  # Stores line segments connecting the points
    scalar_values = vtk.vtkFloatArray()  # Stores scalar values for colouring
    scalar_values.SetName("Pressure")    # Name of the scalar field (for ParaView)

    # =========================================================================
    # Step 3: Process Each Cell in the Grid
    # =========================================================================
    # Loop through all cells (a cell is the area between 4 grid points)
    for row in range(dims[1] - 1):    # Iterate over rows (y-axis)
        for col in range(dims[0] - 1): # Iterate over columns (x-axis)
            
            # -------------------------------------------------------------
            # Get scalar values at the 4 corners of the current cell
            # -------------------------------------------------------------
            # Corner indices (see ASCII art below)
            #  idx01 ------ idx11
            #    |           |
            #    |   Cell    |
            #    |           |
            #  idx00 ------ idx10
            idx00 = row * dims[0] + col      # Bottom-left corner
            idx10 = idx00 + 1                # Bottom-right corner
            idx11 = idx10 + dims[0]          # Top-right corner
            idx01 = idx00 + dims[0]          # Top-left corner

            s00 = scalars.GetTuple1(idx00)  # Value at bottom-left
            s10 = scalars.GetTuple1(idx10)  # Value at bottom-right
            s11 = scalars.GetTuple1(idx11)  # Value at top-right
            s01 = scalars.GetTuple1(idx01)  # Value at top-left

            # -------------------------------------------------------------
            # Check edges for intersections (counterclockwise order)
            # -------------------------------------------------------------
            intersections = []  # Store intersection points for this cell

            # Edge 0: Bottom edge (left to right)
            if (s00 <= isovalue) != (s10 <= isovalue):
                # Linear interpolation to find intersection point
                t = (isovalue - s00) / (s10 - s00) if (s10 != s00) else 0.0
                x = origin[0] + (col + t) * spacing[0]
                y = origin[1] + row * spacing[1]
                intersections.append((x, y))

            # Edge 1: Right edge (bottom to top)
            if (s10 <= isovalue) != (s11 <= isovalue):
                t = (isovalue - s10) / (s11 - s10) if (s11 != s10) else 0.0
                x = origin[0] + (col + 1) * spacing[0]
                y = origin[1] + (row + t) * spacing[1]
                intersections.append((x, y))

            # Edge 2: Top edge (right to left)
            if (s11 <= isovalue) != (s01 <= isovalue):
                t = (isovalue - s11) / (s01 - s11) if (s01 != s11) else 0.0
                x = origin[0] + (col + 1 - t) * spacing[0]
                y = origin[1] + (row + 1) * spacing[1]
                intersections.append((x, y))

            # Edge 3: Left edge (top to bottom)
            if (s01 <= isovalue) != (s00 <= isovalue):
                t = (isovalue - s01) / (s00 - s01) if (s00 != s01) else 0.0
                x = origin[0] + col * spacing[0]
                y = origin[1] + (row + 1 - t) * spacing[1]
                intersections.append((x, y))

            # -------------------------------------------------------------
            # Add line segment if exactly two intersections (non-ambiguous)
            # -------------------------------------------------------------
            if len(intersections) == 2:
                # Add points to the VTKPoints structure
                point0_id = points.InsertNextPoint(intersections[0][0], intersections[0][1], 0.0)
                point1_id = points.InsertNextPoint(intersections[1][0], intersections[1][1], 0.0)
                scalar_values.InsertNextValue(isovalue)  # Assign isovalue to both points
                scalar_values.InsertNextValue(isovalue)
                
                # Create a line segment between the two points
                lines.InsertNextCell(2)  # '2' means a line segment
                lines.InsertCellPoint(point0_id)
                lines.InsertCellPoint(point1_id)

    # =========================================================================
    # Step 4: Save Results
    # =========================================================================
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)  # Attach all points
    polydata.SetLines(lines)    # Attach all line segments
    polydata.GetPointData().SetScalars(scalar_values)  # Attach scalar data for colouring

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)  # Set output filename
    writer.SetInputData(polydata)    # Connect the data
    writer.Write()                   # Write to disk
    print(f"Isocontour successfully written to {output_file}!")

def main():
    """Handles command-line arguments and runs the extraction."""
    
    # Set up command-line interface
    parser = argparse.ArgumentParser(
        description="Extract a 2D isocontour from Hurricane Pressure Data",
        epilog="Example: python extract_isocontour.py --input Isabel_2D.vti --isovalue 100 --output contour.vtp"
    )
    parser.add_argument("--input", type=str, required=True, 
                       help="Path to input .vti file (e.g., Isabel_2D.vti)")
    parser.add_argument("--isovalue", type=float, required=True,
                       help="Isovalue between -1438 and 630")
    parser.add_argument("--output", type=str, required=True,
                       help="Filename for output .vtp file (e.g., contour.vtp)")
    args = parser.parse_args()

    # Validate isovalue range
    if not (-1438 < args.isovalue < 630):
        raise ValueError(f"Isovalue {args.isovalue} is outside allowed range (-1438, 630).")

    # Ensure input file exists
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file '{args.input}' not found.")

    # Create output directory if needed
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run extraction
    extract_isocontour(args.input, args.isovalue, args.output)
    print(f"Success! Contour saved to {args.output}")

if __name__ == "__main__":
    main()