import asyncio
import multiprocessing

import janus

from .config import Config
from .states import State


class Joseph(object):
    """Joseph's heart and soul"""

    def __init__(self, loop=None):
        super(Joseph, self).__init__()

        self.config = Config()
        self.loop = loop or asyncio.get_event_loop()
        self.state = State('STOPPED')
        self.workers = []

        self.queue = janus.PriorityQueue(loop=self.loop)

    def start(self) -> None:
        """ Starts up the application by registering the async start procedure """
        self.add_task(self._stop_procedure)

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        """ Add stop task to queue """
        self.add_task(self._stop_procedure)

    async def _start_procedure(self) -> None:
        """ Performs the actual start up procedure """
        self.state.set_state('STARTING')

        self.add_task(self.config.from_file, 'config.py')
        for _ in self.config['WORKER_COUNT'] or multiprocessing.cpu_count():
            worker = self.loop.run_in_executor(None, self.worker, self.queue)
            self.workers.append(worker)

        self.state.set_state('RUNNING')

    async def _stop_procedure(self) -> None:
        """ Performs the stopping procedure """
        self.state.set_state('STOPPING')

        for worker in self.workers:
            worker.cancel()

        self.loop.stop()
        self.state.set_state('STOPPED')

    async def add_task(self, task: callable, *args, **kwargs) -> None:
        """ Add any coroutine to the queue to be executed later """
        try:
            priority = kwargs.pop('priority')
        except KeyError:
            priority = 9

        future = asyncio.ensure_future(task(*args, **kwargs))
        await self.queue.put((priority, future))

    async def worker(self) -> None:
        """ Worker to pull futures from the queue and run them """
        while True:
            future = await self.queue.get()
            result = await future
            future.set_result(result)
