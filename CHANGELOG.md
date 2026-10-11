# Changelog

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le
[versionnage sémantique](https://semver.org/lang/fr/).

## [0.1.0] - 2026-10-10

Première version en dépôt séparé : le paquet vivait dans `pyphysique` (`src/latex_figures`)
depuis le 8 octobre 2026, et avant cela dans `nicefigures` et une copie `latex_figures`.

### Ajouté

- `parametres_latex(preamble=…)` et `latexify(preamble=…)` : préambule LaTeX
  (`text.latex.preamble`), par défaut `PREAMBULE` (babel français et siunitx), une
  chaîne ou une ligne par élément, `""` pour aucun. L'ancien `parametres_latex` ne
  réglait aucun préambule.
- `restaurer()`, inverse de `latexify` : rend les `rcParams` d'avant le premier appel.
- `__version__`, lue par `pyproject.toml` ; `FORMATS` exporté.
- Dépôt : disposition `src/`, `py.typed`, tests, CI (pytest sous Python 3.11 et 3.14,
  ruff, mypy, `uv build`), publication de la roue sur la release GitHub.

### Repris de pyphysique (8 octobre 2026)

- `latexify`, `parametres_latex`, `fig_size` (tailles en cm, 22 cm au plus),
  `format_axes` avec un `ScalarFormatterVirgule` par axe, `add_subplot_axes`
  (`Axes.inset_axes`), `save_fig` rogné par pdfcrop, ImageMagick ou epstool sans
  shell ni fichier temporaire restant.
- Corrigés alors : formateur partagé entre les axes, str + float au-delà de 22 cm,
  `IndentationError` de `plot.py`, `text.fontsize`, `map`, `shell=True`, fichier
  temporaire jamais effacé, `setlocale` à l'import, `show` avant `savefig`.
