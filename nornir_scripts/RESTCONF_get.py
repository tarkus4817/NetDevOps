import requests
import json
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from supporting_scripts import get_credentials
import yaml

credentials = get_credentials.get_credentials()
nr = InitNornir(config_file="/home/kamil/Hons/nornir_data/config.yaml")
nr.inventory.defaults.username = credentials["username"]
nr.inventory.defaults.password = credentials["password"]
requests.packages.urllib3.disable_warnings()

headers = {
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json'
}

def testconf(task):
    url = f"https://{task.host.hostname}/restconf/data/native/"
    response = requests.get(url, headers=headers, auth=(task.host.username, task.host.password), verify=False).json()
    with open(f"/home/kamil/Hons/host_vars/RESTCONF_native/{task.host}.json", "w") as jsn:
        json.dump(response, jsn, indent=4, sort_keys=False)
    with open(f"/home/kamil/Hons/host_vars/RESTCONF_native/{task.host}.yaml", "w") as yml:
        yaml.safe_dump(response, yml, sort_keys=False)

    if response:
        print(f"Successfully retrieved config from {task.host}")

    return response

#spine = nr.filter(F(groups__contains="spine"))
#result = spine.run(task=testconf)

result = nr.run(task=testconf)
