# coding: utf-8
#
from __future__ import absolute_import

from tkinter import Spinbox
from tkinter import Text
from tkinter.ttk import Combobox
from tkinter.ttk import Entry
from tkinter.ttk import Scrollbar
from tkinter.constants import ACTIVE
from tkinter.constants import DISABLED
from tkinter.constants import END
from tkinter.constants import NORMAL

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
class EntryVidget(
    Vidget,
    Eventor,
):
    """
    EntryVidget contains a main Frame and an Entry widget.
    The entry widget takes all space of the main frame.
    The main frame can be used to configure the size of the entry widget.

    EntryVidget adds the following abilities:
    - Simplify the use of validator function.
    - Notify pre-change and and post-change events.
    """

    # Default validator function
    _DEFAULT_VALIDATOR = (lambda x: True)

    # Event notified when text is to be changed
    TEXT_CHANGE_SOON = 'TEXT_CHANGE_SOON'

    # Event notified when text is changed
    TEXT_CHANGE_DONE = 'TEXT_CHANGE_DONE'

    def __init__(
        self,
        text=None,
        validator=None,
        widget_type=None,
        master=None,
    ):
        """
        Initialize object.

        @param text: Initial text. Default is empty.

        @param validator: Validator function that determines whether text
        entered by user or set by `text_set` method is valid. The validator
        function takes the new value as argument and returns True if the new
        value is valid.

        @param widget_type: One of ['Entry', 'Spinbox', 'Combobox']. Default is
        'Entry'.

        @param master: Master widget.

        @return: None.
        """
        # Initialize Vidget.
        # Create main frame widget.
        Vidget.__init__(self, master=master)

        # Initialize Eventor
        Eventor.__init__(self)

        # If widget type is None or `Entry`
        if widget_type is None or widget_type == 'Entry':
            # Create Entry widget
            self._text_widget = Entry(master=self.widget())

        # If widget type is `Spinbox`
        elif widget_type == 'Spinbox':
            # Create Spinbox widget
            self._text_widget = Spinbox(master=self.widget())

        # If widget type is `Combobox`
        elif widget_type == 'Combobox':
            # Create Combobox widget
            self._text_widget = Combobox(master=self.widget())

        # If widget type is something else
        else:
            # Raise error
            raise ValueError(widget_type)

        # Set the text widget as config target
        self.config_target_set(self._text_widget)

        # Whether the text widget's value is changing
        self._is_changing = False

        # Old widget state
        self._old_widget_state = NORMAL

        # Validator function
        self._validator = validator \
            if validator is not None else EntryVidget._DEFAULT_VALIDATOR

        # Create validator wrapper
        self._validator_wrapper = self._validator_wrapper_create()

        # Register the validator wrapper with Tkinter. Get reference ID.
        self._validator_wrapper_ref_id = \
            self.text_widget().winfo_toplevel().register(
                self._validator_wrapper
            )

        # Mount the validator wrapper to the text widget
        self._validator_wrapper_mount()

        # If the text widget is Combobox
        if isinstance(self._text_widget, Combobox):
            # Bind selected event to event handler
            self._text_widget.bind(
                '<<ComboboxSelected>>', self._on_combobox_selected
            )

        # Cached text
        self._text = self._text_widget.get()

        # Set initial text
        self.text_set(text if text is not None else '', notify=False)

        # Update widget
        self._widget_update()

    def _widget_update(self):
        """
        Update widget config and layout.

        @return: None.
        """
        # Do not use children to compute main frame's geometry
        self.widget().grid_propagate(False)

        # Configure layout weights for children
        self.widget().rowconfigure(0, weight=1)

        self.widget().columnconfigure(0, weight=1)

        # Lay out the text widget to take all space of the main frame
        self._text_widget.grid(
            in_=self.widget(),
            row=0,
            column=0,
            sticky='NSEW',
        )

    def text_widget(self):
        """
        Get the text widget.

        @return: Text widget.
        """
        # Return the text widget
        return self._text_widget

    def text(self):
        """
        Get cached text.

        `self._text` and `self._text_widget.get()` usually give same value.
        But from within the validator wrapper at 3Q7EB, when the new value is
        being validated, the new value is only available in `self._text`.
        Tkinter widget's interval value has not been updated yet.

        @return: Cached text.
        """
        # Return the cached text
        return self._text

    def text_set(
        self,
        text,
        notify=True,
        notify_arg=None,
        is_validator=False,
    ):
        """
        Set text.

        @param text: Text to set.

        @param notify: Whether notify text change events.

        @param notify_arg: Event argument.

        @param is_validator: Whether caller is validator.

        @return: None.
        """
        # If the text is not valid
        if not self.text_is_valid(text):
            # Raise error
            raise ValueError('Text is not valid: {}'.format(text))

        # If the text is valid.

        # If the text is changing
        if self._is_changing:
            # Raise error
            raise ValueError('Text is changing')

        # If the text is not changing.

        # Set text changing flag on
        self._is_changing = True

        # If notify event
        if notify:
            # Notify pre-change event
            self.handler_notify(
                self.TEXT_CHANGE_SOON,
                arg=notify_arg,
                need_info=True,
            )

        # Cache the text
        self._text = text

        # If caller is not validator,
        # need change text widget's value.
        if not is_validator:
            # Unmount the validator wrapper before changing text widget's value
            self._validator_wrapper_unmount()

            # Set text widget to NORMAL state
            self.state_set(NORMAL)

            # Delete the old text from text widget.
            # This will not trigger validation because the validator wrapper
            # has been unmounted.
            self._text_widget.delete(0, END)

            # Insert the new text into text widget.
            self._text_widget.insert(0, text)

            # Set text widget to previous state
            self.state_set_back()

            # Mount the validator wrapper after changing text widget's value
            self._validator_wrapper_mount()

        # If caller is validator
        # no need change text widget's value.

        # If the cached text is not EQ text widget's value
        if self._text != self._text_widget.get():
            # If caller is not validator
            if not is_validator:
                # Set changing flag off
                self._is_changing = False

                # Raise error
                raise ValueError(
                    'Inconsistent state. `{}` != `{}`'.format(
                        repr(self._text),
                        repr(self._text_widget.get()),
                    )
                )

            # If caller is validator,
            # this is normal because text widget's value will be updated after
            # the validator returns.

        # If notify event
        if notify:
            # Notify post-change event
            self.handler_notify(
                self.TEXT_CHANGE_DONE,
                arg=notify_arg,
                need_info=True,
            )

        # Set changing flag off
        self._is_changing = False

    def enabled(self):
        """
        Test whether the text widget is not in DISABLED state.

        @return: Boolean.
        """
        # Get the text widget's state. One of [NORMAL, DISABLED, ACTIVE].
        state = str(self.text_widget()['state'])

        # Test whether the text widget is not in DISABLED state
        return state != DISABLED

    def disabled(self):
        """
        Test whether the text widget is in DISABLED state.

        @return: Boolean.
        """
        # Get the text widget's state. One of [NORMAL, DISABLED, ACTIVE].
        state = str(self.text_widget()['state'])

        # Test whether the text widget is in DISABLED state
        return state == DISABLED

    def state_set(self, state):
        """
        Set the text widget's state.

        @param state: State to set.

        @return: None.
        """
        # If given state is not valid
        if state not in [NORMAL, DISABLED, ACTIVE]:
            # Raise error
            raise ValueError(state)

        # If given state is valid.

        # Store old state
        self._old_widget_state = str(self.text_widget()['state'])

        # Set new state
        self.text_widget()['state'] = state

    def state_set_back(self):
        """
        Set the text widget to old state.

        @return: None.
        """
        # If old state is not valid
        if self._old_widget_state not in [NORMAL, DISABLED, ACTIVE]:
            # Raise error
            raise ValueError(self._old_widget_state)

        # If old state is valid.

        # Set the text widget to old state
        self.text_widget()['state'] = self._old_widget_state

    def is_changing(self):
        """
        Test whether the text widget's value is changing.

        @return: Boolean.
        """
        # Return whether the text widget's value is changing
        return self._is_changing

    def text_is_valid(self, text):
        """
        Test whether given text is valid according to validator.

        @param text: Text to test.

        @return: Boolean.
        """
        # Return whether given text is valid according to validator
        return self._validator(text)

    def _validator_wrapper_create(self):
        """
        Create validator wrapper.
        The wrapper calls original validator to validate the new text value.
        If the new text value is valid, the wrapper will set the text widget
        to the new value, and notify text change events.

        @return: Validator function wrapper.
        """
        # 3Q7EB
        # Create validator wrapper
        def validator_wrapper(new_value):
            # If the text widget is changing
            if self._is_changing:
                # Raise error
                raise ValueError('Text is changing')

            # If the validator function is not given
            if self._validator is None:
                # Set validation result to True
                is_valid = True

            # If the validator function is given
            else:
                try:
                    # Get validation result
                    is_valid = self._validator(new_value)
                # If have error
                except Exception:
                    # Set validation result to False
                    is_valid = False

            # If the new value is valid
            if is_valid:
                # If the text widget is changing
                if self._is_changing:
                    # Raise error
                    raise ValueError('Text is changing')

                # Set the text widget's value.
                # Notify text change events.
                self.text_set(
                    new_value,
                    notify=True,
                    is_validator=True,
                )

                # If the text widget is changing
                if self._is_changing:
                    # Raise error
                    raise ValueError('Text is changing')

            # If the new value is not valid,
            # do nothing.

            # Return the validation result
            return is_valid

        # Return the validator wrapper
        return validator_wrapper

    def _validator_wrapper_mount(self):
        """
        Mount the validator wrapper to the text widget.

        @return: None.
        """
        # Mount the validator wrapper to the text widget
        self.text_widget().config(
            # Validation type
            validate='key',

            # Validator function reference ID, and argument type.
            # Argument type `%P` means the new value.
            validatecommand=(self._validator_wrapper_ref_id, '%P')
        )

    def _validator_wrapper_unmount(self):
        """
        Unmount the validator wrapper from the text widget.

        @return: None.
        """

        # Unmount the validator wrapper from the text widget.
        # Notice `validatecommand=None` does not work.
        self.text_widget().config(validatecommand='')

    def _on_combobox_selected(self, event):
        """
        Combobox selected event handler.

        @param event: Tkinter event object.

        @return: None.
        """
        # Get new value
        new_value = self.text_widget().get()

        # If the new value is not valid
        if not self._validator(new_value):
            # Set old value back
            self.text_widget().set(self._text)

        # If the new value is valid
        else:
            # Set the new value.
            # Notify text change events.
            self.text_set(new_value, notify=True)


#
class TextVidget(Vidget):
    """
    TextVidget contains a main Frame widget, a Text widget and a Scrollbar
    widget.
    """

    def __init__(
        self,
        text=None,
        master=None,
    ):
        """
        Initialize object.

        @param text: Initial text. Default is empty.

        @param master: Master widget.

        @return: None.
        """
        # Initialize Vidget.
        # Create main frame widget.
        Vidget.__init__(self, master=master)

        # Create scrollbar widget
        self._scrollbar = _HiddenScrollbar(master=self.widget())

        # Create text widget
        self._text_widget = Text(
            master=self.widget(),
            # Enable undo
            undo=True,
            # Auto add undo separators
            autoseparators=True,
            # Unlimited number of undos
            maxundo=-1,
        )

        # Set the text widget as config target
        self.config_target_set(self._text_widget)

        # Mount the scrollbar
        self._text_widget.config(yscrollcommand=self._scrollbar.set)

        self._scrollbar.config(command=self._text_widget.yview)

        # Update widget
        self._widget_update()

        # Set initial text
        self.text_add(text if text is not None else '')

    def _widget_update(self):
        """
        Update widget.

        @return: None.
        """
        # Configure children layout weights
        self.widget().rowconfigure(0, weight=1)

        # Column 0 is for the text widget
        self.widget().columnconfigure(0, weight=1)

        # Column 1 is for the scrollbar widget
        self.widget().columnconfigure(1, weight=0)

        # Lay out the text widget
        self._text_widget.grid(
            row=0,
            column=0,
            sticky='NSEW',
        )

        # Lay out the scrollbar widget
        self._scrollbar.grid(
            row=0,
            column=1,
            sticky='NSEW',
        )

    def scrollbar_widget(self):
        """
        Get the scrollbar widget.

        @return: Scrollbar widget.
        """
        # Return the scrollbar widget
        return self._scrollbar

    def text_widget(self):
        """
        Get the text widget.

        @return: Text widget.
        """
        # Return the text widget
        return self._text_widget

    def text(self):
        """
        Get text.

        @return: Text.
        """
        # Return the text
        return self._text_widget.get('1.0', END + '-1c')

    def text_set(self, text):
        """
        Set text.

        @param text: Text to set.

        @return: None.
        """
        # Delete old text
        self._text_widget.delete('1.0', END)

        # Add new text
        self.text_add(text)

    def text_add(self, text):
        """
        Add text.

        @param text: Text to add.

        @return: None.
        """
        # Add the text to the end
        self._text_widget.insert(END, text)
