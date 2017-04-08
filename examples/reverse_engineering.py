#!/usr/bin/python
# coding: utf-8

r"""Decomposing an assembly obtained from a STEP file"""

import wx
import logging
import pdb
import numpy as np 

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

    return assembly

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

def view_assembly_nodes(x,node_index=[0]):
    ccad_viewer = cd.view()
    lshapes1 = [x.G.node[k]['shape'] for k in node_index] 
    lfiles = [x.G.node[k]['name']+'.stp' for k in node_index] 
    rep = './step/ASM0001_ASM_1_ASM/'
    lshapes2 = [cm.from_step(rep+s) for s in lfiles] 
    lq  = [x.G.node[k]['q'] for k in node_index] 
    lptm = [x.G.node[k]['ptm'] for k in node_index] 
    for k,s in enumerate(lshapes2): 
        vec,ang = lq[k].vecang()
        print(lq[k])
        print(lptm[k])
        print(vec,ang)
        s.rotate(np.array([0,0,0]),vec,-ang)
        s.translate(lptm[k])

    # solid instantiated with a list of shells 
    solid = cm.Solid(lshapes2)
    ccad_viewer.display(solid)
    cd.start()
    return lshapes2,lq,lptm
#
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')
    filename = "step/ASM0001_ASM_1_ASM.stp"  # OCC compound
    #filename = "step/MOTORIDUTTORE_ASM.stp" # OCC compound
    #filename = "step/0_tabby2.stp" # OCC compound
    #filename = "step/aube_pleine.stp"  # OCC Solid

    # view_topology_with_aocutils(filename)
    x = reverse_engineering_with_ccad(filename,view=False,direct=True)
    view_assembly_nodes(x,node_index=np.arange(10))
