import os
import unittest
from unittest.mock import patch

from flask import current_app
from flask_testing import TestCase

from manage import app
from app.main.config import basedir

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] == 'HP >>> LoTR')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] == 'HP >>> LoTR')
        self.assertTrue(app.config['DEBUG'] is True)


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)

class TestRuteRoot(TestCase):

    def create_app(self):
        app.config.from_object('app.main.config.ProductionConfig')
        return app

    def test_rute_root(self):
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)

class TestRuteGetData(TestCase):

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    @patch('app.main.controller.user_controlller.GenericGet')
    def test_rute_get_data(self,mock):

        mock_ = mock.return_value 
        mock_.get_catalogs.return_value = {'':''}

        response = app.test_client().get('/get_data/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_.get_catalogs.return_value)

class TestRuteGetDataDegree(TestCase):

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    @patch('app.main.controller.user_controlller.GenericGet')
    def test_rute_get_data_degree(self,mock):
        mock_ = mock.return_value 
        mock_.get_data.return_value = "{'':''}"
        response = app.test_client().get('/get_data/lc_degree?catalogs=ps1&format=csv&amount=all&radius=0.0002777&ra=139.33444972&dec=68.6350604')
        self.assertEqual(response.status_code, 200)

class TestRuteGetDataHms(TestCase):

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    @patch('app.main.controller.user_controlller.GenericGet')
    def test_rute_get_data_hms(self,mock):
        mock_ = mock.return_value 
        mock_.get_data.return_value = "{'':''}"
        response = app.test_client().get('/get_data/lc_hms?catalogs=ztf&format=csv&amount=all&radius=0.0002777&hms=9h17m20.26793280000689s +4h34m32.414496000003936s')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

