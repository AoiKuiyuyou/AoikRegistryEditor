# coding: utf-8
#
from __future__ import absolute_import

from tkinter.ttk import Label

from .vidget import Vidget


#
class LabelVidget(Vidget):
    """
    LabelVidget contains a main Frame and a Label widget.
    The label widget takes all space of the main frame.
    The main frame can be used to configure the size of the label widget.
    """

    def __init__(
        self,
        master=None,
        **kwargs
    ):
        """
        Initialize object.

        @param master: Master widget.

        @param kwargs: Keyword arguments passed to label widget's constructor.

        @return: None.
        """
        # Initialize Vidget.
        # Create main frame widget.
        Vidget.__init__(self, master=master)

        # Create label widget
        self._label = Label(master=self.widget(), **kwargs)

        # Set the label widget as config target
        self.config_target_set(self._label)

        # Update widget
        self._widget_update()

    def _widget_update(self):
        """
        Update widget.

        @return: None.
        """
        # Do not use children to compute main frame's geometry
        self.widget().grid_propagate(False)

        # Configure layout weights for children
        self.widget().rowconfigure(0, weight=1)

        self.widget().columnconfigure(0, weight=1)

        # Lay out the label widget to take all space of the main frame
        self._label.grid(
            in_=self.widget(),
            row=0,
            column=0,
            sticky='NSEW',
        )

    def label_widget(self):
        """
        Get the label widget.

        @return: Label widget.
        """
        # Return the label widget
        return self._label
