from exchange_strategy import ExchangeStrategy

class TradingContext:
    def __init__(self, strategy: ExchangeStrategy):
        self._strategy = strategy

    def get_wallets(self):
        """Fetch wallet information using the selected strategy."""
        return self._strategy.get_wallets()

    def buy(self, symbol, amount):
        """Execute a buy order using the selected strategy."""
        return self._strategy.buy(symbol, amount)

    def sell(self, symbol, quantity):
        """Execute a sell order using the selected strategy."""
        return self._strategy.sell(symbol, quantity)