class InvalidAirportException(Exception):
    """Exception raised when an invalid airport ICAO is entered."""

    def __init__(self, icao):
        self.message = "An invalid airport ICAO was entered."
        self.icao = icao
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} - {self.icao}"

class RepeatException(Exception):
    """Exception raised when the repeat type of a service/schedule is incorrect"""

    def __init__(self):
        self.message = "An invalid repeat type was given."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"

class InvalidDateException(Exception):
    """Exception raised when a date given is invalid"""

    def __init__(self):
        self.message = "An invalid date was given."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"