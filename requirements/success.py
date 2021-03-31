class APIResponse:
    def __init__(self, status, msg, data):
        self.status = status
        self.msg = msg
        self.data = data

    def respond(self):
        return({
            "status": self.status,
            "msg": self.msg,
            "data": self.data
        })
