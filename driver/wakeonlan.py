# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Wake on LAN Power Driver"""

__all__ = []

from provisioningserver.drivers import (
    make_ip_extractor,
    make_setting_field,
    SETTING_SCOPE,
)
from provisioningserver.drivers.power import PowerDriver
from provisioningserver.logger import get_maas_logger
from provisioningserver.utils import shell
from twisted.internet.defer import maybeDeferred
import subprocess


maaslog = get_maas_logger("drivers.power.wakeonlan")

REQUIRED_PACKAGES = [["wakeonlan", "wakeonlan"]]

class WakeOnLANPowerDriver(PowerDriver):

    name = 'wakeonlan'
    description = "Wake on LAN Power Driver"
    settings = [
        make_setting_field('power_mac', "MAC address", required=True),
    ]
    ip_extractor = None
    queryable = False

    def detect_missing_packages(self):
        missing_packages = set()
        for binary, package in REQUIRED_PACKAGES:
            if not shell.has_command_available(binary):
                missing_packages.add(package)
        return list(missing_packages)

    def on(self, system_id, context):
        """Override `on` as we do not need retry logic."""
        return maybeDeferred(self.power_on, system_id, context)

    def off(self, system_id, context):
        """Override `off` as we do not need retry logic."""
        return maybeDeferred(self.power_off, system_id, context)

    def query(self, system_id, context):
        """Override `query` as we do not need retry logic."""
        return maybeDeferred(self.power_query, system_id, context)

    def power_on(self, system_id, context):
        """Power on machine using wake on lan."""
        subprocess.call(["wakeonlan", context.get("power_mac")])


    def power_off(self, system_id, context):
        """Power off machine manually."""
        maaslog.info(
            "You need to power off %s manually." % system_id)

    def power_query(self, system_id, context):
        """Power query machine manually."""
        maaslog.info(
            "You need to check power state of %s manually." % system_id)
        return 'unknown'
