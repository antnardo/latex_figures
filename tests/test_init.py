import re
from pathlib import Path

import latex_figures


def test_version_lue_par_pyproject():
    pyproject = (Path(__file__).parents[1] / "pyproject.toml").read_text()
    assert 'path = "src/latex_figures/__init__.py"' in pyproject
    assert re.fullmatch(r"\d+\.\d+\.\d+", latex_figures.__version__)


def test_api_publique_par_paires():
    assert {"latexify", "restaurer", "save_fig", "fig_size"} <= set(latex_figures.__all__)
