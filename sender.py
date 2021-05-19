import requests 
  
# api-endpoint 
URL = "http://localhost:10025"

def post_url(p):
    try:
        r = requests.post(URL, p, timeout=1.5)
        print(r.text)
    except requests.Timeout:
        pass
    except requests.ConnectionError:
        pass
