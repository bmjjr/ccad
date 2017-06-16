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
import networkx as nx
import matplotlib.pyplot as plt 

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
    assembly = cm.Assembly()
    # read from step file
    assembly.from_step(step_filename, direct= direct)
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

def view_assembly_graph(x,fontsize=18,v=20,bsave=False,bshow=True,blabels=False,alpha=0.5):
    """ view an assembly graph 

    Parameters
    ----------

    x : Assembly graph 


    """
    dxy = { k : (x.pos[k][0],x.pos[k][1]) for k in x.node.keys() }
    dxyl = { k : (x.pos[k][0]+(v*np.random.rand()-v/2.),x.pos[k][1]+(v*np.random.rand()-v/2.)) for k in x.node.keys() }
    dxz = { k : (x.pos[k][0],x.pos[k][2]) for k in x.node.keys() }
    dxzl = { k : (x.pos[k][0]+(v*np.random.rand()-v/2),x.pos[k][2]+(v*np.random.rand()-v/2.)) for k in x.node.keys() }
    dyz = { k : (x.pos[k][2],x.pos[k][1]) for k in x.node.keys() }
    dyzl = { k : (x.pos[k][2]+(v*np.random.rand()-v/2),x.pos[k][1]+(v*np.random.rand()-v/2.)) for k in x.node.keys() }
    node_size = [ x.node[k]['dim'] for k in x.node.keys() ]
    #dlab = {k : str(int(np.ceil(x.node[k]['dim']))) for k in x.node.keys() if x.edge[k].keys()==[] }
    dlab = {k : x.node[k]['name'] for k in x.node.keys() }
    
    plt.figure(figsize=(10,10))
    plt.suptitle(x.origin,fontsize=fontsize+2)
    plt.subplot(2,2,1)
    nx.draw_networkx_nodes(x,dxy,node_size=node_size,alpha=alpha)
    nx.draw_networkx_edges(x,dxy)
    if blabels:
        nx.draw_networkx_labels(x,dxyl,labels=dlab,font_size=fontsize)
    plt.xlabel('X axis (mm)')
    plt.ylabel('Y axis (mm)')
    plt.title("XY plane")
    plt.subplot(2,2,2)
    nx.draw_networkx_nodes(x,dyz,node_size=node_size,alpha=alpha)
    nx.draw_networkx_edges(x,dyz)
    if blabels:
        nx.draw_networkx_labels(x,dyzl,labels=dlab,font_size=fontsize)
    plt.xlabel('Z axis (mm)')
    plt.ylabel('Y axis (mm)')
    plt.title("ZY plane")
    plt.subplot(2,2,3)
    nx.draw_networkx_nodes(x,dxz,node_size=node_size,alpha=alpha)
    nx.draw_networkx_edges(x,dxz)
    if blabels:
        nx.draw_networkx_labels(x,dxzl,labels=dlab,font_size=fontsize)
    plt.title("XZ plane")
    plt.xlabel('X axis (mm)')
    plt.ylabel('Z axis (mm)')
    plt.subplot(2,2,4)
    if blabels:
        nx.draw(x,labels=dlab,alpha=alpha,font_size=fontsize,node_size=node_size)
    else:
        nx.draw(x,alpha=alpha,font_size=fontsize,node_size=node_size)
    if bsave:
        plt.savefig(x.origin+'png')
    if bshow:
        plt.show()

def view_assembly_nodes(x,node_index=-1):
    """
    Parameters
    ----------

    x : An Assembly Graph
    node_index : a list of Assembly nodes (-1 : all nodes)

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

    if x.serialized:
        s.unserialize()

    # viewer initialisation
    ccad_viewer = cd.view()
    # get the list of all shape associated with Assembly x
    #
    # This is for debug purpose.
    # In the final implementation. 
    # The assembly structure is not supposed to save shapes themselves 
    # but only references to files (.py or .step) 
    #
    #lshapes1 = [x.node[k]['shape'] for k in node_index] 
    # get the list of all filename associated with Assembly x
    lfiles = [str(x.node[k]['name'])+'.stp' for k in node_index] 
    # select directory where node files are saved
    # temporary 
    #
    fileorig = x.origin.split('.')[0]
    
    rep = os.path.join('.',fileorig)

    # get the local frame shapes from the list .step files  
    lshapes2 = [cm.from_step(os.path.join(rep,s)) for s in lfiles] 
    

    # get unitary matrix and translation for global frame placement
    lV   = [x.node[k]['V'] for k in node_index] 
    lptm = [x.node[k]['ptc'] for k in node_index] 
    #lbmx = [x.node[k]['bmirrorx'] for k in node_index]
    #
    # iter on selected local shapes and apply the graph stored geometrical transformation sequence
    # 1 : rotation 
    # 2 : translation
    #
    for k,shp in enumerate(lshapes2): 
        V = lV[k]
        shp.transform(V)
        # if 'mx' in x.node[k]:
        #     if x.node[k]['mx']:
        #         print(k,"mx")
        #         shp.mirrorx()
        # if 'my' in x.node[k]:
        #     if x.node[k]['my']:
        #         print(k,"my")
        #         shp.mirrory()
        # if 'mz' in x.node[k]:
        #     if x.node[k]['mz']:
        #         print(k,"mz")
        #         shp.mirrorz()
        #shp.rotate(np.array([0,0,0]),vec,-ang)
        
        shp.translate(lptm[k])
        shp.foreground=(1,1,0.5)

    # create a solid with the transformed shapes
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
    #filename = "MOTORIDUTTORE_ASM.stp" # OCC compound
    #filename = "0_tabby2.stp" # OCC compound
    #filename = "aube_pleine.stp"  # OCC Solid

    # view_topology_with_aocutils(filename)
    x = reverse_engineering_with_ccad(filename,view=False,direct=True)
    #x.node[7]['mz']=False
    lsh,lV,lptm=view_assembly_nodes(x,node_index=[6,7])
#    p6 = x.node[6]['pcloud']
#    p6t = x.node[6]['pc']
#    v6 = x.node[6]['V']
#    p7 = x.node[7]['pcloud']
#    p7t = x.node[7]['pc']
#    v7 = x.node[7]['V']
#    u6 = np.dot(v6,p6)-p6t
#    u7 = np.dot(v7,p7)-p7t
   
    x.save_gml()
    x.save_json()
    node_index=[0,1]
    #lsh,lV,lptm=view_assembly_nodes(x,node_index=node_index)
