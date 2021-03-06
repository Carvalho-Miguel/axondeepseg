# coding: utf-8

import pytest
import os
import inspect
import random
import string
import tempfile
import numpy as np
import shutil

from AxonDeepSeg.morphometrics.compute_morphometrics import *


class TestCore(object):
    def setup(self):
        self.fullPath = os.path.dirname(os.path.abspath(__file__))

        # Move up to the test directory, "test/"
        self.testPath = os.path.split(self.fullPath)[0]

        self.pixelsizeFileName = os.path.join(
            self.testPath,
            '__test_files__',
            '__test_demo_files__',
            'pixel_size_in_micrometer.txt')
        self.pixelsizeValue = 0.07   # For current demo data.

        self.tmpDir = os.path.join(self.fullPath, '__tmp__')
        if not os.path.exists(self.tmpDir):
            os.makedirs(self.tmpDir)

    def teardown(self):
        if os.path.exists(self.tmpDir):
            shutil.rmtree(self.tmpDir)

    # --------------get_pixelsize tests-------------- #
    @pytest.mark.unit
    def test_get_pixelsize_returns_expected_value(self):
        expectedValue = self.pixelsizeValue
        actualValue = get_pixelsize(self.pixelsizeFileName)

        assert actualValue == expectedValue

    @pytest.mark.unit
    def test_get_pixelsize_throws_error_for_nonexisisting_file(self):
        nonExistingFile = ''.join(
            random.choice(string.lowercase) for i in range(16))

        with pytest.raises(IOError):
            get_pixelsize(nonExistingFile)

    @pytest.mark.unit
    def test_get_pixelsize_throws_error_for_invalid_data_file(self):
        with tempfile.NamedTemporaryFile() as tmp:
            # Data written using tempfile module are saved in a binary format
            # by default, which get_pixelsize doesn't currently support.
            tmp.write(repr(self.pixelsizeValue))

            with pytest.raises(ValueError):
                get_pixelsize(tmp.name)

    # --------------get_axon_morphometrics tests-------------- #
    @pytest.mark.unit
    def test_get_axon_morphometrics_returns_expected_type(self):
        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True)

        stats_array = get_axon_morphometrics(pred_axon, path_folder)

        assert isinstance(stats_array, np.ndarray)

    @pytest.mark.unit
    def test_get_axon_morphometrics_returns_expected_keys(self):
        expectedKeys = {'y0',
                        'x0',
                        'axon_diam',
                        'solidity',
                        'eccentricity',
                        'orientation'
                        }

        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True)

        stats_array = get_axon_morphometrics(pred_axon, path_folder)

        for key in stats_array[0].keys():
            assert key in expectedKeys

    # --------------save and load _axon_morphometrics tests-------------- #
    @pytest.mark.unit
    def test_save_axon_morphometrics_creates_file_in_expected_location(self):
        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True
            )

        stats_array = get_axon_morphometrics(pred_axon, path_folder)

        save_axon_morphometrics(self.tmpDir, stats_array)

        # Filename 'axonlist.npy' is hardcoded in function.
        expectedFilePath = os.path.join(self.tmpDir, 'axonlist.npy')

        assert os.path.isfile(expectedFilePath)

    @pytest.mark.unit
    def test_save_axon_morphometrics_throws_error_if_folder_doesnt_exist(self):
        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True
            )

        stats_array = get_axon_morphometrics(pred_axon, path_folder)

        nonExistingFolder = ''.join(random.choice(string.lowercase) for i in range(16))

        with pytest.raises(IOError):
            save_axon_morphometrics(nonExistingFolder, stats_array)

    @pytest.mark.unit
    def test_load_axon_morphometrics_returns_identical_var_as_was_saved(self):
        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True
            )

        original_stats_array = get_axon_morphometrics(pred_axon, path_folder)

        save_axon_morphometrics(self.tmpDir, original_stats_array)

        # Load method only takes in a directory as an argument, expects that
        # 'axonlist.npy' will be in directory.
        loaded_stats_array = load_axon_morphometrics(self.tmpDir)

        assert np.array_equal(loaded_stats_array, original_stats_array)

    @pytest.mark.unit
    def test_load_axon_morphometrics_throws_error_if_folder_doesnt_exist(self):

        nonExistingFolder = ''.join(random.choice(string.lowercase) for i in range(16))

        with pytest.raises(IOError):
            load_axon_morphometrics(nonExistingFolder)

    # --------------display_axon_diameter tests-------------- #
    @pytest.mark.unit
    def test_display_axon_diameter_creates_file_in_expected_location(self):
        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        img = imread(os.path.join(path_folder, 'image.png'))
        path_prediction = os.path.join(
            path_folder,
            'AxonDeepSeg_seg-axonmyelin.png'
            )

        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True)

        pred_myelin = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-myelin.png'),
            flatten=True)

        display_axon_diameter(img, path_prediction, pred_axon, pred_myelin)

        assert os.path.isfile(
            os.path.join(path_folder, 'AxonDeepSeg_map-axondiameter.png')
            )

        os.remove(
            os.path.join(path_folder, 'AxonDeepSeg_map-axondiameter.png')
            )

    # --------------get_aggregate_morphometrics tests-------------- #
    @pytest.mark.unit
    def test_get_aggregate_morphometrics_returns_expected_type(self):
        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True
            )

        pred_myelin = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-myelin.png'),
            flatten=True
            )

        aggregate_metrics = get_aggregate_morphometrics(
            pred_axon,
            pred_myelin,
            path_folder
            )

        assert isinstance(aggregate_metrics, dict)

    @pytest.mark.unit
    def test_get_aggregate_morphometrics_returns_returns_expected_keys(self):
        expectedKeys = {'avf',
                        'mvf',
                        'gratio',
                        'mean_axon_diam',
                        'mean_myelin_diam',
                        'mean_myelin_thickness',
                        'axon_density_mm2'
                        }

        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True
            )

        pred_myelin = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-myelin.png'),
            flatten=True
            )

        aggregate_metrics = get_aggregate_morphometrics(
            pred_axon,
            pred_myelin,
            path_folder
            )

        for key in aggregate_metrics.keys():
            assert key in expectedKeys

    # --------------write_aggregate_morphometrics tests-------------- #
    @pytest.mark.unit
    def test_write_aggregate_morphometrics_creates_file_in_expected_location(self):
        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True
            )

        pred_myelin = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-myelin.png'),
            flatten=True
            )

        aggregate_metrics = get_aggregate_morphometrics(
            pred_axon,
            pred_myelin,
            path_folder
            )

        expectedFilePath = os.path.join(
            self.tmpDir,
            'aggregate_morphometrics.txt'
            )

        write_aggregate_morphometrics(self.tmpDir, aggregate_metrics)

        assert os.path.isfile(expectedFilePath)

    @pytest.mark.unit
    def test_write_aggregate_morphometrics_throws_error_if_folder_doesnt_exist(self):
        path_folder = self.pixelsizeFileName.split('pixel_size_in_micrometer.txt')[0]
        pred_axon = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-axon.png'),
            flatten=True
            )

        pred_myelin = imread(
            os.path.join(path_folder, 'AxonDeepSeg_seg-myelin.png'),
            flatten=True
            )

        aggregate_metrics = get_aggregate_morphometrics(
            pred_axon,
            pred_myelin,
            path_folder
            )

        nonExistingFolder = ''.join(random.choice(string.lowercase) for i in range(16))

        with pytest.raises(IOError):
            write_aggregate_morphometrics(nonExistingFolder, aggregate_metrics)
