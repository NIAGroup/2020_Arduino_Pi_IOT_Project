import sys
import os

DIR = os.path.dirname(os.path.abspath(__name__))
WEB_HOME = os.pardir(DIR)

sys.path.insert(0, DIR)
sys.path.insert(1, WEB_HOME)