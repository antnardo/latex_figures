"""Enregistrement d'une figure, rognée au plus près par un outil externe.

``bbox_inches="tight"`` laisse une marge autour des boîtes de texte ; pdfcrop
(PDF), ImageMagick (PNG) ou epstool (EPS) rognent à l'encre près. La figure
passe par un fichier temporaire, effacé ensuite (l'ancien restait dans /tmp),
et les outils sont lancés sans shell : un chemin avec espaces ne casse plus
rien. Sans l'outil, la figure est enregistrée non rognée, avec un
avertissement.
"""

import shutil
import subprocess
import tempfile
import warnings
from pathlib import Path
from typing import Any

from matplotlib.figure import Figure

__all__ = ["FORMATS", "save_fig"]

#: Format → commandes de rognage possibles, la première trouvée sert ({e} : entrée, {s} : sortie).
FORMATS: dict[str, list[list[str]]] = {
    "pdf": [["pdfcrop", "{e}", "{s}"]],
    "png": [["magick", "{e}", "-trim", "{s}"], ["convert", "{e}", "-trim", "{s}"]],
    "eps": [["epstool", "--bbox", "--copy", "{e}", "{s}"]],
}


def _commande(fmt: str) -> list[str] | None:
    for commande in FORMATS[fmt]:
        if shutil.which(commande[0]):
            return commande
    return None


def save_fig(
    fig: Figure,
    file_name: str | Path,
    fmt: str | None = None,
    dpi: int = 300,
    tight: bool = True,
    crop: bool = True,
) -> Path:
    """Enregistre ``fig`` en PDF, PNG ou EPS (d'après l'extension, ou ``fmt``), rognée.

    L'extension est ajoutée au nom si elle manque. Rend le chemin écrit.
    """
    chemin = Path(file_name).expanduser().resolve()
    fmt = fmt or chemin.suffix.lstrip(".").lower()
    if fmt not in FORMATS:
        raise ValueError(f"Format non pris en charge : {fmt!r} ({', '.join(FORMATS)}).")
    if chemin.suffix.lower() != f".{fmt}":
        chemin = chemin.with_name(chemin.name + f".{fmt}")
    options: dict[str, Any] = {"dpi": dpi, "format": fmt, "bbox_inches": "tight" if tight else None}

    commande = _commande(fmt) if crop else None
    if crop and commande is None:
        outils = ", ".join(c[0] for c in FORMATS[fmt])
        warnings.warn(f"{outils} introuvable : figure non rognée.", stacklevel=2)
    if commande is None:
        fig.savefig(chemin, **options)
        return chemin
    with tempfile.TemporaryDirectory() as dossier:
        brut = Path(dossier) / f"figure.{fmt}"
        fig.savefig(brut, **options)
        arguments = [a.format(e=brut, s=chemin) for a in commande]
        subprocess.run(arguments, check=True, capture_output=True)
    return chemin
