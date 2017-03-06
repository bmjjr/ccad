# coding: utf-8

r"""Simple sphere display test (same as test.py ?)"""

try:
    import ccad.model as cm
except ImportError:
    import model as cm
import OCC.Display.SimpleGui as SimpleGui

s1 = cm.sphere(1.0)
display, start_display, add_menu, add_function_to_menu = \
    SimpleGui.init_display()
display.DisplayShape(s1.shape, update=True)
start_display()
