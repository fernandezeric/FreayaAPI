from flask import request
from flask_restplus import Resource

from ..util.dto import Base
from ..service.user_service import GenericGet

api = Base.api
_gdata = Base

link_ = '\n https://github.com/fernandezeric/Memoria#catalogs-default-'

parser = api.parser()
parser.add_argument('catalogs', type=str, required=True, default='ztf,ps1',
                    help='Names of the catalogs to consult , first need the catalogs are in Freya.\
                    Look catalogs and what return in '+link_, location='args')
parser.add_argument('format', type=str, required=True, default='csv',choices=['csv','votable'],
                    help='format data', location='args')
parser.add_argument('amount', type=str, required=True, default='all',choices=['all','nearest'],
                    help='get all or only one light curve data per catalog', location='args')
parser.add_argument('radius', type=float, required=True, default=0.0002777, 
                    help='Search radius', location='args')

parser_degree = parser.copy()
parser_degree.add_argument('ra', type=float, required=True, default=139.33444972, 
                            help='(degrees) Right Ascension', location='args')
parser_degree.add_argument('dec', type=float, required=True,default=68.6350604, 
                            help='(degrees) Declination', location='args')

parser_hms = parser.copy()
parser_hms.add_argument('hms', type=str, required=True, default='9h17m20.26793280000689s +4h34m32.414496000003936s', 
                        help='hh:mm:ss', location='args')

type_response = ["text/csv","text/xml"]


@api.route('/')
class GetCatalogs(Resource):

    def get(self):
        """ Get Catalogs available in FreyaAPI"""
        return GenericGet().get_catalogs()


@api.route('/lc_degree')
class GetLcDegree(Resource):
    @api.expect(parser_degree)
    @api.produces(type_response)
    def get(self):
        """ Get light curve in area using center point in degree"""
        args = parser_degree.parse_args()
        if args['amount'] == 'all':
            return GenericGet().get_data(args,0,False)
        elif args['amount'] == 'nearest':
            return GenericGet().get_data(args,0,True)

@api.route('/lc_hms')
class GetLcHms(Resource):
    @api.expect(parser_hms)
    @api.produces(type_response)
    def get(self):
        """ Get light curve in area using center point in hms(ICRS)"""
        args = parser_hms.parse_args()
        if args['amount'] == 'all':
            return GenericGet().get_data(args,1,False)
        elif args['amount'] == 'nearest':
            return GenericGet().get_data(args,1,True)