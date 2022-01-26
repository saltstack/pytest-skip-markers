# Copyright 2021-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Platform related utilities.

..
    PYTEST_DONT_REWRITE
"""
from __future__ import generator_stop
import multiprocessing
import os
import pathlib
import platform
import shutil
import subprocess
import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def is_windows() -> bool:
    """
    Simple function to return if a host is Windows or not.

    :return bool: Return true on Windows
    """
    return sys.platform.startswith('win')


@lru_cache(maxsize=None)
def is_linux() -> bool:
    """
    Simple function to return if a host is Linux or not.

    Note for a proxy minion, we need to return something else
    :return bool: Return true on Linux
    """
    return sys.platform.startswith('linux')


@lru_cache(maxsize=None)
def is_darwin() -> bool:
    """
    Simple function to return if a host is Darwin (macOS) or not.

    :return bool: Return true on Darwin(macOS)
    """
    return sys.platform.startswith('darwin')


@lru_cache(maxsize=None)
def is_sunos() -> bool:
    """
    Simple function to return if host is SunOS or not.

    :return bool: Return true on SunOS
    """
    return sys.platform.startswith('sunos')


@lru_cache(maxsize=None)
def is_smartos() -> bool:
    """
    Simple function to return if host is SmartOS (Illumos) or not.

    :return bool: Return true on SmartOS (Illumos)
    """
    if is_sunos():
        return os.uname()[3].startswith('joyent_')
    return False


@lru_cache(maxsize=None)
def is_freebsd() -> bool:
    """
    Simple function to return if host is FreeBSD or not.

    :return bool: Return true on FreeBSD
    """
    return sys.platform.startswith('freebsd')


@lru_cache(maxsize=None)
def is_netbsd() -> bool:
    """
    Simple function to return if host is NetBSD or not.

    :return bool: Return true on NetBSD
    """
    return sys.platform.startswith('netbsd')


@lru_cache(maxsize=None)
def is_openbsd() -> bool:
    """
    Simple function to return if host is OpenBSD or not.

    :return bool: Return true on OpenBSD
    """
    return sys.platform.startswith('openbsd')


@lru_cache(maxsize=None)
def is_aix() -> bool:
    """
    Simple function to return if host is AIX or not.

    :return bool: Return true on AIX
    """
    return sys.platform.startswith('aix')


@lru_cache(maxsize=None)
def is_aarch64() -> bool:
    """
    Simple function to return if host is AArch64 or not.
    """
    return platform.machine().startswith('aarch64')


def is_spawning_platform() -> bool:
    """
    Returns ``True`` if running on a platform which defaults multiprocessing to spawn.
    """
    return multiprocessing.get_start_method(allow_none=False) == 'spawn'


def on_platforms(
    windows: bool = False,
    linux: bool = False,
    darwin: bool = False,
    sunos: bool = False,
    smartos: bool = False,
    freebsd: bool = False,
    netbsd: bool = False,
    openbsd: bool = False,
    aix: bool = False,
    aarch64: bool = False,
    spawning: bool = False,
) -> bool:
    """
    Check to see if we're on one of the provided platforms.

    :keyword bool windows: When :py:const:`True`, check if running on Windows.
    :keyword bool linux: When :py:const:`True`, check if running on Linux.
    :keyword bool darwin: When :py:const:`True`, check if running on Darwin.
    :keyword bool sunos: When :py:const:`True`, check if running on SunOS.
    :keyword bool smartos: When :py:const:`True`, check if running on SmartOS.
    :keyword bool freebsd: When :py:const:`True`, check if running on FreeBSD.
    :keyword bool netbsd: When :py:const:`True`, check if running on NetBSD.
    :keyword bool openbsd: When :py:const:`True`, check if running on OpenBSD.
    :keyword bool aix: When :py:const:`True`, check if running on AIX.
    :keyword bool aarch64: When :py:const:`True`, check if running on AArch64.
    :keyword bool spawning:
        When :py:const:`True`, check if running on a platform which defaults
        multiprocessing to spawn
    """
    if windows and is_windows():
        return True
    if linux and is_linux():
        return True
    if darwin and is_darwin():
        return True
    if sunos and is_sunos():
        return True
    if smartos and is_smartos():
        return True
    if freebsd and is_freebsd():
        return True
    if netbsd and is_netbsd():
        return True
    if openbsd and is_openbsd():
        return True
    if aix and is_aix():
        return True
    if aarch64 and is_aarch64():
        return True
    if spawning and is_spawning_platform():
        return True
    return False


def is_fips_enabled() -> bool:
    """
    Check is FIPS is enabled.

    :return bool: Return true when enabled
    """
    if pathlib.Path('/etc/system-fips').exists():
        return True
    kernel_fips_enabled_path = pathlib.Path('/proc/sys/crypto/fips_enabled')
    if (
        kernel_fips_enabled_path.exists()
        and kernel_fips_enabled_path.read_text(encoding='utf-8').strip() == '1'
    ):
        return True
    sysctl_path = shutil.which('sysctl')
    if not sysctl_path:
        return False
    ret = subprocess.run(
        [sysctl_path, 'crypto.fips_enabled'],
        check=False,
        shell=False,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if ret.returncode == 0:
        stripped_output = ret.stdout.strip()
        if not stripped_output:
            return False
        if '=' not in stripped_output:
            return False
        if stripped_output.split('=')[-1].strip() == '1':
            return True
    return False
