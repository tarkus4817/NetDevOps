from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.filter import F


nr = InitNornir(config_file="nornir_data/config.yaml")

def config_routing(task):
   routing_template = task.run(
       task=template_file,
       name="Buildling Routing Configuration",
       template="eigrp.j2",
       path="./templates",
   )
   routing_output = routing_template.result
   task.run(task=netconf_edit_config, target="running", config=routing_output)


spine = nr.filter (F(groups__contains="spine"))
result = spine.run(task=config_routing)
print_result(result)
