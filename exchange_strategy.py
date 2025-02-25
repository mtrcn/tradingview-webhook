from abc import ABC, abstractmethod

class ExchangeStrategy(ABC):
    @abstractmethod
    def get_wallets(self):
        """Fetch wallet information for the exchange."""
        pass

    @abstractmethod
    def buy(self, symbol, amount, order_id):
        """Execute a buy order on the exchange."""
        pass

    @abstractmethod
    def sell(self, symbol, quantity, order_id):
        """Execute a sell order on the exchange."""
        pass