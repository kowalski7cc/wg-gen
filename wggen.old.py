#!/bin/env python
import os
import base64
from nacl.public import PrivateKey
from enum import Enum, auto
import argparse

WIREGUARD_OUTPUT_FOLDER = "output"


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--networkd ', dest='accumulate', action='store_const',
                        const=sum, default=False,
                        help='Build networkd configuration')



def interactive():
    quantity = input("Quanti certificati client?: ")

    if not quantity.isnumeric():
        print("Invalid input")
        quit(1)

    private_keys = [PrivateKey.generate() for _ in range(int(quantity) + 1)]
    key_pairs = {}

    for private_key in private_keys:
        key_pairs[base64.b64encode(bytes(private_key)).decode()] = base64.b64encode(
            bytes(private_key.public_key)).decode()

    ask_subnet = input("Inserisci la subnet di rete nel formato 'x.x.x.0/xx': ")
    subnet_split = (ask_subnet if ask_subnet != "" else "192.168.10.0/24").split("/")

    ask_server = input("Inserisci l'host ID del server [1]: ")

    WIREGUARD_SUBNET = subnet_split[0][:-2]
    WIREGUARD_SERVER = ask_server if ask_server != "" else "1"

    default_start_ip = "2" if WIREGUARD_SERVER == "1" else "1"

    ask_start = input("Inserisci l'IP da cui iniziare la generazione [" + default_start_ip + "]: ")

    ask_public = input("Inserisci l'IP pubblico del server [0.0.0.0:51820]: ").split(":")

    ask_public = ("0.0.0.0", "51820") if ask_public == [""] else ask_public

    WIREGUARD_CIDR = "/" + subnet_split[1]
    WIREGUARD_PORT = ask_public[1]
    WIREGUARD_ENDPOINT = ask_public[0]
    WIREGUARD_CLIENTIP_START = int(ask_start if ask_start != "" else default_start_ip)

    server_keys = key_pairs.popitem()

    ask_has_server = input("Hai già una configurazione server? ([n]/y): ")

    if ask_has_server.lower() == "y":
        ask_server = input("Inserisci la chiave privata: ")
        if ask_server != "":
            server_keys = (ask_server, base64.b64encode(bytes(PrivateKey(base64.b64decode(ask_server)).public_key)))

    try:
        os.makedirs(WIREGUARD_OUTPUT_FOLDER)
    except:
        pass

    with open(WIREGUARD_OUTPUT_FOLDER + "/config.md", "w") as config_file:
        config_file.write("# Configurazione Wireguard\n\n")
        config_file.write("## Configurazone di rete\n\n")
        config_file.write("- IP Wireguard enpoint: " + WIREGUARD_ENDPOINT + "\n")
        config_file.write("- Porta Wireguard enpoint: " + WIREGUARD_PORT + "\n")
        config_file.write("- Subnet Wireguard network: " +
                          WIREGUARD_SUBNET + ".0" + WIREGUARD_CIDR + "\n")
        config_file.write("- IP Wireguard network server: " +
                          WIREGUARD_SUBNET + "." + WIREGUARD_SERVER + "\n\n")
        config_file.write("## Chiavi Wireguard\n\n")
        config_file.write("| IP | Note | Privkey | Pubkey |\n")
        config_file.write("|----|------|---------|--------|\n")
        ip = WIREGUARD_CLIENTIP_START

        config_file.write("|" + str(WIREGUARD_SERVER) + "|" + "Server"
                          + "|" + server_keys[0] + "|" + server_keys[1] + "|\n")

        for private_key in key_pairs:
            config_file.write("|" + str(ip) + "|" + "Client"
                              + "|" + private_key + "|" + key_pairs[private_key] + "|\n")
            ip += 1

    ip = WIREGUARD_CLIENTIP_START

    with open(WIREGUARD_OUTPUT_FOLDER + "/server.conf", "w") as conf:
        conf.write("[Interface]\n")
        conf.write("PrivateKey = " + server_keys[0] + "\n")
        conf.write("ListenPort = " + WIREGUARD_PORT + "\n")
        conf.write("Address = " + WIREGUARD_SUBNET +
                   "." + WIREGUARD_SERVER + WIREGUARD_CIDR + "\n\n")
        for private_key in key_pairs:
            conf.write("[Peer]\n")
            conf.write("PublicKey = " + key_pairs[private_key] + "\n")
            conf.write("AllowedIPs = " + WIREGUARD_SUBNET +
                       "." + str(ip) + WIREGUARD_CIDR + "\n")
            conf.write("PersistentKeepalive = 25\n\n")
            ip += 1

    ip = WIREGUARD_CLIENTIP_START

    for private_key in key_pairs:
        with open(WIREGUARD_OUTPUT_FOLDER + "/client" + str(ip) + ".conf", "w") as conf:
            conf.write("[Interface]\n")
            conf.write("PrivateKey = " + private_key + "\n")
            conf.write("Address = " + WIREGUARD_SUBNET +
                       "." + str(ip) + WIREGUARD_CIDR + "\n\n")
            conf.write("[Peer]\n")
            conf.write("PublicKey = " + server_keys[1] + "\n")
            conf.write("AllowedIPs = " + WIREGUARD_SUBNET +
                       ".0" + WIREGUARD_CIDR + "\n")
            conf.write("PersistentKeepalive = 25\n")
            conf.write("Endpoint = " + WIREGUARD_ENDPOINT +
                       ":" + WIREGUARD_PORT + "\n")
        ip += 1


if __name__ == '__main__':
    main()
