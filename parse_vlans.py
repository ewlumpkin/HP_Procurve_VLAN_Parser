from pprint import pprint


port_dict = {}


def add_to_dict(line_card, port, vlan_name):
    if "A" in line_card:
        line_card = "gi 1/0/"
    if "B" in line_card:
        line_card = "gi 2/0/"
    if "F" in line_card:
        line_card = "gi 3/0/"
    if "Trk" in line_card:
        line_card = "Po"
    port = line_card + port
    if port in port_dict:
        port_dict[port].add(vlan_name)
    else:
        port_dict[port] = set({vlan_name})


with open("jz_core_vlans", "r") as fd:
    for line in fd.readlines():
        line = line.rstrip()
        line = line.split()
        ports = []
        if line[0] == "vlan":
            vlan_name = line[1]
        else:
            if line[0] == "tagged":
                # print(vlan_name, line[0])
                ports = line[1].split(",")

            elif line[0] == "no":
                # print(vlan_name, line[0])
                ports = line[2].split(",")
            # print(ports)

            for port in ports:
                if "-" in port:
                    port_buf = ""
                    beg_port = ""
                    end_port = ""
                    for i, elem in enumerate(port):
                        if elem.isnumeric():
                            port_buf += elem
                        elif elem == "-":
                            beg_port = int(port_buf)
                            port_buf = ""
                    end_port = int(port_buf)
                    print(beg_port, end_port)
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


for k, v in port_dict.items():
    print("interface", k)
    print("switchport trunk allowed vlan add", end=" ")
    for x in v:
        print(x, end=",")
    print()
