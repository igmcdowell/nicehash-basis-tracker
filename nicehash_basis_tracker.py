from dotenv import dotenv_values
from nicehash_api import private_api
from datetime import datetime
import time
from db_lib import get_db_connection, show_beg_splash
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECONDS_PER_HOUR = 60 * 60
config = dotenv_values(".env.secret")

def write_data(conn, data):
  # expects data in the format [(item1_time, item1_amount, item1_fee, item1_rate), (item2_time, item2_amount, item2_fee, item2_rate),...]
  if len(data) > 0:
    print("Writing %s new data points" % len(data))
  else:
    print("No new data to record. Please run again tomorrow when new hourly data is available")
    return
  values = [(*item, item[1] * item[3], item[2] * item[3]) for item in data]
  conn.cursor().executemany('REPLACE INTO payouts (timestamp, amount, fee, btc_usd, amount_usd, fee_usd) VALUES (?, ?, ?, ?, ?, ?);', values)
  conn.commit()

def get_payouts():
  try:
    api = private_api(
      'https://api2.nicehash.com', 
      config['NICEHASH_ORG_ID'], 
      config['NICEHASH_API_KEY'], 
      config['NICEHASH_API_SECRET']
    )
    return api.get_payouts()['list']
  except Exception as ex:
    print("Unexpected error:", ex)
    exit(1)

def get_price_data(timestamped_payouts):
  # Note: We use CryptoCompare for hourly data. Our timestamps are in milliseconds, but CryptoCompare requires seconds.
  # Also, the closest hour might be the previous hour, so we subtract an hour from our timestamp.
  earliest_ts_s = int(timestamped_payouts[0][0] / 1000) - SECONDS_PER_HOUR
  # we will fetch backward from latest timestamp. Add an hour to ensure we include the hour following our last timestamp
  latest_ts_s = int(timestamped_payouts[-1][0] / 1000) + SECONDS_PER_HOUR
  # calculate the spread in hours. This is the number of entries we will need from CryptoCompare
  num_hours = int((latest_ts_s - earliest_ts_s) / SECONDS_PER_HOUR)

  # Note: cryptodatadownload doesn't send the full cert chain, which causes requests to barf trying to validate.
  # We skip verification, which is safe as we're sending no user data, and only ever reading the response as text.
  data_csv = requests.get('https://www.cryptodatadownload.com/cdd/Bitstamp_BTCUSD_1h.csv', verify=False).content
  # Note: this could be more performant by using iter_lines, but the code would be clunkier, and it's just not that much data
  csv_lines = str(data_csv).split('\\n')
  # Skip over the first two records
  line_idx = 2
  price_data = []
  # Create an array of (timestamp, prices). The CSV comes in latest -> earliest format
  while line_idx < len(csv_lines):
    line = csv_lines[line_idx].split(',')
    if int(line[0]) < earliest_ts_s:
      # exit early once we pass our earliest timestamp
      break
    price_data.append((int(line[0]), float(line[4])))
    line_idx += 1

  # Reverse our data to be earliest -> latest, to match the order of payouts.
  price_data.reverse()
  return price_data

def record_cost_basis():  
  conn = get_db_connection()
  last_timestamp = conn.cursor().execute("select Max(timestamp) from payouts").fetchone()[0] or 0
  payouts = get_payouts()
  timestamped_payouts = sorted([
    (int(payout['created']), float(payout['amount']), float(payout['feeAmount'])) 
    for payout in payouts
    if int(payout['created']) > last_timestamp
  ])
  if len(timestamped_payouts) == 0:
    return

  prices = get_price_data(timestamped_payouts)
  prices_idx = 0
  data = []
  for payout in timestamped_payouts:
    while prices_idx < len(prices) and abs(prices[prices_idx][0] - payout[0]/1000) > (SECONDS_PER_HOUR / 2):
      # Find the closest hourly price. Our timestamp will always be within 30 minutes of either the previous or next hour.
      prices_idx += 1
    if prices_idx < len(prices):
      data.append((*payout, prices[prices_idx][1]))
    else:
      print("Note: hourly data not yet available for %s " % datetime.fromtimestamp(int(payout[0]/1000)))
  write_data(conn, data)

if __name__ == "__main__":
  print("Loading data now!")
  show_beg_splash()
  record_cost_basis()
  exit(0)
