from abc import ABC, abstractmethod


class RoutingStrategy(ABC):
    """
    The RoutingStrategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """
    def __init__(self, flat_graph, projected_graph, g_nodes):
        self._flat_graph = flat_graph
        self._projected_graph = projected_graph
        self._g_nodes = g_nodes

    @abstractmethod
    def get_route(self, start, goal):
        pass

    # Not implemented by all child classes
    # @abstractmethod
    # def backtrack(self):
    #     pass


