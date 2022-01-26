# Copyright 2021-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Windows specific functions.

..
    PYTEST_DONT_REWRITE
"""
from __future__ import generator_stop
from typing import List
from typing import Union

try:
    import pywintypes
    import win32api
    import win32net
    import win32security
except ImportError:
    pass


def is_admin(name: str) -> bool:
    """
    Is the passed user a member of the Administrators group.

    Args:
        name (str): The name to check

    Returns:
        bool: True if user is a member of the Administrators group, False
        otherwise
    """
    groups = get_user_groups(name, True)
    for group in groups:
        if group in ('S-1-5-32-544', 'S-1-5-18'):
            return True
    return False


def get_user_groups(name: str, sid: bool = False) -> List[str]:
    """
    Get the groups to which a user belongs.

    Args:
        name (str): The user name to query
        sid (bool): True will return a list of SIDs, False will return a list of
        group names

    Returns:
        list: A list of group names or sids
    """
    groups = []
    if name.upper() == 'SYSTEM':
        groups = ['SYSTEM']
    else:
        try:
            groups = win32net.NetUserGetLocalGroups(None, name)
        except (win32net.error, pywintypes.error) as exc:
            if exc.winerror in (5, 1722, 2453, 1927, 1355):
                groups = win32net.NetUserGetLocalGroups(None, name, 0)
            else:
                try:
                    groups = win32net.NetUserGetGroups(None, name)
                except win32net.error as exc:
                    if exc.winerror in (5, 1722, 2453, 1927, 1355):
                        groups = win32net.NetUserGetLocalGroups(None, name, 0)
                except pywintypes.error as exc:
                    if exc.winerror in (5, 1722, 2453, 1927, 1355):
                        groups = win32net.NetUserGetLocalGroups(None, name, 1)
                    else:
                        raise
    if not sid:
        return groups
    ret_groups = []
    for group in groups:
        ret_groups.append(get_sid_from_name(group))
    return ret_groups


def get_sid_from_name(name: str) -> str:
    """
    This is a tool for getting a sid from a name. The name can be any object.

    Usually a user or a group.

    Args:
        name (str): The name of the user or group for which to get the sid

    Returns:
        str: The corresponding SID
    """
    if name is None:
        name = 'NULL SID'
    try:
        sid = win32security.LookupAccountName(None, name)[0]
    except pywintypes.error as exc:
        raise Exception('User {} not found: {}'.format(name, exc)) from exc
    sidstr = win32security.ConvertSidToStringSid(sid)
    return sidstr


def get_current_user(with_domain: bool = True) -> Union[str, bool]:
    """
    Gets the user executing the process.

    Args:

        with_domain (bool):
            ``True`` will prepend the user name with the machine name or domain
            separated by a backslash

    Returns:
        str: The user name
    """
    try:
        user_name = win32api.GetUserNameEx(win32api.NameSamCompatible)
        if user_name[-1] == '$':
            test_user = win32api.GetUserName()
            if test_user == 'SYSTEM':
                user_name = 'SYSTEM'
            elif get_sid_from_name(test_user) == 'S-1-5-18':
                user_name = 'SYSTEM'
        elif not with_domain:
            user_name = win32api.GetUserName()
    except pywintypes.error as exc:
        raise Exception('Failed to get current user: {}'.format(exc)) from exc
    if not user_name:
        return False
    return user_name
