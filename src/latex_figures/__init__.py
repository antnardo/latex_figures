"""matplotlib figures that match the LaTeX document they go into: size in centimetres,
the document's fonts and preamble, a decimal comma, insets, and cropping to the ink.

Usage::

    import matplotlib.pyplot as plt
    from latex_figures import apply_style, save_figure, style_axes

    apply_style(8, 6)  # width, height in cm, before creating the figures
    fig, ax = plt.subplots()
    ax.plot(x, y)
    style_axes(ax)  # spines, ticks, decimal comma
    save_figure(fig, "figure.pdf")  # cropped by pdfcrop
"""

from latex_figures.axes import DecimalCommaFormatter, add_inset, style_axes
from latex_figures.export import FORMATS, save_figure
from latex_figures.style import (
    INCH,
    MAX_HEIGHT,
    PREAMBLE,
    apply_style,
    figure_size,
    restore_style,
    style_params,
)

__version__ = "0.3.0"

__all__ = [
    "FORMATS",
    "INCH",
    "MAX_HEIGHT",
    "PREAMBLE",
    "DecimalCommaFormatter",
    "__version__",
    "add_inset",
    "apply_style",
    "figure_size",
    "restore_style",
    "save_figure",
    "style_axes",
    "style_params",
]
