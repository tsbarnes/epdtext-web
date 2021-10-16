import datetime
import logging
import platform
import time

import humanize
import distro
import psutil

# Set the default to wlan0
NETWORK_INTERFACE = "wlan0"
logger = logging.getLogger('epdtext.libs.system')


class System:
    """
    This class provides access to system information
    """
    @staticmethod
    def get_size(data, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        :param data: the size in bytes
        :param suffix: which suffix to use as a single letter
        :return the size converted to the proper suffix
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if data < factor:
                return f"{data:.2f}{unit}{suffix}"
            data /= factor

    @staticmethod
    def temperature():
        return round(psutil.sensors_temperatures()['cpu_thermal'][0].current)

    @staticmethod
    def model():
        with open('/sys/firmware/devicetree/base/model', 'r') as model_file:
            return model_file.read()

    @staticmethod
    def system():
        return platform.system()

    @staticmethod
    def dist():
        return "{0} {1}".format(distro.name(), distro.version())

    @staticmethod
    def machine():
        return platform.machine()

    @staticmethod
    def node():
        return platform.node()

    @staticmethod
    def arch():
        return platform.architecture()[0]

    @staticmethod
    def uptime():
        return humanize.naturaldelta(datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME)))

    @staticmethod
    def network_total_sent():
        net_io = psutil.net_io_counters()
        return System.get_size(net_io.bytes_sent)

    @staticmethod
    def network_total_received():
        net_io = psutil.net_io_counters()
        return System.get_size(net_io.bytes_recv)

    @staticmethod
    def local_ipv4_address():
        for interface_name, interface_addresses in psutil.net_if_addrs().items():
            for address in interface_addresses:
                if interface_name == NETWORK_INTERFACE:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        return address.address
        return None


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Local IPv4 address: {}".format(System.local_ipv4_address()))
