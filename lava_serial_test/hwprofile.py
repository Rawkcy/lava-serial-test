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


def get_hardware_info(conn):
    """
    Return a list of gathered hardware information
    """
    pattern = re.compile('^(?P<key>.+?)\s*:\s*(?P<value>.*)$')
    devices = []


def get_hardware_context(conn):
    """
    Return a dict of hardware profile information
    """
    hardware_context = {}
    devices = []
    devices.extend(get_cpu(conn))
    hardware_context['devices'] = devices
    return hardware_context
