# Nicehash Mining Income/Cost Basis Tracker

## What is this?
Run this script to calculate the cost basis of all crypto mined on Nicehash for the past year (in USD). It uses hourly historical data to get as close as possible, based on the BTC->USD prices according to CryptoDataDownload.

Your data is stored in a sqlite database. You can run your own queries on it, or use the query script in this repo for basic data.

## How do I use this?
You need to generate an API key from Nicehash to use this software. You'll also need to set up Python 3. Once you've set things up just run the following to import all your data:
`python3 nicehash_basis_tracker.py`

When you're ready for an annual report, run
`python3 nicehash_tax_reporter.py`

### How do I install Python?
https://www.python.org/downloads/

### Nicehash API key
Follow the instructions on https://www.nicehash.com/docs/ for getting an API key. Be sure to generate for the PRODUCTION environment.
IMPORTANT: Make sure when generating the key to only provide the permission:
| VBTD - Wallet / View balances transactions and deposit addresses (VBTD)

This script only uses a single API endpoint, and the only thing that API does is read your balance. If you limit your key in this way you don't have to worry about someone stealing your coins, and you don't have to trust this script.

This repo contains a file '.env.example'. You should rename it to '.env.secret', then paste your key and secret into the appropriate lines. You will also need to add your nicehash org id, which is located right above the "Create new API key" button.

## Background/Why this?

Per US tax law, when mining cryptocoins you recognize income equal to the *current* market value of the mined coins as soon as you take possession of them.

I'm no tax professional, but as I understand it, this would be when Nicehash deposits the coin in your Nicehash wallet, since that is the moment you have control of the currency/could transfer it out.

Hourly price data is the best I can find for free.

## Disclaimer
I'm not a tax professional, I do not provide tax advice. Everything in this repo is for informational purposes and should not be considered an individualized recommendation or advice.
If you have any questions, you should talk to a tax professional. 
If you plan on using this script, you should talk to a tax professional. 
If you do anything at all with crypto, you should probably talk to a tax professional.

Further, I've provided this software as-is with no warranty or claim of correctness. Use at your own risk/check the math so you don't go to jail for tax things.
