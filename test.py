from typing import Union
from wgutils import ConfigurationType, WGConfig, Topology, build_interface
import ipaddress
from itertools import islice
from remote_access import buildconfig
from fileutils import write_config

if __name__ == '__main__':
    network: Union[ipaddress.IPv6Network, ipaddress.IPv4Network] = ipaddress.ip_network(
        "192.168.1.0/24", True)

    print(network.network_address)

    addr = build_interface(network[4], network)

    server = WGConfig(address=addr, listen_port=51820)
    configs = [WGConfig(build_interface(a, network)) for a in list(islice(network.hosts(),10, 20))]

    buildconfig(Topology.REMOTE_ACCESS, server, configs, True, keepalive=25)
    write_config("test", "server", [ConfigurationType.WGQUICK], server)

    for p in configs:
        write_config("test", "client-{}".format(p.address.),
                     [ConfigurationType.WGQUICK], p)
