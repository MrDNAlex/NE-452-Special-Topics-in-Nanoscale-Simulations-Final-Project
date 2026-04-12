# NE-452-Special-Topics-in-Nanoscale-Simulations-Final-Project
The final project for NE 452 Special Topics in Nanoscale Simulations covering Enthalpy of Formation Prediction through Molecular Dynamics and Density Functional Theory

# Project Steps
Run the following files, or follow these steps to reproduce our work :
1. Run the GeoOptAll File in the Scripts folder, make sure you have `Docker` installed. (If you want to run parallel calculations run the individual categories)
2. Run the SinglePointAll.py file, to run Single Point energy calculation on individual atoms 
3. Parsed all the Data into Excel and CSV files
4. Plotted the Data

# Reproducing our Results
If you'd like to reproduce our results, follow the Development Environment Steps in the next section, then run the following Python files :
- Scripts/GeoOpt/GeoOptAll.py
- Scripts/SinglePoint/SinglePointAll.py
- Scripts/DataParsing/RunAllParsing.py

## Dependencies 
The following dependencies are required to reproduce our results :
- Docker (Desktop or CLI) or Orca
- Python 3.11+
- Packages in requirements.txt

# Setup Development Environment
To setup your environment run the following commands in your terminal :

Create a new Virtual Environment :
```bash
python -m venv venv
```

Activate the Virtual Environment (Windows) :
```bash
source venv/Scripts/Activate
```

Install the required packages :
```bash
pip install -r requirements.txt
```

One step Setup
```bash
python -m venv venv
source venv/Scripts/Activate
pip install -r requirements.txt
```

# Authors
Alexandre Dufresne-Nappert : a3dufres@uwaterloo.ca

Alexa Orecuia : aoriecui@uwaterloo.ca
