import requests

#create GET request
res = requests.get("http://127.0.0.1:3032/api/motors/0")
print(res.json()) #show JSON file

#create GET request to delete some info
res = requests.delete("http://127.0.0.1:3032/api/motors/2")
print(res.json())

#create GET request to add some info
res = requests.post("http://127.0.0.1:3032/api/motors/3", json={"name": "Kawasaki", "model": "Vulcan1600"})
if res.ok:
    print(res.json())

#create GET request to change some info
res = requests.put("http://127.0.0.1:3032/api/motors/1", json={"name": "Suzuki", "model": "Intruder1800"})
if res.ok:
    print(res.json())
