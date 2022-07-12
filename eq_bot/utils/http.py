import requests

class HttpClient:
    def get(self, url, headers):
        # TODO: Add error handling
        return requests.get(url, headers=headers)
