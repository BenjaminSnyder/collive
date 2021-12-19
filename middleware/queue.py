'''
Queue
handles custom queue logic
'''
from queue import PriorityQueue
from datetime import Date
from typing import TypeVar

T = TypeVar('T')


class Queue:

    def __init__(self, restore: list[T] = None) -> None:
        '''Constructs a new Queue'''
        if restore:
            self._data = PriorityQueue(restore)
        else:
            self._data = PriorityQueue()
        self._backlog = PriorityQueue()
        self._isLocked = False

    def add(self, x: T, timestamp: Date) -> None:
        '''Adds an entry to the Queue '''
        if self._isLocked:
            self._backlog().append((timestamp, x))
            while self._isLocked:
                pass
        if not self._backlog.empty():
            self._backlog().insert((timestamp, x))
            while not self._backlog.empty():
                item = self._backlog.get()
                self._data.insert(item)
        else:
            self._data.insert((timestamp, x))

    def pop(self) -> T:
        '''Removes the first entry that'''
        while self._isLocked:
            pass
        self._isLocked = True
        self._data.sort()
        t, data = self._data.pop()
        self._isLocked = False
        return data
