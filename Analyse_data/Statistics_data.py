import numpy as np
import os
import glob
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


def boxplot(x):
    plt.figure(figsize=(10, 6))
    sns.boxplot(
        x=x,
        color="skyblue",
        width=0.5,
        showmeans=True,
        meanline=True,
        meanprops={"color": "red", "linestyle": "--", "linewidth": 2},
        flierprops={"marker": "o", "markerfacecolor": "orange", "markersize": 8},
    )

    plt.title("Distribution des Scores avec Boxplot", fontsize=16, fontweight="bold")
    plt.xlabel("Score", fontsize=14)
    plt.ylabel("Fréquence", fontsize=14)

    plt.xlim(x.min() - 5, x.max() + 5)

    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


save_data_path = "../Save_Data"

if not os.path.exists("../Save_Data"):
    print(f"Le dossier '{save_data_path}' n'existe pas.")
else:
    print(f"Le dossier '{save_data_path}' existe.")

csv_files = glob.glob(os.path.join(save_data_path, "*.csv"))

all_scores = []

for file in csv_files:
    try:
        data = pd.read_csv(file)
        print(f"\nStatistiques pour le fichier : {file}")
        print(data["Score"].describe())
        boxplot(data["Score"])


        all_scores.append(data["Score"])
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file}: {e}")

if all_scores:
    merged_scores = pd.concat(all_scores, ignore_index=True)
    print("\nDataFrame globales :")
    print(merged_scores.describe())
    boxplot(merged_scores)

    merged_scores.to_csv("merged_scores.csv", index=False)
else:
    print("Problème dans la récolte de données")
