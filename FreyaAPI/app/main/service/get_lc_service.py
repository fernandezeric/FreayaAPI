import importlib
import io
import os
import pandas as pd
import numpy as np
from flask import make_response,abort
from app.main import resources_freya as rf
from Freya_alerce.catalogs.core.format_lc import FormatLC


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
                # format return
                format_ = FormatLC(results_).format_csv()
                # make responde with headers
                data =  make_response(format_)
                data.headers["Content-Disposition"] = "attachment; filename=LightCurveData[{}].csv".format(args_['catalogs'])
                data.headers["Content-type"] = "text/csv"
                return data
            except:
               return make_response('No light curve data find in catalog(s)')
        elif format == 'votable':
            try:
                # format return
                format_ = FormatLC(results_).format_votable()
                # make responde with headers
                data = make_response(format_)
                data.headers["Content-Disposition"] = "attachment; filename=LightCurveData[{}].xml".format(args_['catalogs'])
                data.headers["Content-type"] = "text/xml"
                return data
            except:
                return make_response('No light curve data find in catalog(s)')