"""Figure de la fonction d'Airy prête pour LaTeX : 8 cm × 6 cm, virgule décimale.

``latexify`` règle tailles et polices avant de créer la figure ; ``format_axes``
met en forme les axes ; ``save_fig`` enregistre la figure rognée au plus près
(pdfcrop). On enregistre avant ``plt.show()``, qui vide la figure à la fermeture
de la fenêtre.
"""

from math import pi

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import jv

from latex_figures import format_axes, latexify, save_fig

latexify(8, 6)  # largeur, hauteur en cm


def airy(x):
    return (2 * jv(1, pi * x) / (pi * x)) ** 2


x = np.linspace(-4, 4, 500)

fig, ax = plt.subplots()
ax.plot(x, airy(x))
ax.set_title("Fonction d'Airy")
ax.set_xlabel(r"$x=\frac{a\;\sin\theta}{\lambda}$")
ax.set_ylabel(r"Airy($x$)")
format_axes(ax)

save_fig(fig, "Exemple.pdf")
plt.show()
