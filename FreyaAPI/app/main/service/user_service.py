import importlib
import io
import os
from flask import make_response,abort

from astropy.io import ascii
from astropy.table import Table,vstack
from astropy.io.votable import parse,parse_single_table, writeto

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