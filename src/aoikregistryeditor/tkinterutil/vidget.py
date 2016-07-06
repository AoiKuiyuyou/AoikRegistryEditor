# coding: utf-8
#
from __future__ import absolute_import

from tkinter.ttk import Frame


#
class Vidget(object):
    """
    Vidget contains a widget, instead of being a widget itself using
    inheritance. The benefit is that `An editor has a GUI` is more natural than
    `An editor is a GUI`.

    Vidget delegates widget-related methods, e.g. `grid`, `pack`, and `place`,
    to the widget contained, so that the Vidget object can be used just like a
    widget.
    """

    def __init__(
        self,
        master=None,
        widget=None,
        config_target=None,
    ):
        """
        Initialize object.

        @param master: Master widget.

        @param widget: Main widget. If not given, will create a Frame widget.

        @param config_target: The widget to call `config` method on. Default is
        the main widget.

        @return: None.
        """
        # Master widget
        self._vidget_master = master

        # Config target widget
        self._vidget_config_target = config_target

        # If main widget is given
        if widget is not None:
            # Set main widget
            self._vidget_widget = widget

        # If main widget is not given
        else:
            # Create default main Frame widget
            self._vidget_widget = Frame(master=master)

            # Configure children layout weights
            self._vidget_widget.rowconfigure(0, weight=1)

            self._vidget_widget.columnconfigure(0, weight=1)

    def master(self):
        """
        Get the master widget.

        @return: Master widget.
        """
        # Return the master widget
        return self._vidget_master

    def widget(self):
        """
        Get the main widget.

        @return: Main widget.
        """
        # Return the main widget
        return self._vidget_widget

    def config(self, *args, **kwargs):
        """
        Call `config` method on the config target widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Calls result.
        """
        # Call `config` method on the config target widget
        return self.config_target().config(*args, **kwargs)

    def config_target(self):
        """
        Get the config target widget.

        @return: Config target widget. Default is the main widget.
        """
        # If the config target widget is given
        if self._vidget_config_target is not None:
            # Return the config target widget
            return self._vidget_config_target

        # If the config target widget is not given
        else:
            # Return the main widget
            return self.widget()

    def config_target_set(self, target):
        """
        Set the config target widget.

        @param target: Config target widget. `None` means the main widget.

        @return: None.
        """
        # Set the config target widget
        self._vidget_config_target = target

    def state(self, *args, **kwargs):
        """
        Call `state` method on the config target widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Call result.
        """
        # Call `state` method on the config target widget
        return self.config_target().state(*args, **kwargs)

    def instate(self, *args, **kwargs):
        """
        Call `instate` method on the config target widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Call result.
        """
        # Call `instate` method on the config target widget
        return self.config_target().instate(*args, **kwargs)

    def bind(self, *args, **kwargs):
        """
        Call `bind` method on the config target widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Call result.
        """
        # Call `bind` method on the config target widget
        return self.config_target().bind(*args, **kwargs)

    def tkraise(self, *args, **kwargs):
        """
        Call `tkraise` method on the main widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Call result.
        """
        # Call `tkraise` method on the main widget
        return self.widget().tkraise(*args, **kwargs)

    def lower(self, *args, **kwargs):
        """
        Call `lower` method on the main widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Call result.
        """
        # Call `lower` method on the main widget
        return self.widget().lower(*args, **kwargs)

    def grid(self, *args, **kwargs):
        """
        Call `grid` method on the main widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Call result.
        """
        # Call `grid` method on the main widget
        return self.widget().grid(*args, **kwargs)

    def pack(self, *args, **kwargs):
        """
        Call `pack` method on the main widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Call result.
        """
        # Call `pack` method on the main widget
        return self.widget().pack(*args, **kwargs)

    def place(self, *args, **kwargs):
        """
        Call `place` method on the main widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Call result.
        """
        # Call `place` method on the main widget
        return self.widget().place(*args, **kwargs)

    def grid_forget(self):
        """
        Call `grid_forget` method on the main widget.

        @return: Call result.
        """
        # Call `grid_forget` method on the main widget
        return self.widget().grid_forget()

    def grid_propagate(self, value):
        """
        Call `grid_propagate` method on the main widget.

        @param value: Whether propagate.

        @return: Call result.
        """
        # Call `grid_propagate` method on the main widget
        return self.widget().grid_propagate(value)

    def pack_forget(self):
        """
        Call `pack_forget` method on the main widget.

        @return: Call result.
        """
        # Call `pack_forget` method on the main widget
        return self.widget().pack_forget()

    def pack_propagate(self, value):
        """
        Call `pack_propagate` method on the main widget.

        @param value: Whether propagate.

        @return: Call result.
        """
        # Call `pack_propagate` method on the main widget
        return self.widget().pack_propagate(value)

    def place_forget(self):
        """
        Call `place_forget` method on the main widget.

        @return: Call result.
        """
        # Call `place_forget` method on the main widget
        return self.widget().place_forget()

    def destroy(self):
        """
        Call `destroy` method on the main widget.

        @return: Call result.
        """
        # Call `destroy` method on the main widget
        return self.widget().destroy()

    def after(self, *args, **kwargs):
        """
        Call `after` method on the main widget.

        @param args: Positional arguments.

        @param kwargs: Keyword arguments.

        @return: Call result.
        """
        # Call `after` method on the main widget
        return self.widget().after(*args, **kwargs)
