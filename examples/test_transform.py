import ccad.model as cm 
import ccad.display as cd 
import numpy as np  
import numpy.linalg as la  
#u = t.copy()
#b1 = cm.box(1.,2.,3.)
#b2 = cm.box(1.-e,2.-e,3.-e)
#print b1.center()
#print b2.center()
#v = np.array(b2.center())-np.array(b1.center())
#b2.translate(-v)
#c = b1-b2 
#f = cm.glue([t,b])
#e2.translate((0,1,0))
#""U = np.eye(3)
#u = [1,0,2] 
#U = U[:,u]
def MRot3(a, axe):
    """
    Return a 3D rotation matrix along axe 0|1|2

    Parameters
    ----------

    a   :  angle (radians)
    axe :  0:x 1:y 2:z

    """
    M3 = np.eye(3)
    M2 = np.array(((np.cos(a), -np.sin(a)), (np.sin(a), np.cos(a))))
    if (axe == 0):
        M3[1:3, 1:3] = M2
    if (axe == 1):
        M3[0::2, 0::2] = M2
    if (axe == 2):
        M3[0:2, 0:2] = M2
    return(M3)

def MEulerAngle(alpha, beta, gamma):
    """ Calculate a rotation matrix from 3 Euler angles

    Parameters
    ----------

    alpha  : float
        rotation along axis z
    beta : float
        rotation along axis x
    gamma : float
        rotation along axis y

    Returns
    -------

    T    : np.array (3x3)
        rotation matrix

    Examples
    --------

    >>> import numpy as np
    >>> T=MEulerAngle(np.pi/2,np.pi/2,np.pi/2)

    Warnings
    --------

    Bizarre I was expected

    -1  0  0
     0  0  1
     0  1  0

    """
    Ra = MRot3(alpha, 2)
    Rb = MRot3(beta, 0)
    Rg = MRot3(gamma, 1)

    T = np.dot(np.dot(Ra, Rb), Rg)
    #T  = np.dot(np.dot(Rg,Rb),Ra)
    return(T)

def triedre(U): 
    O = (0., 0.0, 0.0)
    X = U[:,0]
    Y = U[:,1] 
    Z = U[:,2]
    x = cm.segment(O, X)
    y = cm.segment(O, Y)
    z = cm.segment(O, Z)
    t = cm.Wire([x,y,z])
    return(t)

tI = triedre(np.eye(3))
U = MEulerAngle(np.pi/4.,np.pi/3,-np.pi/7)
U = U[:,[1,0,2]]
assert(np.isclose(la.det(U),-1))
tU  = triedre(U)
ntU = tI.copy()
ntU.transform(U)
tI.dump()
print('-')
tU.dump()
print('-')
ntU.dump()
#v1 = cd.view()
#v1.display(c,transparency=0.5,material='copper')
#cd.start()
