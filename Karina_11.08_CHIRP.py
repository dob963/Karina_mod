# CHIRP driver for Quansheng UV-K5 Karina 11.08
# Based on the standard CHIRP UV-K5 driver.
#
# This module keeps the normal UV-K5 memory/settings protocol and only
# accepts firmware identifying itself as Karina 11.08 (or "autumn rain").

from chirp import directory
from chirp.drivers import uvk5


@directory.register
class Karina11Radio(uvk5.UVK5RadioBase):
    VENDOR = "Quansheng"
    MODEL = "UV-K5 Karina 11.08"
    VARIANT = "karina"

    @classmethod
    def k5_approve_firmware(cls, firmware):
        firmware = (firmware or "").lower()
        return "11.08" in firmware or "autumn rain" in firmware
