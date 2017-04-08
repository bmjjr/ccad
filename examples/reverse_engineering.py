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
    """
    Parameters
    ----------

    x : An Assembly Graph
    node_index : a list of Assembly nodes (-1 : all nodes)

    Notes
    -----

    An Assembly is a graph 
    Each node of an assembly has attached
        + A filename describing a solid in its own local frame
        + A quaternion for solid orientation in the global frame
        + A translation vector for solid placement in the global frame

    This function takes an Assembly as argument and produces its view in the global 
    frame. 

    """
    if type(node_index)==int:
        if node_index==-1:
            node_index = x.G.node.keys()
        else:
            node_index=[node_index]

    assert(max(node_index)<=max(x.node.keys())),"Wrong node index"
    # viewer initialisation
    ccad_viewer = cd.view()
    # get the list of all shape associated with Assembly x
    #
    # This is for debug purpose.
    # In the final implementation. The assembly structure is not supposed to save shapes themselves 
    # but only references to files (.py or .step) 
    #
    lshapes1 = [x.G.node[k]['shape'] for k in node_index] 
    # get the list of all filename associated with Assembly x
    lfiles = [x.G.node[k]['name']+'.stp' for k in node_index] 
    # select directory where node files are saved
    # temporary 
    #
    rep = './step/ASM0001_ASM_1_ASM/'
    # get the local frame shapes from the list .step files  
    lshapes2 = [cm.from_step(rep+s) for s in lfiles] 
    # get quaternion and translation for global frame placement
    lq  = [x.G.node[k]['q'] for k in node_index] 
    lptm = [x.G.node[k]['ptm'] for k in node_index] 
    #
    # iter on selected local shapes and apply the graph stored geometrical transformation sequence
    # 1 : rotation 
    # 2 : translation
    #
    for k,s in enumerate(lshapes2): 
        vec,ang = lq[k].vecang()
        print(lq[k])
        print(lptm[k])
        print(vec,ang)
        s.rotate(np.array([0,0,0]),vec,-ang)
        s.translate(lptm[k])

    # create a solid with the transformed shapes 
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
