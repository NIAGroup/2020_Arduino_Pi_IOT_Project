import sys
import os

TEST_INIT = os.path.abspath(__name__)
TEST_DIR = os.path.abspath(os.path.dirname(__name__))
FLASK_HOME = os.path.abspath(os.path.join(TEST_DIR, os.pardir))

sys.path.insert(0, TEST_INIT)
sys.path.insert(1, TEST_DIR)
sys.path.insert(2, FLASK_HOME)