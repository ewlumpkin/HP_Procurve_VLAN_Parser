SOURCE_CONFIG = "Port_Script/hp_port_config.txt"

port_dict = {}


def add_to_dict(module, port, vlan_name, tag):
    # Translate module to switch
    # Feel free to create your own modifications to the dest switches
    # Ex:
    # if "A" in module:
    #   module = "gi 1/0/"
    if "Trk" in module:
        module = "Po"
    port = module + port

    if port not in port_dict:
        port_dict[port] = dict()

    if tag == "tagged":
        if "tagged" in port_dict[port]:
            port_dict[port]["tagged"].append(vlan_name)
        else:
            port_dict[port]["tagged"] = [vlan_name]
    elif tag == "untagged":
        if "untagged" in port_dict[port]:
            port_dict[port]["untagged"].append(vlan_name)
        else:
            port_dict[port]["untagged"] = [vlan_name]


def parse_ports(vlan_name, ports, tag):
    for port in ports:
        # If there is a range of ports, iterate over individual ports
        if "-" in port:
            # Initialize buffer to store port
            port_buf = ""
            # Initialize buffer to store begging port
            beg_port = ""
            # Initialize buffer to store end port
            end_port = ""
            for elem in port:
                if elem.isnumeric():
                    port_buf += elem
                elif elem == "-":
                    # Assign begginging port
                    beg_port = int(port_buf)
                    port_buf = ""
            # Assign end port
            end_port = int(port_buf)
            # Iterate over range of ports
            for port_num in range((end_port - beg_port) + 1):
                if "Trk" in port:
                    add_to_dict(port[0:3], str(end_port - port_num), vlan_name, tag)
                else:
                    add_to_dict(port[0], str(end_port - port_num), vlan_name, tag)

        else:
            if "Trk" in port:
                add_to_dict(port[0:3], port[3:], vlan_name, tag)
            else:
                add_to_dict(port[0], port[1:], vlan_name, tag)


def parse_config():
    with open(SOURCE_CONFIG, "r") as fd:
        for line in fd.readlines():
            line = line.rstrip()
            line = line.split()
            ports = []
            tag = ""
            # We are on VLAN line
            if line[0] == "vlan":
                vlan_name = line[1]
            # We are on port assignment line
            elif line[0] == "untagged":
                tag = "untagged"
                ports = line[1].split(",")
            else:
                # tagged
                if line[0] == "tagged":
                    ports = line[1].split(",")
                # no untagged
                elif line[0] == "no":
                    ports = line[2].split(",")
                tag = "tagged"

            parse_ports(vlan_name, ports, tag)


def print_dict():
    for k, v in port_dict.items():
        print("interface", k)
        # Has tagged and untagged, must be trunk
        if "tagged" in v and "untagged" in v:
            print("switchport mode trunk")
            print("switchport trunk allowed vlan add ", end="")
            print(",".join(v["tagged"]))
            print("switchport trunk native vlan ", end="")
            print(f"{','.join(v['untagged'])}")
        # Has only untagged must be access
        elif "untagged" in v:
            print("switchport mode access")
            print("switchport access vlan ", end="")
            print(",".join(v["untagged"]))
        elif "tagged" in v:
            print("switchport mode trunk")
            print("switchport trunk allowed vlan add ", end="")
            print(",".join(v["tagged"]))
        print()


parse_config()
print_dict()
