# coding: utf-8
#
from __future__ import absolute_import


#
def _create_menu_config():
    """
    Create menu config.

    @return: Menu config list.
    """
    # Registry key paths
    ENV_PREFIX = \
        r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager'

    ENV = ENV_PREFIX + '\Environment'

    ENV_PATH = ENV_PREFIX + '\Environment->PATH'

    ENV_PATHEXT = ENV_PREFIX + '\Environment->PATHEXT'

    ENV_PYTHONPATH = ENV_PREFIX + '\Environment->PYTHONPATH'

    ENV_PYTHONIOENCODING = ENV_PREFIX + '\Environment->PYTHONIOENCODING'

    CU_ENV = r'HKEY_CURRENT_USER\Environment'

    CU_VOLATILE_ENV = r'HKEY_CURRENT_USER\Volatile Environment'

    CV = r'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion'

    EXPLORER_FILEEXTS = CV + '\Explorer\FileExts'

    # Create menu config list
    menu_config = [
        # Hive
        dict(pid='/', id='Hive', type='menu'),
        dict(pid='/Hive', id='ROOT', key=''),
        dict(pid='/Hive', id='HKEY_CLASSES_ROOT'),
        dict(pid='/Hive', id='HKEY_CURRENT_CONFIG'),
        dict(pid='/Hive', id='HKEY_CURRENT_USER'),
        dict(pid='/Hive', id='HKEY_LOCAL_MACHINE'),
        dict(pid='/Hive', id='HKEY_USERS'),

        # Environment
        dict(pid='/', id='Environment', type='menu'),
        dict(pid='/Environment', id=ENV),
        dict(pid='/Environment', id=ENV_PATH),
        dict(pid='/Environment', id=ENV_PATHEXT),
        dict(pid='/Environment', id=ENV_PYTHONPATH),
        dict(pid='/Environment', id=ENV_PYTHONIOENCODING),
        dict(pid='/Environment', id='Separator1', type='separator'),
        dict(pid='/Environment', id=CU_ENV),
        dict(pid='/Environment', id=CU_VOLATILE_ENV),

        # File Types
        dict(pid='/', id='File Types', type='menu'),
        dict(pid='/File Types', id='HKEY_CLASSES_ROOT'),
        dict(pid='/File Types', id=r'HKEY_CLASSES_ROOT\*'),
        dict(pid='/File Types', id=r'HKEY_CLASSES_ROOT\*\shell'),
        dict(pid='/File Types', id=r'HKEY_CLASSES_ROOT\AllFilesystemObjects'),
        dict(
            pid='/File Types',
            id=r'HKEY_CLASSES_ROOT\AllFilesystemObjects\shell',
        ),
        dict(pid='/File Types', id=r'HKEY_CLASSES_ROOT\Folder'),
        dict(pid='/File Types', id=r'HKEY_CLASSES_ROOT\Folder\shell'),
        dict(pid='/File Types', id=r'HKEY_CLASSES_ROOT\Directory'),
        dict(pid='/File Types', id=r'HKEY_CLASSES_ROOT\Directory\shell'),
        dict(pid='/File Types', id=r'HKEY_CLASSES_ROOT\DesktopBackground'),
        dict(
            pid='/File Types',
            id=r'HKEY_CLASSES_ROOT\DesktopBackground\shell',
        ),
        dict(pid='/File Types', id='Separator1', type='separator'),
        dict(pid='/File Types', id=EXPLORER_FILEEXTS),
        dict(pid='/File Types', id='Separator2', type='separator'),
        dict(pid='/File Types', id='HKEY_CLASSES_ROOT\.txt'),
    ]

    # Return the menu config list
    return menu_config


# Create menu specs
MENU_CONFIG = _create_menu_config()
