# latex-figures

[![CI](https://github.com/antnardo/latex_figures/actions/workflows/ci.yml/badge.svg)](https://github.com/antnardo/latex_figures/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/latex-figures)](https://pypi.org/project/latex-figures/)
[![Python](https://img.shields.io/pypi/pyversions/latex-figures)](https://pypi.org/project/latex-figures/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Make a matplotlib figure look like it belongs to the LaTeX document it goes into:
drawn at its final size in centimetres, its text typeset by LaTeX with the document's
preamble, a decimal comma if you write one, and no white margin around it.

## The goal

A plot saved with matplotlib's defaults and dropped into a LaTeX document rarely
matches it. The figure is drawn 6.4 × 4.8 inches wide, then shrunk by
`\includegraphics[width=…]`: its 10 pt labels end up at 6 pt, its lines too thin. Its
text is in DejaVu Sans, not in the document's font, and `\qty{3}{\m\per\s}` cannot
appear in a label. In French, German or most of Europe, the axes read `0.5` where the
text says `0,5`. And `bbox_inches="tight"` still leaves a white band that shifts the
figure off the caption.

`latex-figures` sets matplotlib up once so that every figure comes out right:

```python
import matplotlib.pyplot as plt
import numpy as np

from latex_figures import add_inset, apply_style, save_figure, style_axes

apply_style(8, 6)  # 8 cm × 6 cm, LaTeX text, before creating the figure
x = np.linspace(-4, 4, 500)
fig, ax = plt.subplots()
ax.plot(x, np.sinc(x) ** 2)
ax.set_title("Diffraction by a slit")
ax.set_xlabel(r"$x=\frac{a\sin\theta}{\lambda}$")
ax.set_ylabel(r"$I/I_0$")
style_axes(ax)  # grey spines, outward ticks, decimal comma
inset = add_inset(ax, [0.65, 0.5, 0.3, 0.4])
inset.plot(x, 100 * np.sinc(x) ** 2)
inset.set_xlim(1, 3)
inset.set_ylim(0, 6)
style_axes(inset)
path = save_figure(fig, "slit.pdf")  # saved, then cropped to the ink by pdfcrop
print(path.name)
```

```text
slit.pdf
```

![The figure: a sinc² curve with 1,0 and 0,5 on its vertical axis, and an inset](https://raw.githubusercontent.com/antnardo/latex_figures/main/docs/example.png)

The output is an ordinary PDF (or PNG, or EPS) file. Include it at its natural size,
`\includegraphics{slit.pdf}`, and its text has the size of the document's.
What goes on the axes, and where the file goes, stays yours: the package only sets
matplotlib up and saves.

## The means

1. **Sizes in centimetres.** The width and height you give become
   `figure.figsize`, so the figure is drawn at the size it will be printed, with 11 pt
   labels and 10 pt ticks; the height defaults to the golden ratio of the width.
2. **LaTeX renders the text, with a preamble.** `text.usetex` is on and
   `text.latex.preamble` loads amsmath and siunitx by default, or your own packages:
   labels are typeset by TeX, like the document, and its macros work in them.
3. **The decimal comma comes from a tick formatter**, `DecimalCommaFormatter`, not
   from `locale.setlocale`, which would change number formatting in the whole program
   and fails where no French locale is installed. It writes `1{,}5`, so math mode
   adds no space after the comma.
4. **Each axis gets its own formatter.** A formatter shared by both axes keeps a single
   common factor: the ×10⁵ of one axis would give way to the other's.
5. **Cropping to the ink by an external tool.** pdfcrop, ImageMagick or epstool
   trims what `bbox_inches="tight"` leaves; it runs without a shell, on a temporary
   copy that is deleted afterwards.

## Installation

```bash
pip install latex-figures
```

Python 3.11 or later and matplotlib 3.8 or later. Outside Python, depending on what you
use:

| Program | Needed for | Install |
| --- | --- | --- |
| a TeX distribution with `latex`, dvipng, amsmath, siunitx | `apply_style()` with `usetex=True`, the default | TeX Live, MiKTeX or MacTeX; Debian/Ubuntu: `apt install texlive-latex-extra texlive-science dvipng cm-super` |
| pdfcrop | cropping a PDF | comes with TeX Live (`texlive-extra-utils` on Debian/Ubuntu) |
| ImageMagick (`magick` or `convert`) | cropping a PNG | `brew install imagemagick`, `apt install imagemagick`, `winget install ImageMagick.ImageMagick` |
| epstool | cropping an EPS | `apt install epstool` |

Without TeX, pass `usetex=False`: matplotlib's mathtext renders the labels, without
siunitx. Without the cropping tool, `save_figure` saves the figure uncropped and warns.

## Usage

### Setting matplotlib up

`apply_style(width, height)` changes `matplotlib.rcParams` for every figure created
afterwards, and `restore_style()` gives back the settings from before. For a single
figure, use the same settings in a context:

```python
import matplotlib.pyplot as plt

from latex_figures import style_params

with plt.rc_context(style_params(12, ratio=0.5, family="serif")):
    fig, ax = plt.subplots()  # 12 cm × 6 cm, serif fonts
```

| Parameter | Default | Meaning |
| --- | --- | --- |
| `width` | 16 | width in cm |
| `height` | `ratio` × `width` | height in cm, at most 22 (warning beyond) |
| `ratio` | 0.618 | height / width, when `height` is not given |
| `usetex` | `True` | LaTeX renders the text |
| `family` | `"sans-serif"` | or `"serif"` |
| `preamble` | `PREAMBLE` | LaTeX preamble, a string or a list of lines; `""` for none |

### Your preamble

Give the packages your document loads, so that its macros work in labels:

```python
apply_style(8, 6, preamble=[r"\usepackage[french]{babel}", r"\usepackage{siunitx}"])
```

### Axes

`style_axes(ax)` draws thin grey spines and outward ticks, gives each linear axis a
`DecimalCommaFormatter` (`decimal_comma=False` for a point), and calls `tight_layout`.
`format_ticks=False` keeps the formatters you set. `DecimalCommaFormatter` can also be
used alone:

```python
from latex_figures import DecimalCommaFormatter

ax.yaxis.set_major_formatter(DecimalCommaFormatter())
```

`add_inset(ax, [x0, y0, width, height])` places inset axes, in fractions of `ax`, with
tick labels shrunk to suit their size.

### Saving

`save_figure(fig, path)` takes the format from the extension (`pdf`, `png`, `eps`) or
from `fmt=`, adds the extension when missing, saves at 300 dpi and returns the
absolute path. `crop=False` skips the cropping.

The full reference, with every parameter and error, is in
[docs/DOC.md](https://github.com/antnardo/latex_figures/blob/main/docs/DOC.md).

## Limits

- `apply_style` changes matplotlib's global settings; figures created before it keep
  theirs. Use `style_params` in `plt.rc_context` to leave them alone.
- The preamble is compiled by `latex` (DVI, through dvipng), not by LuaLaTeX or
  XeLaTeX: packages that need those engines, such as fontspec, are not available.
- The text font is one matplotlib knows how to load in LaTeX: Helvetica for
  `"sans-serif"`, Times for `"serif"`. Math is in Computer Modern with Helvetica, in
  Times with Times.
- The decimal comma covers the tick labels of linear axes. Numbers you write in labels,
  legends or annotations are yours to write with a comma (`{,}` in math mode, or
  siunitx).
- Cropping removes the white margin, so the file is a little smaller than the size
  asked for. The text keeps its size as long as the figure is included without
  scaling.

## Development

```bash
uv sync --group dev
uv run ruff format src tests examples
uv run ruff check src tests examples
uv run mypy
uv run pytest
```

The tests marked `latex` compile with LaTeX or run pdfcrop; they are skipped when the
program is missing, and `pytest -m "not latex"` leaves them out.

## License

MIT, see [LICENSE](LICENSE).
