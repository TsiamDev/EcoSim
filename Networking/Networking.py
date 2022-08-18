import requests

url = 'http://192.168.1.11:80/index/'
#data = {'data': 'hello'}

#x = requests.post(url, data = data)

#print(x.text)

client = requests.session()

# Retrieve the CSRF token first
client.get(url)  # sets cookie
#print(client.cookies)

if 'csrftoken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrftoken']
else:
    # older versions
    csrftoken = client.cookies['csrf']
data = {}
data['data'] = 'hello'
data['csrfmiddlewaretoken'] = csrftoken
r = client.post(url, data=data, headers=dict(Referer=url))
print(r)