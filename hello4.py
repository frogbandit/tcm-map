from flask import Flask, render_template, request
from sqlalchemy import *
import simplejson as json
import collections
import requests

import os 
import psycopg2
import urlparse


app = Flask(__name__)

# @app.route('/', methods = ['POST'])
# def getPersonById():
#     personId = int(request.form['personId'])
#     return personId

@app.route("/")
# def search():
# 	return render_template("form.html")

# @app.route("/search", methods=["GET", "POST"])
def hello():

	db = create_engine('postgresql://postgres:cloudminer@localhost:5432/postgres')
	metadata = MetaData(db)
	# users = Table('map_resources_table', metadata, autoload=True)
	users = Table('map_resources_table', metadata, autoload=True)
	s = users.select(not_(users.c.latitude == 0))

	rs = s.execute()
	rows = rs.fetchmany(8000)

	rowarray_list = []

	# filename = request.form["commodity"]
	count = 0
	for row in rows:

		# if filename in row1.commodity_name:
			geometry = {'coordinates': [row.longitude, row.latitude], 'type': "Point"}
			properties = {}
			t = {'type': "Feature", 'id': row.project_name, 'geometry': geometry, 'geometry_name': row.project_name, 'properties': properties, 'commodity': row.commodity_name, 'country_code': row.country_code}
		# for row2 in rows:

		# 	if (row1.latitude == row2.latitude) and (row1.longitude == row2.longitude):
		# 		count = count + 1

		# t = {'lon': row1.longitude, 'lat': row1.latitude, 'project': row1.project_name, 'number': row1.id}
			rowarray_list.append(t)
			count = 0



   	j = json.dumps(rowarray_list,  use_decimal=True, sort_keys = True)
   	print j[-1000:-1]
   	j = '{"type": "FeatureCollection", "features":' + j + ', "crs":{"type":"EPSG","properties":{"code":"4326"}},"bbox":[90.0, -180.0, -90.0, 180.0]}'
   	f = open('static/data/data.json', 'w+')
   	f.write(j)
   	f.close()

	return render_template("HexbinLeaflet6.html")


if __name__ == "__main__":
    app.run(debug=True)
