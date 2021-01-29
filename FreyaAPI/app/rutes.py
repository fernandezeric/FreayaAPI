from flask import Flask
from flask import request,jsonify, make_response,abort
from flask_restplus import Api, Resource, fields

from astropy.io import ascii
from astropy.table import Table,vstack
from astropy.io.votable import parse,parse_single_table, writeto

import io
import importlib

#
from app import app

api =  Api(app,
             version='1.1', 
             title='FreyaAPI',
             description='FreyaAPI is the default API for use the Freya module for getting light curves data from diferent astronomical catalogs',
             contact= '',
             license='',
            )

ns = api.namespace('get_data', description='get ligth curves data using degrees or hms area.')

link_ = '\n https://github.com/fernandezeric/Memoria#catalogs-default-'

parser = api.parser()
parser.add_argument('catalogs', type=str, required=True, default='ztf,ps1',
                            help='Names of the catalogs to consult , first need the catalogs are in Freya.\
                                Look catalogs and what return in '+link_, location='args')
parser.add_argument('format', type=str, required=True, default='csv',choices=['csv','votable'],help='format data', location='args')
parser.add_argument('amount', type=str, required=True, default='all',choices=['all','nearest'],help='get all or only one light curve data per catalog', location='args')
parser.add_argument('radius', type=float, required=True, default=0.0002777, help='Search radius', location='args')

parser_degree = parser.copy()
parser_degree.add_argument('ra', type=float, required=True, default=139.33444972, help='(degrees) Right Ascension', location='args')
parser_degree.add_argument('dec', type=float, required=True,default=68.6350604, help='(degrees) Declination', location='args')

parser_hms = parser.copy()
parser_hms.add_argument('hms', type=str, required=True, default='9h17m20.26793280000689s +4h34m32.414496000003936s', help='hh:mm:ss', location='args')

type_response = ["text/csv","text/xml"]
code_200 = 'Ligth curves data obtained.'
code_400 = 'Value Error.'
code_404 = 'Rute not valid.'

class GenericGet():

    def get_data(self,args_,type_,get_):
        if type_ == 0:
            ra = args_['ra']
            dec = args_['dec']
        elif type_ == 1:
            hms = args_['hms']

        radius = args_['radius']
        format = args_['format']
        first = True

        for catalog in args_['catalogs'].split(","):
            catalog = catalog.upper()
            try:
                module = f'app.resources.{catalog}_resource.resource'
                mod = importlib.import_module(module)
                my_class = getattr(mod, f'Resource{catalog}')
            except:
                continue
            if type_ == 0:
                my_instance = my_class(ra=ra,dec=dec,radius=radius,format=format,nearest=get_).get_lc_deg()
            elif type_ == 1:
                my_instance = my_class(hms=hms,radius=radius,format=format,nearest=get_).get_lc_hms()

            # who read csv in astropy
            if format == 'csv':
                if first :
                    #try read data, if not exist continue
                    try: 
                        my_instance_ = ascii.read(my_instance)
                        my_instance_.add_column(f'{catalog}',name='catalog')
                        results_ = my_instance_
                    except:
                        continue
                    first = False
                else :
                    #try read data, if not exist continue
                    try:
                        my_instance_ = ascii.read(my_instance)
                        my_instance_.add_column(f'{catalog}',name='catalog')
                        results_ = vstack([results_,my_instance_])
                    except:
                        continue
            elif format == 'votable':
                if first:
                    try:
                        votable = my_instance.encode(encoding='UTF-8')
                        bio = io.BytesIO(votable)
                        votable = parse(bio)
                        table = parse_single_table(bio).to_table()
                        results_ = table
                    except:
                        continue
                    first = False
                else :
                    try:
                        votable = my_instance.encode(encoding='UTF-8')
                        bio = io.BytesIO(votable)
                        votable = parse(bio)
                        table = parse_single_table(bio).to_table()
                        results_ = vstack([results_,table])
                    except:
                        continue
        if format == 'csv':
            try:
                buf = io.StringIO()
                ascii.write(results_,buf,format='csv')
                # make responde data with headers
                data =  make_response(buf.getvalue())
                data.headers["Content-Disposition"] = "attachment; filename=LightCurveData[{}].csv".format(args_['catalogs'])
                data.headers["Content-type"] = "text/csv"
                return data
            except:
                return make_response('No light curve data find in catalog(s)')
        elif format == 'votable':
            try:
                buf = io.BytesIO()
                writeto(results_,buf)
                # make responde data with headers
                data = make_response(buf.getvalue().decode("utf-8"))
                data.headers["Content-Disposition"] = "attachment; filename=LightCurveData[{}].xml".format(args_['catalogs'])
                data.headers["Content-type"] = "text/xml"
                return data
            except:
                return make_response('No light curve data find in catalog(s)')
    
# if select two or more catalogs the data (csv/table) using vstack to join in one table

 
@ns.route('/lc_degree')
class GetLcDegree(Resource):
    @api.expect(parser_degree)
    @api.response(200, code_200)
    @api.response(400, code_400)
    @api.response(404,code_404)
    @api.produces(type_response)
    def get(self):
        args = parser_degree.parse_args()
        args = parser_degree.parse_args()
        if args['amount'] == 'all':
            return GenericGet().get_data(args,0,False)
        elif args['amount'] == 'nearest':
            return GenericGet().get_data(args,0,True)

@ns.route('/lc_hms')
class GetLcHms(Resource):
    @api.expect(parser_hms)
    @api.response(200, code_200)
    @api.response(400, code_400)
    @api.response(404,code_404)
    @api.produces(type_response)
    def get(self):
        args = parser_degree.parse_args()
        if args['amount'] == 'all':
            return GenericGet().get_data(args,1,False)
        elif args['amount'] == 'nearest':
            return GenericGet().get_data(args,1,True)
