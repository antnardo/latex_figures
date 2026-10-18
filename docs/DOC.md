# latex-figures reference

Every public name of `latex_figures`, with its parameters, defaults and errors. Sizes
are in centimetres. The [README](../README.md) says what the package is for and how to
start.

- [Style](#style)
  - [`apply_style`](#apply_style)
  - [`style_params`](#style_params)
  - [`restore_style`](#restore_style)
  - [`figure_size`](#figure_size)
- [Axes](#axes)
  - [`style_axes`](#style_axes)
  - [`DecimalCommaFormatter`](#decimalcommaformatter)
  - [`add_inset`](#add_inset)
- [Saving](#saving)
  - [`save_figure`](#save_figure)
- [Constants](#constants)
- [Troubleshooting](#troubleshooting)

The modules are `latex_figures.style`, `latex_figures.axes` and
`latex_figures.export`; everything below is re-exported by `latex_figures`.

## Style

### `apply_style`

```python
apply_style(width=None, height=None, ratio=None, usetex=True,
            family="sans-serif", preamble=None) -> dict[str, Any]
```

Updates `matplotlib.rcParams` with `style_params(...)` and returns them. Call it
before creating the figures; figures already created keep their settings. The first
call saves the settings it changes, for `restore_style`; later calls do not overwrite
that copy. No locale is changed.

### `style_params`

```python
style_params(width=None, height=None, ratio=None, usetex=True,
             family="sans-serif", preamble=None) -> dict[str, Any]
```

The settings without applying them, for `plt.rc_context(style_params(8, 6))`.

| Parameter | Meaning |
| --- | --- |
| `width` | cm, 16 by default |
| `height` | cm; by default `ratio` × `width` |
| `ratio` | the golden ratio (0.618) by default |
| `usetex` | render text with LaTeX (`latex` and dvipng needed) |
| `family` | `"sans-serif"` (Helvetica with `usetex`) or `"serif"` (Times) |
| `preamble` | `text.latex.preamble`: a string, or a list of lines; `PREAMBLE` by default, `""` for none; used only with `usetex` |

The settings: 11 pt font, labels and titles, 10 pt ticks, 8 pt legend, 3 pt markers,
mathtext tick formatting, Arial/Helvetica or Times New Roman/Times (DejaVu as the
fallback without `usetex`), subplot margins suited to a small figure,
`pgf.texsystem = "pdflatex"`.

### `restore_style`

```python
restore_style() -> None
```

Gives back the settings from before the first `apply_style`; does nothing if it was
not called, or a second time.

### `figure_size`

```python
figure_size(width=16.0, height=None, ratio=None) -> tuple[float, float]
```

The size in inches of a figure given in cm. Without `height`, it is `ratio` × `width`
(golden ratio by default). A height over `MAX_HEIGHT` (22 cm) is brought down to it,
with a `UserWarning`.

## Axes

### `style_axes`

```python
style_axes(ax=None, format_ticks=True, decimal_comma=True) -> Axes
```

Grey 0.5 pt spines, ticks outward at the bottom and left, and with `format_ticks` a
formatter of its own on each linear axis: `DecimalCommaFormatter`, or with
`decimal_comma=False` a mathtext `ScalarFormatter` with the same power limits.
Logarithmic axes keep theirs. Calls `tight_layout` on the figure. `ax` defaults to
`plt.gca()`; returns it.

### `DecimalCommaFormatter`

```python
DecimalCommaFormatter(**kwargs)
```

A `matplotlib.ticker.ScalarFormatter` in math notation (`useMathText=True` unless
given), with powers of ten outside [10⁻², 10⁴], writing `1{,}5` for 1.5: `{,}` keeps
math mode from adding a space after the comma. The offset text (`×10⁵`, or `1{,}5` as
an additive offset) gets the comma too. The keyword arguments go to
`ScalarFormatter`.

The comma does not come from `locale`, which acts on the whole program and fails
without a French locale.

### `add_inset`

```python
add_inset(ax, rect) -> Axes
```

Inset axes inside `ax`, `rect = [x0, y0, width, height]` in fractions of `ax`. Tick
labels shrink as the square root of the relative size: an inset a quarter as wide has
labels half the size. Built on `Axes.inset_axes`, so the inset follows `ax` when the
layout changes. Call `style_axes` on the inset for its spines and decimal comma.

## Saving

### `save_figure`

```python
save_figure(fig, path, fmt=None, dpi=300, tight=True, crop=True) -> Path
```

Saves `fig` as PDF, PNG or EPS, from the extension of `path` or from `fmt`, adding the
extension when missing (`"figure"` with `fmt="png"` gives `figure.png`), then crops it
to the ink with the first tool found in `FORMATS`: pdfcrop, ImageMagick (`magick` or
`convert`), epstool. `tight` passes `bbox_inches="tight"` to `savefig`; `crop=False`
skips the tool. No shell is used, and the temporary file is deleted. Returns the
absolute path written.

- `ValueError` for another format;
- a `UserWarning`, and an uncropped figure, when no tool is found;
- `subprocess.CalledProcessError` when the tool fails.

## Constants

| Name | Value |
| --- | --- |
| `PREAMBLE` | `\usepackage{amsmath}` and `\usepackage{siunitx}`, one per line |
| `INCH` | 2.54 (cm) |
| `MAX_HEIGHT` | 22.0 (cm), the usable height of an A4 page |
| `FORMATS` | format → list of cropping commands, `{e}` the input, `{s}` the output |
| `__version__` | the package version |

## Troubleshooting

**`RuntimeError: Failed to process string with tex because latex could not be
found`.** `usetex` is on and `latex` is not on the `PATH` of the process. Install a
TeX distribution, or pass `usetex=False`.

**`LaTeX was not able to process the following string`.** A label uses a macro the
preamble does not load, or a package of the preamble is missing. Add it to `preamble`,
or install it (`siunitx` is in `texlive-science` on Debian/Ubuntu).

**`pdfcrop not found: figure not cropped`.** Install pdfcrop (with TeX Live), or pass
`crop=False` to silence the warning.

**The axes show `0.5` after `style_axes`.** The axis is logarithmic, or
`format_ticks=False` was passed, or a formatter was set after `style_axes`.
