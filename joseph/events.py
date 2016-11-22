import datetime
import inspect
from typing import Union

from .core import Joseph
from .exceptions import InvalidState
from .utils import State


class Namespace(object):
    def __init__(self, namespace: str = None):
        """ Use the callers filename if no namespace is provided """
        self.namespace = namespace or inspect.stack()[1].filename

    def make_event(self, event: str, **data):
        """ Returns an event on the current namespace """
        return Event(self, event, **data)

    def __hash__(self) -> int:
        """ Returns the hash of the current namespace """
        return hash(str(self))

    def __str__(self) -> str:
        """ Returns the namespace as a string """
        return self.namespace

    def __eq__(self, other) -> bool:
        """ Compare the hashes of self and other """
        return hash(self) == hash(other)

    def __ne__(self, other) -> bool:
        """ Inverses :meth: __eq__ """
        return not self.__eq__(other)


class Event(object):
    """ Represents events """

    def __init__(self, namespace: Namespace, event: str = "", strict: bool = True, **data):
        self.NAMESPACE = namespace
        self.EVENT = event
        self.STRICT = strict

        self.__dict__.update(data)

    def __hash__(self) -> int:
        """ If the strict attribute is true, hash the entire object else only hash the string representation """
        return hash(self.__dict__) if self.STRICT else hash(str(self))

    def __str__(self) -> str:
        """ Always includes namespace and might include event if not empty (format: NAMESPACE:EVENT) """
        return "{}:{}".format(self.NAMESPACE, self.EVENT) if self.EVENT else "{}".format(self.NAMESPACE)

    def __eq__(self, other) -> bool:
        """ If either of the events is strict, compare complete events otherwise only compare the string """
        try:
            return self.__dict__ == other.__dict__ if self.STRICT or other.STRICT else str(self) == str(other)
        except AttributeError:
            return False

    def __ne__(self, other) -> bool:
        """ Inverses :meth: __eq__ """
        return not self.__eq__(other)

    @property
    def data(self):
        """ Returns all attributes that are not a constant """
        return {key: value for key, value in self.__dict__.items() if key.islower()}


class EventBus(dict):
    CLOSED_STATES = (
        None,
        "STOPPING",
        "STOPPED"
    )

    def __init__(self, joseph: Joseph):
        super(EventBus, self).__init__()

        self.joseph = joseph
        self.state = State(None)

    def listen(self, event: Union[Event, str], priority: int = 9, **data) -> callable:
        """
        Wrapper function to register a function to be run when the event has been dispatched anywhere in the program

        The event listening for can be either an event instance or the string representation
        of a the event. The priority can be set as an integer, but it _cannot_ be guaranteed
        a function will be called first
        """
        if not isinstance(event, Event):
            event = make_event_from_string(event, **data)

        def inner(func: callable) -> callable:
            """ The inner wrapper function """
            try:
                self[event].append((priority, func))

                # Make sure the listeners stay in order
                self[event].sort()
            except KeyError:
                self[event] = [(priority, func)]
            return func

        return inner

    def dispatch(self, event: Union[str, Event], **data) -> None:
        """
        Prepares the event for dispatching, the event to be dispatched can be either an event instance
         or a string representation of the event.
        """
        if self.state in self.CLOSED_STATES:
            raise InvalidState(
                "The event bus '{}' is in state {}: dispatching new events is not allowed".format(self.__repr__(),
                                                                                                  self.state))

        if isinstance(event, str):
            event = make_event_from_string(event)

        event.__dict__.update(data)
        event.dispatched_at = datetime.datetime.now()
        self._dispatch(event)

    def _dispatch(self, event) -> None:
        """ Calls the listeners if any and adds them to the main event queue """
        for listener in self.get_listeners(event):
            self.joseph.add_task(listener(event), priority=3)

    def get_listeners(self, event: Event) -> iter:
        """ Yields all listeners for provided event, empty iterable if none are listening """
        try:
            for listener in self[event]:
                yield listener
        except KeyError:
            return iter([])

    def stop_soon(self) -> None:
        """ Closes the event bus for new dispatches """
        self.state.set_state("STOPPING")


def make_event_from_string(event, **data) -> Event:
    """ Turns a string event representation into an event instance """
    namespace, event = event.split(":")
    namespace = Namespace(namespace)

    return namespace.make_event(event, **data)
