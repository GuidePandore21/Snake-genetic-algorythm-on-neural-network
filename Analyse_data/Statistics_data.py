import numpy as np
import os
import glob
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


def boxplot(ax, x, title):
    sns.boxplot(
        ax=ax,
        x=x,
        color="skyblue",
        width=0.5,
        showmeans=True,
        meanline=True,
        meanprops={"color": "red", "linestyle": "--", "linewidth": 2},
        flierprops={"marker": "o", "markerfacecolor": "orange", "markersize": 8},
    )
    ax.set_title(title, fontsize=12)
    ax.set_xlabel("Score", fontsize=10)
    ax.set_ylabel("Fréquence", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.7)


save_data_path = "../Save_Data"

if not os.path.exists("../Save_Data"):
    print(f"Le dossier '{save_data_path}' n'existe pas.")
else:
    print(f"Le dossier '{save_data_path}' existe.")

csv_files = glob.glob(os.path.join(save_data_path, "*.csv"))

all_scores = []

if csv_files:
    # Configuration de la grille pour les subplots
    n_cols = 3  # Nombre de colonnes dans la grille
    n_rows = (len(csv_files) + n_cols - 1) // n_cols  # Calcul dynamique du nombre de lignes

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    axes = axes.flatten()  # Aplatir pour un accès facile aux axes

    for i, file in enumerate(csv_files):
        try:
            # Lire les données
            data = pd.read_csv(file)
            print(f"\nStatistiques pour le fichier : {file}")
            print(data["Score"].describe())

            # Ajouter un boxplot dans la grille
            boxplot(axes[i], data["Score"], title=f"Boxplot - {os.path.basename(file)}")

            # Ajouter les scores à la liste globale
            all_scores.append(data["Score"])

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {file}: {e}")

    # Supprimer les axes inutilisés si le nombre de fichiers est inférieur à la grille
    for j in range(len(csv_files), len(axes)):
        fig.delaxes(axes[j])

    # Ajuster l'espacement entre les subplots
    plt.tight_layout()
    plt.show()

    # Fusionner tous les scores en un seul DataFrame
    if all_scores:
        merged_scores = pd.concat(all_scores, ignore_index=True)
        print("\nStatistiques globales :")
        print(merged_scores.describe())

        # Afficher un boxplot global
        plt.figure(figsize=(10, 6))
        sns.boxplot(
            x=merged_scores,
            color="skyblue",
            width=0.5,
            showmeans=True,
            meanline=True,
            meanprops={"color": "red", "linestyle": "--", "linewidth": 2},
            flierprops={"marker": "o", "markerfacecolor": "orange", "markersize": 8},
        )
        plt.title("Boxplot Global des Scores", fontsize=16, fontweight="bold")
        plt.xlabel("Score", fontsize=14)
        plt.ylabel("Fréquence", fontsize=14)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

        # Sauvegarder les données combinées
        merged_scores.to_csv("merged_scores.csv", index=False)
        print("Les données combinées ont été sauvegardées dans 'merged_scores.csv'.")
else:
    print("Aucun fichier CSV trouvé dans le dossier.")
