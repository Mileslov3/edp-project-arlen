"""Local event queue + simple publish/subscribe dispatcher."""
from collections import defaultdict, deque

from .events import Event

WILDCARD = "*"  # handler subscribed to "*" receives every event


class EventQueue:
    def __init__(self):
        self._queue = deque()                    # FIFO queue of events
        self._subscribers = defaultdict(list)    # event type -> [handlers]

    def subscribe(self, event_type, handler):
        self._subscribers[event_type].append(handler)

    def publish(self, event_type, payload=None):
        """Producers and handlers call this to put a new event in the queue."""
        event = Event(event_type, payload or {})
        self._queue.append(event)
        return event

    def run(self):
        """Process events until the queue is empty.
        Handlers may publish new events - they are processed in the same loop."""
        processed = 0
        while self._queue:
            event = self._queue.popleft()
            handlers = self._subscribers[WILDCARD] + self._subscribers[event.type]
            for handler in handlers:
                handler(event)
            processed += 1
        return processed
