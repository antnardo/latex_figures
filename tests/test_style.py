import locale
import shutil

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

import latex_figures
from latex_figures import style
from latex_figures.style import INCH, PREAMBULE, fig_size, latexify, parametres_latex, restaurer


@pytest.fixture
def sans_latexify_precedent():
    style._AVANT = None
    yield
    style._AVANT = None


def test_taille_en_centimetres_convertie_en_pouces():
    assert fig_size(8, 6) == pytest.approx((8 / INCH, 6 / INCH))


def test_hauteur_par_defaut_au_nombre_d_or():
    largeur, hauteur = fig_size(16)
    assert hauteur / largeur == pytest.approx(0.618, abs=1e-3)


def test_hauteur_au_dela_de_22_cm_ramenee_avec_avertissement():
    # L'ancienne version concaténait str et float et levait TypeError.
    with pytest.warns(UserWarning, match="22"):
        assert fig_size(16, 30)[1] == pytest.approx(22 / INCH)


def test_latexify_applique_et_rend_les_parametres(sans_latexify_precedent):
    with mpl.rc_context():
        parametres = latexify(8, 6, usetex=False)
        assert mpl.rcParams["figure.figsize"] == pytest.approx([8 / INCH, 6 / INCH])
        assert parametres["text.usetex"] is False


def test_restaurer_rend_les_reglages_d_avant_le_premier_latexify(sans_latexify_precedent):
    with mpl.rc_context():
        avant = dict(mpl.rcParams)
        latexify(8, 6, usetex=False)
        latexify(10, usetex=False, famille="serif")
        assert mpl.rcParams["font.family"] == ["serif"]
        restaurer()
        assert dict(mpl.rcParams) == avant
        restaurer()  # sans effet une seconde fois
        assert dict(mpl.rcParams) == avant


class TestPreambule:
    def test_babel_et_siunitx_par_defaut(self):
        preambule = parametres_latex()["text.latex.preamble"]
        assert preambule == PREAMBULE
        assert "[french]{babel}" in preambule
        assert "{siunitx}" in preambule

    def test_preambule_donne_en_lignes_ou_en_chaine(self):
        lignes = [r"\usepackage{amsmath}", r"\usepackage{physics}"]
        assert parametres_latex(preamble=lignes)["text.latex.preamble"] == "\n".join(lignes)
        assert parametres_latex(preamble="")["text.latex.preamble"] == ""

    @pytest.mark.skipif(shutil.which("latex") is None, reason="LaTeX absent")
    def test_le_preambule_compile_avec_latex(self, tmp_path):
        with mpl.rc_context(parametres_latex(8, 6)):
            fig, ax = plt.subplots()
            ax.plot([0, 1], [0, 1])
            ax.set_xlabel(r"$v$ (\qty{1}{\m\per\s})")
            fig.savefig(tmp_path / "preambule.pdf")
        assert (tmp_path / "preambule.pdf").stat().st_size > 0


def test_parametres_utilisables_dans_rc_context():
    with mpl.rc_context(parametres_latex(10, ratio=0.5, usetex=False, famille="serif")):
        assert mpl.rcParams["font.family"] == ["serif"]


def test_import_sans_changer_la_locale():
    assert latex_figures.__name__ == "latex_figures"
    assert locale.setlocale(locale.LC_NUMERIC) in ("C", "C.UTF-8", "en_US.UTF-8")
