from nornir_scrapli.tasks import netconf_get
from nornir_utils.plugins.functions import print_result
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.tasks.files import write_file
import xmltodict
import simplejson as json
import yaml


nr = InitNornir(config_file="nornir_data/config.yaml")


def get_all_values_dict(nested_dictionary):
    for key, value in list(nested_dictionary.items()):

        if isinstance(value, dict):

            get_all_values_dict(value)
        elif isinstance(value, list):
            for another_dict in value:
                get_all_values_dict(another_dict)
        else:
            if key == "@xmlns":
                nested_dictionary["_xmlns"] = nested_dictionary[key]
                del nested_dictionary[key]

    return nested_dictionary


def get_native(task):

    looking_for_path = "/native"
    result = task.run(task=netconf_get, filter_= looking_for_path, filter_type="xpath")
    task.run(task=write_file, content=result.result,
             filename=f"/home/kamil/Hons/host_vars/native/{task.host}.xml")

    with open(f"/home/kamil/Hons/host_vars/native/{task.host}.xml") as fd:
        doc = xmltodict.parse(fd.read())
    doc2 = doc["rpc-reply"]["data"]
    for i in list(doc2["native"]):
        doc2["native"].update({"_operation":"replace"})
        doc2["native"].move_to_end("_operation", last=False)

    doc3 = get_all_values_dict(doc2)

    with open(f"/home/kamil/Hons/host_vars/native/{task.host}.json", "w") as f:
        f.write(json.dumps(doc3, indent=4, sort_keys=False))

    with open(f"/home/kamil/Hons/host_vars/native/{task.host}.json", "r") as ld:
        data = json.load(ld)

    with open(f"/home/kamil/Hons/host_vars/native/{task.host}.yaml", "w") as yf:
        yaml.safe_dump(data, yf, allow_unicode=True, sort_keys=False)

    return result


spine = nr.filter(F(groups__contains="spine"))

result = spine.run(task=get_native)

print_result(result)

