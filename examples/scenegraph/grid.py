"""
Simple test of SceneCanvas containing a single line entity
as its entire scenegraph.
"""
from vispy import scenegraph
from vispy import app
from vispy.visuals import transforms
import numpy as np

canvas = scenegraph.SceneCanvas()
canvas.size = 600, 600
canvas.show()

pos = np.empty((1000,2))
pos[:,0] = np.linspace(0, 10, 1000)
pos[:,1] = np.random.normal(size=1000)

grid = canvas.root.add_grid()

b1 = grid.add_view(row=0, col=0, col_span=2)
b2 = grid.add_view(row=1, col=0)
b3 = grid.add_view(row=1, col=1)

l1 = scenegraph.entities.Line(pos)
l1.transform.scale((10, 1))
l1.transform.translate((20, 100))

b1.add(l1)
b2.add(l1)
b3.add(l1)

import sys
if sys.flags.interactive == 0:
    app.run()
