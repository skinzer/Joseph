import asyncio

from .config import Config
from .entities.types import ApplicationEntity
from .states import State


class Joseph(ApplicationEntity):
    """Joseph's heart and soul"""

    def __init__(self, loop: asyncio.BaseEventLoop=None):
        super(Joseph, self).__init__()

        self.config = Config()
        self.loop = loop or asyncio.get_event_loop()
        self.state = State('STOPPED')

    def start(self) -> None:
        """ Starts up the application by registering the async start procedure """
        self.loop.create_task(self._start_procedure())

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.create_task(self._stop_procedure())
            self.loop.run_forever()
        finally:
            self.loop.close()

    async def _start_procedure(self) -> None:
        """ Performs the actual start up procedure """
        # TODO: Implement startup procedure
        self.state.set_state('STARTING')

        self.loop.create_task(self.config.from_file())
        self.state.set_state('RUNNING')

    async def _stop_procedure(self) -> None:
        """ Performs the stopping procedure """
        # TODO: Implement stop procedure
        self.state.set_state('STOPPING')

        self.loop.stop()
        self.state.set_state('STOPPED')
