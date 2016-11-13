import asyncio

from .config import Config


class Joseph(object):
    """Joseph's heart and soul"""

    def __init__(self, loop: asyncio.BaseEventLoop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.config = Config()

    def start(self) -> None:
        self.loop.create_task(self._start_procedure())

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.create_task(self._stop_procedure())
            self.loop.run_forever()
        finally:
            self.loop.close()

    async def _start_procedure(self) -> None:
        # TODO: Implement startup procedure
        self.loop.create_task(self.config.from_file())

    async def _stop_procedure(self) -> None:
        # TODO: Implement stop procedure
        self.loop.stop()
