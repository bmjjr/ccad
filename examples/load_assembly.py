import os
import json 
import pdb
import ccad.model as cm
import ccad.display as cd 
from reverse_engineering import *
dirname = 'step'
filename = "ASM0001_ASM_1_ASM.json"  # OCC compound
assembly = cm.Assembly()
json_filename = os.path.join(dirname,filename)
assembly.load_json(json_filename)
view_assembly_nodes(assembly)

