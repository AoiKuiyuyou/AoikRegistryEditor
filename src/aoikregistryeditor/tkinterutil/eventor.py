# coding: utf-8
#
from __future__ import absolute_import


#
class Event(object):
    """
    Event object that contains event info. These attributes are available:
    - event: Event name.
    - arg: Event argument.
    - notifier: Event notifier.
    """

    def __init__(
        self,
        event,
        arg=None,
        notifier=None,
    ):
        """
        Initialize object.

        @param event: Event name.

        @param arg: Event argument.

        @param notifier: Event notifier.

        @return: None.
        """
        # Event name
        self.event = event

        # Event argument
        self.arg = arg

        # Event notifier
        self.notifier = notifier


#
class _EventHandlerWrapper(object):
    """
    Event handler wrapper that calls original event handler with or without
    event argument, according to `need_arg` value.
    """

    def __init__(self, handler, need_arg):
        """
        Initialize object.

        @param handler: Original event handler.

        @param need_arg: Whether original event handler needs event argument.

        @return: None.
        """
        # Original event handler
        self.handler = handler

        # Whether original event handler needs event argument
        self._need_arg = need_arg

    def __eq__(self, other):
        """
        Equality operator.

        @param other: The other object.

        @return: True if wrapped handlers are equal, otherwise False.
        """
        # If the other object is not of the same type
        if not isinstance(other, self.__class__):
            # Return False
            return False

        # If the other object is of the same type
        else:
            # Test whether wrapped handlers are equal
            return self.handler == other.handler

    def __call__(self, arg):
        """
        Event handler function.

        @param arg: Event argument.

        @return: Original event handler's result.
        """
        # If original event handler needs event argument
        if self._need_arg:
            # Call original event handler with argument.
            # Return call result.
            return self.handler(arg)

        # If original event handler not needs event argument
        else:
            # Call original event handler without argument.
            # Return call result.
            return self.handler()


#
class Eventor(object):
    """
    Eventor provides methods for registering event handlers and notifying them
    of events.
    """

    def __init__(self):
        """
        Initialize object.

        @return: None.
        """
        # Create event handlers dict.
        # Key is event name.
        # Value is a list of handlers for the event.
        self._event_handlers = {}

    def handler_add(self, event, handler, need_arg=False):
        """
        Add event handler for an event.

        @param event: Event name. `None` means every event.

        @param handler: Event handler.

        @param need_arg: Whether the event handler needs event argument.

        @return: None.
        """
        # Create event handler wrapper
        handler_wrapper = _EventHandlerWrapper(handler, need_arg=need_arg)

        # If handlers list for the event has not been created
        if event not in self._event_handlers:
            # Create handlers list for the event.
            # Add the handler wrapper to the handlers list.
            self._event_handlers[event] = [handler_wrapper]

        # If handlers list for the event has been created
        else:
            # If the handler wrapper has been added before
            if handler_wrapper in self._event_handlers[event]:
                # Get error message
                msg = """Handler `{}` has already been added for event\
 `{}`.""".format(handler, event)

                # Raise error
                raise ValueError(msg)

            # If the handler wrapper has not been added before
            else:
                # Add the handler wrapper to the handlers list.
                self._event_handlers[event].append(handler_wrapper)

    def handler_remove(self, handler):
        """
        Remove event handler.

        @param handler: Event handler to remove.

        @return: None.
        """
        # `Remove infos` list.
        # Each info is a tuple: (handler_wrapper, handler_list, event).
        remove_info_s = []

        # For each event name
        for event in self._event_handlers:
            # Get handlers list for the event
            handler_wrapper_s = self._event_handlers[event]

            # For each handler wrapper
            for handler_wrapper in handler_wrapper_s:
                # If the handler wrapper should be removed
                if handler_wrapper.handler == handler:
                    # Add `remove info` to `remove infos` list
                    remove_info_s.append(
                        (handler_wrapper, handler_wrapper_s, event)
                    )

        # If `remove infos` list is empty
        if not remove_info_s:
            # Return
            return

        # If `remove infos` list is not empty.

        # For each `remove info`
        for remove_info in remove_info_s:
            # Get handler wrapper, handlers list, and event name
            handler_wrapper, handler_wrapper_s, event = remove_info

            # Remove the handler wrapper from the handlers list
            handler_wrapper_s.remove(handler_wrapper)

            # If the handlers list is empty
            if not handler_wrapper:
                # Remove the handlers list
                del self._event_handlers[event]

    def handler_remove_all(self):
        """
        Remove all event handlers.

        @return: None.
        """
        # Set event handlers dict to empty
        self._event_handlers = {}

    def handler_notify(
        self,
        event,
        arg=None,
        notifier=None,
        need_info=False,
    ):
        """
        Notify event handlers of given event.

        @param event: Event name.

        @param arg: Event argument.

        @param notifier: Event notifier. Default is `self`.
        Event notifier is used only if `need_info` is True.

        @param need_info: Whether need create event info object and pass the
        event info object as event argument to event handlers.

        @return: None.
        """
        # If the event has no handlers,
        # and there are no `None` handlers listening on every event.
        if event not in self._event_handlers \
                and None not in self._event_handlers:
            # Return
            return

        # If the event has handlers,
        # or there are `None` handlers listening on every event.

        # If need event info object
        if need_info:
            # Create event info object.
            # Use the event info object as event argument.
            arg = Event(
                event=event,
                arg=arg,
                notifier=notifier if notifier is not None else self,
            )

        # If not need event info object
        else:
            # Use the event argument as-is
            arg = arg

        # If the event has handlers,
        if event in self._event_handlers:
            # For each handler in the event's handlers list
            for handler in self._event_handlers[event]:
                # Call the handler
                handler(arg)

        # If there are `None` handlers listening on every event
        if None in self._event_handlers:
            # For each handler in the `None` handlers list
            for handler in self._event_handlers[None]:
                # Call the handler
                handler(arg)
