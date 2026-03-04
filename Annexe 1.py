# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
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

# 3. État initial (Au début, le pont est 100% Neuf)
etat_actuel = np.array([1.0, 0.0, 0.0, 0.0, 0.0])

seuil_critique = 0.1 # Choix arbitraire du seil où la probabilité que l'état soit alarmant 

# duree_simulation = int(input("Entrez la durée de simulation (en années) : ")) # Duréé de simulation
duree_simulation=150

# 4 Simulation sur la durée demandée
annee=0 
budget_total = 0
historique = [etat_actuel]
historique_budget = [0]
for annee in range(1,duree_simulation+1):
      # On multiplie l'état actuel par la matrice P pour avoir l'année suivante
     etat_actuel = np.dot(etat_actuel, P)
     budget_total = budget_total + couts[0]
     historique.append(etat_actuel)
     if etat_actuel[4] > seuil_critique:
         print ("Etats alarmant atteint un seuil critique, au bout de ",annee ," année, maintenance nécessaire")
         budget_total = budget_total + couts[2]
         etat_actuel = np.array([1.0, 0.0, 0.0, 0.0, 0.0]) # Remise à l'état de neuf
     historique_budget.append(budget_total)
historique = np.array(historique)
historique_budget = np.array(historique_budget)


#  5. Affichage du budget et évolution de l'état de l'ouvrage d'art
 
#  1er Graphique : Le Budget 
plt.figure(figsize=(8, 5))
plt.plot(range(duree_simulation + 1), historique_budget, color='purple')
plt.title("Évolution du coût cumulé (Stratégie Corrective)")
plt.xlabel("Années")
plt.ylabel("Dépenses cumulées (€/m²)")
plt.grid(True, linestyle='--')
plt.show()


# 2ème Graphique : Les 4 États

plt.figure(figsize=(10, 6)) # On agrandit un peu car il y a 4 courbes
# On trace les 4 états de votre liste ["excellent", "bon", "dégradé", "mauvais"]
plt.plot(historique[:, 0], label="État excellent", marker='o', color='green')
plt.plot(historique[:, 1], label="État bon", marker='s', color='blue')
plt.plot(historique[:, 2], label="État moyen", marker='s', color='yellow')
plt.plot(historique[:, 3], label="État dégradé", marker='d', color='orange') # marker 'd' = losange
plt.plot(historique[:, 4], label="État mauvais", marker='^', color='red')    # marker '^' = triangle

plt.title(f"Simulation sur {duree_simulation} ans", fontsize=14)
plt.xlabel("Années")
plt.ylabel("Probabilité")
plt.grid(True, linestyle='--')
plt.legend()
plt.ylim(-0.05, 1.05)
plt.show()