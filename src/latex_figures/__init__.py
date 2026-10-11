"""Figures matplotlib prêtes pour LaTeX : taille en cm, polices, virgule décimale,
incrustations, rognage.

Usage ::

    import matplotlib.pyplot as plt
    from latex_figures import format_axes, latexify, save_fig

    latexify(8, 6)  # largeur, hauteur en cm, avant de créer les figures
    fig, ax = plt.subplots()
    ax.plot(x, y)
    format_axes(ax)  # bords, graduations, virgule décimale
    save_fig(fig, "figure.pdf")  # rognée par pdfcrop

Réunit l'ancien ``nicefigures`` (dont ``plot.py``, qui ne compilait plus) et
``latex_figures``, qui en était une copie ; dépôt à part depuis octobre 2026.
"""

from latex_figures.axes import ScalarFormatterVirgule, add_subplot_axes, format_axes
from latex_figures.export import FORMATS, save_fig
from latex_figures.style import (
    INCH,
    MAX_HEIGHT,
    PREAMBULE,
    fig_size,
    latexify,
    parametres_latex,
    restaurer,
)

__version__ = "0.1.0"

__all__ = [
    "FORMATS",
    "INCH",
    "MAX_HEIGHT",
    "PREAMBULE",
    "ScalarFormatterVirgule",
    "__version__",
    "add_subplot_axes",
    "fig_size",
    "format_axes",
    "latexify",
    "parametres_latex",
    "restaurer",
    "save_fig",
]
