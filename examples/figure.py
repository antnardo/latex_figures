"""A figure ready for LaTeX: 8 cm by 6 cm, decimal comma, cropped PDF.

``apply_style`` sets sizes and fonts before the figure is created; ``style_axes`` formats
the axes; ``save_figure`` saves the figure cropped to the ink (pdfcrop). Save before
``plt.show()``, which empties the figure when its window closes. Needs LaTeX with
siunitx, since ``usetex`` is on.

    python examples/figure.py
"""

import matplotlib.pyplot as plt
import numpy as np

from latex_figures import add_inset, apply_style, save_figure, style_axes


def main() -> None:
    apply_style(8, 6)  # width, height in cm
    x = np.linspace(-4, 4, 500)
    fig, ax = plt.subplots()
    ax.plot(x, np.sinc(x) ** 2)
    ax.set_title("Diffraction by a slit")
    ax.set_xlabel(r"$x=\frac{a\sin\theta}{\lambda}$")
    ax.set_ylabel(r"$I/I_0$")
    style_axes(ax)
    inset = add_inset(ax, [0.65, 0.5, 0.3, 0.4])
    inset.plot(x, 100 * np.sinc(x) ** 2)  # the secondary maxima, in percent
    inset.set_xlim(1, 3)
    inset.set_ylim(0, 6)
    style_axes(inset)
    print(save_figure(fig, "slit.pdf").name)


if __name__ == "__main__":
    main()
