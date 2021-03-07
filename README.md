# FreyaAPI Start (). 🚀
FreyaAPI's GitHub, need install Freya-alerce, look this github for more information [Freya](https://github.com/fernandezeric/Memoria), inside can find a Demo.

# New FreyaAPI
Quick creation FreyaAPI used Freya's admin (freya-admin):
```
# In any directory in your system type
freya-admin --newapi

```
In folder where is called create new flask application, it's contains the
necessary routes generic that you only call and not modified, but first you need
add resources(catalogs) with :

```
# Next need install the all modules to need for run FreyaAPI, run this command:
pip install -r requirements.txt

# Then inside folder FreyaAPI install the resource of Freya.

freya-admin --addresource ztf
freya-admin --addresource <name_resource>

```

Finally run API with the manager included.
```
python manage.py run # run FreyaAPI
python manage.py test # run test
```

## Install with Docker (optional) 🔧
When you use the command "freya-admin --newapi", you have inside in the new folder a
dockerfile. Now can install like :

```
sudo docker build -t freyapi .
sudo docker run --name df-freyapi -d -p 5000:5000 freyapi
```

## How use the rute FreyaAPI 📖
The rutes in FreyaAPI are get methods and have four rutes.
```
 # Get light curves of objects with area in degrees.
 args : - catalogs: string
        - ra: float (degrees) 
        - dec: float (degrees)
        - radius: float (arcsec)
        - format: csv,votable
        - amount: all,nearest
 Example:
  http://localhost/get_data/lc_degree?catalogs&ra&dec&radius&format&amount
 
 Example:
  http://localhost/get_data/lc_degree?catalogs&ra&dec&radius&format&amount   
```
```
 # Get light curves of objects with area in hh:mm:ss.
 args : - catalogs: string
        - hms: string
        - radius: float (arcsec)
        - format: csv,votable
        - amount: all,nearest
 Example:
    http://localhost/get_data/lc_hms?catalogs=ztf&hms&radius&format&amount
 
 Example:
   http://localhost/get_data/lc_hms_nearest?catalogs&hms&radius&format&amount 
```