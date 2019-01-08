import requests
def web_open(url,name):
    r = requests.get(url)
    with open(name, 'wb') as f:
        f.write(r.content)
    f = open(name, 'rb')
    return f