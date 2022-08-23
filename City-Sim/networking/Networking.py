import requests
import time

def Set_Globals():
    global client    
    client = requests.session()

def Set_Tractor_Actions(tractor_actions):
    global client 
    get_url = 'http://192.168.1.11:80/index/'
    post_url = 'http://192.168.1.11:80/set_tractor_actions/'
    
    #GET
    # Retrieve the CSRF token first
    client.get(get_url)  # sets cookie
    #print(client.cookies)
    if 'csrftoken' in client.cookies:
        # Django 1.6 and up
        csrftoken = client.cookies['csrftoken']
    else:
        # older versions
        csrftoken = client.cookies['csrf']
    
    #POST
    #Prepare data to send
    data = {}
    print(tractor_actions)
    data['tractor_actions'] = []
    for k, v in tractor_actions.items():
        data[k] = v
        
    data['csrfmiddlewaretoken'] = csrftoken
    r = client.post(post_url, data=data, headers=dict(Referer=post_url))
    print(r)

def Wait_For_User_Input(response, timeout, timewait):
    timer = 0
    while response.status_code == 204:
        time.sleep(timewait)
        timer += timewait
        if timer > timeout:
            break
        if response.status_code == 200:
            break
"""
def Get_Tractor_Actions():
    while True:
        Wait_For_User_Input(response, 15, 1)
"""