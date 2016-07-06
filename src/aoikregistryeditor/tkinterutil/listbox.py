# coding: utf-8
#
from __future__ import absolute_import

from tkinter import Listbox
from tkinter.constants import DISABLED
from tkinter.constants import END
from tkinter.constants import HORIZONTAL
from tkinter.constants import VERTICAL
from tkinter.ttk import Scrollbar

from .eventor import Eventor
from .vidget import Vidget


#
class _HiddenScrollbar(Scrollbar):
    """
    Scrollbar that hides if slider's both ends reached extreme position.
    """

    def set(self, lo, hi):
        """
        Set scrollbar slider's end positions.

        @param lo: Low end position. A float value between 0.0 and 1.0.

        @param hi: High end position. A float value between 0.0 and 1.0.

        @return: None.
        """
        # If scrollbar slider's both ends reached extreme position
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # Hide the scrollbar
            self.grid_remove()

        # If not scrollbar slider's both ends reached extreme position
        else:
            # Show the scrollbar
            self.grid()

        # Call super version
        Scrollbar.set(self, lo, hi)


#
class ListboxVidget(Vidget, Eventor):
    """
    ListboxVidget contains a Listbox widget. It adds the following abilities:
    - Store items of any type, unlike Listbox widget that only stores texts.
    - Remember selected item even if the listbox widget lost focus.
    - Notify pre-change and post-change events.
    """

    # Error raised when trying to change the listbox while a change is going on
    class CircularCallError(ValueError):
        pass

    # Error raised when trying to change the listbox while it is disabled
    class DisabledError(ValueError):
        pass

    # Event notified when the listbox's items are to be changed
    ITEMS_CHANGE_SOON = 'ITEMS_CHANGE_SOON'

    # Event notified when the listbox's items are changed
    ITEMS_CHANGE_DONE = 'ITEMS_CHANGE_DONE'

    # Event notified when the listbox's active item is to be changed
    ITEMCUR_CHANGE_SOON = 'ITEMCUR_CHANGE_SOON'

    # Event notified when the listbox's active item is changed
    ITEMCUR_CHANGE_DONE = 'ITEMCUR_CHANGE_DONE'

    # Events list
    EVENTS = (
        ITEMS_CHANGE_SOON,
        ITEMS_CHANGE_DONE,
        ITEMCUR_CHANGE_SOON,
        ITEMCUR_CHANGE_DONE,
    )

    def __init__(
        self,
        items=None,
        item_to_text=None,
        normal_bg='',
        normal_fg='',
        active_bg='sky blue',
        active_fg='white',
        selected_bg='steel blue',
        selected_fg='white',
        master=None,
    ):
        """
        Initialize object.

        @param items: Items list.

        @param item_to_text: Item-to-text function. Default is `str`.

        @param normal_bg: Unselected item background color.

        @param normal_fg: Unselected item foreground color.

        @param active_bg: Active item background color. `Active` means the item
        is selected (in general meaning) but the listbox has no focus.

        @param active_fg: Active item foreground color. `Active` means the item
        is selected (in general meaning) but the listbox has no focus.

        @param selected_bg: Selected item background color. `Selected` means
        the item is selected (in general meaning) and the listbox has focus.

        @param selected_fg: Selected item foreground color. `Selected` means
        the item is selected (in general meaning) and the listbox has focus.

        @param master: Master widget.

        @return: None.
        """
        # Initialize Vidget.
        # Create main frame widget.
        Vidget.__init__(
            self,
            master=master,
        )

        # Initialize Eventor
        Eventor.__init__(self)

        # If items list is given
        if items is not None:
            # If items list is not list
            if not isinstance(items, list):
                # Raise error
                raise TypeError(items)

            # If items list is list.

        # If items list is not given, or items list is given and is list

        # Items list
        self._items = items if items is not None else []

        # Item-to-text function. Default is `str`.
        self._item_to_text = item_to_text if item_to_text is not None else str

        # Unselected item background color
        self._normal_fg = normal_fg

        # Unselected item foreground color
        self._normal_bg = normal_bg

        # Active item background color
        self._active_fg = active_fg

        # Active item foreground color
        self._active_bg = active_bg

        # Selected item background color
        self._selected_fg = selected_fg

        # Selected item foreground color
        self._selected_bg = selected_bg

        # Whether the listbox is changing
        self._is_changing = False

        # Active index. `-1` means void, i.e. no item is active.
        self._indexcur = -1

        # Whether active index is being reset to same value
        self._is_resetting = False

        # Create listbox widget
        self._listbox = Listbox(
            master=self.widget(),
            relief='groove',
            activestyle='none',
            highlightthickness=0,
            # Active index cache only supports single-selection mode for now.
            # See 2N6OR.
            selectmode='single',
        )

        # Set the listbox widget as config target
        self.config_target_set(self._listbox)

        # Create x-axis scrollbar
        self._scrollbar_xview = _HiddenScrollbar(
            self.widget(),
            orient=HORIZONTAL,
        )

        # Create y-axis scrollbar
        self._scrollbar_yview = _HiddenScrollbar(
            self.widget(),
            orient=VERTICAL,
        )

        # Mount scrollbars
        self._listbox.config(xscrollcommand=self._scrollbar_xview.set)

        self._listbox.config(yscrollcommand=self._scrollbar_yview.set)

        self._scrollbar_xview.config(command=self._listbox.xview)

        self._scrollbar_yview.config(command=self._listbox.yview)

        # Bind single-click event handler
        self._listbox.bind('<Button-1>', self._on_single_click)

        # Bind double-click event handler
        self._listbox.bind('<Double-Button-1>', self._on_double_click)

        # Update listbox widget
        self._listbox_widget_update(keep_active=False)

        # Update widget
        self._widget_update()

    def _widget_update(self):
        """
        Update widget.

        @return: None.
        """
        # Row 0 for listbox and y-axis scrollbar
        self.widget().rowconfigure(0, weight=1)

        # Row 1 for x-axis scrollbar
        self.widget().rowconfigure(1, weight=0)

        # Column 0 for listbox and x-axis scrollbar
        self.widget().columnconfigure(0, weight=1)

        # Column 1 for y-axis scrollbar
        self.widget().columnconfigure(1, weight=0)

        # Lay out listbox
        self._listbox.grid(row=0, column=0, sticky='NSEW')

        # Lay out x-axis scrollbar
        self._scrollbar_xview.grid(row=1, column=0, sticky='EW')

        # Lay out y-axis scrollbar
        self._scrollbar_yview.grid(row=0, column=1, sticky='NS')

    def is_enabled(self):
        """
        Test whether the listbox is enabled.

        @return: Boolean.
        """
        # Return whether the listbox is enabled
        return self._listbox.config('state')[4] != DISABLED

    def is_changing(self):
        """
        Test whether the listbox is changing.

        @return: Boolean.
        """
        # Return whether the listbox is changing
        return self._is_changing

    def is_resetting(self):
        """
        Test whether the listbox is setting active index to the same value.

        @return: Boolean.
        """
        # Return whether the listbox is setting active index to the same value
        return self._is_resetting

    def size(self):
        """
        Get number of items.

        @return: Number of items.
        """
        # Return number of items
        return len(self._items)

    def items(self):
        """
        Get items list.
        Notice do not change the list outside.

        @return: Items list.
        """
        # Return items list
        return self._items

    def items_set(
        self,
        items,
        notify=True,
        keep_active=False,
    ):
        """
        Set items list.

        Notice do not change the list outside.

        @param items: Items list.

        @param notify: Whether notify pre-change and post-change events.

        @param keep_active: Whether keep or clear active index.

        @return: None.
        """
        # If the items is not list
        if not isinstance(items, list):
            # Raise error
            raise TypeError(items)

        # If the items is list.

        # If the listbox is disabled
        if not self.is_enabled():
            # Raise error
            raise ListboxVidget.DisabledError()

        # If the listbox is not disabled.

        # If the listbox is changing
        if self._is_changing:
            # Raise error
            raise ListboxVidget.CircularCallError()

        # If the listbox is not changing.

        # Set changing flag on
        self._is_changing = True

        # If notify events
        if notify:
            # Notify pre-change event
            self.handler_notify(self.ITEMS_CHANGE_SOON)

        # Store the new items
        self._items = items

        # Update listbox widget
        self._listbox_widget_update(
            keep_active=keep_active
        )

        # If notify events
        if notify:
            # Notify post-change event
            self.handler_notify(self.ITEMS_CHANGE_DONE)

        # Set changing flag off
        self._is_changing = False

    def index_is_valid(self, index):
        """
        Test whether given index is valid. Notice -1 is not valid.

        @param index: Index to test.

        @return: Boolean.
        """
        # Test whether given index is valid
        return 0 <= index and index < self.size()

    def index_is_valid_or_void(self, index):
        """
        Test whether given index is valid or is -1.

        @param index: Index to test.

        @return: Boolean.
        """
        # Test whether given index is valid or is -1
        return index == -1 or self.index_is_valid(index)

    def index_first(self):
        """
        Get the first item's index.

        @return: First item's index, or -1 if the listbox is empty.
        """
        # Return the first item's index
        return 0 if self.size() > 0 else -1

    def index_last(self):
        """
        Get the last item's index.

        @return: Last item's index, or -1 if the listbox is empty.
        """
        # Return the last item's index
        return self.size() - 1

    def indexcur(self, internal=False, raise_error=False):
        """
        Get the active index.

        @param internal: See 2N6OR.

        @return: The active index. If no active active, either return -1, or
        raise IndexError if `raise_error` is True.
        """
        # Get active indexes
        indexcurs = self._indexcurs(internal=internal)

        # If have active indexes
        if indexcurs:
            # Return the first active index
            return indexcurs[0]

        # If no active indexes
        else:
            # If raise error
            if raise_error:
                # Raise error
                raise IndexError(-1)

            # If not raise error
            else:
                # Return -1
                return -1

    def _indexcurs(self, internal=False):
        """
        Get active indexes list.

        2N6OR
        @param internal: Whether use listbox widget's selected indexes, instead
        of cached active index.
        Notice listbox widget has no selected indexes if it has no focus.
        Notice using cached active index only supports single-selection mode,
        which means the result list has at most one index.

        @return: Active indexes list.
        """
        # If use listbox widget's selected indexes
        if internal:
            # Return listbox widget's selected indexes list
            return [int(x) for x in self._listbox.curselection()]

        # If not use listbox widget's selected indexes
        else:
            # If cached active index is valid
            if self.index_is_valid(self._indexcur):
                # Return a list with the cached active index
                return [self._indexcur]

            # If cached active index is not valid
            else:
                # Return empty list
                return []

    def indexcur_set(
        self,
        index,
        focus=False,
        notify=True,
        notify_arg=None,
    ):
        """
        Set active index.

        @param index: The index to set.

        @param focus: Whether set focus on the listbox widget.

        @param notify: Whether notify pre-change and post-change events.

        @param notify_arg: Event argument.

        @return: None.
        """
        # If the index is not valid or -1
        if not self.index_is_valid_or_void(index):
            # Raise error
            raise IndexError(index)

        # If the index is valid or is -1.

        # If the listbox is not enabled
        if not self.is_enabled():
            # Raise error
            raise ListboxVidget.DisabledError()

        # If the listbox is enabled.

        # If the listbox is changing
        if self._is_changing:
            # Raise error
            raise ListboxVidget.CircularCallError()

        # If the listbox is not changing.

        # Set changing flag on
        self._is_changing = True

        # Get old active index
        old_indexcur = self._indexcur

        # Set resetting flag on if new and old indexes are equal
        self._is_resetting = (index == old_indexcur)

        # If notify events
        if notify:
            # Notify pre-change event
            self.handler_notify(self.ITEMCUR_CHANGE_SOON, notify_arg)

        # If old active index is valid
        if self.index_is_valid(old_indexcur):
            # Set old active item's background color to normal color
            self._listbox.itemconfig(old_indexcur, background=self._normal_bg)

            # Set old active item's foreground color to normal color
            self._listbox.itemconfig(old_indexcur, foreground=self._normal_fg)

        # Cache new active index
        self._indexcur = index

        # Clear listbox widget's selection
        self._listbox.selection_clear(0, END)

        # Set listbox widget's selection
        self._listbox.selection_set(index)

        # Set listbox widget's activated index
        self._listbox.activate(index)

        # If new active index is valid
        if index != -1:
            # Set new active item's background color to active color
            self._listbox.itemconfig(index, background=self._active_bg)

            # Set new active item's foreground color to active color
            self._listbox.itemconfig(index, foreground=self._active_fg)

        # If set focus
        if focus:
            # Set focus on the listbox widget
            self._listbox.focus_set()

        # If new active index is valid
        if index != -1:
            # Make the active item visible
            self._listbox.see(index)

        # If notify events
        if notify:
            # Notify post-change event
            self.handler_notify(self.ITEMCUR_CHANGE_DONE, notify_arg)

        # Set resetting flag off
        self._is_resetting = False

        # Set changing flag off
        self._is_changing = False

    def indexcur_set_by_event(
        self,
        event,
        focus=False,
        notify=True,
        notify_arg=None,
    ):
        """
        Set active index using a Tkinter event object that contains coordinates
        of the active item.

        @param event: Tkinter event object.

        @param focus: Whether set focus on the listbox widget.

        @param notify: Whether notify pre-change and post-change events.

        @param notify_arg: Event argument.

        @return: None.
        """
        # Get the event's y co-ordinate's nearest listbox item index
        index = self._listbox.nearest(event.y)

        # If the index is not valid
        if not self.index_is_valid_or_void(index):
            # Ignore the event
            return

        # If the index is valid
        else:
            # Set the index as active index
            self.indexcur_set(
                index=index,
                focus=focus,
                notify=notify,
                notify_arg=notify_arg,
            )

    def item(self, index):
        """
        Get item at given index.

        @return: Item at given index, or IndexError if the index is not valid.
        """
        return self.items()[index]

    def itemcur(self, internal=False, raise_error=False):
        """
        Get the active item.

        @param internal: See 2N6OR.

        @param raise_error: Whether raise error if no active item.

        @return: The active item. If no active item, if `raise_error` is
        True, raise IndexError, otherwise return None.
        """
        # Get active index.
        # May raise IndexError if `raise_error` is True.
        indexcur = self.indexcur(
            internal=internal,
            raise_error=raise_error,
        )

        # If no active index
        if indexcur == -1:
            # Return None
            return None

        # If have active index
        else:
            # Return the active item
            return self.items()[indexcur]

    def item_insert(
        self,
        item,
        index=None,
        notify=True,
        keep_active=True,
    ):
        """
        Insert item at given index.

        @param item: Item to insert.

        @param index: Index to insert. `None` means active index, and if no
        active index, insert at the end.

        @param notify: Whether notify pre-change and post-change events.

        @param keep_active: Whether keep or clear active index.

        @return: None.
        """
        # If notify events
        if notify:
            # Notify pre-change events
            self.handler_notify(self.ITEMCUR_CHANGE_SOON)

            self.handler_notify(self.ITEMS_CHANGE_SOON)

        # Get old active index
        active_index = self.indexcur()

        # If the index is None,
        # it means use active index.
        if index is None:
            # Use active index.
            # `-1` works and means appending.
            index = active_index

        # Insert the item to the items list
        self._items.insert(index, item)

        # If old active index is valid
        if active_index != -1:
            # If old active index is GE the inserted index
            if active_index >= index:
                # Shift active index by one
                active_index += 1

            # If old active index is not GE the inserted index, use it as-is.

        # Set new active index
        self.indexcur_set(index=active_index, notify=False)

        # Update listbox widget
        self._listbox_widget_update(
            keep_active=keep_active
        )

        # If notify events
        if notify:
            # Notify post-change events
            self.handler_notify(self.ITEMS_CHANGE_DONE)

            self.handler_notify(self.ITEMCUR_CHANGE_DONE)

    def item_remove(
        self,
        index,
        notify=True,
        keep_active=True,
    ):
        """
        Remove item at given index.

        @param index: Index to remove.

        @param notify: Whether notify pre-change and post-change events.

        @param keep_active: Whether keep or clear active index.

        @return: None.
        """
        # If the index is not valid
        if not self.index_is_valid(index):
            # Raise error
            raise ValueError(index)

        # If the index is valid.

        # If notify events
        if notify:
            # Notify pre-change events
            self.handler_notify(self.ITEMCUR_CHANGE_SOON)

            self.handler_notify(self.ITEMS_CHANGE_SOON)

        # Get old active index
        active_index = self.indexcur()

        # Remove item at the index
        del self._items[index]

        # If old active index is valid
        if active_index != -1:
            # Get the last index
            index_last = self.index_last()

            # If old active index is GT the last index
            if active_index > index_last:
                # Use the last index as new active index
                active_index = index_last

            # If old active index is not GT the last index, use it as-is.

        # Set new active index
        self.indexcur_set(index=active_index, notify=False)

        # Update listbox widget
        self._listbox_widget_update(
            keep_active=keep_active
        )

        # If notify events
        if notify:
            # Notify post-change events
            self.handler_notify(self.ITEMS_CHANGE_DONE)

            self.handler_notify(self.ITEMCUR_CHANGE_DONE)

    def handler_add(
        self,
        event,
        handler,
        need_arg=False,
    ):
        """
        Add event handler for an event.
        If the event is ListboxVidget event, add the event handler to Eventor.
        If the event is not ListboxVidget event, add the event handler to
        listbox widget.

        Notice this method overrides `Eventor.handler_add` in order to add
        non-ListboxVidget event handler to listbox widget.

        @param event: Event name.

        @param handler: Event handler.

        @param need_arg: Whether the event handler needs event argument.

        @return: None.
        """
        # If the event is ListboxVidget event
        if event in self.EVENTS:
            # Add the event handler to Eventor
            return Eventor.handler_add(
                self,
                event=event,
                handler=handler,
                need_arg=need_arg,
            )

        # If the event is not ListboxVidget event,
        # it is assumed to be Tkinter widget event.
        else:
            # Add the event handler to listbox widget
            return self.bind(
                event=event,
                handler=handler,
            )

    def bind(
        self,
        event,
        handler,
    ):
        """
        Add event handler to listbox widget.

        ListboxVidget internally uses `<Button-1>` and `<Double-Button-1>` to
        capture active index changes. So if the given event is `<Button-1>` or
        `<Double-Button-1>`, the given handler will be wrapped.

        @param event: Event name.

        @param handler: Event handler.

        @return: None.
        """
        # If the event is not `<Button-1>` or `<Double-Button-1>`
        if event not in ['<Button-1>', '<Double-Button-1>']:
            # Add the event handler to listbox widget
            self._listbox.bind(event, handler)

        # If the event is `<Button-1>` or `<Double-Button-1>`
        else:
            # Create event handler wrapper
            def handler_wrapper(e):
                """
                Event handler wrapper that sets new active index and then calls
                the wrapped event handler.

                Setting new active index is needed because when this handler is
                called by Tkinter, the active index of the listbox is still
                old.

                @param e: Tkinter event object.

                @return: None.
                """
                # Set new active index
                self.indexcur_set_by_event(e, notify=True)

                # Call the wrapped event handler
                handler(e)

            # Add the event handler wrapper to the listbox widget
            self._listbox.bind(event, handler_wrapper)

    def _on_single_click(self, event):
        """
        `<Button-1>` event handler that updates active index.

        @param event: Tkinter event object.

        @return: None.
        """
        # Updates active index
        self.indexcur_set_by_event(event, notify=True)

    def _on_double_click(self, event):
        """
        `<Double-Button-1>` event handler that updates active index.

        @param event: Tkinter event object.

        @return: None.
        """
        # Updates active index
        self.indexcur_set_by_event(event, notify=True)

    def _listbox_widget_update(
        self,
        keep_active,
    ):
        """
        Update listbox widget's items and selection.

        @param keep_active: Whether keep or clear active index.

        @return: None.
        """
        # Remove old items from listbox widget
        self._listbox.delete(0, END)

        # Insert new items into listbox widget.
        # For each ListboxVidget items.
        for index, item in enumerate(self.items()):
            # Get item text
            item_text = self._item_to_text(item)

            # Insert the item text into listbox widget
            self._listbox.insert(index, item_text)

            # Set the item's normal background color
            self._listbox.itemconfig(index, background=self._normal_bg)

            # Set the item's normal foreground color
            self._listbox.itemconfig(index, foreground=self._normal_fg)

            # Set the item's selected background color
            self._listbox.itemconfig(index, selectbackground=self._selected_bg)

            # Set the item's selected foreground color
            self._listbox.itemconfig(index, selectforeground=self._selected_fg)

        # If keep active index
        if keep_active:
            # Use old active index
            indexcur = self._indexcur

        # If not keep active index
        else:
            # Set active index to -1
            indexcur = self._indexcur = -1

        # Clear old selection
        self._listbox.selection_clear(0, END)

        # Set new selection.
        # `-1` works.
        self._listbox.selection_set(indexcur)

        # Set new active index.
        # `-1` works.
        self._listbox.activate(indexcur)

        # If new active index is valid
        if indexcur != -1:
            # Set active background color
            self._listbox.itemconfig(indexcur, background=self._active_bg)

            # Set active foreground color
            self._listbox.itemconfig(indexcur, foreground=self._active_fg)

            # Make the active item visible
            self._listbox.see(indexcur)
