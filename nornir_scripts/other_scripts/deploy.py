
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result, print_title
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command, netmiko_save_config
from nornir.core.filter import F


# Specify the config file
nr = InitNornir()

def ospf_internal(task):
    # Extracting the Router's "ID" from it's IP address
    pos = str(f"{task.host.hostname}").rfind('.')
    id = str(f"{task.host.hostname}")[pos + 1:]
    loopback_ip = "1.1.1." + str(id)

    # Router's Loopback Configuration
    loopback_commands = ["interface loopback0", "ip address " + loopback_ip + " 255.255.255.255", "ip ospf 1 area 0"]
    deploy_loopback = task.run(netmiko_send_config, config_commands=loopback_commands)

    # Configuration of the OSPF
    ospf_commands = ["router ospf 1", "router-id " + loopback_ip]
    deploy_ospf = task.run(netmiko_send_config, config_commands=ospf_commands)
    
    # General config
    deploy_general = task.run(netmiko_send_config, config_file="general_config")    

    # Save configuration to the NVRAM
    save_config = task.run(netmiko_save_config)



site_prototype = nr.filter (F(groups__contains="site_prototype"))
results = site_prototype.run(task=ospf_internal)

print_title("DEPLOYING CONFIGURATIONS")
print_result(results)

