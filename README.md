# reservo
Helps you reserve aws resources without clicking around the console

# Why?

Through the AWS console, for many of their services that have reservable 
components, you are only able to purchase reservations one-by-one. For a 
small number of reservations, this could be acceptable, but once you get 
over a certain amount, the experience can be painfully long.  

The api interface to the reservations is also not straightforward. For a 
given instance type and all of its parameters (db type, mulitaz?, duration, 
etc) you must look up an available 'reservation offering' and then request 
to purchase a number of this offering.  

With this tool, you can view your desired reservations in a digestible 
format (csv) put this through the tool, and get a list of the exact cli 
commands needed to make your reservations.

# Requirements

```
python3
```

IAM User Permissions:
```
DescribeReservedDBInstancesOfferings
```

# Usage
```
Usage: main.py [options] input_csv

Options:
  -h, --help            show this help message and exit
  -a AWS_SERVICE, --aws-service=AWS_SERVICE
                        The name of a (supported) reservable AWS service
```

input_csv: The header is for reference and should be omitted. This format 
is the one exported by the cloud cost management provider Cloudhealth. 
```csv
Purchase Date,Seller,Account,Region,Instance Class,Product Description,Multi AZ Deployment,Term,Effective Rate,Upfront Price,Hourly Rate,Offering Type,Quantity
2018-4-20,AWS,AccountName,us-east-1,db.m1.small,mysql,Yes,12,$0.059,$516.00,$0.000,All Upfront,3
2018-4-20,AWS,AccountName,us-east-1,db.r3.2xlarge,mysql,No,12,$0.501,$4396.00,$0.000,All Upfront,1
2018-4-20,AWS,AccountName,us-east-1,db.r3.2xlarge,postgresql,Yes,12,$1.003,$8792.00,$0.000,All Upfront,1
```

The required columns are: Instance Class,Product Description,Multi AZ 
Deployment,Term,Offering Type,Quantity

Install the requirements from the requirements.txt and then run:
```bash
python3 main.py --aws-service rds path/to/reservations.csv
```

The output will be a list of cli commands that can be run to perform the 
reservations. There is no dry-run option for these commands. Make sure to 
double-check the instance offering ids before placing the reservation. For 
example:
```bash
aws rds purchase-reserved-db-instances-offering --reserved-db-instances-offering-id abcdefgh-1357-4c13-2468-abcdef7c0d95 --db-instance-count 3
aws rds purchase-reserved-db-instances-offering --reserved-db-instances-offering-id abcdefgh-1357-453b-2468-abcdefa666c2 --db-instance-count 1
aws rds purchase-reserved-db-instances-offering --reserved-db-instances-offering-id abcdefgh-1357-4064-2468-abcdef333c14 --db-instance-count 1
```
