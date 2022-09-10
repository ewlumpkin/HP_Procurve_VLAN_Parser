port_dict = {}


def add_to_dict(line_card, port, vlan_name):
    # Translate line card to switch
    if "A" in line_card:
        line_card = "gi 1/0/"
    elif "B" in line_card:
        line_card = "gi 2/0/"
    elif "F" in line_card:
        line_card = "gi 3/0/"
    elif "Trk" in line_card:
        line_card = "Po"
    port = line_card + port
    if port in port_dict:
        port_dict[port]["tagged"].append(vlan_name)
    else:
        port_dict[port] = dict(tagged=[vlan_name])


def parse_ports(vlan_name, ports):
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
                    add_to_dict(port[0:3], str(end_port - port_num), vlan_name)
                else:
                    add_to_dict(port[0], str(end_port - port_num), vlan_name)

        else:
            if "Trk" in port:
                add_to_dict(port[0:3], port[3:], vlan_name)
            else:
                add_to_dict(port[0], port[1:], vlan_name)


def parse_config():
    with open("Port_Script/jz_core_vlans", "r") as fd:
        for line in fd.readlines():
            line = line.rstrip()
            line = line.split()
            ports = []
            # We are on VLAN line
            if line[0] == "vlan":
                vlan_name = line[1]
            # We are on port assignment line
            else:
                # tagged
                if line[0] == "tagged":
                    ports = line[1].split(",")
                # no untagged
                elif line[0] == "no":
                    ports = line[2].split(",")

            parse_ports(vlan_name, ports)


def print_dict():
    for k, v in port_dict.items():
        print("interface", k)
        print("switchport trunk allowed vlan add", end=" ")
        for x in v["tagged"]:
            print(x, end=",")
        print()


parse_config()

print_dict()
