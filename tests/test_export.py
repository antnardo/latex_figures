import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from latex_figures import export
from latex_figures.export import save_fig


@pytest.fixture
def figure():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    return fig


def test_extension_ajoutee_et_fichier_ecrit_sans_rognage(figure, tmp_path):
    chemin = save_fig(figure, tmp_path / "figure", fmt="png", crop=False)
    assert chemin.name == "figure.png"
    assert chemin.exists()


def test_format_inconnu_refuse(figure, tmp_path):
    with pytest.raises(ValueError, match="non pris en charge"):
        save_fig(figure, tmp_path / "figure.jpg")


def test_outil_absent_enregistre_sans_rogner(figure, tmp_path, monkeypatch):
    monkeypatch.setattr(export.shutil, "which", lambda nom: None)
    with pytest.warns(UserWarning, match="introuvable"):
        chemin = save_fig(figure, tmp_path / "figure.pdf")
    assert chemin.exists()


def test_rognage_sans_shell_et_sans_fichier_temporaire_restant(figure, tmp_path, monkeypatch):
    appels = []

    def faux_run(arguments, **options):
        appels.append((arguments, options))
        entree, sortie = arguments[1], arguments[2]
        assert " " in sortie  # chemin à espaces passé tel quel
        Path(sortie).write_bytes(Path(entree).read_bytes())
        return subprocess.CompletedProcess(arguments, 0)

    monkeypatch.setattr(export.shutil, "which", lambda nom: f"/usr/bin/{nom}")
    monkeypatch.setattr(export.subprocess, "run", faux_run)
    chemin = save_fig(figure, tmp_path / "ma figure.pdf")
    ((arguments, options),) = appels
    assert arguments[0] == "pdfcrop"
    assert "shell" not in options
    assert chemin.exists()
    assert not Path(arguments[1]).exists()  # dossier temporaire effacé


@pytest.mark.skipif(export.shutil.which("pdfcrop") is None, reason="pdfcrop absent")
def test_rognage_reel_avec_pdfcrop(figure, tmp_path):
    assert save_fig(figure, tmp_path / "rognee.pdf").stat().st_size > 0
