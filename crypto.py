from flask import Flask, render_template
import ccxt
import pandas as pd

app = Flask(__name__)

ccxt.exchanges

#kraken = ccxt.kraken()
#print(kraken.fetchOHLCV('BTC/USDT', limit=10))
#pd.DataFrame(binanceus.fetchOHLCV('BTC/USDT',limit=10))

def getprices(exchange, symbol):
    inst = getattr(ccxt, exchange)()
    df = pd.DataFrame(inst.fetchOHLCV(symbol, limit=3))
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df.set_index('Time', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.astype(float)
    return df   
  
price = getprices('coinbasepro', 'BTC/USDT')
print(price)
 
@app.route('/')   
def home():
    prices_binance = getprices('binanceus', 'BTC/USDT')
    prices_coinbase = getprices('coinbasepro', 'BTC/USDT')
    prices_kraken = getprices('kraken', 'BTC/USDT')
    return render_template('index.html', 
                            tables_binance=[prices_binance.to_html(classes='data')], titles_binance=prices_binance.columns.values,
                            tables_coinbase=[prices_coinbase.to_html(classes='data')], titles_coinbase=prices_coinbase.columns.values,
                            tables_kraken=[prices_kraken.to_html(classes='data')], titles_kraken=prices_kraken.columns.values)

if __name__ == '__main__':
    app.run(debug=True)



#Kraken, Coinbase(pro), BinanceUS
#3.1.4
