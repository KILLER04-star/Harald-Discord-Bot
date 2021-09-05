import base64


def encode(text):  # base64 encode
    bytes = base64.b64encode(str(text).encode("utf-8"))
    return str(bytes, "utf-8")


def decode(text):  # base64 decode
    bytes = base64.b64decode(str(text).encode("utf-8"))
    return str(bytes, "utf-8")


def isAdmin(user):  # Checks if the user has the admin-role of the server
    return str(user.guild_permissions) == "<Permissions value=2147483647>"
