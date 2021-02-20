import requests
import json
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from rich import print
from nornir.core.filter import F

nr = InitNornir()


def test(task):
    dev_name = task.host
    my_list = []
    result = task.run(netmiko_send_command, command_string="show ip ospf neigh", use_genie=True)
    task.host["facts"] = result.result
    interfaces = task.host["facts"]["interfaces"]
    for interface in interfaces:
        neighbor = interfaces[interface]["neighbors"]
        for adjacency in neighbor:
            my_list.append(adjacency)
    num_neighbors = len(my_list)
    if num_neighbors == 2:
        print(f"{dev_name}: [green]PASSED[/green]")
    else:
        print(f"{dev_name}: [red]FAILED[/red]")
        fail_report(dev_name)


def fail_report(dev_name):
    header = {"Authorization": "Bearer Zjc0YmQxODItNmYxNy00Y2FkLTk1NTEtMzY0MjQ2MmNjZjVjZjk5Y2QyYWItM2U2_PF84_consumer",
              "Content-Type": "application/json"}

    data = {"roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vNTlmNGExYjAtMTA0ZS0xMWViLWJhMDYtN2I0ZTU2ODFiMzhi",
            "text": f'{dev_name} FAIL: OSPF NEIGHBOR DIED'}

    return requests.post("https://api.ciscospark.com/v1/messages/", headers=header, data=json.dumps(data), verify=True)

leaf = nr.filter (F(groups__contains="leaf"))
results = leaf.run(task=test)
