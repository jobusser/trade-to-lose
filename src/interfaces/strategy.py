from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def on_data(self, data):
        """Callback method to receive data from a DataProvider."""
        pass
    
    @abstractmethod
    def decide_trade(self):
        """Decide whether to trade based on received data."""
        pass
