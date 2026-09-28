# CHIRP driver for Quansheng UV-K5 Karina 11.08
#
# Full functionality is inherited from CHIRP's official UV-K5 driver:
# memories, VFO memories, tones/DTCS, power, bandwidth, scanlists,
# settings, FM memories, DTMF and the normal UV-K5 read/write protocol.
#
# This file only adds a Karina 11.08 model and accepts the Karina firmware.

from chirp import directory
from chirp.drivers import uvk5


@directory.register
@directory.detected_by(uvk5.UVK5Radio)
class Karina11Radio(uvk5.UVK5Radio):
    VENDOR = "Quansheng"
    MODEL = "UV-K5 Karina 11.08"
    VARIANT = "karina"

    @classmethod
    def k5_approve_firmware(cls, firmware):
        firmware = (firmware or "").lower()
        return "11.08" in firmware or "autumn rain" in firmware
