# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the "skip_if_no_remote_network" marker helper.
"""
import os
from unittest import mock

import pytestskipmarkers.utils.markers as markers
from pytestskipmarkers.utils import socket


def test_has_remote_network():
    with mock.patch("pytestskipmarkers.utils.markers.socket.socket"):
        assert markers.skip_if_no_remote_network() is None


def test_no_remote_network():
    mock_socket = mock.MagicMock()
    mock_socket.connect = mock.MagicMock(side_effect=socket.error)
    with mock.patch("pytestskipmarkers.utils.markers.socket.socket", return_value=mock_socket):
        skip_reason = markers.skip_if_no_remote_network()
        assert skip_reason is not None
        assert skip_reason == "No internet network connection was detected"


def test_remote_network_with_no_internet_env_variable():
    with mock.patch.dict(os.environ, {"NO_INTERNET": "1"}):
        skip_reason = markers.skip_if_no_remote_network()
        assert skip_reason is not None
        assert skip_reason == "Environment variable NO_INTERNET is set"
