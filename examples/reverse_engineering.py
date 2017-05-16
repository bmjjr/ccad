#!/usr/bin/python
# coding: utf-8

r"""Decomposing an assembly obtained from a STEP file"""

import wx
import logging
import pdb
import numpy as np 
import os 

import ccad.model as cm
import ccad.display as cd
import ccad.quaternions as cq
import numpy.linalg as la

from aocxchange.step import StepImporter
from aocutils.display.wx_viewer import Wx3dViewer
import OCC.Display.SimpleGui as SimpleGui


def reverse_engineering_with_ccad(_step_filename,dirname='step',view=False ,direct = False):
    r"""Reverse engineering using ccad

    Parameters
    ----------

    step_filename : str
        Path to the STEP file
    view : bool, optional (default is False)
        Launch the ccad viewer?
    direct : boolean 

    """
    step_filename = os.path.join(dirname,_step_filename)
    # get Assembly from step file
    assembly = cm.Assembly.from_step(step_filename, direct= direct)
    # tag nodes with geometrical information
    assembly.tag_nodes()



    # save individual components in separated files
    assembly.write_components()

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

def view_assembly_nodes(x,node_index=[0],typ='original'):
    """
    Parameters
    ----------

    x : An Assembly Graph
    node_index : a list of Assembly nodes (-1 : all nodes)
    typ : string 
        'original' | 'parts'

    Notes
    -----

    An Assembly is a graph 
    Each node of an assembly has attached
        + a filename describing a solid in its own local frame
        + a quaternion for solid orientation in the global frame
        + a translation vector for solid placement in the global frame

    This function takes an Assembly as argument and produces the view in the global 
    frame. 

    """
    if type(node_index)==int:
        if node_index==-1:
            node_index = x.node.keys()
        else:
            node_index=[node_index]

    assert(max(node_index)<=max(x.node.keys())),"Wrong node index"
    # viewer initialisation
    ccad_viewer = cd.view()
    # get the list of all shape associated with Assembly x
    #
    # This is for debug purpose.
    # In the final implementation. 
    # The assembly structure is not supposed to save shapes themselves 
    # but only references to files (.py or .step) 
    #
    lshapes1 = [x.node[k]['shape'] for k in node_index] 
    # get the list of all filename associated with Assembly x
    lfiles = [x.node[k]['name']+'.stp' for k in node_index] 
    # select directory where node files are saved
    # temporary 
    #
    fileorig = x.origin.split('.')[0]
    
    rep = os.path.join('.',fileorig)
    #rep = './step/MOTORIDUTTORE_ASM/'
    #rep = './step/ASM0001_ASM_1_ASM/'  # OCC compound'
    #rep = './step/MOTORIDUTTORE_ASM/'
    # get the local frame shapes from the list .step files  
    lshapes2 = [cm.from_step(os.path.join(rep,s)) for s in lfiles] 


    # get unitary matrix and translation for global frame placement
    lV   = [x.node[k]['V'] for k in node_index] 
    lptm = [x.node[k]['ptc'] for k in node_index] 
    lbmx = [x.node[k]['bmirrorx'] for k in node_index]
    #
    # iter on selected local shapes and apply the graph stored geometrical transformation sequence
    # 1 : rotation 
    # 2 : translation
    #
    for k,shp in enumerate(lshapes2): 
        #print(type(shp))
        #print lfiles[k]
        #print lbmx[k]
        V = lV[k]
        #print V
        #print la.det(V)
        bmirrorx = lbmx[k]
        q = cq.Quaternion()
        q.from_mat(V)
        vec, ang = q.vecang()
        print(vec,ang)
        shp.rotate(np.array([0,0,0]),vec,-ang)
        if bmirrorx:
            shp.mirrorx()
        shp.translate(lptm[k])
        shp.foreground=(1,1,0.5)

    # create a solid with the transformed shapes
    if typ=='original': 
        solid = cm.Solid(lshapes1)
    else:
        solid = cm.Solid(lshapes2)
    ccad_viewer.set_background((1,1,1)) # White
    ccad_viewer.display(solid,transparency=0.5,material='copper')
    cd.start()
    return lshapes2,lV,lptm
#
if __name__ == "__main__":
    #level = logging.INFO
    level = 0 
    logging.basicConfig(level=level,
                        format='%(asctime)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')
    filename = "ASM0001_ASM_1_ASM.stp"  # OCC compound
    #filename = "step/MOTORIDUTTORE_ASM.stp" # OCC compound
    #filename = "step/0_tabby2.stp" # OCC compound
    #filename = "step/aube_pleine.stp"  # OCC Solid

    # view_topology_with_aocutils(filename)
    x = reverse_engineering_with_ccad(filename,view=False,direct=True)
    lsh,lV,lptm=view_assembly_nodes(x,node_index=-1)
