import os

DIR = os.path.abspath(__name__)
HOME = os.path.abspath(os.path.join(DIR, os.pardir, os.pardir))

# Make sure your modules are accessed first in case of overlap.
os.sys.path.insert(0, DIR)
os.sys.path.insert(2, HOME)
