from flask_restplus import Api
from flask import Blueprint

from .main.controller.get_lc_controller import api as ns

blueprint = Blueprint('api', __name__)

api =  Api(blueprint,
             version='1.2', 
             title='FreyaAPI',
             description='FreyaAPI is the default API for use the Freya module for getting light curves data from diferent astronomical catalogs',
             contact='',
             license='',
            )

api.add_namespace(ns, path='/get_data')