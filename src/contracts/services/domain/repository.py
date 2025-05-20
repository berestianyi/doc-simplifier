from abc import ABC, abstractmethod

class ContractRepositoryInterface(ABC):
    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_by_id(self, contract_id: int):
        pass

    @abstractmethod
    def list(self):
        pass