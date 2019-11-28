#################################################
# Script that parses tenant's input config file
# and creates the required files for Ansible
#################################################

import ipaddress
import yaml
import os
import sys
import datetime
import logging
import csv

main = {}
tenant = []

# Parse the input CSV file and generate a yaml file.
CSV_file = "./" + str(sys.argv[1])
with open(CSV_file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',' )
    line_count = 0

    for row in csv_reader:
        tenant_list = {}
        #print (row[2])
        line_count += 1
        tenant_list["container_1"] = row[0]
        tenant_list["container_2"] = row[1]
        tenant_list["network_type"] = row[2]
        #print (container_1, container_2, network_type)
        tenant.append(tenant_list)

    #print (tenant)
    print (line_count)

    main["tenant"] = tenant
    print (main)
