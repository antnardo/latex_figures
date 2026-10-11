# latex_figures

Figures matplotlib prêtes pour un document LaTeX : dimensions en centimètres, polices
et préambule LaTeX (babel français, siunitx), virgule décimale sans changer la locale,
incrustations, rognage au plus près par pdfcrop. C'est l'outil des figures de cours et
de corrigés ; il réunit l'ancien `nicefigures` et sa copie `latex_figures`.

## Installation

```bash
pip install git+https://github.com/antnardo/latex_figures
```

ou, depuis un clone, `pip install -e .` ; ou encore, sans installation, le dossier `src`
dans le `PYTHONPATH`. Dépendances : Python ≥ 3.11 et matplotlib ≥ 3.8. Pour
`latexify(usetex=True)`, le défaut, il faut une distribution LaTeX avec babel et
siunitx ; pour `save_fig` rogné, pdfcrop (PDF), ImageMagick (PNG) ou epstool (EPS).

## Usage

```python
import matplotlib.pyplot as plt
from latex_figures import format_axes, latexify, save_fig

latexify(8, 6)                # 8 cm × 6 cm, avant de créer les figures
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel(r"$t$ (\qty{1}{\s})")   # siunitx est dans le préambule
format_axes(ax)               # bords gris, graduations sortantes, 1,5 et ×10⁵
save_fig(fig, "figure.pdf")   # enregistrée puis rognée par pdfcrop
```

`latexify` règle `rcParams` pour toutes les figures à venir ; `restaurer()` rend les
réglages d'avant. Pour une seule figure, `plt.rc_context(parametres_latex(8, 6))`.

## API

| Fonction | Rôle |
| --- | --- |
| `latexify(fig_width=16, fig_height=None, ratio=None, usetex=True, famille="sans-serif", preamble=None)` | règle `rcParams` (tailles en cm, hauteur = largeur × nombre d'or par défaut, 22 cm au plus, préambule `PREAMBULE` : babel français et siunitx, ou le vôtre) et rend le dictionnaire appliqué |
| `restaurer()` | rend à matplotlib les réglages d'avant le premier `latexify` (son inverse) |
| `parametres_latex(...)` | le même dictionnaire sans l'appliquer, pour `plt.rc_context` |
| `fig_size(largeur, hauteur=None, ratio=None)` | taille en pouces d'une figure donnée en cm |
| `format_axes(ax=None, format_ticks=True)` | bords, graduations ; avec `format_ticks`, un `ScalarFormatterVirgule` par axe linéaire ; `tight_layout` |
| `ScalarFormatterVirgule()` | formateur mathtext à virgule, puissances de 10 hors de [10⁻², 10⁴] |
| `add_subplot_axes(ax, rect)` | incrustation `[x0, y0, l, h]` en fraction de `ax`, graduations réduites |
| `save_fig(fig, chemin, fmt=None, dpi=300, tight=True, crop=True)` | PDF, PNG ou EPS (`FORMATS`), rogné par l'outil externe s'il existe, avec un avertissement sinon |

Aucune locale n'est modifiée : la virgule vient du formateur, pas de
`setlocale("fr_FR")`. Le préambule ne sert qu'avec `usetex` ; `preamble=""` n'en met
aucun, une liste de chaînes donne une ligne par élément.

## Exemples

`examples/exemple_figure.py` : la fonction d'Airy en 8 cm × 6 cm, virgule décimale,
PDF rogné. Il demande scipy (`uv run examples/exemple_figure.py` avec le groupe
`dev`).

## Développement

```bash
uv sync --group dev
uv run ruff format src tests examples
uv run ruff check src tests examples
uv run mypy
uv run --python 3.11 pytest   # version minimale (environnement pythontex)
uv run --python 3.14 pytest
uv build
```

Le test qui compile le préambule est sauté sans LaTeX. La version est
`latex_figures.__version__`, lue par `pyproject.toml` ; la release GitHub dont
l'étiquette est cette version (`v0.1.0`) reçoit la roue et le sdist (`publish.yml`).

## Licence

MIT (`LICENSE`).
