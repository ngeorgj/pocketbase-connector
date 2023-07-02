import json  
import requests  
  
class PocketBaseConnector:  

    url = ""  
  
    def __init__(self, url, **kwargs):  
        self.url = url  
        if kwargs:  
            for k, v in kwargs.items():  
                setattr(self, k, v)  
  
    def resource(self, name):  
        return self.Resource(self, name)  
  
    def get(self, resource, params={'perPage': 100}):  
        return \  
            requests.get(self.url + f"/api/collections/{resource}/records",  
                         headers={'Content-Type': "application/json"},  
                         params=params).json()['items']  
  
    def post(self, resource, params={}, **data: dict):  
        r = requests.post(self.url + f"/api/collections/{resource}/records", data=json.dumps(data),  
                          headers={'Content-Type': "application/json"},  
                          params=params)  
        print(f'POST {self.url}/api/collections/{resource}/records {r.status_code}\n{r.json()}')  
        return r  
  
    def delete(self, resource, resource_id):  
        r = requests.delete(self.url + f"/api/collections/{resource}/records/{resource_id}")  
        print(f'DELETE {self.url}/api/collections/{resource}/records/{resource_id} {r.status_code}')  
        return r  
  
    def update(self, resource, resource_id, **data):  
        r = requests.patch(self.url + f"/api/collections/{resource}/records/{resource_id}", data=json.dumps(data),  
                           headers={'Content-Type': "application/json"})  
        print(f'PATCH {self.url}/api/collections/{resource}/records/{resource_id} {r.status_code}')  
        return r  
  
    class Resource:  
  
        def __init__(self, base, name):  
            self.base: PocketBaseConnector = base  
            self.name = name  
  
        def create(self, **kwargs):  
            return self.base.post(self.name, **kwargs)  
  
        def get(self, **kwargs):  
            return self.base.get(self.name, params={**kwargs})  
  
        def delete(self, resource_id):  
            return self.base.delete(self.name, resource_id)  
  
        def update(self, resource_id, **kwargs):  
            self.base.update(self.name, resource_id, **kwargs)  
  
  
# Singleton  
pbc = PocketBaseConnector('http://cyberdeck:8090')

pbc.resource('users').create(name='test user')
pbc.resource('users').get() # all

