# TODO(rox): entire bundle stream should be made in here I think ...
def add_attachments(conn, path, mime_type, content):
    """
    Add attachments to the bundle stream
    """
    attachments = []
    attachment = {}

    attachment['pathname'] = path
    attachment['mime_type'] = mime_type
    attachment['content'] = content
    attachments.append(attachment)

    return attachments
