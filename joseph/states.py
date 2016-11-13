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

    def __init__(self, state: [int, str, None] = None):
        self.state = None
        self.set_state(state)

    def set_state(self, state: [int, str, None]):
        """ Update the state """
        try:
            self.state = self.STATES[state]
        except TypeError:
            self.state = self.STATES[self.STATES.index(str)]

    def increase_state(self):
        """ Update the state to next state """
        self.set_state(self.current_index + 1)

    def decrease_state(self):
        """ Update the state to the previous state """
        self.set_state(self.current_index - 1)

    @property
    def current_index(self):
        return self.STATES.index(self.state)

    def __str__(self):
        return self.state
