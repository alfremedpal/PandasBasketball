
class StatusCode404(Exception):
    def __init__(self):
        message = """
                    The page could not be found; url build failed.
                    You could have mistyped the player code or the team.
                    """
        super().__init__(message)

class TableNonExistent(Exception):
    def __init__(self):
        message = """
                    The table could not be found.
                    You could have mistyped the table name.
                    If it was a playoffs table the player might not have partipated in playoffs yet.
                    If it was for the last 'n' days, it is possible there is no info for that day range.
                    """
        super().__init__(message)