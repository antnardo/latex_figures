import locale
import re
import tomllib
from pathlib import Path

import latex_figures


def test_version_read_by_pyproject():
    pyproject = tomllib.loads((Path(__file__).parents[1] / "pyproject.toml").read_text())
    assert pyproject["tool"]["hatch"]["version"]["path"] == "src/latex_figures/__init__.py"
    assert re.fullmatch(r"\d+\.\d+\.\d+", latex_figures.__version__)


def test_every_exported_name_exists():
    for name in latex_figures.__all__:
        assert hasattr(latex_figures, name), name


def test_import_leaves_the_locale_alone():
    assert locale.setlocale(locale.LC_NUMERIC) in ("C", "C.UTF-8", "en_US.UTF-8")
