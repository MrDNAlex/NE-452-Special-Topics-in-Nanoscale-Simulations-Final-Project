from Data import FUNCTIONALS, HARTREE_TO_KJMOL
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def Compare():
    # Create a Plots Directory
    os.makedirs("Results/Plots", exist_ok=True)

    # Load the Reference DataFrames
    masterDataFrame = pd.read_csv("Results/MasterEnthalpies.csv")
    literatureEnthalpiesDataFrame = pd.read_csv("Results/LiteratureEnthalpies.csv")

    comparisonDataFrame = literatureEnthalpiesDataFrame.copy()

    # Copy the Final Result Data Frames, and create a kJ/mol equivalent
    for func in FUNCTIONALS:
        columnName = f"{func} Enthalpy of Formation"
        comparisonDataFrame[f"{columnName} (Eh)"] = masterDataFrame[columnName]
        comparisonDataFrame[f"{columnName} (kJ/mol)"] = comparisonDataFrame[f"{columnName} (Eh)"] * HARTREE_TO_KJMOL

    # Get the Absolute Error of each functional
    for func in FUNCTIONALS:
        calculationColumn = f"{func} Enthalpy of Formation (kJ/mol)"
        literatureColumn = "Lit Enthalpy (kJ/mol)"
        errorColumn = f"{func} Error (kJ/mol)"
        absErrorColumn = f"{func} Abs Error (kJ/mol)"
        
        comparisonDataFrame[errorColumn] = comparisonDataFrame[calculationColumn] - comparisonDataFrame[literatureColumn]
        comparisonDataFrame[absErrorColumn] = comparisonDataFrame[errorColumn].abs()

    MAEValues = {}
    for func in FUNCTIONALS:
        absoluteErrorColumn = f"{func} Abs Error (kJ/mol)"
        MAEValues[func] = comparisonDataFrame[absoluteErrorColumn].mean()

    print(comparisonDataFrame)
    comparisonDataFrame.to_csv("Results/Comparisons.csv")

    # Plot Mean Absolute Error
    plt.figure(figsize=(8, 6))

    # Create bars representing the overall average error
    bars = plt.bar(MAEValues.keys(), MAEValues.values(), color=['skyblue', 'lightgreen', 'salmon', 'orchid', 'orange'])

    plt.title("Mean Absolute Error (MAE) by Functional", fontsize=14)
    plt.xlabel("Density Functional", fontsize=12)
    plt.ylabel("MAE (kJ/mol)", fontsize=12)

    # Add text labels on top of bars
    for bar in bars:
        yValue = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yValue + (max(MAEValues.values()) * 0.02), 
                round(yValue, 2), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("Results/Plots/MAE_Comparison.png")

    # Graph Individual Molecule Errors
    xPositions = np.arange(len(comparisonDataFrame['Molecule']))
    barWidth = 0.15 
    multiplier = 0

    fig, ax = plt.subplots(figsize=(14, 6))

    # Loop through each functional and plot its errors
    for func in FUNCTIONALS:
        absoluteErrorColumn = f"{func} Abs Error (kJ/mol)"
        offset = barWidth * multiplier
        
        ax.bar(xPositions + offset, comparisonDataFrame[absoluteErrorColumn], barWidth, label=func)
        multiplier += 1

    ax.set_title("Absolute Enthalpy Error per Molecule", fontsize=14)
    ax.set_xlabel("Molecule", fontsize=12)
    ax.set_ylabel("Absolute Error (kJ/mol)", fontsize=12)

    # Center the x-ticks under the grouped bars
    ax.set_xticks(xPositions + barWidth * (len(FUNCTIONALS) - 1) / 2)
    ax.set_xticklabels(comparisonDataFrame['Molecule'], rotation=45, ha='right')

    # Draw manual category lines and labels
    manualBoundaries = [8.5, 13.5]
    manualCenters = [3.5, 11.0, 17.5]
    manualLabels = ['Alkanes', 'Organic', 'Pro-Drug']

    # Adjust y-axis limits to fit headers
    yMax = ax.get_ylim()[1]
    ax.set_ylim(top=yMax * 1.2)
    yMax = ax.get_ylim()[1]

    offset = barWidth * (len(FUNCTIONALS) - 1) / 2

    # Draw the vertical lines
    for boundary in manualBoundaries:
        ax.axvline(x=boundary + offset, color='gray', linestyle='--', alpha=0.5, linewidth=2)

    # Place the text headers
    for center, label in zip(manualCenters, manualLabels):
        ax.text(x=center + offset, y=yMax * 0.90, s=label, 
                ha='center', va='bottom', fontsize=16, fontweight='bold', color='dimgray')

    ax.legend(title='Functional')

    plt.tight_layout()
    plt.savefig("Results/Plots/MAE_Molecule_Comparison.png")

    # 1. Define the number of atoms for each molecule
    atomCounts = {
        'Methane': 5, 'Ethane': 8, 'Propane': 11, 'Butane': 14, 
        'Pentane': 17, 'Hexane': 20, 'Heptane': 23, 'Octane': 26, 
        'Nonane': 29, 'Ethanol': 9, 'Pyrrole': 10, 'Acetone': 10, 
        'Acetic Acid': 8, 'Benzene': 12, 'Toluene': 15, 'Methanol': 6,
        'Propanol': 12, 'Formaldehyde': 4, 'Acetaldehyde': 7,
        'Aspirin': 21, 'Acetaminophen': 20, 'Diclofenac': 30, 'Ibuprofen': 33, 
        'Azobenzene': 24, 'Caffeine': 24, 'Hydrocortisone': 56, 
        'Dexamethasone': 57, 'Prednisone': 52
    }

    # Map the counts and sort the DataFrame
    comparisonDataFrame['Atom Count'] = comparisonDataFrame['Molecule'].map(atomCounts)
    comparisonDataFrame['Atom Count'] = comparisonDataFrame['Atom Count'].fillna(0).astype(int)

    # Sort strictly by the size of the molecule
    comparisonDataFrame = comparisonDataFrame.sort_values('Atom Count').reset_index(drop=True)

    # Setup the graph layout
    xPositions = np.arange(len(comparisonDataFrame['Molecule']))
    barWidth = 0.15 
    multiplier = 0

    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot the bars
    for func in FUNCTIONALS:
        absoluteErrorColumn = f"{func} Abs Error (kJ/mol)"
        offset = barWidth * multiplier
        ax.bar(xPositions + offset, comparisonDataFrame[absoluteErrorColumn], barWidth, label=func)
        multiplier += 1

    # Make it Pretty
    ax.set_title("Absolute Enthalpy Error per Molecule (Sorted by Size)", fontsize=18, pad=20)
    ax.set_ylabel("Absolute Error (kJ/mol)", fontsize=14)
    ax.set_xlabel("Molecule (Increasing Atom Count →)", fontsize=14)

    # Set standard bottom labels
    tickPositions = xPositions + barWidth * (len(FUNCTIONALS) - 1) / 2
    ax.set_xticks(tickPositions)

    # Create compound labels showing the molecule and its atom count
    sizeLabels = [f"{mol}\n({count} atoms)" for mol, count in zip(comparisonDataFrame['Molecule'], comparisonDataFrame['Atom Count'])]
    ax.set_xticklabels(sizeLabels, rotation=45, ha='right', fontsize=11)

    # Clean up borders and legend
    ax.legend(title='Functional', bbox_to_anchor=(1.01, 1), loc='upper left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig("Results/Plots/Size_Sorted_Molecule_Errors.png")
    plt.show()

if __name__ == "__main__":
    Compare()