import sys
import re


ARM_KEYMAP = {
    'Processor': 'cpu_model_name',
    'Features': 'cpu_features',
    'CPU implementer': 'cpu_implementer',
    'CPU architecture': 'cpu_architecture',
    'CPU variant': 'cpu_variant',
    'CPU part': 'cpu_part',
    'CPU revision': 'cpu_revision',
}

ARM_VALMAP = {
    'CPU implementer': lambda value: int(value, 16),
    'CPU architecture': int,
    'CPU variant': lambda value: int(value, 16),
    'CPU part': lambda value: int(value, 16),
    'CPU revision': int,
}


def get_cpu_devs(conn):
    """
    Return a list of gathered hardware information
    """
    pattern = re.compile('^(?P<key>.+?)\s*:\s*(?P<value>.*)$')
    cpunum = 0
    devices = []
    cpudevs = []
    cpudevs.append({})

    # TODO maybe there is other types
    keymap, valmap = ARM_KEYMAP, ARM_VALMAP

    try:
        (retcode, cpuinfo) = conn.do("cat /proc/cpuinfo")
        if retcode != 0 or cpuinfo is None:
            raise IOError("Failed to get content of file(%s)" % "/proc/cpuinfo")
        for line in cpuinfo:
            match = pattern.match(line)
            if match:
                key, value = match.groups()
                key = key.strip()
                value = value.strip()
                try:
                    key, value = _translate_cpuinfo(keymap, valmap, key, value)
                except ValueError:
                    pass
                if cpudevs[cpunum].get(key):
                    cpunum += 1
                    cpudevs.append({})
                cpudevs[cpunum][key] = value
        for c in range(len(cpudevs)):
            device = {}
            device['device_type'] = 'device.cpu'
            device['description'] = 'Processor #{0}'.format(c)
            device['attributes'] = cpudevs[c]
            devices.append(device)
    except IOError:
        print >> sys.stderr, "WARNING: Could not read cpu information"
    return devices

def get_mem_devs(conn):
    """ Return a list of memory devices

    This returns up to two items, one for physical RAM and another for swap
    """
    devices = []

    pattern = re.compile('^(?P<key>.+?)\s*:\s*(?P<value>.+) kB$', re.M)

    try:
        (retcode, meminfo) = conn.do("cat /proc/meminfo")
        if retcode != 0 or meminfo is None:
            raise IOError("Faile to get content of file(%s)" % "/proc/meminfo")
        for line in meminfo:
            match = pattern.search(line)
            if not match:
                continue
            key, value = match.groups()
            key = key.strip()
            value = value.strip()
            if key not in ('MemTotal', 'SwapTotal'):
                continue
            #Kernel reports in 2^10 units
            capacity = int(value) << 10
            if capacity == 0:
                continue
            if key == 'MemTotal':
                kind = 'RAM'
            else:
                kind = 'swap'
            description = "{capacity}MiB of {kind}".format(
                capacity=capacity >> 20, kind=kind)
            device = {}
            device['description'] = description
            device['attributes'] = {'capacity': str(capacity), 'kind': kind}
            device['device_type'] = "device.mem"
            devices.append(device)
    except IOError:
        print >> sys.stderr, "WARNING: Could not read memory information"
    return devices


def get_hardware_context(conn):
    """
    Return a dict of hardware profile information
    """
    hardware_context = {}
    devices = []
    devices.extend(get_cpu_devs(conn))
    devices.extend(get_mem_devs(conn))
    hardware_context['devices'] = devices
    return hardware_context
