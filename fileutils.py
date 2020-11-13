import base64
import os
import jinja2

from nacl.public import PrivateKey
from typing import List
from wgutils import WGConfig, WGPeer, ConfigurationType
from jinja2 import Template

WIREGUARD_TEMPLATE = "wgquic.conf.jinja2"



def write_config(folder: str, name: str, config_type: List[ConfigurationType], config: WGConfig):
    for t in config_type:
        {
            ConfigurationType.WGQUICK: write_wgquick_config,
            ConfigurationType.NETWORK_MANAGER: write_networkmanager_config,
            ConfigurationType.NETWORKD: write_networkd_config,
            ConfigurationType.NETCLT: write_netclt_config
        }.get(t)("{}/{}.conf".format(folder, name), config)


def write_wgquick_config(output: str, config: WGConfig) -> None:
    with open("templates/{}".format(WIREGUARD_TEMPLATE)) as file_:
        template: Template = Template(file_.read())
        render = template.render(privkey=str(base64.b64encode(bytes(
            config.privkey)).decode()), listen_port=config.listen_port, address=config.address, peers=config.peers)
        os.makedirs(os.path.relpath(os.path.join(output, os.pardir)), exist_ok=True)
        with open(output, "w") as out:
            out.write(render)


def write_networkmanager_config(filename: str, config: WGConfig) -> None:
    pass


def write_networkd_config(filename: str, config: WGConfig) -> None:
    pass


def write_netclt_config(filename: str, config: WGConfig) -> None:
    pass


def write_index(filename: str, config_list: List[WGConfig]) -> None:
    pass


if __name__ == '__main__':
    print("You can't run this file")
