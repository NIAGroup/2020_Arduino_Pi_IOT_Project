import sys
import os

RESOURCES_INIT = os.path.abspath(__name__)
RESOURCES_DIR = os.path.abspath(os.path.dirname(__name__))

sys.path.insert(0, RESOURCES_INIT)
sys.path.insert(1,RESOURCES_DIR)

