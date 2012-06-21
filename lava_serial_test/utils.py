def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def clean_and_return_log(conn):
    """
    Clean out non ascii characters from logfile
    Returns clean list of data

    NOTE: we seek twice to read and write from beginning
    """
    conn.proc.logfile_read.seek(0)
    lines = conn.proc.logfile_read.readlines()
    for line in lines:
        if not is_ascii(line):
            lines.remove(line)

    conn.proc.logfile_read.seek(0)
    conn.proc.logfile_read.writelines(lines)
    conn.proc.logfile_read.truncate()
    conn.proc.close()

    return lines
