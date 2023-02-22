"""Security client API."""

import requests


class SecurityServerError(Exception):
    pass


class Api:
    """Server API."""

    ADDRESS = '192.168.100.50'
    PORT = '8000'

    def _send_request(self, endpoint, vars=None):
        """Send request to server."""
        link = f"http://{self.ADDRESS}:{self.PORT}/{endpoint}"
        if vars is not None:
            for i, (key, val) in enumerate(vars.items()):
                if i == 0:
                    link += '?'
                else:
                    link += '&'
                link += (f'{key}={val}')
        try:
            response = requests.get(link)
        except:
            raise SecurityServerError('Unable to connect to the server.')
        if response.status_code != 200:
            raise SecurityServerError(f'Server responds with {response.status_code}.')
        return response.json()

    def get_sensors_data(self):
        """Get sensors data."""
        try:
            return self._send_request("get_sensor_status")
        except SecurityServerError:
            # Server is down
            return [
                {"location": "Bed room", "state": "Unknown"},
                {"location": "Kid room", "state": "Unknown"},
                {"location": "Front door", "state": "Unknown"}
            ]

    def get_arm_data(self):
        """Get arm data."""
        try:
            return self._send_request("get_arm_status")
        except SecurityServerError:
            # Server is down
            return {"location": "Home", "state": "Unknown"}

    def arm(self):
        """Set arm state."""
        return self._send_request("arm")

    def unarm(self):
        """Set unarm state."""
        return self._send_request("unarm")

    def verify(self, pattern):
        """Verify pattern."""
        return self._send_request("verify", vars={'pattern': pattern})
