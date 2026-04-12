import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#excel file
excel_file = "/Users/alexaoriecuia/Desktop/NE452/452 project/run/cost.xlsx"  
sheet_name = 'Sheet2'                

df = pd.read_excel(excel_file, sheet_name=sheet_name)

#Define funcitonals
functionals = {"LDA": {"mae": "LDA MAE","time": "LDA Time","marker": "o","color": "tab:blue"},
               "PBE": {"mae": "PBE MAE","time": "PBE Time","marker": "s","color": "tab:orange"},
               "B3LYP": {"mae": "B3LYP MAE","time": "B3LYP Time","marker": "^","color": "tab:green"},
               "wB97X-D3": {"mae": "wB97x-D MAE","time": "wB97x-D3 Time","marker": "D","color": "tab:red"},
               "M06-2X": {"mae": "M06-2X MAE","time": "M06-2X Time","marker": "P","color": "tab:purple"}}

plt.figure(figsize=(13, 9))

#plot for each functional
for func_name, props in functionals.items():
    x = df[props["time"]].astype(float).values
    y = df[props["mae"]].astype(float).values
    labels = df["Molecule"].values
    color = props["color"]

    #scatter plot
    plt.scatter( x, y,s=80,marker=props["marker"],color=color,label=func_name)

    #Annotate data points
    for xi, yi, label in zip(x, y, labels):
        plt.annotate(label, (xi, yi), fontsize=10, alpha=0.8)

    #plot line of best fit
    logx = np.log10(x)
    logy = np.log10(y)

    coeffs = np.polyfit(logx, logy, 1)
    fit_fn = np.poly1d(coeffs)

    logy_pred = fit_fn(logx)

    #Calculate R^2
    ss_res = np.sum((logy - logy_pred) ** 2)
    ss_tot = np.sum((logy - np.mean(logy)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    #Smooth
    x_fit = np.logspace(np.min(logx), np.max(logx), 200)
    y_fit = 10 ** fit_fn(np.log10(x_fit))


    #Include R^2 values in legend
    plt.plot(x_fit,y_fit,color=color,linewidth=2,alpha=0.95,label=f"{func_name} (R²={r_squared:.3f})")

    #plot the region of standard deviation
    residuals = logy - fit_fn(logx)
    sigma = np.std(residuals)

    y_upper = 10 ** (fit_fn(np.log10(x_fit)) + sigma)
    y_lower = 10 ** (fit_fn(np.log10(x_fit)) - sigma)

    plt.fill_between(x_fit, y_lower, y_upper,color=color,alpha=0.18)

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Computation Time (s)", fontsize=14)
plt.ylabel("Mean Absolute Error (MAE)", fontsize=14)
plt.title("Cost vs Accuracy Comparison of DFT Functionals", fontsize=16)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=11)
plt.tight_layout()

plt.show()