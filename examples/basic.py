#!/usr/bin/python
# coding: utf-8

r"""Basic example

Probably the simplest example of using ccad

"""

import ccad.model as cm
import ccad.display as cd
import numpy as np 
s1 = cm.box(2.0,2.0,2.0)
s1.chamfer(0.5)
lver = s1.subshapes('Vertex')
[ np.array(x.center()) for x in lver]
v1 = cd.view()
v1.display(s1)
cd.start()
