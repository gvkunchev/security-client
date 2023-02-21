import requests


class Api:
    """Server API."""

    ADDRESS = '192.168.100.50'
    PORT = '8000'

    def __init__(self):
        """Initializator."""
        pass

    def get_sensors_data(self):
        endpoint = "get_sensor_status"
        response = requests.get(f"http://{self.ADDRESS}:{self.PORT}/{endpoint}")
        if response.status_code != 200:
            raise Exception('Unable to connect to the server.')
        return response.json()
