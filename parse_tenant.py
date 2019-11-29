#################################################
# Script that parses tenant's input config file
# and creates the required files for Ansible
#################################################

import sys
import yaml
import csv
import os
import subprocess
import os.path
from os import path

main = {}
main_tenant = {}
tenant = []
container = []

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
       
        # Bridge network type 
        if row[2] == "Bridge" or row[2] == "L2":
            tenant_list["namespace_1"] = "ns2"
            tenant_list["namespace_2"] = "ns2"

            # IP address per tenant network
            tenant_list["c1_IP"] = "10.10." + str(line_count) + ".1/24" 
            tenant_list["c2_IP"] = "10.10." + str(line_count) + ".2/24" 
            
        # L3 network type 
        if row[2] == "L3":
            tenant_list["namespace_1"] = "ns1"
            tenant_list["namespace_2"] = "ns3"

            # IP address per tenant network
            tenant_list["c1_IP"] = "10.1." + str(line_count) + ".1/24" 
            tenant_list["c2_IP"] = "10.2." + str(line_count) + ".2/24" 

            # route per tenant network
            tenant_list["c1_route"] = "10.2." + str(line_count) + ".0/24" 
            tenant_list["c2_route"] = "10.1." + str(line_count) + ".0/24" 

        # VXLAN network type 
        if row[2] == "VXLAN":
            tenant_list["namespace_1"] = "ns1"
            tenant_list["namespace_2"] = "ns3"

            # IP address per tenant network
            tenant_list["c1_IP"] = "10.10." + str(line_count) + ".1/24" 
            tenant_list["c2_IP"] = "10.10." + str(line_count) + ".2/24" 

        # GRE network type 
        if row[2] == "GRE":
            tenant_list["namespace_1"] = "ns1"
            tenant_list["namespace_2"] = "ns3"

            # IP address per tenant network
            tenant_list["c1_IP"] = "10.3." + str(line_count) + ".1/24" 
            tenant_list["c2_IP"] = "10.4." + str(line_count) + ".2/24" 

            # route per tenant network
            tenant_list["c1_route"] = "10.4." + str(line_count) + ".0/24" 
            tenant_list["c2_route"] = "10.3." + str(line_count) + ".0/24" 

        # veth pairs
        tenant_list["C1_veth"] = row[0] + "c1"
        tenant_list["C2_veth"] = row[1] + "c2"
        tenant_list["ns1_veth"] = row[0] + "n1"
        tenant_list["ns2_veth"] = row[1] + "n2"

        # populate dict
        tenant.append(tenant_list)


    # populate list
    main["Tenant"] = tenant



# Creating yaml file
with open("./tenant.yml", "w") as file:
    doc = yaml.dump(main, file, default_flow_style=False)

# Flag for ansible exit status
success = True

# Call ansible playbook
exit_status = os.system("ansible-playbook infra_setup.yml -v")
if exit_status != 0:
  print ("Initial setup creation failed")
  success = False

# Call ansible playbook
exit_status = os.system("ansible-playbook tenant_setup.yml --extra-vars 'tenant_file=tenant.yml' -v")
if exit_status != 0:
  print ("Setup creation failed")
  success = False

# If setup creation was successfull, proceed in obtaining container PIDs
if success:
    # Parse the input CSV file
    CSV_file = "./" + str(sys.argv[1])
    with open(CSV_file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',' )
        line_count = 0

        for row in csv_reader:
            container_list = {}

            c1_pid = subprocess.Popen("docker inspect -f '{{.State.Pid}}' " + str(row[0]), shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0].rstrip()
            fpath = "/var/run/netns/" + str(c1_pid)
            if not path.exists(fpath):
                os.system("ln -s /proc/" + str(c1_pid) + "/ns/net /var/run/netns/" + str(c1_pid))

            container_list["container_1"] = row[0]
            container_list["c1_pid"] = c1_pid
            container_list["C1_veth"] = row[0] + "c1"


            c2_pid = subprocess.Popen("docker inspect -f '{{.State.Pid}}' " + str(row[1]), shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0].rstrip()
            fpath = "/var/run/netns/" + str(c2_pid)
            if not path.exists(fpath):
                os.system("ln -s /proc/" + str(c2_pid) + "/ns/net /var/run/netns/" + str(c2_pid))

            container_list["container_2"] = row[1]
            container_list["c2_pid"] = c2_pid
            container_list["C2_veth"] = row[1] + "c2"

            container.append(container_list)
        #print (container)

    main_tenant["Container"] = container
    #print (main_tenant)

# Creating yaml file
with open("./tenant_container.yml", "w") as file:
    doc = yaml.dump(main_tenant, file, default_flow_style=False)

# Call ansible playbook
exit_status = os.system("ansible-playbook tenant_setup_1.yml --extra-vars 'tenant_file=tenant.yml tenant_container=tenant_container.yml' -v")
if exit_status != 0:
  print ("Network creation failed")
  success = False
