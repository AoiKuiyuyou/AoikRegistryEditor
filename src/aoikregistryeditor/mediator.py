# coding: utf-8
#
from __future__ import absolute_import

from argparse import ArgumentParser
import sys
from tkinter import Tk
from traceback import format_exc

from .aoikimportutil import load_obj
from .registry_editor import RegistryEditor
from .tkinterutil.label import LabelVidget


#
def get_cmdargs_parser():
    """
    Create command arguments parser.

    @return: Command arguments parser.
    """
    # Create command arguments parser
    parser = ArgumentParser()

    # Specify arguments

    #
    menu_conf_uri_default = 'aoikregistryeditor.menu_config::MENU_CONFIG'

    parser.add_argument(
        '-m', '--menu-conf',
        dest='menu_config_uri',
        default=menu_conf_uri_default,
        metavar='MENU_CONF',
        help='Menu config object URI. Default is `{}`.'.format(
            menu_conf_uri_default
        ),
    )

    #
    parser.add_argument(
        '--menu-conf-default',
        dest='print_menu_conf_default',
        action='store_true',
        help='Print default menu config module.',
    )

    #
    ui_config_func_uri_default = 'aoikregistryeditor.ui_config::configure_ui'

    parser.add_argument(
        '-u', '--ui-conf',
        dest='ui_config_func_uri',
        default=ui_config_func_uri_default,
        metavar='UI_CONF',
        help='UI config function URI. Default is `{}`.'.format(
            ui_config_func_uri_default
        ),
    )

    #
    parser.add_argument(
        '--ui-conf-default',
        dest='print_ui_conf_default',
        action='store_true',
        help='Print default UI config module.',
    )

    #
    field_editor_factory_uri_default = \
        'aoikregistryeditor.field_editor_config::field_editor_factory'

    parser.add_argument(
        '-f', '--field-editor',
        dest='field_editor_factory_uri',
        default=field_editor_factory_uri_default,
        metavar='FACTORY',
        help='Field editor factory URI. Default is `{}`.'.format(
            field_editor_factory_uri_default
        ),
    )

    #
    parser.add_argument(
        '--field-editor-default',
        dest='print_field_editor_config_default',
        action='store_true',
        help='Print default field editor factory config module.',
    )

    # Return the command arguments parser
    return parser


#
def main_core(args=None, step_func=None):
    """
    The main function that implements the core functionality.

    @param args: Command arguments list.

    @param step_func: A function to set step information for the upper context.

    @return: Exit code.
    """
    # If step function is not given
    if step_func is None:
        # Raise error
        raise ValueError('Argument `step_func` is not given')

    # If step function is given.

    # Set step info
    step_func(title='Parse command arguments')

    # Create command arguments parser
    args_parser = get_cmdargs_parser()

    # If arguments are not given
    if args is None:
        # Use command arguments
        args = sys.argv[1:]

    # Parse command arguments
    args = args_parser.parse_args(args)

    # If print default menu config module
    if args.print_menu_conf_default:
        # Set step info
        step_func(title='Print default menu config module')

        # Import default menu config module
        from . import menu_config as config_module

        # Print default menu config module's content
        sys.stdout.write(open(config_module.__file__).read())

        # Exit
        return

    # If not print default menu config module.

    # If print default UI config module
    if args.print_ui_conf_default:
        # Set step info
        step_func(title='Print default UI config module')

        # Import default UI config module
        from . import ui_config as config_module

        # Print default UI config module's content
        sys.stdout.write(open(config_module.__file__).read())

        # Exit
        return

    # If not print default UI config module.

    # If print default field editor factory config module
    if args.print_field_editor_config_default:
        # Set step info
        step_func(title='Print default field editor factory config module')

        # Import default field editor config module
        from . import field_editor_config as config_module

        # Print default field editor config module's content
        sys.stdout.write(open(config_module.__file__).read())

        # Exit
        return

    # If not print default field editor factory config module.

    # Set step info
    step_func(title='Create TK root')

    # Create TK root
    tk = Tk()

    # Add window title
    tk.title('AoikRegistryEditor')

    # Set step info
    step_func(title='Create status bar label')

    # Create status bar label
    status_bar_label = LabelVidget(master=tk)

    # Create status bar set function
    def status_bar_set(text):
        status_bar_label.config(text=text)

    # Set step info
    step_func(title='Load field editor factory')

    # Get field editor factory function URI
    field_editor_factory_uri = args.field_editor_factory_uri

    # Load field editor factory function
    field_editor_config_module, field_editor_factory = load_obj(
        field_editor_factory_uri,
        mod_name='aoikregistryeditor._field_editor_config',
        retn_mod=True,
    )

    # Set step info
    step_func(title='Create registry editor')

    # Create registry editor
    editor = RegistryEditor(
        field_editor_factory=field_editor_factory,
        status_bar_set=status_bar_set,
        master=tk,
    )

    # Set step info
    step_func(title='Load menu config')

    # Get menu config URI
    menu_config_uri = args.menu_config_uri

    # Load menu config
    menu_config_module, menu_config = load_obj(
        menu_config_uri,
        mod_name='aoikregistryeditor._menu_config',
        retn_mod=True,
    )

    # Set step info
    step_func(title='Create menu tree')

    # Create menu tree
    menutree = editor.menutree_create(specs=menu_config)

    # Set step info
    step_func(title='Add menu tree to root window')

    # Add the menu tree's top menu to root window
    tk.config(menu=menutree.menu_top())

    # Set step info
    step_func(title='Get UI config info dict')

    # Get UI config info dict
    ui_info = dict(
        tk=tk,
        menutree=menutree,
        status_bar_label=status_bar_label,
        editor=editor,
        path_bar_label=editor._path_bar_label,
        path_bar=editor._path_bar,
        child_keys_labelframe=editor._child_keys_labelframe,
        child_keys_listbox=editor._child_keys_listbox,
        fields_labelframe=editor._fields_labelframe,
        fields_listbox=editor._fields_listbox,
        field_editor_labelframe=editor._field_editor_labelframe,
        field_add_label=editor._field_add_label,
        field_del_label=editor._field_del_label,
        field_load_label=editor._field_load_label,
        field_save_label=editor._field_save_label,
        field_add_dialog=editor._field_add_dialog,
    )

    # Set step info
    step_func(title='Load UI config function')

    # Get UI config function URI
    ui_config_func_uri = args.ui_config_func_uri

    # Load UI config function
    ui_config_module, ui_config_func = load_obj(
        ui_config_func_uri,
        mod_name='aoikregistryeditor._ui_config',
        retn_mod=True,
    )

    # Set step info
    step_func(title='Call UI config function')

    # Call UI config function
    ui_config_func(ui_info)

    # Set step info
    step_func(title='Run TK event loop')

    # Run TK event loop
    tk.mainloop()


#
def main_wrap(args=None):
    """
    The main function that provides exception handling.
    Call "main_core" to implement the core functionality.

    @param args: Command arguments list.

    @return: Exit code.
    """
    # A dict that contains step info
    step_info = {
        'title': '',
        'exit_code': 0
    }

    # A function that updates step info
    def step_func(title=None, exit_code=None):
        # If title is not None
        if title is not None:
            # Update title
            step_info['title'] = title

        # If exit code is not None
        if exit_code is not None:
            # Update exit code
            step_info['exit_code'] = exit_code

    #
    try:
        # Call "main_core" to implement the core functionality
        return main_core(args=args, step_func=step_func)
    # Catch keyboard interrupt
    except KeyboardInterrupt:
        # Return without error
        return 0
    # Catch other exceptions
    except Exception:
        # Get step title
        step_title = step_info.get('title', '')

        # Get traceback
        tb_msg = format_exc()

        # If step title is not empty
        if step_title:
            # Get message
            msg = '# Error: {}\n---\n{}---\n'.format(step_title, tb_msg)
        else:
            # Get message
            msg = '# Error\n---\n{}---\n'.format(tb_msg)

        # Output message
        sys.stderr.write(msg)

        # Get exit code
        exit_code = step_info.get('exit_code', 1)

        # Return exit code
        return exit_code
