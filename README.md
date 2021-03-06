# House comparison dashboard
This is a little dashboard to help you look wholisitcally at the houses you're
looking at to help you sort and filter on houses you're looking at on a number
of facets to better understand the market you're shopping in

###  How to use:
1) Create proper conda environment
```
conda create -n dashboard python=3.6 --file=requirements.txt
pip install googlemaps 
``` 
2) Get a google [distancematrix api key](https://developers.google.com/maps/documentation/distance-matrix/) 
and alter 'GDM_KEY' on your 'config.py'

3) Download your redfin favorites into the 'redfin_exports' folder and change 
the associated line in 'update_favorites.py'

4) Run necessary files to build and populate databases with your Redfin information.
```
source activate dashboard
bash initial_db_create.py
bash update_favorites.py
```
5) Serve the dashboard (it should open in your default browser)
```
bokeh serve dashboard --show
```
### Third Party Data Dependencies
* Redfin Favorites export
* Google distancematrix api key 

### License
*This is intended for personal use only and cannot be used for any commercial purposes without prior express consent