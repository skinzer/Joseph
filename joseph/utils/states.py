from typing import Union

from joseph.exceptions import InvalidState


class State(object):
    """
    Keeps track of the state of any given object

    Increasing or decreasing the state of an object, while there are no
    more states left will deliberately raise an Index error
    """
    STATES = (
        None,
        'STARTING',
        'RUNNING',
        'STOPPING',
        'STOPPED'
    )

    def __init__(self, state: Union[int, str, None] = None, states: iter = None):
        self.state = None
        self.set_state(state)

        if states:
            self.STATES = tuple([None, ])
            for state in states:
                self.add_state(state)

    def set_state(self, state: Union[int, str, None]) -> None:
        """ Update the state """
        try:
            if isinstance(state, int):
                self.state = self.STATES[state]
            else:
                self.state = self.STATES[self.STATES.index(state)]
        except (ValueError, IndexError):
            raise InvalidState("State {} is not in the available states: {}".format(state, self.STATES.__repr__()))

    def add_state(self, state) -> None:
        """ While probably not needed, a state can be added at runtime """
        self.STATES += tuple([state, ])

    def increase_state(self) -> None:
        """ Update the state to next state """
        self.set_state(self.current_index + 1)

    def decrease_state(self) -> None:
        """ Update the state to the previous state """
        self.set_state(self.current_index - 1)

    @property
    def current_index(self) -> int:
        """ Returns the index of the current state in the states tuple """
        return self.STATES.index(self.state)

    def __str__(self) -> str:
        """ Returns the current state, empty string if no state has been set yet """
        return self.state if isinstance(self.state, str) else ""

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            result = str(self) == other
        elif isinstance(other, State):
            result = self.state == other.state
        else:
            result = self.state == other

        return result

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
