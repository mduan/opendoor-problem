import csv
import flask
import os
import requests

app = flask.Flask(__name__)

def str_to_int(str_, default):
  return int(str_) if str_ else default

@app.route('/listings', methods=['GET'])
def listings():
  args = flask.request.args

  min_price = str_to_int(args.get('min_price'), float('-inf'))
  max_price = str_to_int(args.get('max_price'), float('inf'))
  min_bed = str_to_int(args.get('min_bed'), float('-inf'))
  max_bed = str_to_int(args.get('max_bed'), float('inf'))
  min_bath = str_to_int(args.get('min_bath'), float('-inf'))
  max_bath = str_to_int(args.get('max_bath'), float('inf'))
  page = str_to_int(args.get('page'), 0)
  results_per_page = str_to_int(args.get('results_per_page'), 100)

  house_listings = []
  start_idx = page * results_per_page
  end_idx = (page + 1) * results_per_page
  for curr_idx, house in enumerate(app.config.houses):
    if curr_idx >= end_idx: # early terminate when we have enough results for current page
      break
    price = house['price']
    num_beds = house['bedrooms']
    num_baths = house['bathrooms']
    if (price >= min_price and price <= max_price and
        num_beds >= min_bed and num_beds <= max_bed and
        num_baths >= min_bath and num_baths <= max_bath and
        curr_idx >= start_idx and curr_idx < end_idx):
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
      print curr_idx

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
  app.debug = True
  app.config.houses = fetch_houses()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
