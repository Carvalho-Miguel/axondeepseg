# coding: utf-8

import pytest
import os
import numpy as np
from scipy.misc import imread

from AxonDeepSeg.visualization.visualize import *


class TestCore(object):
    def setup(self):
        self.fullPath = os.path.dirname(os.path.abspath(__file__))

        # Move up to the test directory, "test/"
        self.testPath = os.path.split(self.fullPath)[0]

        self.pathModel = os.path.join(
            self.testPath,
            '__test_files__',
            '__test_model__',
            'Model'
            )

    def teardown(self):
        pass

    # --------------visualize_training tests-------------- #
    @pytest.mark.unit
    def test_visualize_training_runs_successfully(self):

        assert visualize_training(self.pathModel)
