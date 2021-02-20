from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config, netconf_unlock, netconf_lock, netconf_discard, netconf_commit
from supporting_scripts import get_credentials
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

        result = task.run(task=netconf_edit_config, target="candidate", config=xml_str)
        return Result(host=task.host, result=result.result)

def config_lock(task):
    task.run(task=netconf_lock, target="candidate", name="Locking Candidate Configuration")


def config_discard(task):
    task.run(task=netconf_discard, name="Discarding Candidate Configuration")


def config_commit(task):
    task.run(task=netconf_commit, name="Committing Candidate Configuration")


def config_unlock(task):
    task.run(task=netconf_unlock, target="candidate", name="Unlocking Candidate Configuration")

def main():
    credentials = get_credentials.get_credentials()
    nr = InitNornir(config_file="/home/kamil/Hons/nornir_data/config.yaml")
    nr.inventory.defaults.username = credentials["username"]
    nr.inventory.defaults.password = credentials["password"]
    #spine = nr.filter(F(groups__contains="spine"))

    lock = nr.run(task=config_lock)
    print_result(lock)

    for feature in Features_to_push:
        results = nr.run(task=edit_nc_config_from_yaml, feature=feature)
        print_result(results)

    failed_changes = nr.data.failed_hosts
    if failed_changes:
        revert = nr.run(task=config_discard)
        print_result(revert)
    else:
        commit_config = nr.run(task=config_commit)
        print_result(commit_config)

    unlock = nr.run(task=config_unlock)
    print_result(unlock)


if __name__ == "__main__":
    main()
