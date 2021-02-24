from flask_restplus import Namespace, fields

class Base():
    api = Namespace('get_data', description='get ligth curves data using degrees or hms area.')

class ParamasDegree():

    def __init__(self,api):
        pass