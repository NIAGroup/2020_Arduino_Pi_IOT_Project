import sys
import os

FLASK_INIT = os.path.abspath(__name__)
FLASK_DIR = os.path.abspath(os.path.dirname(__name__))
WEB_HOME = os.path.abspath(os.path.join(FLASK_DIR, os.pardir))

sys.path.insert(0, FLASK_INIT)
sys.path.insert(1, FLASK_DIR)
sys.path.insert(2, WEB_HOME)
