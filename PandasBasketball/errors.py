
class StatusCode404(Exception):
    def __init__(self):
        message = """The page could not be found; url build failed.\n
                    You could have mistyped the player url code"""
        super().__init__(message)

class TableNonExistent(Exception):
    def __init__(self):
        message = """The stat table could not be found.\n
                    You could have mistyped the table name.\n
                    If it was a playoffs table the player might not have partipated in playoffs yet."""
        super().__init__(message)