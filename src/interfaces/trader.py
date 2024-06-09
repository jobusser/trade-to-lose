from abc import ABC, abstractmethod

from strategy import Strategy

class Trader(ABC):
    @abstractmethod
    def __init__(self, strategy: Strategy, data_providers: list):
        """Initialize the Trader with a strategy and a list of data providers."""
        pass
    
    @abstractmethod
    def subscribe_strategy_to_providers(self):
        """Subscribe the strategy to all data providers."""
        pass
    
    @abstractmethod
    def execute_trade(self, trade_decision):
        """Execute a trade based on the strategy's decision."""
        pass
