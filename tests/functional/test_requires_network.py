"""
    tests.functional.markers.test_requires_network
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the ``@pytest.mark.requires_network`` marker
"""
from unittest import mock

from pytestskipmarkers.utils import ports
from pytestskipmarkers.utils import socket


def test_has_local_network(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.requires_network
        def test_one():
            assert True
        """
    )
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
            res = pytester.runpytest_inprocess("-p", "no:salt-factories-log-server")
            res.assert_outcomes(skipped=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")
