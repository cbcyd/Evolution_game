import pytest
from evolution.services.event_bus import EventBus
from evolution.core.events import Event, CellDiedEvent
from evolution.core.cell import Cell
from evolution.behaviors.strategies import random_walk_strategy

class MockSubscriber:
    def __init__(self):
        self.called = False
        self.event = None

    def __call__(self, event: Event):
        self.called = True
        self.event = event

def test_event_bus_subscribe_and_publish():
    event_bus = EventBus()
    subscriber = MockSubscriber()

    event_bus.subscribe(CellDiedEvent, subscriber)

    cell = Cell(energy=0, x=0, y=0, strategy=random_walk_strategy, genome=None)
    event = CellDiedEvent(cell=cell)

    event_bus.publish(event)

    assert subscriber.called
    assert subscriber.event is event
