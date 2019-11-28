#################################################
# Script that parses tenant's input config file
# and creates the required files for Ansible
#################################################

import sys
import yaml
import csv

main = {}
tenant = []

# Parse the input CSV file
CSV_file = "./" + str(sys.argv[1])
with open(CSV_file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',' )
    line_count = 0
 
    for row in csv_reader:
        tenant_list = {}
        line_count += 1
        tenant_list["container_1"] = row[0]
        tenant_list["container_2"] = row[1]
        tenant_list["network_type"] = row[2]
        
        if row[2] == "Bridge" or row[2] == "L2":
            tenant_list["namespace_1"] = "ns2"
            tenant_list["namespace_2"] = "ns2"
            
        if row[2] == "L3":
            tenant_list["namespace_1"] = "ns2"
            tenant_list["namespace_2"] = "ns3"

        if row[2] == "VXLAN":
            tenant_list["namespace_1"] = "ns1"
            tenant_list["namespace_2"] = "ns3"

        if row[2] == "GRE":
            tenant_list["namespace_1"] = "ns1"
            tenant_list["namespace_2"] = "ns2"

        tenant_list["c1_IP"] = "10.10." + str(line_count) + ".1/24" 
        tenant_list["c2_IP"] = "10.10." + str(line_count) + ".2/24" 

        tenant_list["C1_veth"] = row[0] + "c1"
        tenant_list["C2_veth"] = row[1] + "c2"
        tenant_list["ns1_veth"] = row[0] + "n1"
        tenant_list["ns2_veth"] = row[1] + "n2"

        tenant.append(tenant_list)

    main["tenant"] = tenant

# Creating yaml file
with open("./tenant.yml", "w") as file:
    doc = yaml.dump(main, file, default_flow_style=False)
