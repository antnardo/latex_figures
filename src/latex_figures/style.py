"""Réglages de matplotlib pour des figures insérées dans un document LaTeX.

Les dimensions sont en centimètres, comme dans le document. Les réglages
partent de ceux du « Cookbook » de SciPy (Matplotlib/LaTeX_Examples).
"""

import math
import warnings
from typing import Any

import matplotlib as mpl

__all__ = ["INCH", "MAX_HEIGHT", "fig_size", "latexify", "parametres_latex"]

INCH = 2.54  # cm
MAX_HEIGHT = 22.0  # cm, hauteur utile d'une page A4
NOMBRE_OR = (math.sqrt(5) - 1) / 2  # 0,618


def fig_size(
    fig_width: float = 16.0, fig_height: float | None = None, ratio: float | None = None
) -> tuple[float, float]:
    """Taille (largeur, hauteur) en pouces d'une figure donnée en cm.

    Sans hauteur, elle vaut ``ratio`` × largeur (nombre d'or par défaut). Au-delà de
    22 cm, la hauteur est ramenée à 22 cm, avec un avertissement.
    """
    if fig_height is None:
        fig_height = fig_width * (NOMBRE_OR if ratio is None else ratio)
    if fig_height > MAX_HEIGHT:
        warnings.warn(
            f"Hauteur de figure {fig_height} cm trop grande : ramenée à {MAX_HEIGHT} cm.",
            stacklevel=2,
        )
        fig_height = MAX_HEIGHT
    return fig_width / INCH, fig_height / INCH


def parametres_latex(
    fig_width: float | None = None,
    fig_height: float | None = None,
    ratio: float | None = None,
    usetex: bool = True,
    famille: str = "sans-serif",
) -> dict[str, Any]:
    """Paramètres rc de ``latexify``, à passer aussi à ``plt.rc_context``.

    ``fig_width`` en cm (16 par défaut), ``fig_height`` en cm ou ``ratio`` × largeur,
    ``famille`` : ``"sans-serif"`` ou ``"serif"``.
    """
    largeur, hauteur = fig_size(16.0 if fig_width is None else fig_width, fig_height, ratio)
    return {
        "pgf.texsystem": "pdflatex",
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "axes.formatter.use_mathtext": True,
        "font.size": 11,
        "text.usetex": usetex,
        "font.family": famille,
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "legend.fontsize": 8,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "lines.markersize": 3,
        "figure.figsize": [largeur, hauteur],
        "figure.subplot.left": 0.16,
        "figure.subplot.right": 0.94,
        "figure.subplot.bottom": 0.14,
        "figure.subplot.top": 0.96,
        "figure.subplot.wspace": 0.3,
        "figure.subplot.hspace": 0.2,
    }


def latexify(
    fig_width: float | None = None,
    fig_height: float | None = None,
    ratio: float | None = None,
    usetex: bool = True,
    famille: str = "sans-serif",
) -> dict[str, Any]:
    """Applique ``parametres_latex`` à matplotlib (avant de créer les figures) et les rend.

    Les figures déjà créées gardent leurs réglages ; inutile de relancer la console.
    Aucune locale n'est modifiée : la virgule décimale vient de ``format_axes``.
    """
    parametres = parametres_latex(fig_width, fig_height, ratio, usetex, famille)
    # Les stubs de matplotlib ≥ 3.11 n'acceptent que des clés littérales ; matplotlib
    # vérifie de toute façon chaque clé à l'exécution.
    mpl.rcParams.update(parametres)  # type: ignore[arg-type]
    return parametres
