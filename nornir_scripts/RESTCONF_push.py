import requests
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from supporting_scripts import get_credentials
import yaml
import json


def native_conf(task, headers):

    url = f"https://{task.host.hostname}/restconf/data/native/"
    with open(f"/home/kamil/Hons/host_vars/RESTCONF_native/{task.host}.yaml") as yml:
        data = yaml.safe_load(yml)
    request = requests.put(
        url, headers=headers, data=json.dumps(data), auth=(task.host.username, task.host.password), verify=False)

    return request


def main():

    requests.packages.urllib3.disable_warnings()
    headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json, application/yang-data.errors+json",
    }
    
    credentials = get_credentials.get_credentials()
    nr = InitNornir(config_file="/home/kamil/Hons/nornir_data/config.yaml")
    nr.inventory.defaults.username = credentials["username"]
    nr.inventory.defaults.password = credentials["password"]

    #spine = nr.filter(F(groups__contains="spine"))
    #native_result = spine.run(task=native_conf, name="PUSHING NATIVE VIA RESTCONF", headers=headers,)
    native_result = nr.run(task=native_conf, name="PUSHING NATIVE VIA RESTCONF", headers=headers)

    print_result(native_result)


if __name__ == "__main__":
    main()
