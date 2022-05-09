# Copyright 2021-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the ``@pytest.mark.requires_network`` marker.
"""
import sys
from unittest import mock

import pytest

from pytestskipmarkers.utils import ports
from pytestskipmarkers.utils import socket

pytestmark = [
    pytest.mark.skipif(
        sys.platform.startswith("win")
        and sys.version_info >= (3, 8)
        and sys.version_info < (3, 10),
        reason="PyTest's capture and pytester.runpytest_inprocess looks broken on Windows and Py(>3.8,<3.10)",
    ),
]


def test_has_local_network(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.requires_network
        def test_one():
            assert True
        """
    )
    with mock.patch(
        "pytestskipmarkers.utils.ports.get_unused_localhost_port",
        side_effect=[ports.get_unused_localhost_port() for n in range(10)],
    ):
        with mock.patch("pytestskipmarkers.utils.markers.socket.socket"):
            res = pytester.runpytest()
            res.assert_outcomes(passed=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_no_local_network(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.requires_network
        def test_one():
            assert True
        """
    )
    mock_socket = mock.MagicMock()
    mock_socket.bind = mock.MagicMock(side_effect=socket.error)
    with mock.patch(
        "pytestskipmarkers.utils.ports.get_unused_localhost_port",
        side_effect=[ports.get_unused_localhost_port() for n in range(10)],
    ):
        with mock.patch("pytestskipmarkers.utils.markers.socket.socket", return_value=mock_socket):
            res = pytester.runpytest_inprocess()
            res.assert_outcomes(skipped=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")
