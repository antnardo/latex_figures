"""Mise en forme des axes : bords discrets, graduations sortantes, virgule décimale."""

from collections.abc import Sequence
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.ticker import ScalarFormatter

__all__ = ["ScalarFormatterVirgule", "add_subplot_axes", "format_axes"]


def _virgule(texte: str) -> str:
    # En mode mathématique (mathtext ou LaTeX), « {,} » évite l'espace qui suit
    # une virgule de ponctuation.
    return texte.replace(".", "{,}")


class ScalarFormatterVirgule(ScalarFormatter):
    """``ScalarFormatter`` en notation mathématique, à virgule décimale, puissances de 10
    hors de [10⁻², 10⁴].

    La virgule ne demande plus ``locale.setlocale("fr_FR")``, que l'ancien module
    exécutait à l'import pour tout le programme (et qui échoue sans locale française).
    """

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("useMathText", True)
        super().__init__(**kwargs)
        self.set_powerlimits((-2, 4))

    def __call__(self, x: float, pos: int | None = None) -> str:
        return _virgule(super().__call__(x, pos))

    def get_offset(self) -> str:
        return _virgule(super().get_offset())


def format_axes(ax: Axes | None = None, format_ticks: bool = True) -> Axes:
    """Bords gris et fins, graduations sortantes, et (``format_ticks``) un formateur à
    virgule par axe linéaire. Appelle ``tight_layout`` sur la figure de ``ax``.

    Chaque axe reçoit son propre formateur : l'ancien formateur unique, partagé, ne
    gardait qu'un facteur commun (×10⁵ de l'axe x perdu au profit de celui de y).
    """
    if ax is None:
        ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("gray")
        spine.set_linewidth(0.5)
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_tick_params(direction="out", which="both", color="gray")
        if format_ticks and axis.get_scale() == "linear":
            axis.set_major_formatter(ScalarFormatterVirgule())
    figure = ax.get_figure()
    if figure is not None:
        figure.tight_layout()  # type: ignore[union-attr]
    return ax


def add_subplot_axes(ax: Axes, rect: Sequence[float]) -> Axes:
    """Axes en incrustation dans ``ax`` ; ``rect = [x0, y0, largeur, hauteur]`` en
    fraction de ``ax`` (par exemple ``[0.6, 0.1, 0.3, 0.3]``).

    Les étiquettes des graduations sont réduites comme la racine de la taille relative.
    L'incrustation suit ``ax`` si la mise en page change (``Axes.inset_axes``).

    Exemple ::

        ax_inset = add_subplot_axes(ax, rect=[0.6, 0.1, 0.3, 0.3])
        ax_inset.plot(lambdas, sinus, "o", ms=3)
        ax_inset.set_xlim(0, 650)
    """
    x0, y0, largeur, hauteur = rect
    incrustation = ax.inset_axes((x0, y0, largeur, hauteur))
    for axis, facteur in ((incrustation.xaxis, largeur), (incrustation.yaxis, hauteur)):
        etiquettes = axis.get_ticklabels()
        taille = etiquettes[0].get_fontsize() if etiquettes else 10.0
        axis.set_tick_params(labelsize=taille * facteur**0.5)
    return incrustation
