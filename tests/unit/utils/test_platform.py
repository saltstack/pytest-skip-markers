# Copyright 2021-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Tests for pytestskipmarkers.utils.platform.
"""
import logging
import subprocess
from unittest import mock

import pytest

import pytestskipmarkers.utils.platform

log = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def reset_lru_cache():
    for name in dir(pytestskipmarkers.utils.platform):
        if not name.startswith("is_"):
            continue
        func = getattr(pytestskipmarkers.utils.platform, name, None)
        if func:
            try:
                func.cache_clear()
                log.debug("Called %s.cache_clear()", func.__qualname__)
            except AttributeError:
                pass
    try:
        yield
    finally:
        for name in dir(pytestskipmarkers.utils.platform):
            if not name.startswith("is_"):
                continue
            func = getattr(pytestskipmarkers.utils.platform, name, None)
            if func:
                try:
                    func.cache_clear()
                    log.debug("Called %s.cache_clear()", func.__qualname__)
                except AttributeError:
                    pass


def test_is_linux():
    return_value = True
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="linux")):
        assert pytestskipmarkers.utils.platform.is_linux() is return_value


def test_is_not_linux():
    return_value = False
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="win32")):
        assert pytestskipmarkers.utils.platform.is_linux() is return_value


def test_is_darwin():
    return_value = True
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="darwin")):
        assert pytestskipmarkers.utils.platform.is_darwin() is return_value


def test_is_not_darwin():
    return_value = False
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="linux")):
        assert pytestskipmarkers.utils.platform.is_darwin() is return_value


def test_is_windows():
    return_value = True
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="win32")):
        assert pytestskipmarkers.utils.platform.is_windows() is return_value


def test_is_not_windows():
    return_value = False
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="linux")):
        assert pytestskipmarkers.utils.platform.is_windows() is return_value


def test_is_sunos():
    return_value = True
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="sunos")):
        assert pytestskipmarkers.utils.platform.is_sunos() is return_value


def test_is_not_sunos():
    return_value = False
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="linux")):
        assert pytestskipmarkers.utils.platform.is_sunos() is return_value


@pytest.mark.skip_on_windows(reason="Windows does not have `os.uname()`")
def test_is_smartos():
    return_value = True
    with mock.patch("pytestskipmarkers.utils.platform.is_sunos", return_value=True), mock.patch(
        "os.uname", return_value=(None, None, None, "joyent_")
    ):
        assert pytestskipmarkers.utils.platform.is_smartos() is return_value


def is_sunos_ids(value):
    return "is_sunos={}".format(value)


@pytest.mark.skip_on_windows(reason="Windows does not have `os.uname()`")
@pytest.mark.parametrize("is_sunos", [True, False], ids=is_sunos_ids)
def test_is_not_smartos(is_sunos):
    return_value = False
    with mock.patch("pytestskipmarkers.utils.platform.is_sunos", return_value=is_sunos), mock.patch(
        "os.uname", return_value=(None, None, None, "joy")
    ):
        assert pytestskipmarkers.utils.platform.is_smartos() is return_value


def test_is_freebsd():
    return_value = True
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="freebsd")):
        assert pytestskipmarkers.utils.platform.is_freebsd() is return_value


def test_is_not_freebsd():
    return_value = False
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="linux")):
        assert pytestskipmarkers.utils.platform.is_freebsd() is return_value


def test_is_netbsd():
    return_value = True
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="netbsd")):
        assert pytestskipmarkers.utils.platform.is_netbsd() is return_value


def test_is_not_netbsd():
    return_value = False
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="linux")):
        assert pytestskipmarkers.utils.platform.is_netbsd() is return_value


def test_is_openbsd():
    return_value = True
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="openbsd")):
        assert pytestskipmarkers.utils.platform.is_openbsd() is return_value


def test_is_not_openbsd():
    return_value = False
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="freebsd")):
        assert pytestskipmarkers.utils.platform.is_openbsd() is return_value


def test_is_aix():
    return_value = True
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="aix")):
        assert pytestskipmarkers.utils.platform.is_aix() is return_value


def test_is_not_aix():
    return_value = False
    with mock.patch("sys.platform", new_callable=mock.PropertyMock(return_value="linux")):
        assert pytestskipmarkers.utils.platform.is_aix() is return_value


def test_is_aarch64():
    return_value = True
    with mock.patch("platform.machine", return_value="aarch64"):
        assert pytestskipmarkers.utils.platform.is_aarch64() is return_value


def test_is_not_aarch64():
    return_value = False
    with mock.patch("platform.machine", return_value="not_aarch64"):
        assert pytestskipmarkers.utils.platform.is_aarch64() is return_value


def test_is_fips_enabled_etc_system_fips(fs):
    fs.create_file("/etc/system-fips")
    assert pytestskipmarkers.utils.platform.is_fips_enabled() is True


@pytest.mark.parametrize("value, expected", [("0", False), ("1", True)])
def test_is_fips_enabled_procfs(fs, value, expected):
    fs.create_file("/proc/sys/crypto/fips_enabled", contents=value)
    assert pytestskipmarkers.utils.platform.is_fips_enabled() is expected


@pytest.mark.parametrize(
    "output, expected",
    (
        ("", False),
        ("crypto.fips_enabled", False),
        ("crypto.fips_enabled =", False),
        ("crypto.fips_enabled = 0", False),
        ("crypto.fips_enabled=1", True),
        ("crypto.fips_enabled = 1", True),
        ("crypto.fips_enabled =  1", True),
    ),
)
def test_is_fips_enabled_sysctl(output, expected):
    subprocess_run_return_value = subprocess.CompletedProcess(  # type: ignore[var-annotated]
        args=(), returncode=0, stdout=output, stderr=None
    )
    with mock.patch("shutil.which", return_value="sysctl"), mock.patch(
        "subprocess.run", return_value=subprocess_run_return_value
    ):
        assert pytestskipmarkers.utils.platform.is_fips_enabled() is expected


def test_is_spawning_platform():
    with mock.patch("multiprocessing.get_start_method", return_value="spawn"):
        assert pytestskipmarkers.utils.platform.is_spawning_platform() is True


def test_is_not_spawning_platform():
    with mock.patch("multiprocessing.get_start_method", return_value="fork"):
        assert pytestskipmarkers.utils.platform.is_spawning_platform() is False
