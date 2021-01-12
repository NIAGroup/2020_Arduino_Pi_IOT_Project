import sys
import os

SRC_INIT = os.path.abspath(__name__)
SRC_DIR = os.path.abspath(os.path.dirname(__name__))

sys.path.insert(0, SRC_INIT)
sys.path.insert(1,SRC_DIR)

