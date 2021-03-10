import importlib
import io
import os
import pandas as pd
import numpy as np
from flask import make_response,abort

from astropy.io import ascii
from astropy.io.votable import parse,parse_single_table,from_table, writeto
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from astropy.table import Table, Column

from app.main import resources_freya as rf


class GenericGet():

    def get_catalogs(self):
        dir_resources = rf.__path__[0]
        catalogs = []
        for f in os.listdir(dir_resources):
            if f !='__pycache__' and f !='__init__.py':
                catalogs.append(f.split("_")[0])
        return make_response({'catalogs' : catalogs})

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
                module = f'app.main.resources_freya.{catalog}_resource.resource'
                mod = importlib.import_module(module)
                my_class = getattr(mod, f'Resource{catalog}')
            except:
                continue
            if type_ == 0:
                my_instance = my_class(ra=ra,dec=dec,radius=radius,format='numpy',nearest=get_).get_lc_deg()
            elif type_ == 1:
                my_instance = my_class(hms=hms,radius=radius,format='numpy',nearest=get_).get_lc_hms()

            if first:
                results_ = my_instance
                first = False
            else :
                results_ = np.vstack((results_,my_instance))

        if format == 'csv':
            try:
                df = pd.DataFrame({'obj':results_[:,0],'ra':results_[:,1],
                    'dec':results_[:,2],'mjd':results_[:,3],
                    'mag':results_[:,4],'magerr':results_[:,5],
                    'filter':results_[:,6],'catalog':results_[:,7]})
                buf = io.StringIO()
                df.to_csv(buf,index=False)
                
                # make responde data with headers
                data =  make_response(buf.getvalue())
                data.headers["Content-Disposition"] = "attachment; filename=LightCurveData[{}].csv".format(args_['catalogs'])
                data.headers["Content-type"] = "text/csv"
                return data
            except:
                return make_response('No light curve data find in catalog(s)')
        elif format == 'votable':
            try:
                names_column = ['obj','ra','dec','mjd','mag','magerr','filter','catalog']
                descriptions_column = ['Id of object in catalog the original catalog',
                                        'Right ascension','Declination',
                                        'Julian Day','Magnitude','Magnitude Error',
                                        'Filter code','Original Catalog']

                table_ = Table(rows=results_,names=names_column,descriptions=descriptions_column)                             
                votable= VOTableFile.from_table(table_)
                buf = io.BytesIO()
                writeto(votable,buf)
                
                # make responde data with headers
                data = make_response(buf.getvalue().decode("utf-8"))
                data.headers["Content-Disposition"] = "attachment; filename=LightCurveData[{}].xml".format(args_['catalogs'])
                data.headers["Content-type"] = "text/xml"
                return data
            except:
                return make_response('No light curve data find in catalog(s)')