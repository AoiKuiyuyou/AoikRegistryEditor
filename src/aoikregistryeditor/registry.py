# coding: utf-8
#
from __future__ import absolute_import

import pywintypes
from win32api import RegCloseKey
from win32api import RegDeleteValue
from win32api import RegEnumKeyEx
from win32api import RegEnumValue
from win32api import RegOpenKeyEx
from win32api import RegQueryValueEx
from win32api import RegSetValueEx
from win32con import KEY_ALL_ACCESS
from win32con import KEY_READ
from win32con import KEY_WOW64_64KEY
from win32con import HKEY_CLASSES_ROOT
from win32con import HKEY_CURRENT_CONFIG
from win32con import HKEY_CURRENT_USER
from win32con import HKEY_LOCAL_MACHINE
from win32con import HKEY_USERS
from win32con import HWND_BROADCAST
from win32con import SMTO_ABORTIFHUNG
from win32con import WM_SETTINGCHANGE
from win32gui import SendMessageTimeout

from .eventor import Eventor


#
def send_WM_SETTINGCHANGE():
    """
    Send WM_SETTINGCHANGE to notify registry changes.

    @return: None.
    """
    #
    try:
        # Send WM_SETTINGCHANGE to notify registry changes
        SendMessageTimeout(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            'Environment',
            SMTO_ABORTIFHUNG,  # Return fast if receiving thread hangs
            10,  # Timeout in milliseconds
        )
    # If have error
    except pywintypes.error:
        # Ignore
        pass


# Map registry hive name to hive integer
_HIVE_NAME_TO_INT = {
    'HKEY_CLASSES_ROOT': HKEY_CLASSES_ROOT,
    'HKEY_CURRENT_CONFIG': HKEY_CURRENT_CONFIG,
    'HKEY_CURRENT_USER': HKEY_CURRENT_USER,
    'HKEY_LOCAL_MACHINE': HKEY_LOCAL_MACHINE,
    'HKEY_USERS': HKEY_USERS,
}


#
def _hive_name_to_int(name):
    """
    Map registry hive name to hive integer.

    @param name: Hive name.

    @return: Hive integer, or None if the hive name not exists.
    """
    # Map registry hive name to hive integer
    return _HIVE_NAME_TO_INT.get(name, None)


#
def _regkey_handle_get(path, mask=None):
    """
    Get registry key handle.

    @param path: Registry key path.

    @param mask: Permission mask.

    @return: Registry key handle, or raise error if failed.
    """
    # Split the registry key path into hive name and no-hive path
    hive_name, _, nohive_path = path.partition('\\')

    # If no-hive path is empty,
    # it means path given is solely hive name.
    if nohive_path == '':
        # Set no-hive path to None
        nohive_path = None

    # Get hive integer
    hive_int = _hive_name_to_int(hive_name)

    # If hive integer is not found
    if hive_int is None:
        # Get error message
        msg = 'Invalid registry key path: {}'.format(path)

        # Raise error
        raise ValueError(msg)

    # If hive integer is found.

    # If permission mask is not given
    if mask is None:
        # Set default permission mask
        mask = KEY_ALL_ACCESS | KEY_WOW64_64KEY

    # Get registry key handle.
    # May raise `pywintypes.error`.
    regkey_handle = RegOpenKeyEx(
        hive_int,
        nohive_path,
        0,  # Always 0
        mask,
    )

    # Return the registry key handle
    return regkey_handle


#
def regkey_get(path, mask=None):
    """
    Create RegKey object for given registry key path.

    @param path: Registry key path.

    @param mask: Permission mask.

    @return: RegKey object, or None if failed getting the registry key handle.
    """
    # If the registry key path is root key path
    if path == RegKey.ROOT:
        # Return RootRegKey object
        return RootRegKey()

    # If the registry key path is not root key path.

    #
    try:
        # Get registry key handle
        regkey_handle = _regkey_handle_get(path, mask=mask)
    # If have error
    except Exception:
        # Set registry key handle to None
        regkey_handle = None

    # If failed getting registry key handle
    if regkey_handle is None:
        # Return None
        return None

    # If not failed getting registry key handle.

    # Create RegKey object
    regkey = RegKey(
        handle=regkey_handle,
        path=path,
    )

    # Return the RegKey object
    return regkey


#
def regkey_exists(path):
    """
    Test whether given registry key path exists, and user permissions are
    granted to read the registry key.

    @param path: Registry key path.

    @return: Boolean.
    """
    # Create RegKey object for given registry key path
    regkey = regkey_get(path, mask=KEY_READ)

    # If the RegKey object is created,
    # it means the registry key path exists.
    if regkey is not None:
        # Close the RegKey object
        regkey.close()

        # Return True
        return True

    # If the RegKey object is not created,
    # it means the registry key path not exists,
    # or user permissions are not granted to read the registry key.
    else:
        # Return False
        return False


#
def regkey_parent_path(path):
    """
    Get given registry key path's parent registry key path.

    @param path: Registry key path.

    @return: Parent registry key path.
    """
    # If the key path is root key path or hive key path
    if path == RegKey.ROOT or path in RegKey.HKEYS:
        # Return the root key path
        return RegKey.ROOT

    # If the key path is not root key path or hive key path

    # Get parent key path.
    # Assume the given path has path separator in it.
    parent_path, sep, child_part = path.rpartition('\\')

    # Return the parent key path
    return parent_path


#
def regkey_child_names(path):
    """
    Get given registry key path's child key names list.

    @param path: Registry key path.

    @return: Child key names list.
    """
    # If the key path is root key path
    if path == RegKey.ROOT:
        # Return hive key names
        return RegKey.HKEYS

    # If the key path is not root key path.

    # Create RegKey object for given registry key path
    regkey = regkey_get(path)

    # If the RegKey object is not created
    if regkey is None:
        # Return None
        return None

    # If the RegKey object is created.
    else:
        # Return child key names list
        return regkey.child_names()


#
class RegVal(object):
    """
    RegVal represents a registry key's field.
    """

    def __init__(self, regkey, name, type):
        """
        Initialize object.

        @param regkey: RegKey object of the registry key containing the field.

        @param name: Field name.

        @param type: Field type.

        @return: None.
        """
        # RegKey object
        self._regkey = regkey

        # Field name
        self._name = name

        # Field type
        self._type = type

    def __str__(self):
        """
        Get string of the object.

        @return: String of the object.
        """
        # Return the field name
        return self._name

    def name(self):
        """
        Get field name.

        @return: Field name
        """
        # Return the field name
        return self._name

    def name_set(self, name):
        """
        Set field name.

        @param name: Field name to set.

        @return: None.
        """
        # Set the field name
        self._name = name

    def type(self):
        """
        Get field type.

        @return: Field type
        """
        # Return the field type
        return self._type

    def type_set(self, type):
        """
        Set field type.

        @param type: Field type to set.

        @return: None.
        """
        # Set the field type
        self._type = type

    def data(self):
        """
        Get field data.

        @return: Field data.
        """
        # Read field data from registry.
        # Return the field data.
        return self._regkey.field_data(name=self._name)

    def data_set(self, data):
        """
        Set field data.

        @param data: Field data to set.

        @return: None
        """
        # Write field data to registry
        success = self._regkey.field_write(
            name=self._name,
            type=self._type,
            data=data,
        )

        # If have no success
        if not success:
            # Raise error
            raise ValueError(data)

    def delete(self):
        """
        Delete the field.

        @return: Whether the operation is successful.
        """
        # Delete the field.
        # Return whether the operation is successful.
        return self._regkey.field_delete(self._name)


#
class RegKey(object):
    """
    RegKey represents a registry key.
    """

    # Root path
    ROOT = ''

    # Hive names list
    HKEYS = tuple(_HIVE_NAME_TO_INT.keys())

    def __init__(self, handle, path):
        """
        Initialize object.

        @param handle: Registry key handle.

        @param path: Registry key path.

        @return: None.
        """
        # Registry key handle
        self._handle = handle

        # Registry key path
        self._path = path

    def __str__(self):
        """
        Get string of the object.

        @return: String of the object.
        """
        # Return the key path
        return self._path

    def path(self):
        """
        Get key path.

        @return: Key path
        """
        # Return the key path
        return self._path

    def child_names(self):
        """
        Get child key names list.

        @return: Child key names list.
        """
        # Ensure registry key handle is set
        assert self._handle

        # Child key names list
        child_name_s = []

        # Get child key info tuples
        info_tuple_s = RegEnumKeyEx(self._handle)

        # For each child key info tuple
        for info_tuple in info_tuple_s:
            # Get child key name
            child_name = info_tuple[0]

            # Add the child key name to child key names list
            child_name_s.append(child_name)

        # Return the child key names list
        return child_name_s

    def child_paths(self):
        """
        Get child key paths list.

        Notice this method assumes the key is not root key.

        @return: Child key paths list.
        """
        # Return child key paths list
        return [self._path + '\\' + name for name in self.child_names()]

    def fields(self):
        """
        Get key fields list. Each field is a RegVal object.

        @return: Key fields list.
        """
        # Ensure registry key handle is set
        assert self._handle

        # Fields list
        field_s = []

        # Field index
        field_index = 0

        # For each field index
        while True:
            #
            try:
                # Get field name and type.
                # May raise `pywintypes.error`.
                field_name, _, field_type = RegEnumValue(
                    self._handle,
                    field_index,
                )

            # If have error,
            # it means no more field
            except pywintypes.error:
                # Stop the loop
                break

            # If have no error.

            # Create RegVal object
            field = RegVal(
                regkey=self,
                name=field_name,
                type=field_type,
            )

            # Add the RegVal object to fields list
            field_s.append(field)

            # Increment field index
            field_index += 1

        # Return the fields list
        return field_s

    def _field_data_type_tuple(self, name):
        """
        Get field data and type tuple: (data, type).

        @return: Field data and type tuple: (data, type), or None if have
        error.
        """
        # Ensure registry key handle is set
        assert self._handle

        #
        try:
            # Return field data and type tuple: (data, type)
            return RegQueryValueEx(self._handle, name)

        # If have error
        except pywintypes.error:
            # Return None
            return None

    def field_type(self, name):
        """
        Get field type.

        @param name: Field name.

        @return: Field type, or None if have error.
        """
        # Get field data and type tuple
        data_type_tuple = self._field_data_type_tuple(name)

        # If have error
        if data_type_tuple is None:
            # Return None
            return None

        # If have no error
        else:
            # Get the field type
            _, field_type = data_type_tuple

            # Return the field type
            return field_type

    def field_data(self, name):
        """
        Get field data.

        @param name: Field name.

        @return: Field data, or None if have error.
        """
        # Get field data and type tuple
        data_type_tuple = self._field_data_type_tuple(name)

        # If have error
        if data_type_tuple is None:
            # Return None
            return None

        # If have no error
        else:
            # Get the field data
            field_data, _ = data_type_tuple

            # Return the field data
            return field_data

    def field_write(self, name, type, data):
        """
        Write field.

        @param name: Field name.

        @param type: Field type.

        @param data: Field data.

        @return: Whether the operation is successful.
        """
        # Ensure registry key handle is set
        assert self._handle

        #
        try:
            # Write field
            RegSetValueEx(
                self._handle,
                name,
                0,
                type,
                data,
            )

            # Send WM_SETTINGCHANGE to notify registry changes
            send_WM_SETTINGCHANGE()

            # If have no error.

            # Return the operation is successful
            return True

        # If have error
        except pywintypes.error:
            # Return the operation is not successful
            return False

    def field_delete(self, name):
        """
        Delete field.

        @param name: Field name.

        @return: Whether the operation is successful.
        """
        # Ensure registry key handle is set
        assert self._handle

        #
        try:
            # Delete field
            RegDeleteValue(
                self._handle,
                name,
            )

            # Send WM_SETTINGCHANGE to notify registry changes
            send_WM_SETTINGCHANGE()

            # If have no error.

            # Return the operation is successful
            return True

        # If have error
        except pywintypes.error:
            # Return the operation is not successful
            return False

    def close(self):
        """
        Close the registry key handle.

        @return: None.
        """
        # If the registry key handle is closed
        if self.closed():
            # Raise error
            raise ValueError('Already closed')

        # If the registry key handle is not closed
        else:
            # Close the registry key handle
            RegCloseKey(self._handle)

            # Set the registry key handle to None
            self._handle = None

    def closed(self):
        """
        Test whether the registry key handle is closed.

        @return: Boolean.
        """
        # Test whether the registry key handle is closed
        return self._handle is None


#
class RootRegKey(RegKey):
    """
    RootRegKey represents registry root key that contains the hive keys.
    """

    def __init__(self):
        """
        Initialize object.

        @return: None.
        """
        # Initialize RegKey.
        # Registry key handle is None for root key.
        # Registry key path is empty for root key.
        RegKey.__init__(self, handle=None, path='')

    def child_names(self):
        """
        Get child key names list.

        @return: Child key names list.
        """
        # Return hive names for root key
        return RegKey.HKEYS

    def child_paths(self):
        """
        Get child key paths list.

        @return: Child key paths list.
        """
        # Return hive names for root key
        return RegKey.HKEYS

    def fields(self):
        """
        Get key fields list. Each field is a RegVal object.

        @return: Key fields list.
        """
        # Return empty list for root key
        return []

    def field_type(self, name):
        # Raise error for root key
        raise ValueError("Root key has no fields.")

    def field_data(self, name):
        # Raise error for root key
        raise ValueError("Root key has no fields.")

    def field_write(self, name, type, data):
        # Raise error for root key
        raise ValueError("Root key has no fields.")

    def close(self):
        """
        Close the registry key handle.

        @return: None.
        """
        # Do nothing for root key
        pass

    def closed(self):
        """
        Test whether the registry key handle is closed.

        @return: Boolean.
        """
        # Return False for root key
        return False


#
class RegKeyPathNavigator(Eventor):
    """
    RegKeyPathNavigator has an active registry key path, and provides methods
    to change the active registry key path.
    """

    # Event notified when active key path is to be changed
    PATH_CHANGE_SOON = 'PATH_CHANGE_SOON'

    # Event notified when active key path is changed
    PATH_CHANGE_DONE = 'PATH_CHANGE_DONE'

    # Registry root key path
    ROOT = ''

    #
    def __init__(self, path=None):
        """
        Initialize object.

        @param path: Active key path. Default is root key path.

        @return: None.
        """
        # Initialize Eventor
        Eventor.__init__(self)

        # Active key path
        self._path = path if path is not None else self.ROOT

        # Go to the active path
        self.go_to_path(self._path)

    def regkey(self):
        """
        Get RegKey object for the active key path.

        @return: RegKey object for the active key path.
        """
        # Return RegKey object for the active key path
        return regkey_get(self.path())

    def path(self):
        """
        Get the active key path.

        @return: Active key path.
        """
        # Return the active key path
        return self._path

    def parent_path(self):
        """
        Get the active key path's parent key path.

        @return: Active key path's parent key path.
        """
        # Return the active key path's parent key path
        return regkey_parent_path(self._path)

    def child_path(self, child_name):
        """
        Get the active key path's child key path, given the child key name.

        @param child_name: Child key name.

        @return: Active key path's child key path.
        """
        # If the active key path is root key path
        if self._path == self.ROOT:
            # Use child name as child path
            child_path = child_name

        # If the active key path is not root key path
        else:
            # Add separator between parent key path and child key name
            child_path = self._path + '\\' + child_name

        # Return the child key path
        return child_path

    def child_names(self):
        """
        Get the active key path's child key names list.

        @return: Active key path's child key names list.
        """
        # Return the active key path's child key names list
        return regkey_child_names(self._path)

    def go_to_path(self, path, check=False):
        """
        Go to given key path.

        @param path: Key path to go to.

        @param check: Whether check if the key path exists, and raise error if
        the key path not exists.

        @return: New active key path.
        """
        # If check key path
        if check:
            # If the key path not exists
            if not regkey_exists(path):
                # Raise error
                raise ValueError(path)

            # If the key path exists.

        # Notify pre-change event
        self.handler_notify(self.PATH_CHANGE_SOON, self)

        # Set new active path
        self._path = path

        # Notify post-change event
        self.handler_notify(self.PATH_CHANGE_DONE, self)

        # Return the new active path
        return self._path

    def go_to_root(self, check=False):
        """
        Go to root key path.

        @param check: Whether check if the key path exists, and raise error if
        the key path not exists.

        @return: New active key path.
        """
        # Go to root key path
        return self.go_to_path(self.ROOT, check=check)

    def go_to_parent(self, check=False):
        """
        Go to the active key path's parent key path.

        @param check: Whether check if the key path exists, and raise error if
        the key path not exists.

        @return: New active key path.
        """
        # Get the active key path's parent key
        parent_path = self.parent_path()

        # Go to the active key path's parent key
        return self.go_to_path(parent_path, check=check)

    def go_to_child(self, child_name, check=False):
        """
        Go to the active key path's child key path, given the child key name.

        @param child_name: Child key name.

        @param check: Whether check if the key path exists, and raise error if
        the key path not exists.

        @return: New active key path.
        """
        # Get the active key path's child key path
        child_path = self.child_path(child_name)

        # Go to the active key path's child key path
        return self.go_to_path(child_path, check=check)
