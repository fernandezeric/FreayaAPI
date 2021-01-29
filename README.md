# FreyaAPI Start (). 🚀
FreyaAPI's GitHub, need install Freya-alerce, look this github for more information [Freya](https://github.com/fernandezeric/Memoria)

# New FreyaAPI
Quick creation FreyaAPI used Freya's admin (freya-admin):
```
# In any directory in your system
freya-admin --newapi

```
In folder where is called create new flask application, it's contains the
necessary routes generic that you only call and not modified, but first you need
add resources(catalogs) with :

```
# Inside folder FreyaAPI

freya-admin --addresource ztf
freya-admin --addresource ztf_local

```
The catalogs add with --addresource need first add into Freya or module. 

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
  http://localhost/get_data/lc_degree?catalogs=ztf&ra=139.33444972&dec=68.6350604&radius=0.0002777&format=csv&amount=all
 
 Example:
  http://localhost/get_data/lc_degree?catalogs=ztf&ra=139.33444972&dec=68.6350604&radius=0.0002777&format=votable&amount=nearest   
```
```
 # Get light curves of objects with area in hh:mm:ss.
 args : - catalogs: string
        - hms: string
        - radius: float (arcsec)
        - format: csv,votable
        - amount: all,nearest
 Example:
    http://localhost/get_data/lc_hms?catalogs=ztf&hms=%279h17m20.26793280000689s%20+4h34m32.414496000003936s%27&radius=0.0002777&format=csv&amount=all
 
 Example:
   http://localhost/get_data/lc_hms_nearest?catalogs=ztf&hms=%279h17m20.26793280000689s%20+4h34m32.414496000003936s%27&radius=0.0002777&format=votable&amount=nearest 
```