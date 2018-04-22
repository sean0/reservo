import unittest

import boto3

from aws_service_reserver.rds_helper import RdsHelper
from botocore.stub import Stubber

from aws_service_reserver.reservation_models import Reservation
from aws_service_reserver.tests.test_instance_offering_data import m1_small_offering, r3_2xlarge_mysql_aurora_mysql


class TestRdsHelper(unittest.TestCase):

    def setUp(self):
        client = boto3.client('rds')
        self.stubber = Stubber(client)
        self.rds_helper = RdsHelper(client)

    def test_get_rds_offering(self):
        m1_small_reservation = Reservation(
            instance_type="db.m1.small",
            db_class="mysql",
            multi_region=True,
            offering_type="Partial Upfront",
            number_of_reservations=1,
            duration_in_months='12'
        )

        expected_params = {
            'DBInstanceClass': 'db.m1.small',
            'Duration': '1',
            'MultiAZ': True,
            'OfferingType': 'Partial Upfront',
            'ProductDescription': 'mysql'
        }

        self.stubber.add_response('describe_reserved_db_instances_offerings', m1_small_offering, expected_params)

        with self.stubber:
            self.assertEqual(self.rds_helper.get_rds_instance_offering(m1_small_reservation), '0056db9a-7421-4207-8f54-92b563e53e19')

    def test_get_rds_offering_multiple_offerings(self):

        r3_2xlarge_reservation = Reservation(
            instance_type="db.r3.2xlarge",
            db_class="mysql",
            multi_region=True,
            offering_type="Partial Upfront",
            number_of_reservations=1,
            duration_in_months='12'
        )
        expected_params = {
            'DBInstanceClass': 'db.r3.2xlarge',
            'Duration': '1',
            'MultiAZ': True,
            'OfferingType': 'Partial Upfront',
            'ProductDescription': 'mysql'
        }

        self.stubber.add_response('describe_reserved_db_instances_offerings', r3_2xlarge_mysql_aurora_mysql, expected_params)

        with self.stubber:
            self.assertEqual(self.rds_helper.get_rds_instance_offering(r3_2xlarge_reservation), '005865f3-389f-2077-881d-bf330891b1ac')
