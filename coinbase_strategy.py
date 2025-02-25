import logging, uuid, os
from dotenv import load_dotenv
from coinbase.rest import RESTClient
from exchange_strategy import ExchangeStrategy


class CoinbaseStrategy(ExchangeStrategy):
    def __init__(self):
        COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
        COINBASE_API_SECRET = os.getenv('COINBASE_API_SECRET')
        self.client = RESTClient(api_key=COINBASE_API_KEY, api_secret=COINBASE_API_SECRET, verbose=False)

    def get_wallets(self):
        """Fetch wallet information from Coinbase."""
        wallets = self.client.get_accounts()
        return wallets['accounts']

    def buy(self, symbol, amount):
        """Execute a buy order on Coinbase."""
        order_id = str(uuid.uuid4())

        order = self.client.market_order_buy(
            client_order_id=order_id,
            product_id=symbol,
            quote_size=str(amount))
        return order

    def sell(self, symbol, quantity):
        """Execute a sell order on Coinbase."""
        order_id = str(uuid.uuid4())

        order = self.client.market_order_sell(
            client_order_id=order_id,
            product_id=symbol,
            base_size=str(quantity))
        return order