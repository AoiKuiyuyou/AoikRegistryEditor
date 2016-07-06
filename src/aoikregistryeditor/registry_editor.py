# coding: utf-8
#
from __future__ import absolute_import

from tkinter import IntVar
from tkinter import messagebox
from tkinter.constants import ACTIVE
from tkinter.constants import DISABLED
from tkinter.constants import NORMAL
from tkinter.ttk import Frame
from tkinter.ttk import Label
from tkinter.ttk import LabelFrame
from tkinter.ttk import Radiobutton
from win32con import KEY_ALL_ACCESS
from win32con import KEY_READ
from win32con import KEY_WRITE

from .registry import RegKeyPathNavigator
from .registry import regkey_exists
from .registry import regkey_get
from .tkinterutil.label import LabelVidget
from .tkinterutil.listbox import ListboxVidget
from .tkinterutil.menu import MenuTree
from .tkinterutil.text import TextVidget
from .tkinterutil.text import EntryVidget
from .tkinterutil.toplevel import center_window
from .tkinterutil.toplevel import DialogVidget
from .tkinterutil.toplevel import get_window_center
from .tkinterutil.vidget import Vidget


#
class FieldEditor(object):
    """
    Field editor interface class.
    """

    def field_is_supported(self, field):
        """
        Test whether given field is supported by the field editor.

        @param field: Field's RegVal object.

        @return: Boolean.
        """
        # Raise error
        raise NotImplemented()

    def data(self):
        """
        Get data in the field editor.

        @return: Data in the field editor.
        """
        # Raise error
        raise NotImplemented()

    def data_set(self, data):
        """
        Set data in the field editor.

        @param data: Data to set.

        @return: None.
        """
        # Raise error
        raise NotImplemented()

    def enable(self, enabled):
        """
        Enable or disable the filed editor.

        @param enabled: Whether enable.

        @return: None.
        """
        # Raise error
        raise NotImplemented()

    def enabled(self):
        """
        Test whether the filed editor is enabled.

        @return: Boolean.
        """
        # Raise error
        raise NotImplemented()

    def widget(self):
        """
        Get the filed editor's widget.

        @return: Filed editor's widget.
        """
        # Raise error
        raise NotImplemented()

    def destroy(self):
        """
        Destroy the filed editor.

        @return: None.
        """
        # Raise error
        raise NotImplemented()


#
class FilteredFieldEditor(FieldEditor):
    """
    FilteredFieldEditor contains a TextVidget.
    It applies get filter when getting field data from registry, and applies
    set filter when setting field data to registry.
    """

    def __init__(
        self,
        field,
        get_filter,
        set_filter,
        master,
        normal_bg=None,
        disabled_bg=None,
    ):
        """
        Initialize object.

        @param field: Field's RegVal object.

        @param get_filter: Get filter.

        @param set_filter: Set filter.

        @param master: Master widget.

        @param normal_bg: Normal state background color.

        @param disabled_bg: Disabled state background color.
        """
        # Field's RegVal object
        self._field = field

        # Create text vidget
        self._text_vidget = TextVidget(master=master)

        # Get filter
        self._get_filter = get_filter

        # Set filter
        self._set_filter = set_filter

        # Normal state background color
        self._normal_bg = normal_bg

        # Disabled state background color
        self._disabled_bg = disabled_bg

        # Whether the field editor is enabled
        self._enabled = True

    def field(self):
        """
        Get field's RegVal object.

        @return: Field's RegVal object.
        """
        # Return the field's RegVal object
        return self._field

    def field_set(self, field):
        """
        Set field's RegVal object.

        @param field: Field's RegVal object to set.

        @return: None.
        """
        # Set the field's RegVal object
        self._field = field

    def field_is_supported(self, field):
        """
        Test whether given field is supported by the field editor.

        @param field: Field's RegVal object.

        @return: Boolean.
        """
        # Get field type
        field_type = field.type()

        # Test whether the field type is `String` or `Extended String`
        # 1: String.
        # 2: Extended String.
        return field_type in [1, 2]

    def text_vidget(self):
        """
        Get the text vidget.

        @return: Text vidget.
        """
        # Return the text vidget
        return self._text_vidget

    def data(self):
        """
        Get data in the field editor.

        @return: Data in the field editor.
        """
        # Get the text vidget's data
        data = self._text_vidget.text()

        # Apply get filter on the data
        data = self._get_filter(data)

        # Return the filtered data
        return data

    def data_set(self, data):
        """
        Set data in the field editor.

        @param data: Data to set.

        @return: None.
        """
        # Apply set filter on the data
        data = self._set_filter(data)

        #
        self._text_vidget.text_set(data)

    def enable(self, enabled):
        """
        Enable or disable the filed editor.

        @param enabled: Whether enable.

        @return: None.
        """
        # Set the enabled state
        self._enabled = enabled

        # If the state is enabled
        if self._enabled:
            # Set text vidget's state to normal
            self._text_vidget.config(state=NORMAL)

            # If normal state background color is given
            if self._normal_bg is not None:
                # Set text vidget's normal state background color
                self._text_vidget.config(background=self._normal_bg)

        # If the state is not enabled
        else:
            # If disabled state background color is given
            if self._disabled_bg is not None:
                # Set text vidget's disabled state background color
                self._text_vidget.config(background=self._disabled_bg)

            # Set text vidget's state to disabled
            self._text_vidget.config(state=DISABLED)

    def enabled(self):
        """
        Test whether the filed editor is enabled.

        @return: Boolean.
        """
        # Return whether the filed editor is enabled
        return self._enabled

    def widget(self):
        """
        Get the filed editor's widget.

        @return: Filed editor's widget.
        """
        # Return the filed editor's widget
        return self._text_vidget.widget()

    def destroy(self):
        """
        Destroy the filed editor.

        @return: None.
        """
        # Hide the text vidget
        self._text_vidget.grid_forget()

        # Destroy the text vidget
        self._text_vidget.destroy()


#
class RegistryEditor(Vidget):

    def __init__(
        self,
        field_editor_factory,
        status_bar_set,
        master=None,
    ):
        """
        Initialize object.

        @param field_editor_factory: Field editor factory function.
        The factory function should take these arguments (see 5WMYV):
        - field: Field's RegVal object.
        - old_editor: Old field editor object.
        - master: Master widget for the new field editor's widget.
        The factory function should return a field editor that supports methods
        in the FieldEditor interface class.

        @param status_bar_set: Status bar set function.

        @param master: Master widget.

        @return: None.
        """
        # Initialize Vidget.
        # Create main frame widget.
        Vidget.__init__(self, master=master)

        # Field editor factory function
        self._field_editor_factory = field_editor_factory

        # Status bar set function
        self._status_bar_set = status_bar_set

        # Create registry key path navigator
        self._path_nav = RegKeyPathNavigator()

        # Create registry key path bar textfield
        self._path_bar = EntryVidget(master=self.widget())

        # Create child keys listbox
        self._child_keys_listbox = ListboxVidget(master=self.widget())

        # Child keys listbox's active index cache.
        # Key is registry key path.
        # Value is active child key index.
        self._child_keys_listbox_indexcur_memo = {}

        # Create fields listbox
        self._fields_listbox = ListboxVidget(
            master=self.widget(),
        )

        # Field editor
        self._field_editor = None

        # Create `field add` label
        self._field_add_label = LabelVidget(master=self.widget())

        # Create `field del` label
        self._field_del_label = LabelVidget(master=self.widget())

        # Create `field load` label
        self._field_load_label = LabelVidget(master=self.widget())

        # Create `field save` label
        self._field_save_label = LabelVidget(master=self.widget())

        # Create `field add` dialog
        self._field_add_dialog = DialogVidget(
            master=self.widget(),
            confirm_buttion_text='Ok',
            cancel_buttion_text='Cancel',
        )

        # Create `field add` dialog's view frame
        self._field_add_frame = Frame(
            master=self._field_add_dialog.toplevel()
        )

        # Create `field add` dialog's `field name` label
        self._field_add_name_label = Label(master=self._field_add_frame)

        # Create `field add` dialog's `field name` textfield
        self._field_add_name_textfield = EntryVidget(
            master=self._field_add_frame
        )

        # Create `field add` dialog's `field type` label
        self._field_add_type_label = Label(
            master=self._field_add_frame
        )

        # Create `field add` dialog's `field type` radio buttons frame
        self._field_add_type_rbuttons_frame = Frame(
            master=self._field_add_frame,
        )

        # Create `field add` dialog's radio button variable
        self._field_add_type_var = IntVar()

        # Create `field add` dialog's radio button for `String` field type
        self._field_add_type_v_string_rbutton = Radiobutton(
            master=self._field_add_type_rbuttons_frame,
            text='String',
            variable=self._field_add_type_var,
            value=1,
        )

        # Create `field add` dialog's radio button for `Extended String` field
        # type
        self._field_add_type_v_extstr_rbutton = Radiobutton(
            master=self._field_add_type_rbuttons_frame,
            text='Extended String',
            variable=self._field_add_type_var,
            value=2,
        )

        # Set `field add` dialog's radio button variable's initial value
        self._field_add_type_var.set(1)

        # Bind widget event handlers
        self._widget_bind()

        # Update widget
        self._widget_update()

        # Go to root key path
        self._path_nav.go_to_root()

    def _widget_bind(self):
        """
        Bind widget event handlers.

        @return: None.
        """
        # Path bar textfield adds text change event handler
        self._path_bar.handler_add(
            self._path_bar.TEXT_CHANGE_DONE,
            self._path_bar_on_text_change
        )

        # Path bar textfield adds navigator path change event handler
        self._path_nav.handler_add(
            self._path_nav.PATH_CHANGE_DONE,
            self._path_bar_on_nav_path_change
        )

        # Child keys listbox adds click event handler
        self._child_keys_listbox.handler_add(
            '<Button-1>',
            self._child_keys_listbox_on_click
        )

        # Child keys listbox adds double click event handler
        self._child_keys_listbox.handler_add(
            '<Double-Button-1>',
            self._child_keys_listbox_on_double_click
        )

        # Child keys listbox adds right click event handler
        self._child_keys_listbox.handler_add(
            '<Button-3>',
            self._child_keys_listbox_on_right_click
        )

        # Child keys listbox adds navigator path change event handler
        self._path_nav.handler_add(
            self._path_nav.PATH_CHANGE_DONE,
            self._child_keys_listbox_on_nav_path_change
        )

        # Fields listbox adds navigator path change event handler
        self._path_nav.handler_add(
            self._path_nav.PATH_CHANGE_DONE,
            self._fields_listbox_on_nav_pathcur_change
        )

        # Field editor adds `fields listbox items change` event handler
        self._fields_listbox.handler_add(
            self._fields_listbox.ITEMS_CHANGE_DONE,
            self._field_editor_update
        )

        # Field editor adds `fields listbox itemcur change` event handler
        self._fields_listbox.handler_add(
            self._fields_listbox.ITEMCUR_CHANGE_DONE,
            self._field_editor_update
        )

        # `Field add label` adds click event handler
        self._field_add_label.bind(
            '<Button-1>',
            self._field_add_label_on_click,
        )

        # `Field add label` adds click release event handler
        self._field_add_label.bind(
            '<ButtonRelease-1>',
            self._field_add_label_on_click_release,
        )

        # `Field add label` adds `child keys listbox items change` event
        # handler
        self._child_keys_listbox.handler_add(
            self._child_keys_listbox.ITEMS_CHANGE_DONE,
            self._field_add_label_update,
        )

        # `Field add label` adds `child keys listbox indexcur change` event
        # handler
        self._child_keys_listbox.handler_add(
            self._child_keys_listbox.ITEMCUR_CHANGE_DONE,
            self._field_add_label_update,
        )

        # `Field delete label` adds click event handler
        self._field_del_label.bind(
            '<Button-1>',
            self._field_del_label_on_click,
        )

        # `Field delete label` adds click release event handler
        self._field_del_label.bind(
            '<ButtonRelease-1>',
            self._field_del_label_on_click_release,
        )

        # `Field delete label` adds `fields listbox items change` event handler
        self._fields_listbox.handler_add(
            self._fields_listbox.ITEMS_CHANGE_DONE,
            self._field_del_label_update,
        )

        # `Field delete label` adds `fields listbox indexcur change` event
        # handler
        self._fields_listbox.handler_add(
            self._fields_listbox.ITEMCUR_CHANGE_DONE,
            self._field_del_label_update
        )

        # `Field load label` adds click event handler
        self._field_load_label.bind(
            '<Button-1>',
            self._field_load_label_on_click,
        )

        # `Field load label` adds click release event handler
        self._field_load_label.bind(
            '<ButtonRelease-1>',
            self._field_load_label_on_click_release,
        )

        # `Field save label` adds click event handler
        self._field_save_label.bind(
            '<Button-1>',
            self._field_save_label_on_click,
        )

        # `Field save label` adds click release event handler
        self._field_save_label.bind(
            '<ButtonRelease-1>',
            self._field_save_label_on_click_release,
        )

    def _widget_update(self):
        """
        Update widget config and layout.

        @return: None.
        """

        # Configure layout weights for children.
        # Row 0 is for path bar.
        self.widget().rowconfigure(0, weight=0)

        # Row 1 is for child keys listbox, fields listbox, and field editor
        self.widget().rowconfigure(1, weight=1)

        # Column 0 is for child keys listbox
        self.widget().columnconfigure(0, weight=1, uniform='a')

        # Column 1 is for fields listbox
        self.widget().columnconfigure(1, weight=1, uniform='a')

        # Column 2 is for field editor
        self.widget().columnconfigure(2, weight=2, uniform='a')

        # Create path bar frame
        self._path_bar_frame = Frame(master=self.widget())

        # Lay out path bar frame
        self._path_bar_frame.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky='NSEW',
        )

        # Configure layout weights for children.
        # Use only one row.
        self._path_bar_frame.rowconfigure(0, weight=1)

        # Column 0 is for path bar label
        self._path_bar_frame.columnconfigure(0, weight=0)

        # Column 1 is for path bar textfield
        self._path_bar_frame.columnconfigure(1, weight=1)

        # Create path bar label
        self._path_bar_label = Label(master=self.widget())

        # Configure path bar label
        self._path_bar_label.config(text='Key:')

        # Lay out path bar label
        self._path_bar_label.grid(
            in_=self._path_bar_frame,
            row=0,
            column=0,
            sticky='NSEW',
        )

        # Raise path bar textfield's z-index
        self._path_bar.tkraise()

        # Lay out path bar textfield
        self._path_bar.grid(
            in_=self._path_bar_frame,
            row=0,
            column=1,
            sticky='NSEW',
        )

        # Create child keys labelframe
        self._child_keys_labelframe = LabelFrame(master=self.widget())

        # Configure child keys labelframe
        self._child_keys_labelframe.config(text='Child Keys')

        # Lay out child keys labelframe
        self._child_keys_labelframe.grid(
            in_=self.widget(),
            row=1,
            column=0,
            sticky='NSEW',
        )

        # Configure layout weights for children.
        # Use only one row.
        self._child_keys_labelframe.rowconfigure(0, weight=1)

        # Use only one column.
        self._child_keys_labelframe.columnconfigure(0, weight=1)

        # Raise child keys listbox's z-index
        self._child_keys_listbox.tkraise()

        # Lay out child keys listbox
        self._child_keys_listbox.grid(
            in_=self._child_keys_labelframe,
            row=0,
            column=0,
            sticky='NSEW',
        )

        # Create fields labelframe
        self._fields_labelframe = LabelFrame(master=self.widget())

        # Configure fields labelframe
        self._fields_labelframe.config(text='Fields')

        # Lay out fields labelframe
        self._fields_labelframe.grid(
            in_=self.widget(),
            row=1,
            column=1,
            sticky='NSEW',
        )

        # Configure layout weights for children.
        # Row 0 is for field add label and field delete label.
        self._fields_labelframe.rowconfigure(0, weight=0)

        # Row 1 is for fields listbox
        self._fields_labelframe.rowconfigure(1, weight=1)

        # Use only one column
        self._fields_labelframe.columnconfigure(0, weight=1)

        # Raise fields listbox's z-index
        self._fields_listbox.tkraise()

        # Lay out fields listbox
        self._fields_listbox.grid(
            in_=self._fields_labelframe,
            row=1,
            column=0,
            sticky='NSEW',
        )

        # Raise field add label's z-index
        self._field_add_label.tkraise()

        # Lay out field add label
        self._field_add_label.grid(
            in_=self._fields_labelframe,
            row=0,
            column=0,
            sticky='W',
        )

        # Raise field delete label's z-index
        self._field_del_label.tkraise()

        # Lay out field delete label
        self._field_del_label.grid(
            in_=self._fields_labelframe,
            row=0,
            column=0,
            sticky='W',
            # Add left padding to appear as the second label in the row
            padx=(40, 0),
        )

        # Create field editor labelframe
        self._field_editor_labelframe = LabelFrame(master=self.widget())

        # Lay out field editor labelframe
        self._field_editor_labelframe.grid(
            in_=self.widget(),
            row=1,
            column=2,
            sticky='NSEW',
        )

        # Configure layout weights for children.
        # Row 0 is for field load label and field save label.
        self._field_editor_labelframe.rowconfigure(0, weight=0)

        # Row 1 is for field editor
        self._field_editor_labelframe.rowconfigure(1, weight=1)

        # Use only one column
        self._field_editor_labelframe.columnconfigure(0, weight=1)

        # Raise field load label's z-index
        self._field_load_label.tkraise()

        # Lay out field load label
        self._field_load_label.grid(
            in_=self._field_editor_labelframe,
            row=0,
            column=0,
            sticky='W',
        )

        # Raise field save label's z-index
        self._field_save_label.tkraise()

        # Lay out field save label
        self._field_save_label.grid(
            in_=self._field_editor_labelframe,
            row=0,
            column=0,
            sticky='W',
            # Add left padding to appear as the second label in the row
            padx=(40, 0),
        )

        # Configure layout weights for children.
        # Row 0 is for field name.
        self._field_add_frame.rowconfigure(0, weight=0)

        # Row 1 is for field type.
        self._field_add_frame.rowconfigure(1, weight=0)

        # Column 0 is for prompt labels
        self._field_add_frame.columnconfigure(0, weight=0)

        # Column 1 is for textfield and radio buttons.
        self._field_add_frame.columnconfigure(1, weight=1)

        # Configure `field add` dialog's field name prompt label
        self._field_add_name_label.config(text='Field Name:')

        # Lay out `field add` dialog's field name prompt label
        self._field_add_name_label.grid(
            in_=self._field_add_frame,
            row=0,
            column=0,
            sticky='NSEW',
        )

        # Lay out `field add` dialog's field name textfield
        self._field_add_name_textfield.grid(
            in_=self._field_add_frame,
            row=0,
            column=1,
            sticky='NSEW',
            padx=(5, 0)
        )

        # Configure `field add` dialog's field type prompt label
        self._field_add_type_label.config(text='Field Type:')

        # Lay out `field add` dialog's field type prompt label
        self._field_add_type_label.grid(
            in_=self._field_add_frame,
            row=1,
            column=0,
            sticky='NSEW',
        )

        # Lay out `field add` dialog's field type radio buttons frame
        self._field_add_type_rbuttons_frame.grid(
            in_=self._field_add_frame,
            row=1,
            column=1,
            sticky='NSEW',
        )

        # Lay out `field add` dialog's `String` field type radio button
        self._field_add_type_v_string_rbutton.grid(
            in_=self._field_add_type_rbuttons_frame,
            row=0,
            column=0,
            sticky='W',
        )

        # Lay out `field add` dialog's `Extended String` field type radio
        # button
        self._field_add_type_v_extstr_rbutton.grid(
            in_=self._field_add_type_rbuttons_frame,
            row=0,
            column=1,
            sticky='W',
        )

        # Set `field add` dialog's view widget
        self._field_add_dialog.view_set(self._field_add_frame)

        # Set `field add` dialog's title
        self._field_add_dialog.title('Create field')

    def _path_nav_goto(self, path):
        """
        Go to registry key path. Show error dialog if failed.

        @param path: Registry key path to go to.

        @return: Whether successful.
        """
        #
        try:
            # Set path navigator to go to given key path
            self._path_nav.go_to_path(path, check=True)

        # If have error
        except ValueError:
            # Show error dialog
            messagebox.showwarning(
                'Error',
                'Cannot open key: `{}`.'.format(path)
            )

            # Return not successful
            return False

        # If have no error,
        # return successful
        return True

    def _path_bar_update(self):
        """
        Update registry key path bar.

        @return: None.
        """
        # Get path bar's registry key path
        key_path = self._path_bar.text()

        # If the registry key path not exists
        if not regkey_exists(key_path):
            # Set path bar label's state to disabled
            self._path_bar_label.config(state=DISABLED)

        # If the registry key path exists
        else:
            # Set path bar label's state to normal
            self._path_bar_label.config(state=NORMAL)

    def _path_bar_on_text_change(self):
        """
        Registry key path bar's text change event handler.

        @return: None.
        """
        # Update path bar
        self._path_bar_update()

        # Get path bar's registry key path
        key_path = self._path_bar.text()

        # If the registry key path exists
        if regkey_exists(key_path):
            # Set path navigator to go to the registry key path
            self._path_nav_goto(key_path)

        # If the registry key path not exists,
        # do nothing.

    def _path_bar_on_nav_path_change(self):
        """
        Registry key path bar's `path navigator path change` event handler.

        @return: None.
        """
        # If the path bar is changing
        if self._path_bar.is_changing():
            # Do nothing to avoid circular call
            return

        # If the path bar is not changing.

        # Get the path navigator's key path
        nav_key_path = self._path_nav.path()

        # If the path navigator's key path is not EQ the path bar's key path
        if nav_key_path != self._path_bar.text():
            # Update the path bar's text
            self._path_bar.text_set(text=nav_key_path, notify=False)

            # Update the path bar
            self._path_bar_update()

    def _child_keys_listbox_indexcur_remember(self):
        """
        Remember active registry key path's child keys listbox active index.

        @return: None.
        """
        # Get the path navigator's active registry key path
        key_path = self._path_nav.path()

        # Get child keys listbox's active index
        indexcur = self._child_keys_listbox.indexcur()

        # If the active registry key path is not root path,
        # and the child keys listbox's active item is `go up` (see 6PMTJ)
        if key_path != self._path_nav.ROOT and indexcur == 0:
            # Do not remember
            return
        else:
            # Remember the child keys listbox active index
            self._child_keys_listbox_indexcur_memo[key_path] = indexcur

    def _child_keys_listbox_indexcur_recover(self):
        """
        Recover active registry key path's child keys listbox active index.

        @return: None.
        """
        # Get active registry key path
        key_path = self._path_nav.path()

        # Get remembered child keys listbox active index for the active
        # registry key path
        memo_index = self._child_keys_listbox_indexcur_memo.get(key_path, None)

        # If have no remembered child keys listbox active index
        if memo_index is None:
            # Do nothing
            return

        # If have remembered child keys listbox active index.

        # Get child keys listbox last index
        index_last = self._child_keys_listbox.index_last()

        # If the remembered active index is EQ child keys listbox's active
        # index
        if memo_index == self._child_keys_listbox.indexcur():
            # Do noting
            return

        # If the remembered active index is GT the last index,
        # it means the remembered active index is no longer valid.
        elif memo_index > index_last:
            try:
                # Delete the remembered active index
                del self._child_keys_listbox_indexcur_memo[key_path]
            # If have KeyError
            except KeyError:
                # Ignore
                pass

        # If the remembered active index is not GT the last index
        else:
            # Set child keys listbox to the remembered active index
            self._child_keys_listbox.indexcur_set(
                memo_index,
                notify=True
            )

    def _child_keys_listbox_on_click(self, event):
        # Remember active registry key path's child keys listbox active index
        self._child_keys_listbox_indexcur_remember()

    def _child_keys_listbox_on_double_click(self, event):
        """
        Child keys listbox double click event handler.

        @param event: Tkinter event object.

        @return: None.
        """
        # Remember active registry key path's child keys listbox active index
        self._child_keys_listbox_indexcur_remember()

        # Get active key path
        old_key_path = self._path_nav.path()

        # If double clicked item is `go up` (see 6PMTJ)
        if old_key_path != self._path_nav.ROOT \
                and self._child_keys_listbox.indexcur() == 0:
            # Go to parent key path
            success = self._path_nav_goto(self._path_nav.parent_path())

            # If have success
            if success:
                # Get old key name
                _, _, old_key_name = old_key_path.rpartition('\\')

                # If the old key name is not empty
                if old_key_name:
                    # For each child key names in the child keys listbox
                    for index, child_key_name in enumerate(
                            self._child_keys_listbox.items()):
                        # If the child key name is EQ the old key name
                        if child_key_name == old_key_name:
                            # Set the index to active
                            self._child_keys_listbox.indexcur_set(
                                index=index,
                                notify=True,
                            )

                            # Stop finding
                            break

            # If have no success,
            # do nothing.

        # If double clicked item is not `go up` (see 6PMTJ)
        else:
            # Get child key name
            child_key_name = self._child_keys_listbox.itemcur()

            # Get child key path
            child_key_path = self._path_nav.child_path(child_key_name)

            # Go to the child key path
            self._path_nav_goto(child_key_path)

    def _child_keys_listbox_on_right_click(self, event):
        """
        Child keys listbox right click event handler.

        @param event: Tkinter event object.

        @return: None.
        """
        # Get active key path
        key_path = self._path_nav.path()

        # If the active key path is not root key path
        if key_path != self._path_nav.ROOT:
            # Go to parent key path
            self._path_nav_goto(self._path_nav.parent_path())

        # If the active key path is root key path,
        # do nothing.

    def _child_keys_listbox_on_nav_path_change(self):
        """
        Child keys listbox's `path navigator path change` event handler.

        @return: None.
        """
        # Get active key path
        key_path = self._path_nav.path()

        # Get path navigator's child key names
        child_key_name_s = self._path_nav.child_names()

        # If child key names is None,
        # it means failed opening the key.
        if child_key_name_s is None:
            # Show error dialog
            messagebox.showwarning(
                'Error',
                'Cannot read child keys of key: `{}`'.format(key_path)
            )

            # Set child key names to empty
            child_key_name_s = []

        # If child key names is not None
        else:
            # Copy the child key names to a new list
            child_key_name_s = list(child_key_name_s)

        # Get status message
        status_msg = 'Key: `{}`'.format(key_path)

        # Set status message to status bar
        self._status_bar_set(status_msg)

        # Sort child key names
        child_key_name_s = list(
            sorted(child_key_name_s, key=(lambda x: x.lower()))
        )

        # 6PMTJ
        # If the active key path is not root path
        if key_path != self._path_nav.ROOT:
            # Insert `go up` item to the child key names list
            child_key_name_s.insert(0, '..')

        # If the active key path is root path,
        # do not insert `go up` item.

        # Set the child key names to child keys listbox
        self._child_keys_listbox.items_set(child_key_name_s, notify=True)

        # Recover remembered active index
        self._child_keys_listbox_indexcur_recover()

    def _fields_listbox_on_nav_pathcur_change(self):
        """
        Fields listbox's `path navigator path change` event handler.

        @return: None.
        """
        # Get active key path
        key_path = self._path_nav.path()

        # For each permission mask from lager permission to smaller permission
        for mask in [KEY_ALL_ACCESS, KEY_WRITE, KEY_READ]:
            # Try getting RegKey object with the permission mask
            regkey = regkey_get(path=key_path, mask=mask)

            # If have success
            if regkey is not None:
                # Stop trying
                break

        # If the RegKey object is None,
        # it means the key path can not be opened.
        if regkey is None:
            # Show error dialog
            messagebox.showwarning(
                'Error',
                'Cannot read fields of key: `{}`'.format(key_path)
            )

            # Set fields listbox to empty
            self._fields_listbox.items_set([], notify=True)

        # If the RegKey object is not None.
        else:
            # Get the registry key's fields
            field_s = regkey.fields()

            # If the registry key have fields
            if field_s:
                # Sort the fields by field name
                field_s = list(
                    sorted(field_s, key=(lambda x: x.name().lower()))
                )

                # Set the fields to the fields listbox
                self._fields_listbox.items_set(field_s, notify=True)

                # Set fields listbox's indexcur to 0
                self._fields_listbox.indexcur_set(0, notify=True)
            else:
                # Set fields listbox to empty
                self._fields_listbox.items_set([], notify=True)

    def _field_editor_update(self):
        """
        Update field editor.

        @return: None.
        """
        # Get old field editor
        old_field_editor = self._field_editor

        # Get fields listbox's active registry field
        field = self._fields_listbox.itemcur()

        # 5WMYV
        # Create new field editor.
        # Notice the factory function may return the old editor object.
        self._field_editor = self._field_editor_factory(
            field=field,
            old_editor=old_field_editor,
            master=self._field_editor_labelframe,
        )

        # Set enabled flag on
        is_enabled = True

        # Field data.
        # Use `None.__class__` to distinguish with None returned at 5GN0P.
        field_data = None.__class__

        # If have no active registry field
        if field is None:
            # Set enabled flag off
            is_enabled = False

        # If have active registry field
        else:
            # Get active key path
            key_path = self._path_nav.path()

            # Get status message
            status_msg = 'Key: `{}->{}`'.format(key_path, field.name())

            # Set status message to status bar
            self._status_bar_set(status_msg)

            # Test whether the field is supported by the field editor
            is_enabled = self._field_editor.field_is_supported(field)

            # If the field is supported by the field editor
            if is_enabled:
                # 5GN0P
                # Read field data from registry
                field_data = field.data()

                # If field data is None
                if field_data is None:
                    # Set enabled flag off
                    is_enabled = False
                else:
                    # Set enabled flag on
                    is_enabled = True

            # If the field is not supported by the field editor,
            # no need read field data from registry.

        # If enabled flag is on
        if is_enabled:
            # Get field editor labelframe's label
            labelframe_text = 'Field `{}`'.format(field.name())

            # Set field editor labelframe's label
            self._field_editor_labelframe.config(text=labelframe_text)

            # Set field editor to enabled
            self._field_editor.enable(True)

            # Set field editor data
            self._field_editor.data_set(field_data)

            # Set field load label's state to normal
            self._field_load_label.config(state=NORMAL)

            # Set field save label's state to normal
            self._field_save_label.config(state=NORMAL)

        # If enabled flag is off
        else:
            # Set field editor labelframe's label
            self._field_editor_labelframe.config(text='Field')

            # Set field editor data to empty
            self._field_editor.data_set('')

            # Set field editor to disabled
            self._field_editor.enable(False)

            # Set field load label's state to disabled
            self._field_load_label.config(state=DISABLED)

            # Set field save label's state to disabled
            self._field_save_label.config(state=DISABLED)

        # Lay out field editor
        self._field_editor.widget().grid(
            in_=self._field_editor_labelframe,
            row=1,
            column=0,
            columnspan=2,
            sticky='NSEW',
            pady=(0, 10),
        )

        # If old field editor is not new field editor
        if old_field_editor is not self._field_editor:
            # If old field editor is not None
            if old_field_editor is not None:
                # Destroy old field editor
                old_field_editor.destroy()

        # If failed reading field data at 5GN0P
        if field_data is None:
            # Show error dialog
            messagebox.showwarning(
                'Error',
                'Failed reading field data.'
            )

    def _field_add_label_update(self):
        """
        Update field add label.

        @return: None.
        """
        # If active key path is root key path
        if self._path_nav.path() == self._path_nav.ROOT:
            # Set field add label's state to disabled
            self._field_add_label.config(state=DISABLED)

        # If active key path is not root key path
        else:
            # Set field add label's state to normal
            self._field_add_label.config(state=NORMAL)

    def _field_add_label_on_click(self, event):
        """
        Field add label click event handler.

        @event: Tkinter event object.

        @return: None.
        """
        # If field add label is in disabled state
        if self._field_add_label.instate([DISABLED]):
            # Do nothing
            return

        # If field add label is not in disabled state
        else:
            # Set field add label's state to active
            self._field_add_label.config(state=ACTIVE)

    def _field_add_label_on_click_release(self, event):
        """
        Field add label click release event handler.

        @event: Tkinter event object.

        @return: None.
        """
        # If field add label is in disabled state
        if self._field_add_label.instate([DISABLED]):
            # Do nothing
            return

        # If field add label is not in disabled state.

        # Set field add label's state to normal
        self._field_add_label.config(state=NORMAL)

        # If active key path is root key path
        if self._path_nav.path() == self._path_nav.ROOT:
            # Do nothing
            return

        # If active key path is not root key path.

        # Get active key path's RegKey object
        regkey = self._path_nav.regkey()

        # If have no RegKey object,
        # it means the active key path is not accessible
        if regkey is None:
            # Do nothing
            return

        # If have RegKey object.

        # Create confirm button event handler
        def confirm_handler():
            """
            `field add` dialog's confirm button event handler.

            @return: None.
            """
            # Get field name.
            # Notice empty string is valid field name.
            field_name = self._field_add_name_textfield.text()

            # Get field type
            field_type = self._field_add_type_var.get()

            # If the field type is not valid.
            # 1: String.
            # 2: Extended String.
            if field_type not in [1, 2]:
                # Raise error
                raise ValueError(field_type)

            # If the field type is valid.

            # For each field in fields listbox
            for field in self._fields_listbox.items():
                # If the field name exists
                if field.name().lower() == field_name.lower():
                    # Show error dialog
                    messagebox.showwarning(
                        'Error',
                        'Field name exists: `{}`.'.format(field_name)
                    )

                    # Ignore.
                    # Notice the `field add` dialog is still showing.
                    return

            # If the field name not exists.

            # Create registry field
            success = regkey.field_write(
                name=field_name,
                type=field_type,
                data='',
            )

            # If have no success
            if not success:
                # Show error dialog
                messagebox.showwarning(
                    'Error',
                    'Failed creating field: `{}`.'.format(field_name)
                )

                # Notice the `field add` dialog is still showing.

            # If have success
            else:
                # Update fields listbox
                self._fields_listbox_on_nav_pathcur_change()

                # For each field in fields listbox
                for index, field in enumerate(self._fields_listbox.items()):
                    # If the field's name is EQ the newly created field name
                    if field.name().lower() == field_name.lower():
                        # Set the index to active
                        self._fields_listbox.indexcur_set(
                            index=index,
                            notify=True,
                        )

                        # Stop finding
                        break

                # Hide `field add` dialog
                self._field_add_dialog.withdraw()

                # Release focus grab on `field add` dialog
                self._field_add_dialog.grab_release()

        # Set field name textfield to empty
        self._field_add_name_textfield.text_set('')

        # Set focus on the field name textfield
        self._field_add_name_textfield.text_widget().focus()

        # Set field type to `String`
        self._field_add_type_var.set(1)

        # Set confirm handler
        self._field_add_dialog.confirm_handler_set(confirm_handler)

        # Set focus grab on `field add` dialog
        self._field_add_dialog.grab_set()

        # Show `field add` dialog
        self._field_add_dialog.deiconify()

        # Center `field add` dialog around the main window
        center_window(
            self._field_add_dialog.toplevel(),
            point=get_window_center(self.widget().winfo_toplevel()),
        )

    def _field_del_label_update(self):
        """
        Update field delete label.

        @return: None.
        """
        # If fields listbox has not active index
        if self._fields_listbox.indexcur() == -1:
            # Set field delete label's state to disabled
            self._field_del_label.config(state=DISABLED)

        # If fields listbox has active index
        else:
            # Set field delete label's state to normal
            self._field_del_label.config(state=NORMAL)

    def _field_del_label_on_click(self, event):
        """
        Field delete label click event handler.

        @event: Tkinter event object.

        @return: None.
        """
        # If field delete label is in disabled state
        if self._field_del_label.instate([DISABLED]):
            # Do nothing
            return

        # If field delete label is not in disabled state
        else:
            # Set field delete label's state to active
            self._field_del_label.config(state=ACTIVE)

    def _field_del_label_on_click_release(self, event):
        """
        Field delete label click release event handler.

        @event: Tkinter event object.

        @return: None.
        """
        # If field delete label is in disabled state
        if self._field_del_label.instate([DISABLED]):
            # Do nothing
            return

        # If field delete label is not in disabled state.

        # Set field delete label's state to normal
        self._field_del_label.config(state=NORMAL)

        # Get active field
        field = self._fields_listbox.itemcur()

        # If have no active field
        if field is None:
            # Ignore the click event
            return

        # If have active field.

        # Get field name
        field_name = field.name()

        # Show confirmation dialog
        is_confirmed = messagebox.askokcancel(
            title='Delete field'.format(field_name),
            message='Delete field `{}`?'.format(field_name)
        )

        # If the operation is canceled
        if not is_confirmed:
            # Do nothing
            return

        # If the operation is not canceled.

        # Get old active index
        old_indexcur = self._fields_listbox.indexcur()

        # Delete the registry field
        success = field.delete()

        # If have no success
        if not success:
            # Show error dialog
            messagebox.showwarning(
                'Error',
                'Failed deleting field `{}`.'.format(field_name)
            )

        # If have success
        else:
            # Update fields listbox
            self._fields_listbox_on_nav_pathcur_change()

            # Get fields listbox's last index
            index_last = self._fields_listbox.index_last()

            # If old active index is not valid
            if old_indexcur > index_last:
                # Use last index as new active index
                indexcur = index_last

            # If old active index is valid
            else:
                # Use old indexcur as new active index
                indexcur = old_indexcur

            # Set new indexcur
            self._fields_listbox.indexcur_set(
                indexcur,
                notify=True,
            )

    def _field_load_label_on_click(self, event):
        """
        Field load label click event handler.

        @event: Tkinter event object.

        @return: None.
        """
        # If field load label is in disabled state
        if self._field_load_label.instate([DISABLED]):
            # Do nothing
            return

        # If field load label is not in disabled state
        else:
            # Set field load label's state to active
            self._field_load_label.config(state=ACTIVE)

    def _field_load_label_on_click_release(self, event):
        """
        Field load label click release event handler.

        @event: Tkinter event object.

        @return: None.
        """
        # If field load label is in disabled state
        if self._field_load_label.instate([DISABLED]):
            # Do nothing
            return

        # If field load label is not in disabled state.
        else:
            # Set field load label's state to normal
            self._field_load_label.config(state=NORMAL)

            # Update field editor
            self._field_editor_update()

    def _field_save_label_on_click(self, event):
        """
        Field save label click event handler.

        @event: Tkinter event object.

        @return: None.
        """
        # If field save label is in disabled state
        if self._field_save_label.instate([DISABLED]):
            # Do nothing
            return

        # If field save label is not in disabled state
        else:
            # Set field save label's state to active
            self._field_save_label.config(state=ACTIVE)

    def _field_save_label_on_click_release(self, event):
        """
        Field save label click release event handler.

        @event: Tkinter event object.

        @return: None.
        """
        # If field save label is in disabled state
        if self._field_save_label.instate([DISABLED]):
            # Do nothing
            return

        # If field save label is not in disabled state.

        # Set field save label's state to normal
        self._field_save_label.config(state=NORMAL)

        # Get fields listbox's active field
        field = self._fields_listbox.itemcur()

        # If have no active field
        if field is None:
            # Do nothing
            return

        # If have active field
        else:
            try:
                # Get field editor data
                data = self._field_editor.data()

                # Write data to registry field
                field.data_set(data=data)

            # If have error
            except Exception:
                # Show error dialog
                messagebox.showwarning(
                    'Error',
                    "Failed writing data to registry."
                )

    def menutree_create(self, specs, id_sep=None):
        """
        Create menu tree by specs.

        @param specs: A list of spec dicts. Each spec dict can have these keys:
        - pid: Parent menu item ID.

        - id: Item ID.

        - type: Item type, one of ['menu', 'separator', 'command'].
          Default is `command`.

        - id_is_full: Whether `id` is full ID. Default is False.
          If `id` is not full ID, the full ID is generated by concatenating
          `pid`, `id_sep`, and `id`.

        - label': Item label. Default is use `id` value.

        - key: Registry key path. Used if `type` is 'command'.
          The registry key path can contain a field name pointer `->` (see
          2T5EK).

        @param id_sep: ID parts separator used when converting a relative ID to
        full ID. Default is `/`.

        @return: MenuTree object.
        """
        # Create menu tree
        menutree = MenuTree(master=self.widget())

        # ID parts separator
        id_sep = id_sep if id_sep is not None else '/'

        # For each spec dict
        for spec in specs:
            # Get item type.
            # Default is `command`.
            item_type = spec.get('type', 'command')

            # Get item PID
            pid = spec['pid']

            # Get item ID
            id = spec['id']

            # Get whether item ID is full ID.
            # Default is False.
            id_is_full = spec.get('id_is_full', False)

            # Get item label.
            # Default is use `id` value.
            label = spec.get('label', id)

            # If the item type is `menu`
            if item_type == 'menu':
                # Create menu item
                menutree.add_menu(
                    pid=pid,
                    id=id,
                    id_is_full=id_is_full,
                    id_sep=id_sep,
                    label=label,
                )

            # If the item type is `separator`
            elif item_type == 'separator':
                # Create separator item
                menutree.add_separator(
                    pid=pid,
                    id=id,
                    id_is_full=id_is_full,
                )

            # If the item type is `command`
            elif item_type == 'command':
                # Get registry key path
                key_path = spec.get('key', None)

                # If registry key path is not given
                if key_path is None:
                    # Use given item ID as registry key path
                    key_path = id

                # Get whether item ID is full ID.
                # Default is False.
                id_is_full = spec.get('id_is_full', False)

                # Get menu item label.
                # Default is use full item ID.
                label = spec.get('label', None)

                # 2T5EK
                # If the key path contains field name pointer `->`
                if key_path.find('->') != -1:
                    # Split the key path to real key path and field name
                    key_path, _, field_name = key_path.partition('->')

                # If the key path not contains field name pointer `->`
                else:
                    # Set field name to None
                    field_name = None

                # Create click event handler
                def on_click(
                    key_path=key_path,
                    field_name=field_name,
                ):
                    """
                    Command item's click event handler.

                    @param key_path: Registry key path.

                    @param field_name: Registry key's field name.

                    @return: None.
                    """
                    # Go to the key path
                    success = self._path_nav_goto(key_path)

                    # If have no success
                    if not success:
                        # Ignore
                        return

                    # If have success.

                    # If field name is specified in the spec
                    if field_name is not None:
                        # For each field in fields listbox
                        for index, field in enumerate(
                            self._fields_listbox.items()
                        ):
                            # If the field's name is EQ field name in the spec
                            if field.name().lower() == field_name.lower():
                                # Set the index to active
                                self._fields_listbox.indexcur_set(
                                    index,
                                    focus=True,
                                    notify=True,
                                )

                                # Stop finding
                                break

                    # If field name is not specified in the spec,
                    # no need set active item for fields listbox.

                # Create command item
                menutree.add_command(
                    pid=pid,
                    id=id,
                    command=on_click,
                    id_is_full=id_is_full,
                    id_sep=id_sep,
                    label=label,
                )

            # If the item type is something else
            else:
                # Raise error
                raise ValueError(item_type)

        # Return the menu tree
        return menutree
