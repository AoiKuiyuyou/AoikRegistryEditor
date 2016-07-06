# coding: utf-8
#
from __future__ import absolute_import

from tkinter import Toplevel
from tkinter.ttk import Button
from tkinter.ttk import Frame


#
def get_window_center(window):
    """
    Get a window widget's center point (cx, cy).

    @param window: Window widget.

    @return: Center point (cx, cy).
    """
    # Get center x
    cx = window.winfo_x() + (window.winfo_width() // 2)

    # Get center y
    cy = window.winfo_y() + (window.winfo_height() // 2)

    # Return the center point
    return cx, cy


#
def center_window(window, point=None):
    """
    Center a window widget around a point.

    Modified from `http://stackoverflow.com/a/10018670`.

    @param window: Window widget.

    @param point: Point to center around. Default is screen center point.

    @return: None.
    """
    # Get content width
    content_width = window.winfo_width()

    # Get frame width
    outframe_width = window.winfo_rootx() - window.winfo_x()

    # Get window full width
    window_width = content_width + 2 * outframe_width

    # Get content height
    content_height = window.winfo_height()

    # Get title bar height
    titlebar_height = window.winfo_rooty() - window.winfo_y()

    # Get window full height
    window_height = content_height + titlebar_height + outframe_width

    # If center point is given
    if point:
        # Use the center point's x and y
        cx, cy = point

    # If center point is not given
    else:
        # Use screen center point's x
        cx = window.winfo_screenwidth() // 2

        # Use screen center point's y
        cy = window.winfo_screenheight() // 2

    # Get position x
    x = cx - (window_width // 2)

    # Get position y
    y = cy - (window_height // 2)

    # Set the window's geometry
    window.geometry('{}x{}+{}+{}'.format(content_width, content_height, x, y))


#
class ToplevelVidget(object):
    """
    ToplevelVidget contains a Toplevel widget.
    """

    def __init__(
        self,
        close_handler=None,
        master=None,
    ):
        """
        Initialize object.

        @param close_handler: Window close button event handler.

        @param master: Master widget.

        @return: None.
        """

        # Create toplevel widget
        self._toplevel = Toplevel(master=master)

        # Hide the toplevel widget
        self._toplevel.withdraw()

        # Window close button event handler
        self._close_handler = close_handler \
            if close_handler is not None else self._close_handler_default

        # Register window close button event handler
        self._toplevel.protocol('WM_DELETE_WINDOW', self._close_handler)

    def toplevel(self):
        """
        Get the toplevel widget.

        @return: toplevel widget.
        """
        return self._toplevel

    def __getattr__(self, name):
        """
        Delegate attribute lookup to the toplevel widget.

        @return: Attribute value, or raise AttributeError.
        """
        return getattr(self._toplevel, name)

    def _close_handler_default(self):
        """
        Default window close button event handler.

        @return: None.
        """
        # Hide the toplevel widget
        self._toplevel.withdraw()

        # Release grab on the toplevel widget
        self._toplevel.grab_release()


#
class DialogVidget(ToplevelVidget):
    """
    DialogVidget contains a Toplevel widget, a main Frame widget, a custom view
    widget, and two button widgets for `Confirm` and `Cancel`.
    """

    def __init__(
        self,
        view_widget=None,
        confirm_handler=None,
        confirm_buttion_text='Confirm',
        cancel_handler=None,
        cancel_buttion_text='Cancel',
        close_handler=None,
        master=None,
    ):
        """
        Initialize object.

        @param view_widget: Custom view widget.

        @param confirm_handler: Confirm button event handler.

        @param confirm_buttion_text: Confirm button text.

        @param cancel_handler: Cancel button event handler.

        @param cancel_buttion_text: Cancel button text.

        @param close_handler: Window close button event handler.

        @param master: Master widget.

        @return: None.
        """
        # Initialize ToplevelVidget
        ToplevelVidget.__init__(
            self,
            close_handler=close_handler,
            master=master,
        )

        # Create main frame
        self._frame = Frame(master=self._toplevel)

        # Custom view widget
        self._view_widget = view_widget

        # Confirm button event handler
        self._confirm_handler = confirm_handler \
            if confirm_handler is not None else self._confirm_handler_default

        # Create confirm button
        self._confirm_button = Button(
            master=self._toplevel,
            text=confirm_buttion_text,
            command=self._confirm_handler,
        )

        # Cancel button event handler
        self._cancel_handler = cancel_handler \
            if cancel_handler is not None else self._cancel_handler_default

        # Create cancel button
        self._cancel_button = Button(
            master=self._toplevel,
            text=cancel_buttion_text,
            command=self._cancel_handler,
        )

        # If the view widget is given
        if self._view_widget is not None:
            # Set view widget
            self.view_set(self._view_widget)

        # Update widget
        self._widget_update()

    def _widget_update(self):
        """
        Update widget.

        @return: None.
        """
        # Configure layout weights for children
        self._toplevel.rowconfigure(0, weight=1)

        self._toplevel.columnconfigure(0, weight=1)

        # Lay out the main frame widget
        self._frame.grid(
            in_=self._toplevel,
            row=0,
            column=0,
            sticky='NSEW',
        )

        # Do not use children to compute main frame's geometry info
        self._frame.grid_propagate(False)

        # Configure layout weights for children.

        # Row 0 is for the view widget.
        self._frame.rowconfigure(0, weight=1)

        # Row 1 is for the confirm and cancel button widgets.
        self._frame.rowconfigure(0, weight=0)

        # Use only one column
        self._frame.columnconfigure(0, weight=1)

        # Lay out the confirm button
        self._confirm_button.grid(
            in_=self._frame,
            row=1,
            column=0,
            sticky='W',
        )

        # Lay out the cancel button
        self._cancel_button.grid(
            in_=self._frame,
            row=1,
            column=0,
            sticky='E',
        )

    def main_frame(self):
        """
        Get the main frame widget.

        @return: Main frame widget.
        """
        # Return the main frame widget
        return self._frame

    def view_set(self, widget):
        """
        Set view widget.

        @param widget: View widget.

        @return: None.
        """
        # Hide old view widget
        if self._view_widget is not None:
            self._view_widget.grid_forget()

        # Store new view widget
        self._view_widget = widget

        # Lay out new view widget
        self._view_widget.grid(
            in_=self._frame,
            row=0,
            column=0,
            sticky='NSEW',
        )

    def confirm_button(self):
        """
        Get the confirm button widget.

        @return: Confirm button widget.
        """
        # Return the confirm button widget
        return self._confirm_button

    def confirm_handler_set(self, handler):
        """
        Set confirm button event handler.

        @handler: Confirm button event handler.

        @return: None.
        """
        # Store confirm button event handler
        self._confirm_handler = handler

        # Set confirm button event handler
        self._confirm_button.config(command=self._confirm_handler)

    def _confirm_handler_default(self):
        """
        Default confirm button event handler.

        @return: None.
        """
        # Do nothing
        pass

    def cancel_button(self):
        """
        Get the cancel button widget.

        @return: Cancel button widget.
        """
        # Return the cancel button widget
        return self._cancel_button

    def cancel_handler_set(self, handler):
        """
        Set cancel button event handler.

        @handler: Cancel button event handler.

        @return: None.
        """
        # Store cancel button event handler
        self._cancel_handler = handler

        # Set cancel button event handler
        self._cancel_button.config(command=self._cancel_handler)

    def _cancel_handler_default(self):
        """
        Default cancel button event handler.

        @return: None.
        """
        # Hide the toplevel widget
        self._toplevel.withdraw()

        # Release grab on the toplevel widget
        self._toplevel.grab_release()
