from distutils.dir_util import copy_tree
from pathlib import Path
import os

home = str(Path.home())

copy_tree(".", home + "\\Desktop")
os.chdir(home + "\\Desktop")

os.system("py serveurjeu_jmd.py")
