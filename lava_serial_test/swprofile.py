import re


def get_kernel_details(conn):
    info = ''
    (return_code, info) = conn.get_shellcmdoutput('uname -a')
    return ''.join(info).strip()


def get_kernel_args(conn):
    info = ''
    (return_code, info) = conn.get_shellcmdoutput('cat /proc/cmdline')
    return ''.join(info).strip()


# read log file and get U-Boot and Texas Instruments
def get_uboot_info(conn):
    ti, uboot = '', ''
    ti_pattern, uboot_pattern = re.compile("Texas Instruments"), re.compile("U-Boot")
    found_ti, found_uboot = False, False

    # Reset cursor to beginning of file
    conn.proc.logfile_read.seek(0)
    for line in conn.proc.logfile_read:
        if ti_pattern.search(line) and not found_ti:
            ti, found_ti = line.strip(), True
        elif uboot_pattern.search(line) and not found_uboot:
            uboot, found_uboot = line.strip(), True
    return ti, uboot


def get_package_info(conn):
    packages_info = []
    (return_code, pkginfo) = conn.get_shellcmdoutput('opkg list_installed')

    if pkginfo is None or return_code != 0:
        return packages_info
    pattern = re.compile(
                    ("^\s*(?P<package_name>[^:]+?)\s+-"
                     "\s+(?P<version>[^\s].+)\s*$"), re.M)

    for line in pkginfo:
        match = pattern.search(line)
        if match:
            package_name, version = match.groups()
            package = {'name': package_name.strip(),
                'version': version.strip()}
            packages_info.append(package)
    return packages_info


def get_software_context(conn):
    """
    Return dict used for storing software_context information

    image - the image information of the gumstix device
    uboot - the image information of the gumstix device
    args - the command line arguments
    packages - opkg information for the gumstix device
    """

    software_context = {'image': {'name': get_kernel_details(conn)},
    #                    'uboot_ti_info': get_uboot_info(conn),
    #                    'args': get_kernel_args(conn),
                        'packages': get_package_info(conn)
                        }
    return software_context
