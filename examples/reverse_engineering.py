#!/usr/bin/python
# coding: utf-8

r"""Decomposing an assembly obtained from a STEP file"""

import wx
import logging

import ccad.model as cm
import ccad.display as cd

from aocxchange.step import StepImporter
from aocutils.display.wx_viewer import Wx3dViewer
import OCC.Display.SimpleGui as SimpleGui


def reverse_engineering_with_ccad(step_filename, view=False ,direct = False):
    r"""Reverse engineering using ccad

    Parameters
    ----------
    step_filename : str
        Path to the STEP file
    view : bool, optional (default is False)
        Launch the ccad viewer?

    """
    assembly = cm.Assembly.from_step(step_filename, direct= direct)
    assembly.write_components()
    assembly.tag_nodes()

    if view:
        ccad_viewer = cd.view()
        for shell in assembly.shape.subshapes("Shell"):
            ccad_viewer.display(shell)
        cd.start()

    return(assembly)

def view_topology_with_aocutils(step_filename):
    r"""View the STEP file contents in the aocutils wx viewer.

    The aocutils wx viewer is good to visualize topology.

    Parameters
    ----------
    step_filename : str
        Path to the STEP file

    """

    importer = StepImporter(filename=step_filename)

    class MyFrame(wx.Frame):
        r"""Frame for testing"""
        def __init__(self):
            wx.Frame.__init__(self, None, -1)
            self.p = Wx3dViewer(self)
            for shape in importer.shapes:
                self.p.display_shape(shape)
            self.Show()

    app = wx.App()
    frame = MyFrame()
    app.SetTopWindow(frame)
    app.MainLoop()

def view_node(x,node_index=0):
    ccad_viewer = cd.view()
    shape = x.G.node[node_index]['shape'] 
    for shell in shape.subshapes("Shell"):
        ccad_viewer.display(shell)
    cd.start()
#
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')
    filename = "step/ASM0001_ASM_1_ASM.stp"  # OCC compound
    #filename = "step/MOTORIDUTTORE_ASM.stp" # OCC compound
    #filename = "step/0_tabby2.stp" # OCC compound
    # filename = "step/aube_pleine.stp"  # OCC Solid

    # view_topology_with_aocutils(filename)
    x = reverse_engineering_with_ccad(filename,view=False,direct=True)
