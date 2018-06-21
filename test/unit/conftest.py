"""Test fixtures."""
from __future__ import print_function
from __future__ import unicode_literals

from builtins import super

import pytest
from napalm_base.test import conftest as parent_conftest

from napalm_base.test.double import BaseTestDouble
from napalm_base.utils import py23_compat

from napalm_procurve import procurve


@pytest.fixture(scope='class')
def set_device_parameters(request):
    """Set up the class."""
    def fin():
        request.cls.device.close()
    request.addfinalizer(fin)

    request.cls.driver = procurve.ProcurveDriver
    request.cls.patched_driver = PatchedProcurveDriver
    request.cls.vendor = 'procurve'
    parent_conftest.set_device_parameters(request)


def pytest_generate_tests(metafunc):
    """Generate test cases dynamically."""
    parent_conftest.pytest_generate_tests(metafunc, __file__)


class PatchedProcurveDriver(procurve.ProcurveDriver):
    """Patched Procurve Driver."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Patched Skeleton Driver constructor."""
        super().__init__(hostname, username, password, timeout, optional_args)

        self.patched_attrs = ['device']
        self.device = FakeProcurveDevice()

    def disconnect(self):
        pass

    def is_alive(self):
        return {
            'is_alive': True  # In testing everything works..
        }

    def open(self):
        pass


class FakeProcurveDevice(BaseTestDouble):
    """Procurve device test double."""

    def send_command(self, command):
        """Fake run_commands."""
        filename = '{}.{}'.format(self.sanitize_text(command), 'txt')
        full_path = self.find_file(filename)
        result = self.read_txt_file(full_path)
        return py23_compat.text_type(result)

    def disconnect(self):
        pass
