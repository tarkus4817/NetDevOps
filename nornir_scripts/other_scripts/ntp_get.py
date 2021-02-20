from nornir_scrapli.tasks import netconf_get
from nornir_utils.plugins.functions import print_result
from nornir import InitNornir
from xml.dom import minidom
import logging

nr = InitNornir(config_file="nornir_data/config2.yaml")

def yang_sucks(task):
   result = task.run(task=netconf_get, filter_= "/ntp-oper-data", filter_type="xpath")


result = nr.run(task=yang_sucks)
print_result(result)
