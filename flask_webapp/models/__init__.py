import sys
import os

MODELS_INIT = os.path.abspath(__name__)
MODELS_DIR = os.path.abspath(os.path.dirname(__name__))

sys.path.insert(0, MODELS_INIT)
sys.path.insert(1,MODELS_DIR)

