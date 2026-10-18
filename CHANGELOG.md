# Changelog

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-10-18

First release on PyPI.

### Added

- `apply_style`, `style_params` and `restore_style`: matplotlib set up for a figure of
  a given size in centimetres, with LaTeX text and a preamble (`PREAMBLE`: amsmath and
  siunitx).
- `figure_size`: the size in inches of a figure given in centimetres, at most 22 cm
  high.
- `style_axes` and `DecimalCommaFormatter`: discreet spines, outward ticks, a decimal
  comma without changing the locale.
- `add_inset`: inset axes with tick labels to scale.
- `save_figure`: PDF, PNG or EPS cropped to the ink by pdfcrop, ImageMagick or epstool.

[0.2.0]: https://github.com/antnardo/latex_figures/releases/tag/v0.2.0
