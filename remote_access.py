from typing import List, Optional, Union
from wgutils import WGConfig, WGPeer, Topology
import base64
import ipaddress


def build_allowed(topology: Topology, address: Union[ipaddress.IPv6Address, ipaddress.IPv4Address],
                  network: Union[ipaddress.IPv6Network, ipaddress.IPv4Network],
                  extra: Optional[List[str]] = None, isolate_clients: bool = False, server: bool = False
                  ) -> List[str]:

    if extra is None:
        extra = []

    extra.append("{}/{}".format(address.compressed if server or isolate_clients else network.network_address,
                                32 if server or isolate_clients else network.prefixlen))
    return extra


def buildconfig(topology: Topology, server: WGConfig, peers: List[WGConfig], isolate: bool = False, keepalive: Optional[int] = None,
                endpoint: Optional[Union[ipaddress.IPv6Address, ipaddress.IPv4Network]] = ipaddress.ip_address("0.0.0.0")):

    server.peers = [
        WGPeer(str(base64.b64encode(bytes(p.privkey.public_key)).decode()),
               allowed=build_allowed(topology, p.address, p.address, server=True), keepalive=keepalive) for p in peers
    ]

    for p in peers:
        p.peers = [
            WGPeer(str(base64.b64encode(bytes(server.privkey.public_key)).decode()),
                   allowed=build_allowed(topology, server.address.ip, server.address.network, server=False, isolate_clients=isolate), endpoint=endpoint)
        ]
