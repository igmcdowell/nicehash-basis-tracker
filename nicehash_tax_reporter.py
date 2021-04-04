from db_lib import get_db_connection, show_beg_splash

def run_report(conn, year):
  query = """
    SELECT amount, btc_usd, amount_usd, fee_usd, datetime(timestamp/1000,'unixepoch') as converted_time 
    FROM payouts 
    WHERE converted_time > datetime('%s-01-01') and converted_time < datetime('%s-01-01', '1 year')
  """ % (year, year)
  results = conn.cursor().execute(query).fetchall()
  total_mined = 0
  total_fees = 0
  conversion_rate = 0
  btc_earned = 0
  for result in results:
    total_mined += result[2]
    total_fees += result[3]
    btc_earned += result[0]
    conversion_rate += result[0] * result[1]

  print("Total mined: $%s" % round(total_mined, 2))
  print("Total Nicehash fees: $%s" % round(total_fees, 2))
  print("Total cost basis: $%s" % round(total_mined - total_fees, 2))
  print("Average BTC-USD rate: $%s" % round(conversion_rate / btc_earned, 2))

if __name__ == "__main__":
  show_beg_splash()
  year = input("Enter the 4 digit year to run report for. Example: 2021\n")
  conn = get_db_connection()
  run_report(conn, year)
  exit(0)
