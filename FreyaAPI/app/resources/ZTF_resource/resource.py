import sys
import importlib
from Freya_alerce.catalogs.core.data_lc import DataLcDegree,DataLcHms
class ResourceZTF():
    """
    Parameters
    ----------
    ra : (float) Right ascension
    dec :  (float) Declination
    hms : (string) HH:MM:SS
    radius: (float) Search radius
    format: (string) csv or votable
    nearest : (bool) selected the object most close to point
    """
    def __init__(self,**kwagrs):
        self.ra = kwagrs.get('ra')
        self.dec = kwagrs.get('dec')
        self.hms = kwagrs.get('hms')
        self.radius = kwagrs.get('radius')
        self.format = kwagrs.get('format')
        self.nearest = kwagrs.get('nearest')
 
    """
    Get light curves data from astronomical objects called Freya’s for specific catalog, using degree area.  
    """       
    def get_lc_deg(self):
        data_method = DataLcDegree(catalog='ZTF',ra=self.ra,dec=self.dec,radius=self.radius,format=self.format,nearest=self.nearest).get_data()
        return data_method

    """
    Get the all light curves data from astronomical objects called Freya’s for specific catalog, using hh:mm:ss(ICRS) area.  
    """
    def get_lc_hms(self):
        data_method = DataLcHms(catalog='ZTF',hms=self.hms,radius=self.radius,format=self.format,nearest=self.nearest).get_data()
        return data_method
