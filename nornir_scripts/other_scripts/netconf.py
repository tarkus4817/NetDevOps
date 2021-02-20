from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.filter import F

nr = InitNornir(config_file="nornir_data/config2.yaml")

def load_vars(task):
    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["facts"] = data.result
    config_ospf(task)


def config_ospf(task):
    ospf_template = task.run(
        task=template_file,
        name="Building OSPF Configuration",
        template="ospf.j2",
        path="./templates",
    )
    ospf_output = ospf_template.result
    task.run(task=netconf_edit_config, target="running", config=ospf_output)

spine = nr.filter (F(groups__contains="spine"))
result = spine.run(task=load_vars)
print_result(result)
