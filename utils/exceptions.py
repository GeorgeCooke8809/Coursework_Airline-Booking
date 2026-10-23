class InvalidAirportException(Exception):
    """Exception raised when an invalid airport ICAO is entered."""

    def __init__(self, icao):
        self.message = "An invalid airport ICAO was entered."
        self.icao = icao
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} - {self.icao}"