import matplotlib.pyplot as plt
import numpy as np
import pytest

from latex_figures.axes import ScalarFormatterVirgule, add_subplot_axes, format_axes


@pytest.fixture
def axes():
    _, ax = plt.subplots()
    ax.plot(np.linspace(0, 3e5, 10), np.linspace(0, 2e-3, 10))
    return ax


def test_chaque_axe_a_son_propre_formateur(axes):
    format_axes(axes)
    assert axes.xaxis.get_major_formatter() is not axes.yaxis.get_major_formatter()


def test_facteurs_communs_independants(axes):
    # Avec un formateur partagé, le dernier axe dessiné imposait son facteur à l'autre.
    format_axes(axes)
    axes.figure.canvas.draw()
    x_offset = axes.xaxis.get_major_formatter().get_offset()
    y_offset = axes.yaxis.get_major_formatter().get_offset()
    assert "10^{5}" in x_offset
    assert "10^{\N{MINUS SIGN}3}" in y_offset


def test_virgule_decimale_sans_locale():
    formateur = ScalarFormatterVirgule()
    fig, ax = plt.subplots()
    ax.set_xlim(0, 2)
    ax.xaxis.set_major_formatter(formateur)
    fig.canvas.draw()
    assert formateur(1.5) == r"$\mathdefault{1{,}50}$"  # graduations 0, 0,25…


def test_axe_logarithmique_garde_son_formateur():
    _, ax = plt.subplots()
    ax.set_yscale("log")
    format_axes(ax)
    assert not isinstance(ax.yaxis.get_major_formatter(), ScalarFormatterVirgule)


def test_format_ticks_faux_garde_les_formateurs(axes):
    avant = axes.xaxis.get_major_formatter()
    format_axes(axes, format_ticks=False)
    assert axes.xaxis.get_major_formatter() is avant


def test_bords_gris(axes):
    format_axes(axes)
    assert all(spine.get_visible() for spine in axes.spines.values())


def test_incrustation_dans_les_axes(axes):
    incrustation = add_subplot_axes(axes, [0.6, 0.1, 0.3, 0.3])
    axes.figure.canvas.draw()
    parent = axes.get_position()
    position = incrustation.get_position()
    assert position.x0 == pytest.approx(parent.x0 + 0.6 * parent.width)
    assert position.width == pytest.approx(0.3 * parent.width)
