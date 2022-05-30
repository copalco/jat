class EventSourcedConnectionRepository:

    def __init__(self, event_store) -> None:
        self._event_store = event_store
