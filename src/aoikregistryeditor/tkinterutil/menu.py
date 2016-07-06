# coding: utf-8
#
from __future__ import absolute_import

from collections import OrderedDict
from tkinter import Menu
from tkinter.constants import END


#
class MenuTree(object):
    """
    MenuTree provides methods to operate a tree of menu items.
    These methods refer to menu items using custom string IDs, instead of
    internal object references.

    Notice do not change the menu tree outside.
    """

    # Info dict keys.

    # Item ID key
    INFO_K_ID = 'INFO_K_ID'

    # Item ID key for top menu
    INFO_K_ID_V_TOP = '/'

    # Item PID key
    INFO_K_PID = 'INFO_K_PID'

    # Item widget key
    INFO_K_ITEM_WIDGET = 'INFO_K_ITEM_WIDGET'

    # Item index key
    INFO_K_ITEM_INDEX = 'INFO_K_ITEM_INDEX'

    #
    def __init__(
        self,
        id_to_full=None,
        id_to_label=None,
        id_sep=None,
        master=None,
    ):
        """
        Initialize object.

        @param id_to_full: Function converts relative ID to full ID.

        @param id_to_label: Function converts ID to menu label.

        @param id_sep: ID parts separator.

        @param master: Master widget.

        @return: None.
        """
        # Master widget
        self._master = master

        # ID parts separator.
        self._id_sep = id_sep if id_sep is not None else '/'

        # Function converts relative ID to full ID
        self._id_to_full = id_to_full \
            if id_to_full is not None else self._id_to_full_default

        # Function converts ID to menu label
        self._id_to_label = id_to_label \
            if id_to_label is not None else self._id_to_label_default

        # Dict that contains menu item infos.
        # Key is menu item ID.
        # Value is menu item info dict.
        self._id_to_info = OrderedDict()

        # Create top menu.
        # `tearoff` is not allowed.
        self._menu_top = Menu(master=self._master, tearoff=False)

        # Create top menu's info dict
        self._id_to_info[self.INFO_K_ID_V_TOP] = {
            # Top menu's ID is `/`
            self.INFO_K_ID: self.INFO_K_ID_V_TOP,

            # Top menu's PID is None
            self.INFO_K_PID: None,

            # Top menu's item widget
            self.INFO_K_ITEM_WIDGET: self._menu_top,

            # Top menu's item index is None
            self.INFO_K_ITEM_INDEX: None,
        }

    def master(self):
        """
        Get the master widget.

        @return: Master widget.
        """
        # Return the master widget
        return self._master

    def menu_top(self):
        """
        Get the top menu widget.

        Notice do not change the menu tree outside.

        @return: Top menu widget.
        """
        # Return the top menu widget
        return self._menu_top

    def item_widget(self, id):
        """
        Get item widget by item ID.

        @param id: Item ID.

        @return: Item widget.
        """
        # Get item info dict
        info = self._id_to_info.get(id, None)

        # If item info dict not exists
        if info is None:
            # Raise error
            raise ValueError('Item ID not exists: `{}`'.format(id))

        # If item info dict exists
        else:
            # Return the item widget
            return info[self.INFO_K_ITEM_WIDGET]

    def item_index(self, id):
        """
        Get item index as child of a parent menu.

        @param id: Item ID.

        @return: Item index as child of a parent menu.
        """
        # Get item info dict
        info = self._id_to_info.get(id, None)

        # If item info dict not exists
        if info is None:
            # Raise error
            raise ValueError('Item ID not exists: `{}`'.format(id))

        # If item info dict exists
        else:
            # Return the item index as child of a parent menu
            return info[self.INFO_K_ITEM_INDEX]

    def item_ids(self):
        """
        Get item IDs list.

        @return: Item IDs list.
        """
        # Return the item IDs list.
        return list(self._id_to_info.keys())

    def item_exists(self, id):
        """
        Test whether given item ID exists.

        @param id: Item ID.

        @return: Boolean.
        """
        # Return whether given item ID exists
        return id in self._id_to_info

    def item_is_menu(self, id):
        """
        Test whether given item ID refers to menu item.

        @param id: Item ID.

        @return: Boolean.
        """
        # Get item info dict
        info = self._id_to_info.get(id, None)

        # If item info dict not exists
        if info is None:
            # Raise error
            raise ValueError('Item ID not exists: `{}`'.format(id))

        # If item info dict exists
        else:
            # Get item widget
            widget = info[self.INFO_K_ITEM_WIDGET]

            # Return whether the item widget is menu
            return isinstance(widget, Menu)

    def item_child_indexes(self, id):
        """
        Get given menu item's child item indexes.

        @param id: Menu item ID.

        @return: Menu item's child item indexes.
        """
        # If given item ID not refers to menu item
        if not self.item_is_menu(id):
            # Raise error
            raise ValueError('Item ID not refers to menu: `{}`'.format(id))

        # If given item ID refers to menu item.

        # Child indexes list
        child_index_s = []

        # For each item info dict
        for info in self._id_to_info.values():
            # Get the item PID
            pid = info[self.INFO_K_PID]

            # If the item's parent item is the given menu item.
            if pid == id:
                # Get the item's index
                index = info[self.INFO_K_ITEM_INDEX]

                # Add the item's index to the child indexes list
                child_index_s.append(index)

        # Sort the child indexes list
        child_index_s.sort()

        # Return the child indexes list
        return child_index_s

    def item_child_index_last(self, id):
        """
        Get given menu item's last child item index.

        Notice if given menu item has been added child items without using
        methods of this class, this may give different result compared to
        `self._item_child_index_last_internal`.

        @param id: Menu item ID.

        @return: Menu item's last child item index, or -1 if no child item.
        """
        # If given item ID not refers to menu item
        if not self.item_is_menu(id):
            # Raise error
            raise ValueError('Item ID not refers to menu: `{}`'.format(id))

        # If given item ID refers to menu item.

        # Get given menu item's child item indexes.
        # Can be empty.
        index_s = self.item_child_indexes(id=id)

        # If have child item
        if index_s:
            # Return the last child item index
            return index_s[-1]

        # If no child item
        else:
            # Return -1
            return -1

    def _item_child_index_last_internal(self, id):
        """
        Get given menu item's last child item index, according to the menu
        widget's internal state.

        @param id: Menu item ID.

        @return: Menu item's last child item index, or -1 if no child item.
        """
        # Get item info dict
        info = self._id_to_info.get(id, None)

        # If item info dict not exists
        if info is None:
            # Raise error
            raise ValueError('Item ID not exists: `{}`'.format(id))

        # If item info dict exists
        else:
            # Get widget
            widget = info[self.INFO_K_ITEM_WIDGET]

            # If the widget is not menu
            if not isinstance(widget, Menu):
                # Raise error
                raise ValueError('Item ID not refers to menu: `{}`'.format(id))

            # If the widget is menu.

            # Get the last child item index.
            # Can be None.
            index_end = widget.index(END)

            # If no child item
            if index_end is None:
                # Return -1
                return -1

            # If have child item
            else:
                # Return the last child item index
                return index_end

    def menu(self, id):
        """
        Get menu widget by item ID.

        @param id: Menu item ID.

        @return: Menu widget.
        """
        # Get item info dict
        info = self._id_to_info.get(id, None)

        # If item info dict not exists
        if info is None:
            # Raise error
            raise ValueError('Item ID not exists: `{}`'.format(id))

        # If item info dict exists
        else:
            # Get item widget
            widget = info[self.INFO_K_ITEM_WIDGET]

            # If the item widget is not menu widget
            if not isinstance(widget, Menu):
                # Raise error
                raise ValueError('Item ID not refers to menu: `{}`'.format(id))
            # If the item widget is menu widget
            else:
                # Return the menu widget
                return widget

    def _add_info_dict(self, pid, id, index, widget):
        """
        Add item info dict. Should be called after adding given widget to the
        parent menu referred to by `pid`.

        @param pid: Menu item PID.

        @param id: Menu item ID.

        @param widget: Menu widget, or one of ['commmand', 'separator'].

        @return: None.
        """
        # If item ID exists
        if self.item_exists(id):
            # Raise error
            raise ValueError('Item ID exists: `{}`'.format(id))

        # If item ID not exists.

        # If PID not refers to a menu
        if not self.item_is_menu(pid):
            # Raise error
            raise ValueError('Item ID not refers to menu: `{}`'.format(pid))

        # If PID refers to a menu.

        # Get parent menu's last child index
        index_last = self.item_child_index_last(pid)

        # Get parent menu's internal last child index
        index_last_internal = self._item_child_index_last_internal(pid)

        # If the two indexes are not off by one,
        # it means this method is not called after adding given widget to the
        # parent menu referred to by `pid`.
        if index_last != index_last_internal - 1:
            # Raise error
            raise ValueError(
                'Menu item has been modified outside: `{}`'.format(pid)
            )

        # If the two indexes are off by one.

        # If given index is not valid
        if not (0 <= index <= index_last + 1):
            # Raise error
            raise ValueError('Item index is not valid: `{}`'.format(index))

        # Shift indexes of other child item info dicts.
        # For each item info dict.
        for info in self._id_to_info.values():
            # Get the item's PID
            pid_x = info[self.INFO_K_PID]

            # If the item's PID is EQ given PID
            if pid_x == pid:
                # Get the item's index
                index_x = info[self.INFO_K_ITEM_INDEX]

                # If the item's index is GE given index
                if index_x >= index:
                    # Shift the item's index by 1
                    info[self.INFO_K_ITEM_INDEX] = index_x + 1

        # Add item info dict for the item
        self._id_to_info[id] = {
            self.INFO_K_ID: id,
            self.INFO_K_PID: pid,
            self.INFO_K_ITEM_INDEX: index,
            self.INFO_K_ITEM_WIDGET: widget,
        }

    def add_item(
        self,
        widget_factory,
        pid,
        id,
        id_is_full=False,
        id_sep=None,
        index=None,
        label=None,
    ):
        """
        Add an item to a parent menu item.

        @param widget_factory: Widget factory.

        @param pid: Menu item PID.

        @param id: Menu item ID.

        @param id_is_full: Whether given item ID is full.

        @param id_sep: ID parts separator.

        @param label: Menu label.

        @param index: Item index as child of a parent menu. Default is the end.

        @return: None.
        """
        # If given PID not refers to menu widget
        if not self.item_is_menu(pid):
            # Raise error
            raise ValueError('Item ID not refers to menu: `{}`'.format(pid))

        # If given PID refers to menu widget.

        # ID parts separator
        id_sep = id_sep if id_sep is not None else self._id_sep

        # If given item ID is full
        if id_is_full:
            # Use the given item ID as full ID
            full_id = id

        # If given item ID is not full
        else:
            # Convert the relative ID to full ID
            full_id = self._id_to_full(id=id, pid=pid, id_sep=id_sep)

        # If the item ID exists
        if self.item_exists(full_id):
            # Raise error
            raise ValueError('Item ID exists: `{}`'.format(full_id))

        # If the item ID not exists.

        # If menu label is not given
        if label is None:
            # Convert the item ID to menu label
            label = self._id_to_label(id=full_id, id_sep=id_sep)

        # Get last item index
        last_index = self.item_child_index_last(pid)

        # Get internal last item index
        last_index_internal = self._item_child_index_last_internal(pid)

        # If the two indexes are not consistent
        if last_index != last_index_internal:
            # Raise error
            raise ValueError(
                'Menu item has been modified outside: `{}`'.format(pid)
            )

        # If the two indexes are consistent.

        # If index is not given
        if index is None:
            # Set index to last item index plus one
            index = last_index + 1

        # If index is not valid
        if not (0 <= index <= last_index + 1):
            # Raise error
            raise ValueError('Item index is not valid: `{}`'.format(index))

        # If index is valid.

        # Get parent menu
        parent_menu = self.menu(pid)

        # Create widget
        widget = widget_factory(
            parent_menu=parent_menu,
            index=index,
            label=label,
        )

        # Add item info dict
        self._add_info_dict(
            pid=pid,
            id=full_id,
            index=index,
            widget=widget,
        )

    def remove_item(
        self,
        id,
    ):
        """
        Remove an item.
        If the item is a menu, remove its child items recursively.

        @param id: Item ID.

        @return: None.
        """
        # If given item ID is top menu ID
        if id == self.INFO_K_ID_V_TOP:
            # Raise error
            raise ValueError('Cannot remove top menu: `{}`'.format(id))

        # If given item ID is not top menu ID.

        # Get item info dict
        info = self._id_to_info.get(id, None)

        # If item info dict not exists
        if info is None:
            # Raise error
            raise ValueError('Item ID not exists: `{}`'.format(id))

        # If item info dict exists

        # Get item PID
        item_pid = info[self.INFO_K_PID]

        # Get item index
        item_index = info[self.INFO_K_ITEM_INDEX]

        # Get parent menu
        parent_menu = self.menu(item_pid)

        # Remove item at the index
        parent_menu.delete(item_index)

        # For each x item id
        for x_item_id in self.item_ids():
            # If the x item id not exists.
            # This is possible because the code below remove child items
            # recursively.
            if not self.item_exists(x_item_id):
                # Ignore the x item id
                continue

            # If the x item id exists.

            # Get x item's info dict
            x_info = self._id_to_info[x_item_id]

            # Get x item's PID
            x_pid = x_info[self.INFO_K_PID]

            # If x item's PID is EQ ID of the item to remove,
            # it means it is a child item of the item to remove.
            if x_pid == id:
                # Remove the child item
                self.remove_item(
                    x_item_id,
                )

            # If x item's PID is EQ PID of the item to remove,
            # it means it is a sibling item of the item to remove.
            elif x_pid == item_pid:
                # Get x item's index
                x_index = x_info[self.INFO_K_ITEM_INDEX]

                # If x item's index is GT index of the item to remove
                if x_index > item_index:
                    # Shift x item's index by one
                    x_info[self.INFO_K_ITEM_INDEX] = x_index - 1

            # If x item is something else
            else:
                # Ignore the x item
                continue

        # Delete the item's info dict
        del self._id_to_info[id]

    def add_menu(
        self,
        pid,
        id,
        id_is_full=False,
        id_sep=None,
        index=None,
        label=None,
    ):
        """
        Add menu item.

        @param pid: Menu item PID.

        @param id: Menu item ID.

        @param id_is_full: Whether given item ID is full.

        @param id_sep: ID parts separator.

        @param index: Item index as child of a parent menu. Default is the end.

        @param label: Menu label.

        @return: None.
        """
        # Create widget factory
        def widget_factory(**kwargs):
            """
            Widget factory function.

            @param kwargs: Keyword arguments given by caller method `add_item`.

            @return: Menu widget.
            """
            # Get parent menu
            parent_menu = kwargs['parent_menu']

            # Create menu widget.
            # `tearoff` is not allowed.
            menu = Menu(master=parent_menu, tearoff=False)

            # Get item index
            index = kwargs['index']

            # Get item label
            label = kwargs['label']

            # Insert the menu widget into the parent menu
            parent_menu.insert_cascade(index=index, menu=menu, label=label)

            # Return the menu widget
            return menu

        # Add item
        self.add_item(
            widget_factory=widget_factory,
            pid=pid,
            id=id,
            id_is_full=id_is_full,
            id_sep=id_sep,
            index=index,
            label=label,
        )

    def add_command(
        self,
        pid,
        id,
        command,
        id_is_full=False,
        id_sep=None,
        index=None,
        label=None,
    ):
        """
        Add command item.

        @param pid: Menu item PID.

        @param id: Menu item ID.

        @param command: Command function.

        @param id_is_full: Whether given item ID is full.

        @param id_sep: ID parts separator.

        @param index: Item index as child of a parent menu. Default is the end.

        @param label: Menu label.

        @return: None.
        """
        # Create widget factory
        def widget_factory(**kwargs):
            """
            Widget factory function.

            @param kwargs: Keyword arguments given by caller method `add_item`.

            @return: Internal widget type name `command`.
            """
            # Get parent menu
            parent_menu = kwargs['parent_menu']

            # Get item index
            index = kwargs['index']

            # Get item label
            label = kwargs['label']

            # Insert command widget into the parent menu
            parent_menu.insert_command(
                index=index,
                label=label,
                command=command,
            )

            # Return the internal widget type name
            return 'command'

        # Add item
        self.add_item(
            widget_factory=widget_factory,
            pid=pid,
            id=id,
            id_is_full=id_is_full,
            id_sep=id_sep,
            index=index,
            label=label,
        )

    def add_separator(
        self,
        pid,
        id,
        id_is_full=False,
        id_sep=None,
        index=None,
    ):
        """
        Add separator item.

        @param pid: Menu item PID.

        @param id: Menu item ID.

        @param id_is_full: Whether given item ID is full.

        @param id_sep: ID parts separator.

        @param index: Item index as child of a parent menu. Default is the end.

        @return: None.
        """
        # Create widget factory
        def widget_factory(**kwargs):
            """
            Widget factory function.

            @param kwargs: Keyword arguments given by caller method `add_item`.

            @return: Internal widget type name `separator`.
            """
            # Get parent menu
            parent_menu = kwargs['parent_menu']

            # Get index
            index = kwargs['index']

            # Insert separator widget into the parent menu
            parent_menu.insert_separator(index=index)

            # Return the internal widget name
            return 'separator'

        # Add item
        self.add_item(
            widget_factory=widget_factory,
            pid=pid,
            id=id,
            id_is_full=id_is_full,
            id_sep=id_sep,
            index=index,
        )

    def _id_to_full_default(self, id, pid, id_sep):
        """
        Default function that converts relative ID to full ID.
        E.g. `Exit`-> `/File/Exit`

        @param id: Menu item relative ID.

        @param pid: Menu item PID.

        @param id_sep: ID parts separator.

        @return: Item full ID.
        """
        # If parent menu is top menu
        if pid == self.INFO_K_ID_V_TOP:
            # If the separator is EQ top menu ID, e.g. `/`
            if id_sep == self.INFO_K_ID_V_TOP:
                # Not add separator between parent ID and child relative ID
                return pid + id

        # If parent menu is not top menu,
        # or parent menu is top menu but the separator is not EQ top menu ID.

        # Add separator between parent ID and child relative ID
        return pid + id_sep + id

    def _id_to_label_default(self, id, id_sep):
        """
        Default function that converts ID to menu label.
        E.g. `/File/Exit`-> `Exit`

        @param id: Menu item ID.

        @param id_sep: ID parts separator.

        @return: Menu label.
        """
        # Split the item ID into prefix and label
        prefix, _, label = id.rpartition(id_sep)

        # Return the label
        return label
