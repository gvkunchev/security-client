import requests


class Api:
    """Server API."""

    ADDRESS = '192.168.100.50'
    PORT = '8000'

    def _send_request(self, endpoint):
        """Send request to server."""
        response = requests.get(f"http://{self.ADDRESS}:{self.PORT}/{endpoint}")
        if response.status_code != 200:
            raise Exception('Unable to connect to the server.')
        return response.json()

    def get_sensors_data(self):
        """Get sensors data."""
        return self._send_request("get_sensor_status")
    
    def get_arm_data(self):
        """Get arm data."""
        return self._send_request("get_arm_status")
    
    def arm(self):
        """Set arm state."""
        return self._send_request("arm")
    
    def unarm(self):
        """Set unarm state."""
        return self._send_request("unarm")
