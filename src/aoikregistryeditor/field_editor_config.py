# coding: utf-8
#
from __future__ import absolute_import

from aoikregistryeditor.registry_editor import FilteredFieldEditor


#
def semicolon_to_newline(text):
    """
    Convert semicolons in given text to newlines.

    @param text: Text to convert.

    @return: Converted text.
    """
    # Convert semicolons to newlines.
    # Return converted text.
    return '\n'.join(x for x in text.split(';'))


#
def newline_to_semicolon(text):
    """
    Convert newlines in given text to semicolons.

    @param text: Text to convert.

    @return: Converted text.
    """
    # Convert newlines to semicolons.
    # Return converted text.
    return ';'.join(x for x in text.split('\n'))


#
def field_editor_factory(field, old_editor, master):
    """
    Field editor factory.

    @param field: Field's RegVal object.

    @param old_editor: Old field editor object.

    @param master: Master widget.
    """
    # If the old editor is None
    if old_editor is None:
        # Create filtered field editor
        editor = FilteredFieldEditor(
            field=field,
            get_filter=newline_to_semicolon,
            set_filter=semicolon_to_newline,
            master=master,
            normal_bg='white',
            disabled_bg='gainsboro',
        )

        # Set the field editor's font
        editor.text_vidget().config(font=('Consolas', 16))

    # If the old editor is not None
    else:
        # Use the old editor
        editor = old_editor

        # Set the old editor's field object
        editor.field_set(field)

    # Return the field editor
    return editor
