from abc import ABC, abstractmethod

class DataProvider(ABC):
    @abstractmethod
    def provide_data(self):
        """
        Callback method to provide data to Strategy.
        """
        pass

   
