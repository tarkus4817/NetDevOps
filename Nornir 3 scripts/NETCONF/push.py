"""
This module is a modification of a module developed by Dmitry Figol
https://github.com/dmfigol
"""

from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result
from lxml import etree
from ruamel.yaml import YAML
from dmitry_nojinja import nojinja
from nornir.core.filter import F


Features_to_push = ["ntp", "router", "interface", "crypto", "enable", "ip", "line"]

def edit_nc_config_from_yaml(task, feature):
    with open(f"host_vars/{feature}/{task.host}.yaml") as f:
        yaml = YAML(typ="safe")
        data = yaml.load(f)
        xml = nojinja.dict_to_xml(data, root="config")
        xml_str = etree.tostring(xml).decode("utf-8")
        result = task.run(task=netconf_edit_config, config=xml_str)
        return Result(host=task.host, result=result.result)


def main():
    nr = InitNornir(config_file="nornir_data/config.yaml")
    spine = nr.filter(F(groups__contains="spine"))

    for feature in Features_to_push:
        results = spine.run(task=edit_nc_config_from_yaml, feature=feature)
        print_result(results)


if __name__ == "__main__":
    main()
