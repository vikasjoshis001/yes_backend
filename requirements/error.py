class APIResponse:
    def __init__(self, status, msg, error):
        self.status = status
        self.msg = msg
        self.error = error

    def respond(self):
        return({
            "status": self.status,
            "msg": self.msg,
            "error": self.error
        })
