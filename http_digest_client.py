import md5
import requests

from requests.auth import HTTPBasicAuth


class DigestClient(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def prep_for_call(self):
        response = requests.get(self.url + '/nonce')
        self.nonce = response.text

    def make_call(self):
        self.prep_for_call()
        password_hash = md5.new(self.nonce + self.password)
        self.password = password_hash.hexdigest()
        response = requests.get(self.url + '/hello',
                                auth=HTTPBasicAuth(
                                    self.username, self.password
                                ))

        print response.text

digest_client = DigestClient(
    'http://localhost:4000',
    'phil',
    'Ill send an SOS to the world'
)

digest_client.make_call()

