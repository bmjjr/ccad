import ccad.model as cm 
import ccad.display as cd 
import numpy as np  
O = (0., 0.0, 0.0)
X = (1.0, 0.0, 0.0)
Y = (0., 1.0, 0.0)
Z = (0., 0.0, 1.0)
x = cm.segment(O, X)
y = cm.segment(O, Y)
z = cm.segment(O, Z)
t = cm.Wire([x,y,z])
#e2.translate((0,1,0))
#""U = np.eye(3)
#u = [1,0,2] 
#U = U[:,u]
#e2.transform(U)
v1=cd.view()
v1.display(t)
cd.start()
