# Copyright 2021-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Namespaced ``socket`` module.

This module's sole purpose is to have the standard library :py:mod:`socket` module
functions under a different namespace to be used in pytest-skip-markers so that
projects using it, which need to mock :py:mod:`socket` functions, don't influence
the pytest-skip-markers run time behavior.
"""
from __future__ import generator_stop
from socket import *
