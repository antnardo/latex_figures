import matplotlib.pyplot as plt
import numpy as np
import pytest

from latex_figures.axes import DecimalCommaFormatter, add_inset, style_axes


@pytest.fixture
def axes():
    _, ax = plt.subplots()
    ax.plot(np.linspace(0, 3e5, 10), np.linspace(0, 2e-3, 10))
    return ax


def test_each_axis_gets_its_own_formatter(axes):
    style_axes(axes)
    assert axes.xaxis.get_major_formatter() is not axes.yaxis.get_major_formatter()


def test_common_factors_stay_independent(axes):
    # With a shared formatter, the last axis drawn would impose its factor on the other.
    style_axes(axes)
    axes.figure.canvas.draw()
    assert "10^{5}" in axes.xaxis.get_major_formatter().get_offset()
    assert "10^{\N{MINUS SIGN}3}" in axes.yaxis.get_major_formatter().get_offset()


def test_decimal_comma_without_locale():
    formatter = DecimalCommaFormatter()
    fig, ax = plt.subplots()
    ax.set_xlim(0, 2)
    ax.xaxis.set_major_formatter(formatter)
    fig.canvas.draw()
    assert formatter(1.5) == r"$\mathdefault{1{,}50}$"  # ticks 0, 0.25…


def test_decimal_point_on_request(axes):
    style_axes(axes, decimal_comma=False)
    axes.set_xlim(0, 2)
    axes.figure.canvas.draw()
    formatter = axes.xaxis.get_major_formatter()
    assert not isinstance(formatter, DecimalCommaFormatter)
    assert "{,}" not in formatter(1.5)


def test_log_axis_keeps_its_formatter():
    _, ax = plt.subplots()
    ax.set_yscale("log")
    style_axes(ax)
    assert not isinstance(ax.yaxis.get_major_formatter(), DecimalCommaFormatter)


def test_format_ticks_false_keeps_the_formatters(axes):
    before = axes.xaxis.get_major_formatter()
    style_axes(axes, format_ticks=False)
    assert axes.xaxis.get_major_formatter() is before


def test_current_axes_used_by_default(axes):
    assert style_axes() is axes


def test_spines_visible_and_grey(axes):
    style_axes(axes)
    assert all(spine.get_visible() for spine in axes.spines.values())
    assert all(spine.get_linewidth() == 0.5 for spine in axes.spines.values())


def test_default_ticks_outward_bottom_left(axes):
    style_axes(axes)
    axes.figure.canvas.draw()
    params = axes.xaxis.get_tick_params()
    assert params["direction"] == "out"
    assert params["bottom"] and not params["top"]
    assert params["color"] == "gray"
    assert len(axes.xaxis.get_minorticklocs()) == 0


def test_ticks_inward_on_four_sides(axes):
    style_axes(axes, ticks="in", mirror=True, minor=True, color="black")
    axes.figure.canvas.draw()
    for axis, sides in ((axes.xaxis, ("bottom", "top")), (axes.yaxis, ("left", "right"))):
        for which in ("major", "minor"):
            params = axis.get_tick_params(which=which)
            assert params["direction"] == "in"
            assert all(params[side] for side in sides)
            assert params["color"] == "black"
        assert len(axis.get_minorticklocs()) > 0
    assert axes.spines["top"].get_edgecolor() == (0, 0, 0, 1)


def test_mirror_keeps_labels_bottom_left(axes):
    style_axes(axes, mirror=True)
    tick = axes.xaxis.get_major_ticks()[0]
    assert tick.label1.get_visible() and not tick.label2.get_visible()


def test_unknown_tick_direction_refused(axes):
    with pytest.raises(ValueError, match="ticks must be one of"):
        style_axes(axes, ticks="inside")


def test_inset_placed_inside_the_axes(axes):
    inset = add_inset(axes, [0.6, 0.1, 0.3, 0.3])
    axes.figure.canvas.draw()
    parent = axes.get_position()
    position = inset.get_position()
    assert position.x0 == pytest.approx(parent.x0 + 0.6 * parent.width)
    assert position.width == pytest.approx(0.3 * parent.width)


def test_inset_tick_labels_shrink_with_its_size(axes):
    size = axes.xaxis.get_ticklabels()[0].get_fontsize()
    inset = add_inset(axes, [0.5, 0.5, 0.25, 0.25])
    assert inset.xaxis.get_ticklabels()[0].get_fontsize() == pytest.approx(size * 0.5)
