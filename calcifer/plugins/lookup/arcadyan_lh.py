import base64
import re
import requests

_token_page = 'http://{}/login.htm'
_info_page = 'http://{}/cgi/cgi_login.js?_tn={}'

def extract_cgi_token(gateway_addr):
    response = requests.get(_token_page.format(gateway_addr))
    response.raise_for_status()

    # Ok, now we have to grab the token payload from the login page
    token = base64.b64decode( # The token is stored hidden in the base 64
        re.search('data:image/gif;base64,[^"]+', # of an inline image in the page
                  response.text).group(0)[78:]) # right at the very end!
    return token.decode()

def fetch_wan_ipv4(gateway_addr, token):
    magic_header = {'Referer': _token_page.format(gateway_addr)}

    response = requests.get(_info_page.format(gateway_addr, token),
                            headers = magic_header)
    response.raise_for_status()

    wan_ipv4 = re.search('curr_wan_ip4_addr="([^"]+)"',
                         response.text).group(1)
    return wan_ipv4

def get_wan_ip(settings={}):
    gateway_addr = settings['gateway']
    # Do the silly side-quest before we can get our data
    token = extract_cgi_token(gateway_addr)
    return fetch_wan_ipv4(gateway_addr, token)
