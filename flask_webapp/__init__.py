import sys
import os

DIR = os.path.abspath(os.path.dirname(__name__))
WEB_HOME = os.path.abspath(os.path.join(DIR, os.pardir))

sys.path.insert(0, DIR)
sys.path.insert(1, WEB_HOME)