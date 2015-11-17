import csv
import flask
import os
import requests

app = flask.Flask(__name__)

@app.route('/listings', methods=['GET'])
def listings():
  args = flask.request.args
  min_price = int(args.get('min_price')) or float('-inf')
  max_price = int(args.get('max_price')) or float('inf')
  min_bed = int(args.get('min_bed')) or float('-inf')
  max_bed = int(args.get('max_bed')) or float('inf')
  min_bath = int(args.get('min_bath')) or float('-inf')
  max_bath = int(args.get('max_bath')) or float('inf')

  house_listings = []
  for house in app.config.houses:
    price = house['price']
    num_beds = house['bedrooms']
    num_baths = house['bathrooms']
    if (price >= min_price and price <= max_price and
        num_beds >= min_bed and num_beds <= max_bed and
        num_baths >= min_bath and num_baths <= max_bath):
      house_listings.append({
        'type': 'Feature',
        'geometry': {
          'type': 'Point',
          'coordinates': [house['lng'], house['lat']],
        },
        'properties': {
          'id': house['id'],
          'price': house['price'],
          'street': house['street'],
          'bedroom': house['bedrooms'],
          'bathrooms': house['bathrooms'],
          'sq_ft': house['sq_ft'],
        },
      })

  response = {
    'type': 'FeatureCollection',
    'features': house_listings,
  }

  return flask.jsonify(response)

def fetch_houses():
  resp = requests.get('https://s3.amazonaws.com/opendoor-problems/listings.csv')

  houses = []
  rows = resp.text.split('\n')
  for idx, row in enumerate(rows):
    if not idx or not row: # to skip first header line and the last empty line
      continue
    entries = row.split(',')
    houses.append({
      'id': entries[0],
      'street': entries[1],
      'status': entries[2],
      'price': int(entries[3]),
      'bedrooms': int(entries[4]),
      'bathrooms': int(entries[5]),
      'sq_ft': int(entries[6]),
      'lat': float(entries[7]),
      'lng': float(entries[8]),
    })

  return houses

if __name__ == '__main__':
  app.config.houses = fetch_houses()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
