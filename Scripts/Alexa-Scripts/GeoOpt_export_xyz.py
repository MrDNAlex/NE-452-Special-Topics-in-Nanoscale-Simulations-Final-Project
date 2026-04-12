#find the optimized geometry coordinates within ORCA output file
#extract the coordinates 
#export corrdinates into an XYZ file for further processing

import os

def extract_optimized_geometry_orca(outfile, xyz_out=None):
    with open(outfile, "r") as f:
        lines = f.readlines()

    #Find all cartesian coordinate blocks
    coord_indices = []
    for i, line in enumerate(lines):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in line:
            coord_indices.append(i)

    #use the last coordinates for optimized geometry
    start = coord_indices[-1] + 2  #skip title and dashed line from ORCA formatting

    atoms = []
    for line in lines[start:]:
        if not line.strip():
            break  # end of coordinate block

        parts = line.split()
        if len(parts) < 4:
            break

        atom = parts[0]
        try:
            x, y, z = map(float, parts[1:4])
            atoms.append((atom, x, y, z))
        except ValueError:
            break
    
    # If no output filename is given, save beside the ORCA output file
    if xyz_out is None:
        base = os.path.splitext(outfile)[0]
        xyz_out = base + ".xyz"

    #write XYZ file
    with open(xyz_out, "w") as f:
        f.write(f"{len(atoms)}\n")
        f.write("Optimized geometry extracted from ORCA output\n")
        for atom, x, y, z in atoms:
            f.write(f"{atom:2s} {x:12.6f} {y:12.6f} {z:12.6f}\n")

    print(f"Optimized geometry written to: {xyz_out}")

#filepath for output file and new xyz file
extract_optimized_geometry_orca("/Users/alexaoriecuia/Desktop/NE452/452 project/run/Pro_Drug/Diclofenac_LDA.out")