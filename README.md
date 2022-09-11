# HP VLAN Configuration Parser and Converter

This converts the HP Procurve VLAN configuration to a VLAN configuration suitable to migrate to Cisco switches.

The difficulty of migrating from HP to Cisco is that the Procurves apply ports to VLANs and Cisco applies VLANs to Ports.  This is further complicated by the face that ports can be represented atomically and in ranges within the configuration.  

This parser will parse the configuration of an HP Procurve switch and create interface configuration for you to further manipulate to your desires.

## Example Usage

`python parse_hp_vlans.py hp_port_config.txt`

An example source coniguration can be found in the root directory of the project to give you an idea of the usage of the script.