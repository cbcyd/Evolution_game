import logging
from collections import defaultdict
from typing import Callable, List, Type
import weakref

from evolution.core.events import Event

class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(weakref.WeakSet)

    def subscribe(self, event_type: Type[Event], callback: Callable):
        self._subscribers[event_type].add(callback)
        logging.info(f"Subscribed {callback} to {event_type}")

    def publish(self, event: Event):
        event_type = type(event)
        if event_type in self._subscribers:
            # We need to iterate over a copy, as the weakset might change
            # during iteration if a subscriber is garbage collected.
            for callback in list(self._subscribers[event_type]):
                try:
                    callback(event)
                except Exception as e:
                    logging.error(f"Error in event callback {callback}: {e}")
