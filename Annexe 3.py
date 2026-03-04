# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 15:49:46 2026

@author: Devra
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Définir les états et Matrice Transition P et les coûts
etats = ["excellent", "bon", "moyen","dégradé","mauvais"]

# Les lignes doivent sommer à 1
P = np.array([
    [0.944, 0.055, 0.001, 0.000, 0.000],    # De excellent vers...
    [0.000, 0.976, 0.024, 0.000, 0.000],    # De bon vers...
    [0.000, 0.000, 0.997, 0.003, 0.000],    # De moyen vers...
    [0.000, 0.000, 0.000, 0.970, 0.030],    # De dégradé vers... 
    [0.000, 0.000, 0.000, 0.000, 1.000]     # De mauvais vers... cette état est absorbant
 
])  

# --- Coûts unitaires (en €/m2) ---
# Indice 0 : Inspection 
# Indice 1 : Maintenance Préventive 
# Indice 2 : Maintenance Corrective

couts = [15, 400, 1500]
seuil_critique = 0.1 # Choix arbitraire du seil où la probabilité que l'état soit alarmant 

# duree_simulation = int(input("Entrez la durée de simulation (en années) : ")) # Duréé de simulation
duree_simulation=150

# --- 2. INITIALISATION DES DEUX SCÉNARIOS ---
# On crée un pont et un budget pour chaque stratégie
etat_corr = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
etat_prev = np.array([1.0, 0.0, 0.0, 0.0, 0.0])

budget_corr = 0
budget_prev = 0

historique_budget_corr = [0]
historique_budget_prev = [0]

# --- 3. SIMULATION COMPARATIVE ---
for annee in range(1, duree_simulation + 1):
    
    # A. Dégradation des deux ponts
    etat_corr = np.dot(etat_corr, P)
    etat_prev = np.dot(etat_prev, P)
    
    # B. Coût d'inspection pour les deux (+15€)
    budget_corr = budget_corr + couts[0]
    budget_prev = budget_prev + couts[0]

    # C. Application de la Stratégie CORRECTIVE (On surveille l'état Alarmant : indice 4)
    if etat_corr[4] > seuil_critique:
        budget_corr = budget_corr + couts[2]   # On paie 1500€
        etat_corr = np.array([1.0, 0.0, 0.0, 0.0, 0.0]) # Remise à neuf
        
    # D. Application de la Stratégie PRÉVENTIVE (On surveille l'état Bon : indice 2)
    if etat_prev[2] > 0.4:
        budget_prev = budget_prev + couts[1]  # On paie 400€
        etat_prev = np.array([1.0, 0.0, 0.0, 0.0, 0.0]) # Remise à neuf
        
    # E. Enregistrement des budgets
    historique_budget_corr.append(budget_corr)
    historique_budget_prev.append(budget_prev)

# --- 4. AFFICHAGE DU GRAPHIQUE COMPARATIF ---
plt.figure(figsize=(10, 6))

# On trace la ligne de la stratégie Corrective (en rouge)
plt.plot(range(duree_simulation + 1), historique_budget_corr, label="Stratégie Corrective", color='red', linewidth=2, marker='o', markersize=4)

# On trace la ligne de la stratégie Préventive (en vert)
plt.plot(range(duree_simulation + 1), historique_budget_prev, label="Stratégie Préventive", color='green', linewidth=2, marker='s', markersize=4)

plt.title(f"Optimisation : Comparaison des coûts cumulés sur {duree_simulation} ans", fontsize=14)
plt.xlabel("Années", fontsize=12)
plt.ylabel("Dépenses cumulées (€/m²)", fontsize=12)
plt.grid(True, linestyle='--')
plt.legend(fontsize=12)
plt.show()

# Affichage du bilan dans la console
print(f"--- BILAN SUR {duree_simulation} ANS ---")
print(f"Coût total Correctif : {budget_corr} €/m²")
print(f"Coût total Préventif : {budget_prev} €/m²")