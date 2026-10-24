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

class InvalidTimeException(Exception):
    """Exception raised when a time given is invalid"""

    def __init__(self):
        self.message = "An invalid time was given."
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

class ExistenceException(Exception):
    """Exception raised when the record a foreign key is referencing does not exist"""

    def __init__(self):
        self.message = "An invalid foreign key was given. The record likely does not exist"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"