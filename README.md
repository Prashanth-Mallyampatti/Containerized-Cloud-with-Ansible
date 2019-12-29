# Cloud Automation

Execution:

`python3 init.py <csv_file_name>`

Example:

`python3 init.py test.csv`

Assumptions:
1. Input CSV file is valid. 
    1. Only 4 types of network types - GRE, L3, Bridge, L2 
    2. No spaces or extra characters in the file
    3. Tuple format: `<src container>,<dst container>,<network_type>`
2. Container names are unique.
3. One CSV file for each tenant
4. CSV file one time update.
5. IP addresses for the tenant containers are assigned by the provider.
6. All containers are built with a default Ubuntu:18.04 operating system
