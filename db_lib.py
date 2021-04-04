import sqlite3

def get_db_connection():
  conn = sqlite3.connect('nicehash_tax_tracking.db')
  conn.cursor().execute('CREATE TABLE IF NOT EXISTS payouts (timestamp INTEGER PRIMARY KEY, amount REAL, fee REAL, btc_usd REAL, amount_usd REAL, fee_usd REAL)')
  return conn

def show_beg_splash():
  print("Thanks for using my basis tracker. Any/all support is appreciated!")
  print("USDT: 0x5cc6999C86432Cc8dA11B5ba4aB019356a706E62")
  print("ETH:  0xE6872572502527846EF5F2e11327D5c0169b0064")
  print("BTC:  34Xje9XuKJp2tQ8ZUEvZUoLn9Z2KW6zFgd")
  print("BCH:  qr2w4wxpsw6g00ahh6r4ep020s7dw0cnru5sswja4w")
  print("LTC:  MGSHLiUCUTWXHUavu8rQRAFdo5AceRvwBP")
  print("ZEC:  t1TEgKct33is6NyeheDbgz8bpqGzHKgsziE")
