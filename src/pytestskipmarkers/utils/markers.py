# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
PyTest Markers related utilities.

..
    PYTEST_DONT_REWRITE
"""
import contextlib
import logging
import os
import shutil
from typing import Any
from typing import cast
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Union

import pytest

import pytestskipmarkers.utils.platform
import pytestskipmarkers.utils.ports as ports
import pytestskipmarkers.utils.socket as socket

if TYPE_CHECKING:
    from _pytest.nodes import Item

log = logging.getLogger(__name__)


def skip_if_not_root() -> Optional[str]:
    """
    Helper function to check for root/Administrator privileges.

    Returns:
        str: The reason of the skip
    """
    if not pytestskipmarkers.utils.platform.is_windows():
        if os.getuid() != 0:
            return "You must be logged in as root to run this test"
    else:
        from pytestskipmarkers.utils import win_functions

        current_user = win_functions.get_current_user()
        if TYPE_CHECKING:
            assert current_user
        if current_user != "SYSTEM":
            if not win_functions.is_admin(cast(str, current_user)):
                return "You must be logged in as an Administrator to run this test"
    return None


def skip_if_binaries_missing(
    binaries: Union[List[str], Tuple[str, ...]],
    check_all: bool = True,
    reason: Optional[str] = None,
) -> Optional[str]:
    """
    Helper function to check for existing binaries.

    Args:
        binaries (list or tuple):
            Iterator of binaries to check
        check_all (bool):
            If ``check_all`` is ``True``, the default, all binaries must exist.
            If ``check_all`` is ``False``, then only one the passed binaries needs to be found.
            Useful when, for example, passing a list of python interpreter names(python3.5,
            python3, python), where only one needs to exist.
        reason (str):
            The skip reason.

    Returns:
        str: The reason for the skip.
        None: Should not be skipped.
    """
    if check_all is False:
        # We only need one of the passed binaries to exist
        for binary in binaries:
            if shutil.which(binary) is not None:
                break
        else:
            if reason is not None:
                return reason
            return "None of the following binaries was found: {}".format(", ".join(binaries))
    else:
        for binary in binaries:
            if shutil.which(binary) is None:
                if reason is not None:
                    return reason
                return f"The '{binary}' binary was not found"
    log.debug("All binaries found. Searched for: %s", ", ".join(binaries))
    return None


def skip_if_no_local_network() -> Optional[str]:
    """
    Helper function to check for existing local network.

    Returns:
        str: The reason for the skip.
        None: Should not be skipped.
    """
    check_port = ports.get_unused_localhost_port()
    has_local_network = False
    try:
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as pubsock:
            pubsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            pubsock.bind(("", check_port))
        has_local_network = True
    except OSError:
        # I wonder if we just have IPV6 support?
        try:
            with contextlib.closing(socket.socket(socket.AF_INET6, socket.SOCK_STREAM)) as pubsock:
                pubsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                pubsock.bind(("", check_port))
            has_local_network = True
        except OSError:
            # Let's continue
            pass
    if has_local_network is False:
        return "No local network was detected"
    return None


def skip_if_no_remote_network() -> Optional[str]:
    """
    Helper function to check for existing remote network(internet).

    Returns:
        str: The reason for the skip.
        None: Should not be skipped.
    """
    if os.environ.get("NO_INTERNET"):
        return "Environment variable NO_INTERNET is set"

    # We are using the google.com DNS records as numerical IPs to avoid
    # DNS look ups which could greatly slow down this check
    has_remote_network = False
    for addr in (
        "172.217.17.14",
        "172.217.16.238",
        "173.194.41.198",
        "173.194.41.199",
        "173.194.41.200",
        "173.194.41.201",
        "173.194.41.206",
        "173.194.41.192",
        "173.194.41.193",
        "173.194.41.194",
        "173.194.41.195",
        "173.194.41.196",
        "173.194.41.197",
        "216.58.201.174",
    ):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.25)
            sock.connect((addr, 80))
            sock.close()
            # We connected? Stop the loop
            has_remote_network = True
            break
        except OSError:
            # Let's check the next IP
            continue

    if has_remote_network is False:
        return "No internet network connection was detected"
    return None


def skip_on_env(
    varname: str,
    present: bool = True,
    eq: Optional[str] = None,
    ne: Optional[str] = None,
    reason: Optional[str] = None,
) -> Optional[str]:
    """
    Helper function to check for environment variables.

    If any of the checks match, return the skip reason.

    Args:
        varname(str):
            The environment variable to check
        present(bool):
            When ``True``, skip if variable is present in the environment.
            When ``False``, skip if variable is not present in the environment.
        eq(str):
            Skips when the variable is present in the environment and matches this value.
        ne(str):
            Skips when the variable is present in the environment and does not match this value.
        reason(str):
            The custom reason message to use.

    Returns:
        str: The skip reason
        None: Should not be skipped.
    """
    if eq and ne:
        raise pytest.UsageError("Cannot pass both `eq` and `ne`.")
    if present is False and (eq or ne):
        raise pytest.UsageError("Cannot pass `present=False` and either `eq` or `ne`.")
    if present is False and varname not in os.environ:
        if not reason:
            reason = f"The variable '{varname}' is not present in the environ."
        return reason
    elif present is True and varname in os.environ:
        varname_value = os.environ[varname]
        if eq:
            if varname_value == eq:
                if not reason:
                    reason = f"'{varname}' present in environ and '{varname}=={eq}'"
        elif ne:
            if varname_value != ne:
                if not reason:
                    reason = f"'{varname}' present in environ and '{varname}!={eq}'"
        elif not reason:
            reason = f"The variable '{varname}' is present in the environ."
        return reason
    return None


def evaluate_markers(item: "Item") -> None:
    """
    Fixtures injection based on markers or test skips based on CLI arguments.
    """
    destructive_tests_marker = item.get_closest_marker("destructive_test")
    if destructive_tests_marker is not None:
        if destructive_tests_marker.args or destructive_tests_marker.kwargs:
            raise pytest.UsageError(
                "The 'destructive_test' marker does not accept any arguments or keyword arguments"
            )
        if item.config.getoption("--run-destructive") is False:
            raise pytest.skip.Exception("Destructive tests are disabled", _use_item_location=True)

    expensive_tests_marker = item.get_closest_marker("expensive_test")
    if expensive_tests_marker is not None:
        if expensive_tests_marker.args or expensive_tests_marker.kwargs:
            raise pytest.UsageError(
                "The 'expensive_test' marker does not accept any arguments or keyword arguments"
            )
        if item.config.getoption("--run-expensive") is False:
            raise pytest.skip.Exception("Expensive tests are disabled", _use_item_location=True)

    skip_if_not_root_marker = item.get_closest_marker("skip_if_not_root")
    if skip_if_not_root_marker is not None:
        if skip_if_not_root_marker.args or skip_if_not_root_marker.kwargs:
            raise pytest.UsageError(
                "The 'skip_if_not_root' marker does not accept any arguments or keyword arguments"
            )
        skip_reason = skip_if_not_root()
        if skip_reason:
            raise pytest.skip.Exception(skip_reason, _use_item_location=True)

    skip_if_binaries_missing_marker = item.get_closest_marker("skip_if_binaries_missing")
    if skip_if_binaries_missing_marker is not None:
        binaries = skip_if_binaries_missing_marker.args
        if not binaries:
            raise pytest.UsageError(
                "The 'skip_if_binaries_missing' marker needs at least one binary name to be passed"
            )
        for arg in binaries:
            if not isinstance(arg, str):
                raise pytest.UsageError(
                    "The 'skip_if_binaries_missing' marker only accepts strings as arguments. If you are "
                    "trying to pass multiple binaries, each binary should be an separate argument."
                )
        message = cast(Dict[str, Any], skip_if_binaries_missing_marker.kwargs).pop("message", None)
        if message:
            item.warn(
                pytest.PytestWarning(
                    """Please stop passing 'message="{0}"' and instead pass 'reason="{0}"'""".format(
                        message
                    )
                )
            )
            cast(Dict[str, Any], skip_if_binaries_missing_marker.kwargs)["reason"] = message
        skip_reason = skip_if_binaries_missing(binaries, **skip_if_binaries_missing_marker.kwargs)
        if skip_reason:
            raise pytest.skip.Exception(skip_reason, _use_item_location=True)

    requires_network_marker = item.get_closest_marker("requires_network")
    if requires_network_marker is not None:
        only_local_network = requires_network_marker.kwargs.get("only_local_network", False)
        local_skip_reason = skip_if_no_local_network()
        if local_skip_reason:
            # Since we're only supposed to check local network, and no
            # local network was detected, skip the test
            raise pytest.skip.Exception(local_skip_reason, _use_item_location=True)

        if only_local_network is False:
            remote_skip_reason = skip_if_no_remote_network()
            if remote_skip_reason:
                raise pytest.skip.Exception(remote_skip_reason, _use_item_location=True)

    # Platform Skip Markers
    skip_on_windows_marker = item.get_closest_marker("skip_on_windows")
    if skip_on_windows_marker is not None:
        if skip_on_windows_marker.args:
            raise pytest.UsageError("The skip_on_windows marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_windows_marker.kwargs).pop("reason", None)
        if skip_on_windows_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_windows marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on Windows"
        if pytestskipmarkers.utils.platform.is_windows():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_windows_marker = item.get_closest_marker("skip_unless_on_windows")
    if skip_unless_on_windows_marker is not None:
        if skip_unless_on_windows_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_windows marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_windows_marker.kwargs).pop("reason", None)
        if skip_unless_on_windows_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_windows marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not Windows, skipped"
        if not pytestskipmarkers.utils.platform.is_windows():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_linux_marker = item.get_closest_marker("skip_on_linux")
    if skip_on_linux_marker is not None:
        if skip_on_linux_marker.args:
            raise pytest.UsageError("The skip_on_linux marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_linux_marker.kwargs).pop("reason", None)
        if skip_on_linux_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_linux marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on Linux"
        if pytestskipmarkers.utils.platform.is_linux():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_linux_marker = item.get_closest_marker("skip_unless_on_linux")
    if skip_unless_on_linux_marker is not None:
        if skip_unless_on_linux_marker.args:
            raise pytest.UsageError("The skip_unless_on_linux marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_unless_on_linux_marker.kwargs).pop("reason", None)
        if skip_unless_on_linux_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_linux marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not Linux, skipped"
        if not pytestskipmarkers.utils.platform.is_linux():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_darwin_marker = item.get_closest_marker("skip_on_darwin")
    if skip_on_darwin_marker is not None:
        if skip_on_darwin_marker.args:
            raise pytest.UsageError("The skip_on_darwin marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_darwin_marker.kwargs).pop("reason", None)
        if skip_on_darwin_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_darwin marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on Darwin"
        if pytestskipmarkers.utils.platform.is_darwin():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_darwin_marker = item.get_closest_marker("skip_unless_on_darwin")
    if skip_unless_on_darwin_marker is not None:
        if skip_unless_on_darwin_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_darwin marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_darwin_marker.kwargs).pop("reason", None)
        if skip_unless_on_darwin_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_darwin marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not Darwin, skipped"
        if not pytestskipmarkers.utils.platform.is_darwin():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_sunos_marker = item.get_closest_marker("skip_on_sunos")
    if skip_on_sunos_marker is not None:
        if skip_on_sunos_marker.args:
            raise pytest.UsageError("The skip_on_sunos marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_sunos_marker.kwargs).pop("reason", None)
        if skip_on_sunos_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_sunos marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on SunOS"
        if pytestskipmarkers.utils.platform.is_sunos():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_sunos_marker = item.get_closest_marker("skip_unless_on_sunos")
    if skip_unless_on_sunos_marker is not None:
        if skip_unless_on_sunos_marker.args:
            raise pytest.UsageError("The skip_unless_on_sunos marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_unless_on_sunos_marker.kwargs).pop("reason", None)
        if skip_unless_on_sunos_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_sunos marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not SunOS, skipped"
        if not pytestskipmarkers.utils.platform.is_sunos():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_smartos_marker = item.get_closest_marker("skip_on_smartos")
    if skip_on_smartos_marker is not None:
        if skip_on_smartos_marker.args:
            raise pytest.UsageError("The skip_on_smartos marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_smartos_marker.kwargs).pop("reason", None)
        if skip_on_smartos_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_smartos marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on SmartOS"
        if pytestskipmarkers.utils.platform.is_smartos():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_smartos_marker = item.get_closest_marker("skip_unless_on_smartos")
    if skip_unless_on_smartos_marker is not None:
        if skip_unless_on_smartos_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_smartos marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_smartos_marker.kwargs).pop("reason", None)
        if skip_unless_on_smartos_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_smartos marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not SmartOS, skipped"
        if not pytestskipmarkers.utils.platform.is_smartos():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_freebsd_marker = item.get_closest_marker("skip_on_freebsd")
    if skip_on_freebsd_marker is not None:
        if skip_on_freebsd_marker.args:
            raise pytest.UsageError("The skip_on_freebsd marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_freebsd_marker.kwargs).pop("reason", None)
        if skip_on_freebsd_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_freebsd marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on FreeBSD"
        if pytestskipmarkers.utils.platform.is_freebsd():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_freebsd_marker = item.get_closest_marker("skip_unless_on_freebsd")
    if skip_unless_on_freebsd_marker is not None:
        if skip_unless_on_freebsd_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_freebsd marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_freebsd_marker.kwargs).pop("reason", None)
        if skip_unless_on_freebsd_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_freebsd marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not FreeBSD, skipped"
        if not pytestskipmarkers.utils.platform.is_freebsd():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_netbsd_marker = item.get_closest_marker("skip_on_netbsd")
    if skip_on_netbsd_marker is not None:
        if skip_on_netbsd_marker.args:
            raise pytest.UsageError("The skip_on_netbsd marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_netbsd_marker.kwargs).pop("reason", None)
        if skip_on_netbsd_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_netbsd marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on NetBSD"
        if pytestskipmarkers.utils.platform.is_netbsd():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_netbsd_marker = item.get_closest_marker("skip_unless_on_netbsd")
    if skip_unless_on_netbsd_marker is not None:
        if skip_unless_on_netbsd_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_netbsd marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_netbsd_marker.kwargs).pop("reason", None)
        if skip_unless_on_netbsd_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_netbsd marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not NetBSD, skipped"
        if not pytestskipmarkers.utils.platform.is_netbsd():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_openbsd_marker = item.get_closest_marker("skip_on_openbsd")
    if skip_on_openbsd_marker is not None:
        if skip_on_openbsd_marker.args:
            raise pytest.UsageError("The skip_on_openbsd marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_openbsd_marker.kwargs).pop("reason", None)
        if skip_on_openbsd_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_openbsd marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on OpenBSD"
        if pytestskipmarkers.utils.platform.is_openbsd():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_openbsd_marker = item.get_closest_marker("skip_unless_on_openbsd")
    if skip_unless_on_openbsd_marker is not None:
        if skip_unless_on_openbsd_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_openbsd marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_openbsd_marker.kwargs).pop("reason", None)
        if skip_unless_on_openbsd_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_openbsd marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not OpenBSD, skipped"
        if not pytestskipmarkers.utils.platform.is_openbsd():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_aix_marker = item.get_closest_marker("skip_on_aix")
    if skip_on_aix_marker is not None:
        if skip_on_aix_marker.args:
            raise pytest.UsageError("The skip_on_aix marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_aix_marker.kwargs).pop("reason", None)
        if skip_on_aix_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_aix marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on AIX"
        if pytestskipmarkers.utils.platform.is_aix():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_aix_marker = item.get_closest_marker("skip_unless_on_aix")
    if skip_unless_on_aix_marker is not None:
        if skip_unless_on_aix_marker.args:
            raise pytest.UsageError("The skip_unless_on_aix marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_unless_on_aix_marker.kwargs).pop("reason", None)
        if skip_unless_on_aix_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_aix marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not AIX, skipped"
        if not pytestskipmarkers.utils.platform.is_aix():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_aarch64_marker = item.get_closest_marker("skip_on_aarch64")
    if skip_on_aarch64_marker is not None:
        if skip_on_aarch64_marker.args:
            raise pytest.UsageError("The skip_on_aarch64 marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_aarch64_marker.kwargs).pop("reason", None)
        if skip_on_aarch64_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_aarch64 marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on AArch64"
        if pytestskipmarkers.utils.platform.is_aarch64():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_aarch64_marker = item.get_closest_marker("skip_unless_on_aarch64")
    if skip_unless_on_aarch64_marker is not None:
        if skip_unless_on_aarch64_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_aarch64 marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_aarch64_marker.kwargs).pop("reason", None)
        if skip_unless_on_aarch64_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_aarch64 marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not AArch64, skipped"
        if not pytestskipmarkers.utils.platform.is_aarch64():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_spawning_platform_marker = item.get_closest_marker("skip_on_spawning_platform")
    if skip_on_spawning_platform_marker is not None:
        if skip_on_spawning_platform_marker.args:
            raise pytest.UsageError(
                "The skip_on_spawning_platform marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_on_spawning_platform_marker.kwargs).pop("reason", None)
        if skip_on_spawning_platform_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_spawning_platform marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on spawning platforms"
        if pytestskipmarkers.utils.platform.is_spawning_platform():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_spawning_platform_marker = item.get_closest_marker(
        "skip_unless_on_spawning_platform"
    )
    if skip_unless_on_spawning_platform_marker is not None:
        if skip_unless_on_spawning_platform_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_spawning_platform marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_spawning_platform_marker.kwargs).pop(
            "reason", None
        )
        if skip_unless_on_spawning_platform_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_spawning_platform marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform does not default multiprocessing to spawn, skipped"
        if not pytestskipmarkers.utils.platform.is_spawning_platform():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_photonos_marker = item.get_closest_marker("skip_on_photonos")
    if skip_on_photonos_marker is not None:
        if skip_on_photonos_marker.args:
            raise pytest.UsageError("The skip_on_photonos marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_photonos_marker.kwargs).pop("reason", None)
        if skip_on_photonos_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_photonos marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on PhotonOS"
        if pytestskipmarkers.utils.platform.is_photonos():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_unless_on_photonos_marker = item.get_closest_marker("skip_unless_on_photonos")
    if skip_unless_on_photonos_marker is not None:
        if skip_unless_on_photonos_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_photonos marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_photonos_marker.kwargs).pop("reason", None)
        if skip_unless_on_photonos_marker.kwargs:
            raise pytest.UsageError(
                "The skip_unless_on_photonos marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Platform is not PhotonOS, skipped"
        if not pytestskipmarkers.utils.platform.is_photonos():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_fips_enabled_platform_marker = item.get_closest_marker("skip_on_fips_enabled_platform")
    if skip_on_fips_enabled_platform_marker is not None:
        if skip_on_fips_enabled_platform_marker.args:
            raise pytest.UsageError(
                "The skip_on_fips_enabled_platform marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_on_fips_enabled_platform_marker.kwargs).pop(
            "reason", None
        )
        if skip_on_fips_enabled_platform_marker.kwargs:
            raise pytest.UsageError(
                "The skip_on_fips_enabled_platform marker only accepts 'reason' as a keyword argument."
            )
        if reason is None:
            reason = "Skipped on FIPS enabled platform"
        if pytestskipmarkers.utils.platform.is_fips_enabled():
            raise pytest.skip.Exception(reason, _use_item_location=True)

    skip_on_platforms_marker = item.get_closest_marker("skip_on_platforms")
    if skip_on_platforms_marker is not None:
        if skip_on_platforms_marker.args:
            raise pytest.UsageError("The skip_on_platforms marker does not accept any arguments")
        reason = cast(Dict[str, Any], skip_on_platforms_marker.kwargs).pop("reason", None)
        if not skip_on_platforms_marker.kwargs:
            raise pytest.UsageError(
                "Pass at least one platform to skip_on_platforms as a keyword argument"
            )
        if not any(skip_on_platforms_marker.kwargs.values()):
            raise pytest.UsageError(
                "Pass at least one platform with a True value to skip_on_platforms as a keyword argument"
            )
        if reason is None:
            reason = "Skipped on platform match"
        try:
            if pytestskipmarkers.utils.platform.on_platforms(**skip_on_platforms_marker.kwargs):
                raise pytest.skip.Exception(reason, _use_item_location=True)
        except TypeError as exc:
            raise pytest.UsageError(f"Passed an invalid platform to skip_on_platforms: {exc}")

    skip_unless_on_platforms_marker = item.get_closest_marker("skip_unless_on_platforms")
    if skip_unless_on_platforms_marker is not None:
        if skip_unless_on_platforms_marker.args:
            raise pytest.UsageError(
                "The skip_unless_on_platforms marker does not accept any arguments"
            )
        reason = cast(Dict[str, Any], skip_unless_on_platforms_marker.kwargs).pop("reason", None)
        if not skip_unless_on_platforms_marker.kwargs:
            raise pytest.UsageError(
                "Pass at least one platform to skip_unless_on_platforms as a keyword argument"
            )
        if not any(skip_unless_on_platforms_marker.kwargs.values()):
            raise pytest.UsageError(
                "Pass at least one platform with a True value to skip_unless_on_platforms as a keyword argument"
            )
        if reason is None:
            reason = "Platform(s) do not match, skipped"
        try:
            if not pytestskipmarkers.utils.platform.on_platforms(
                **skip_unless_on_platforms_marker.kwargs
            ):
                raise pytest.skip.Exception(reason, _use_item_location=True)
        except TypeError as exc:
            raise pytest.UsageError(
                f"Passed an invalid platform to skip_unless_on_platforms: {exc}"
            )

    skip_on_env_marker = item.get_closest_marker("skip_on_env")
    if skip_on_env_marker is not None:
        args = list(skip_on_env_marker.args)
        if not args:
            raise pytest.UsageError(
                "The 'skip_on_env' marker needs at least one argument to be passed, the environment "
                "variable name."
            )
        envvar = args.pop(0)
        if args:
            raise pytest.UsageError(
                "The 'skip_on_env' only accepts one argument, the environment variable name."
            )
        if not isinstance(envvar, str):
            raise pytest.UsageError("The environment variable argument must be a string.")

        kwargs = cast(Dict[str, Any], skip_on_env_marker.kwargs).copy()
        present = kwargs.pop("present", True)
        eq = kwargs.pop("eq", None)
        ne = kwargs.pop("ne", None)
        reason = kwargs.pop("reason", None)
        if kwargs:
            raise pytest.UsageError(
                "The 'skip_on_env' marker only accepts 'present', 'eq', 'ne' and 'reason' as "
                "keyword arguments."
            )
        skip_reason = skip_on_env(envvar, present=present, eq=eq, ne=ne, reason=reason)
        if skip_reason:
            raise pytest.skip.Exception(skip_reason, _use_item_location=True)
