import locale

import matplotlib as mpl
import pytest

import latex_figures
from latex_figures.style import INCH, fig_size, latexify, parametres_latex


def test_taille_en_centimetres_convertie_en_pouces():
    assert fig_size(8, 6) == pytest.approx((8 / INCH, 6 / INCH))


def test_hauteur_par_defaut_au_nombre_d_or():
    largeur, hauteur = fig_size(16)
    assert hauteur / largeur == pytest.approx(0.618, abs=1e-3)


def test_hauteur_au_dela_de_22_cm_ramenee_avec_avertissement():
    # L'ancienne version concaténait str et float et levait TypeError.
    with pytest.warns(UserWarning, match="22"):
        assert fig_size(16, 30)[1] == pytest.approx(22 / INCH)


def test_latexify_applique_et_rend_les_parametres():
    with mpl.rc_context():
        parametres = latexify(8, 6, usetex=False)
        assert mpl.rcParams["figure.figsize"] == pytest.approx([8 / INCH, 6 / INCH])
        assert parametres["text.usetex"] is False


def test_parametres_utilisables_dans_rc_context():
    with mpl.rc_context(parametres_latex(10, ratio=0.5, usetex=False, famille="serif")):
        assert mpl.rcParams["font.family"] == ["serif"]


def test_import_sans_changer_la_locale():
    assert latex_figures.__name__ == "latex_figures"
    assert locale.setlocale(locale.LC_NUMERIC) in ("C", "C.UTF-8", "en_US.UTF-8")
