import re


def check_overflow(info):
    overflow = []
    info_list = info[0].split(' ')
    while len(''.join(info_list).strip()) > 130:
        # No check for if overflow is also too long
        overflow.append(info_list.pop())
    return (info_list, overflow)


def get_kernel_details(conn, cmd):
    (return_code, info) = conn.get_shellcmdoutput(cmd)
    if return_code != 0:
        return 'Could not retrieve output of "%s"' % cmd
    (checked_info, overflow) = check_overflow(info)
    # Trying to be clever with checking overflow here but this may not actually be a good solution (Ash??)
    if overflow:
        overflow_str = ''.join(overflow)
        conn.proc.logfile_read.write('\n\n**WARNING: Bundle stream parameter length limit exceeded for command "%s"\nAdditional arguments were "%s"\n' % (cmd, overflow_str))
    return ''.join(checked_info)


# read log file and get U-Boot and spl strings
def get_log_with_regex(conn, regex):
    match = ''
    pattern = re.compile(regex)

    # Reset cursor to beginning of file
    conn.proc.logfile_read.seek(0)
    for line in conn.proc.logfile_read:
        if pattern.search(line):
            match = line.strip()
            match.replace(' ', '_')
            break
    conn.proc.logfile_read.seek(0, 2)
    return match


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

    NOTE: 'version' value is limited to 130 characters
    """

    packages =  get_package_info(conn)
    packages.extend([
        {'name': 'u-boot', 'version': get_log_with_regex(conn, 'U-Boot')},
        {'name': 'spl', 'version': get_log_with_regex(conn, 'Texas Instruments')},
        {'name': 'kernel_args', 'version': get_kernel_details(conn, 'cat /proc/cmdline')}
    ])
    software_context = {'image': {'name': get_kernel_details(conn, 'uname -a')},
                        'packages': packages
                        }
    return software_context
