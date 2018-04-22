import warnings

import boto3


class RdsHelper:

    def __init__(self, client=boto3.client('rds')):
        self.client = client

    def get_rds_instance_offering(self, reservation):
        response = self.client.describe_reserved_db_instances_offerings(
            DBInstanceClass=reservation.instance_type,
            Duration=reservation.duration,
            ProductDescription=reservation.db_class,
            OfferingType=reservation.offering_type,
            MultiAZ=reservation.multi_region
        )
        reservation_offerings = response['ReservedDBInstancesOfferings']
        if len(reservation_offerings) > 1:
            warnings.warn('Received more than one offering from the AWS API. Using the first one that matches the'
                          ' product description {}'.format(reservation.db_class)
                          )

        # Product description does not filter for an exact match, so for example
        # 'mysql' would find offerings for both mysql and aurora-mysql
        for offering in reservation_offerings:
            if offering['ProductDescription'] == reservation.db_class:
                return offering['ReservedDBInstancesOfferingId']

        return reservation_offerings[0]['ReservedDBInstancesOfferingId']
