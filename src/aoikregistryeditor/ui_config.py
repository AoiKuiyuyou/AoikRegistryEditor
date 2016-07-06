# coding: utf-8
#
from __future__ import absolute_import

import os.path
from tkinter import PhotoImage
from tkinter.ttk import Sizegrip
from tkinter.ttk import Style

import aoikregistryeditor.static


#
def configure_ui(info):
    """
    UI config function.

    @param info: UI config info dict.

    @return: None.
    """
    # Background color
    bg_color = 'white smoke'

    # Create ttk style object
    STYLE = Style()

    # Configure TFrame style's background
    STYLE.configure(
        'TFrame',
        background=bg_color,
    )

    # Configure TLabelframe style's background
    STYLE.configure(
        'TLabelframe',
        background=bg_color,
    )

    # Configure TLabelframe.Label style's background
    STYLE.configure(
        'TLabelframe.Label',
        background=bg_color,
    )

    # Configure TLabel style's background
    STYLE.configure(
        'TLabel',
        background=bg_color,
    )

    # Configure TRadiobutton style's background
    STYLE.configure(
        'TRadiobutton',
        background=bg_color,
    )

    # Get TK root window
    tk = info['tk']

    # Set window title
    tk.title('AoikRegistryEditor')

    # Set window geometry
    tk.geometry('1280x720')

    # Configure layout weights for children.
    # Row 0 is for registry editor.
    tk.rowconfigure(0, weight=1)

    # Row 1 is for status bar
    tk.rowconfigure(1, weight=0)

    # Use only one column
    tk.columnconfigure(0, weight=1)

    # Get menu tree
    menutree = info['menutree']

    # Add `File` menu
    menutree.add_menu(pid='/', id='File', index=0)

    # Add `Exit` command
    menutree.add_command(pid='/File', id='Exit', command=tk.quit)

    # Get status bar label
    status_bar_label = info['status_bar_label']

    # Set status bar label's main frame's height
    status_bar_label.widget().config(height=20)

    # Set status bar label's background
    status_bar_label.config(background='#F0F0F0')

    # Lay out the status bar label
    status_bar_label.grid(
        in_=tk,
        row=2,
        column=0,
        sticky='NSEW',
        padx=(5, 0),
    )

    # Create size grip
    sizegrip = Sizegrip(master=tk)

    # Lay out the size grip
    sizegrip.grid(
        in_=tk,
        row=2,
        column=0,
        sticky='E',
    )

    # Get registry editor
    editor = info['editor']

    # Lay out the registry editor
    editor.grid(
        row=0,
        column=0,
        sticky='NSEW',
    )

    # Set registry editor's inner padding
    editor.config(padding=10)

    # Get path bar label
    path_bar_label = info['path_bar_label']

    # Get static files' directory path
    static_dir = os.path.dirname(
        os.path.abspath(aoikregistryeditor.static.__file__)
    )

    # Get path bar label's normal state image file path
    image_path = os.path.join(static_dir, 'path_bar_label_normal.png')

    # Load path bar label's normal state image file
    path_bar_label._normal_image = PhotoImage(file=image_path)

    # Get path bar label's disabled state image file path
    image_path = os.path.join(static_dir, 'path_bar_label_disabled.png')

    # Load path bar label's disabled state image file
    path_bar_label._disabled_image = PhotoImage(file=image_path)

    # Set path bar label's images
    path_bar_label.config(
        image=(
            path_bar_label._normal_image,
            'disabled', path_bar_label._disabled_image,
        )
    )

    # Get path bar textfield
    path_bar = info['path_bar']

    # Set path bar textfield's font
    path_bar.config(font=('Consolas', 12))

    # Set path bar textfield's outer padding
    path_bar.grid(padx=(3, 0))

    # Get child keys labelframe
    child_keys_labelframe = info['child_keys_labelframe']

    # Set child keys labelframe's outer padding
    child_keys_labelframe.grid(pady=(5, 0))

    # Set child keys labelframe's inner padding
    child_keys_labelframe.config(padding=5)

    # Get child keys listbox
    child_keys_listbox = info['child_keys_listbox']

    # Set child keys listbox's font
    child_keys_listbox.config(font=('Consolas', 12))

    # Get fields labelframe
    fields_labelframe = info['fields_labelframe']

    # Set fields labelframe's outer padding
    fields_labelframe.grid(padx=(10, 0), pady=(5, 0))

    # Set fields labelframe's inner padding
    fields_labelframe.config(padding=5)

    # Get fields listbox
    fields_listbox = info['fields_listbox']

    # Set fields listbox's font
    fields_listbox.config(font=('Consolas', 12))

    # Create event handler to set fields listbox background
    def _fields_listbox_set_background():
        # If fields listbox is not empty
        if fields_listbox.size() > 0:
            # Set background color for non-empty listbox
            fields_listbox.config(background='white')

        # If fields listbox is empty
        else:
            # Set background color for empty listbox
            fields_listbox.config(background='gainsboro')

    # Call the event handler to initialize the background color
    _fields_listbox_set_background()

    # Add the event handler to fields listbox
    fields_listbox.handler_add(
        fields_listbox.ITEMS_CHANGE_DONE,
        _fields_listbox_set_background
    )

    # Get field editor labelframe
    field_editor_labelframe = info['field_editor_labelframe']

    # Set field editor labelframe's outer padding
    field_editor_labelframe.grid(padx=(10, 0), pady=(5, 0))

    # Set field editor labelframe's inner padding
    field_editor_labelframe.config(padding=5)

    # Get field add label
    field_add_label = info['field_add_label']

    # Set field add label's main frame size
    field_add_label.widget().config(width=40, height=40)

    # Get field add label's normal state image file path
    image_path = os.path.join(static_dir, 'field_add_normal.png')

    # Load field add label's normal state image file
    field_add_label._normal_image = PhotoImage(file=image_path)

    # Get field add label's active state image file path
    image_path = os.path.join(static_dir, 'field_add_active.png')

    # Load field add label's active state image file
    field_add_label._active_image = PhotoImage(file=image_path)

    # Get field add label's hover state image file path
    image_path = os.path.join(static_dir, 'field_add_hover.png')

    # Load field add label' hover state image file
    field_add_label._hover_image = PhotoImage(file=image_path)

    # Set field add label's images.
    # Notice `disabled` state is excluded from other states.
    # Notice `active` state takes precedence over `hover` state.
    field_add_label.config(
        image=(
            field_add_label._normal_image,
            '!disabled active', field_add_label._active_image,
            '!disabled hover', field_add_label._hover_image,
        )
    )

    # Get field delete label
    field_del_label = info['field_del_label']

    # Set field delete label's main frame size
    field_del_label.widget().config(width=40, height=40)

    # Get field delete label's normal state image file path
    image_path = os.path.join(static_dir, 'field_del_normal.png')

    # Load field delete label's normal state image file
    field_del_label._normal_image = PhotoImage(file=image_path)

    # Get field delete label's active state image file path
    image_path = os.path.join(static_dir, 'field_del_active.png')

    # Load field delete label's active state image file
    field_del_label._active_image = PhotoImage(file=image_path)

    # Get field delete label's hover state image file path
    image_path = os.path.join(static_dir, 'field_del_hover.png')

    # Load field delete label's hover state image file
    field_del_label._hover_image = PhotoImage(file=image_path)

    # Set field delete label's images.
    # Notice `disabled` state is excluded from other states.
    # Notice `active` state takes precedence over `hover` state.
    field_del_label.config(
        image=(
            field_del_label._normal_image,
            '!disabled active', field_del_label._active_image,
            '!disabled hover', field_del_label._hover_image,
        )
    )

    # Get field load label
    field_load_label = info['field_load_label']

    # Set field load label's main frame size
    field_load_label.widget().config(width=40, height=40)

    # Get field load label's normal state image file path
    image_path = os.path.join(static_dir, 'field_load_normal.png')

    # Load field load label's normal state image file
    field_load_label._normal_image = PhotoImage(file=image_path)

    # Get field load label's active state image file path
    image_path = os.path.join(static_dir, 'field_load_active.png')

    # Load field load label's active state image file
    field_load_label._active_image = PhotoImage(file=image_path)

    # Get field load label's hover state image file path
    image_path = os.path.join(static_dir, 'field_load_hover.png')

    # Load field load label's hover state image file
    field_load_label._hover_image = PhotoImage(file=image_path)

    # Set field load label's images.
    # Notice `disabled` state is excluded from other states.
    # Notice `active` state takes precedence over `hover` state.
    field_load_label.config(
        image=(
            field_load_label._normal_image,
            '!disabled active', field_load_label._active_image,
            '!disabled hover', field_load_label._hover_image,
        )
    )

    # Get field save label
    field_save_label = info['field_save_label']

    # Set field save label's main frame size
    field_save_label.widget().config(width=40, height=40)

    # Get field save label's normal state image file path
    image_path = os.path.join(static_dir, 'field_save_normal.png')

    # Load field save label's normal state image file
    field_save_label._normal_image = PhotoImage(file=image_path)

    # Get field save label's active state image file path
    image_path = os.path.join(static_dir, 'field_save_active.png')

    # Load field save label's active state image file
    field_save_label._active_image = PhotoImage(file=image_path)

    # Get field save label's hover state image file path
    image_path = os.path.join(static_dir, 'field_save_hover.png')

    # Load field save label's hover state image file
    field_save_label._hover_image = PhotoImage(file=image_path)

    # Set field save label's images.
    # Notice `disabled` state is excluded from other states.
    # Notice `active` state takes precedence over `hover` state.
    field_save_label.config(
        image=(
            field_save_label._normal_image,
            '!disabled active', field_save_label._active_image,
            '!disabled hover', field_save_label._hover_image,
        )
    )

    # Get field add dialog
    field_add_dialog = info['field_add_dialog']

    # Set field add dialog's geometry
    field_add_dialog.toplevel().geometry('300x110')

    # Set field add dialog to not resizable
    field_add_dialog.toplevel().resizable(width=False, height=False)

    # Set field add dialog's background
    field_add_dialog.toplevel().config(background=bg_color)

    # Set field add dialog's main frame's outer padding
    field_add_dialog.main_frame().grid(padx=5, pady=5)

    # Set field add dialog's confirm button's outer padding
    field_add_dialog.confirm_button().grid(pady=(15, 0))

    # Set field add dialog's cancel button's outer padding
    field_add_dialog.cancel_button().grid(pady=(15, 0))

    # Set field add dialog's field add type label's outer padding
    editor._field_add_type_label.grid(
        pady=(10, 0),
    )

    # Set field add dialog's field add type radio buttons frame's outer padding
    editor._field_add_type_rbuttons_frame.grid(
        padx=(3, 0),
        pady=(10, 0),
    )
