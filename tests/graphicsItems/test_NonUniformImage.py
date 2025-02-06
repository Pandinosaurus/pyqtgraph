import numpy as np
import pytest

import pyqtgraph as pg
import pyqtgraph.functions as fn
from pyqtgraph.colormap import ColorMap
from pyqtgraph.graphicsItems.NonUniformImage import NonUniformImage
from pyqtgraph.Qt import QtTest
from tests.image_testing import assertImageApproved

app = pg.mkQApp()


def test_NonUniformImage_scale_dimensions():

    x = [1.0, 3.0, 10.0]
    y = [1.0, 2.0, 4.0]
    X, Y = np.meshgrid(x, y, indexing='ij')
    Z = X * Y

    for args in [(Z, y, Z), (x, Z, Z)]:
        with pytest.raises(Exception) as ex:
            NonUniformImage(*args)
        assert "x and y must be 1-d arrays." in str(ex)


def test_NonUniformImage_scale_monotonicity():

    x = [1.0, 0.0, 10.0]
    y = [1.0, 2.0, 4.0]
    X, Y = np.meshgrid(x, y, indexing='ij')
    Z = X * Y

    for args in [(x, y, Z), (y, x, Z)]:
        with pytest.raises(Exception) as ex:
            NonUniformImage(*args)
        assert "The values in x and y must be monotonically increasing." in str(ex)


def test_NonUniformImage_data_dimensions():

    x = [1.0, 3.0, 10.0]
    y = [1.0, 2.0, 4.0]

    with pytest.raises(Exception) as ex:
        NonUniformImage(x, y, x)
    assert "The length of x and y must match the shape of z." in str(ex)


def test_NonUniformImage_lut():

    window = pg.GraphicsLayoutWidget()
    viewbox = pg.ViewBox()
    window.setCentralWidget(viewbox)
    window.resize(200, 200)
    window.show()

    x = [1.0, 3.0, 10.0]
    y = [1.0, 2.0, 4.0]
    X, Y = np.meshgrid(x, y, indexing='ij')
    Z = X * Y

    image = NonUniformImage(x, y, Z, border=fn.mkPen('g'))

    cmap = ColorMap(None, [0.0, 1.0])
    image.setLookupTable(cmap.getLookupTable(nPts=256))

    viewbox.addItem(image)

    QtTest.QTest.qWaitForWindowExposed(window)
    QtTest.QTest.qWait(100)

    assertImageApproved(window, 'nonuniform_image/lut-3x3')


def test_NonUniformImage_colormap():

    window = pg.GraphicsLayoutWidget()
    viewbox = pg.ViewBox()
    window.setCentralWidget(viewbox)
    window.resize(200, 200)
    window.show()

    x = [1.0, 3.0, 10.0]
    y = [1.0, 2.0, 4.0]
    X, Y = np.meshgrid(x, y, indexing='ij')
    Z = X * Y

    Z[:, 0] = [-np.inf, np.nan, np.inf]

    image = NonUniformImage(x, y, Z, border=fn.mkPen('g'))

    cmap = ColorMap(pos=[0.0, 1.0], color=[(0, 0, 0), (255, 255, 255)])
    image.setColorMap(cmap)

    viewbox.addItem(image)

    QtTest.QTest.qWaitForWindowExposed(window)
    QtTest.QTest.qWait(100)

    assertImageApproved(window, 'nonuniform_image/colormap-3x3')
