import unittest
from .process_response import ProcessAPICall


class TestProcessAPICall(unittest.TestCase):
    def SetUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app.config["HI_TEMP"] = 6000
        self.app.config["LO_TEMP"] = 2700
        self.app_context.push()
