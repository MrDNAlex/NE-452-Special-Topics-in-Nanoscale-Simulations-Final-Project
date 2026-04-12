#from structure file, identify indices of atoms
#calculate bond lengths and angles
#export calculations into an excel file

! pip install "pandas<3"
! pip install git+https://github.com/Nano-DNA-Studios/NCL.git#egg=NCL

import pandas as pd
from ncl import Molecule

#read structure file
filepath = '/Users/alexaoriecuia/Desktop/Pro_Drug/Prednisone.xyz'
molecule2 = Molecule("Pred", filepath)
    
molecule2.displayBondGraph() 
print(molecule2.bonds) #prints raw data frame

#create list to store bond length data
bond_rows = []

#find bond neighbours and bond distances
for i, row in molecule2.bonds.iterrows():
    atom1 = row["Index"]
    atom1_type = row["Atom"]
    neighbors = row["Bonds"]
    distances = row["Bond Distance"]
    
    #append data to list
    for j, atom2 in enumerate(neighbors):
        bond_rows.append({
            "Atom1_Index": atom1,
            "Atom1_Type": atom1_type,
            "Atom2_Index": atom2,
            "Atom2_Type": molecule2.bonds.loc[atom2, "Atom"],
            "Bond_Length (Å)": distances[j]
        })

#convert list to dataframe
bond_df = pd.DataFrame(bond_rows)

#create list to store angle data
angle_rows = []

atom_types = molecule2.bonds.set_index("Index")["Atom"]

#find bond angles
for i, row in molecule2.bonds.iterrows():
    center = row["Index"]
    neighbors = row["Bonds"]
    
    #compare unique neighbours
    for a in range(len(neighbors)):
        for b in range(a+1, len(neighbors)):
            atom1 = neighbors[a]
            atom3 = neighbors[b]
            
            #calculate angle
            angle = molecule2.getAngleBetweenAtoms(atom1, center, atom3)
            
            #append data to list
            angle_rows.append({
                "Atom1_Index": atom1,
                "Atom1_Type": atom_types[atom1],
                "Center_Index": center,
                "Center_Type": atom_types[center],
                "Atom3_Index": atom3,
                "Atom3_Type": atom_types[atom3],
                "Angle (deg)": angle
            })

#convert list to dataframe
angle_df = pd.DataFrame(angle_rows)

#export data to excel file
with pd.ExcelWriter("molecule_analysis.xlsx") as writer:
    bond_df.to_excel(writer, sheet_name="Bond Lengths", index=False)
    angle_df.to_excel(writer, sheet_name="Angles", index=False)