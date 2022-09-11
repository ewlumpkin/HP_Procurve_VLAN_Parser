# HP VLAN Configuration Parser and Converter

This converts an HP Procurve VLAN configuration to a VLAN configuration suitable to migrate to Cisco switches.

The difficulty of migrating from HP to Cisco is that the Procurves apply ports to VLANs and Cisco applies VLANs to Ports.  This is further complicated by the fact that ports can be represented atomically *and* in ranges within the configuration.  

This parser will parse the configuration of an HP Procurve switch and create interface configuration for you to further manipulate to your desires.

## Example Usage

`python parse_hp_vlans.py hp_port_config.txt`

You must only use the vlan configuration snippet from the Procurve configuration in the source file.  The script is not built to handle a full configuration currently.

An example source configuration can be found in the root directory of the project to give you an idea of the usage of the script.