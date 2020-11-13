import ipaddress
from typing import Optional, Union, List

from nacl.public import PrivateKey
import nacl.secret
import nacl.utils
from enum import Enum, auto


class ConfigurationType(Enum):
    WGQUICK = auto()
    NETWORK_MANAGER = auto()
    NETWORKD = auto()
    NETCLT = auto()


class Topology(Enum):
    POINT_TO_POINT = auto()
    REMOTE_ACCESS = auto()
    SITE_TO_SITE = auto()
    SITE_TO_MULTI_SITE = auto()


class WGPeer:
    pubkey: str
    preshared: Optional[str] = None
    allowed: List[str]
    endpoint: Optional[Union[ipaddress.IPv6Address,
                             ipaddress.IPv4Network]] = None
    keepalive: Optional[int] = None

    def __init__(self, pubkey: str, allowed: List[str], endpoint: Optional[Union[ipaddress.IPv6Address, ipaddress.IPv4Network]] = None,
                 preshared: Optional[str] = None, keepalive: Optional[int] = None):
        self.preshared = preshared
        self.endpoint = endpoint
        self.allowed = allowed
        self.keepalive = keepalive
        self.pubkey = pubkey


class WGConfig:
    privkey: PrivateKey
    address: Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface]
    peers: List[WGPeer] = []
    listen_port: Optional[int] = None

    def __init__(self, address: Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface],
                 privkey: PrivateKey = PrivateKey.generate(), listen_port: Optional[int] = listen_port):
        self.privkey = privkey
        self.address = address
        self.listen_port = listen_port


def build_interface(address: Union[ipaddress.IPv4Address, ipaddress.IPv6Address],
                    network: Union[ipaddress.IPv4Network, ipaddress.IPv6Network]):
    return ipaddress.ip_interface("{}/{}".format(address, network.prefixlen))
