# A collection of useful functions for various purposes related to network automation

# Function to convert wildcard number to netmask
def wildcard_to_netmask(ip_wildcard_dict):
    ip_netmask_dict = {}
    for ip in ip_wildcard_dict:
        netmask = []
        split_netmask = ip_wildcard_dict[ip].split(".")
        for octet in split_netmask:
            wildcard_octet = 255 - int(octet)
            netmask.append(str(wildcard_octet))
        netmask = ".".join(netmask)
        ip_netmask_dict[ip] = netmask

    return ip_netmask_dict


# code to convert netmask ip to cidr number
def netmask_to_cidr(netmask):
    '''
    :param netmask: netmask ip addr (eg: 255.255.255.0)
    :return: equivalent cidr number to given netmask ip (eg: 24)
    '''
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])
