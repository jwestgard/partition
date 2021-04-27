class ConfigError(Exception):
    """ Custom exception class raised by invalid args """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
