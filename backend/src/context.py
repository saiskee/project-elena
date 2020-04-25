class Context:
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy):
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._strategy = strategy

    @property
    def strategy(self):
        """
        The Context reference to one of the Strategy objects.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        """
        Set the strategy (route type).
        """

        self._strategy = strategy

    def run_strategy_route(self, start, goal, weight='length') -> None:
        """
        Call the routing implementation of the specific concrete strategy.
        """
        result = self._strategy.get_route(start, goal)
        return result

