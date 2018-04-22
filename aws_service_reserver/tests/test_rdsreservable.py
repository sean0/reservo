import unittest
from unittest.mock import patch

from aws_service_reserver.rdsreservable import RdsReservable
from aws_service_reserver.reservation_models import ReservationData


class TestRDSReservable(unittest.TestCase):
    def setUp(self):
        self.rds_reservable = RdsReservable()

    def test_import_fields(self):
        reservation_data = ReservationData('test_csv.csv')
        self.assertEqual(reservation_data.reservations[0].instance_type, 'db.m1.small')
        self.assertEqual(reservation_data.reservations[0].db_class, 'mysql')
        self.assertEqual(reservation_data.reservations[0].multi_region, 'Yes')
        self.assertEqual(reservation_data.reservations[0].offering_type, 'All Upfront')
        self.assertEqual(reservation_data.reservations[0].number_of_reservations, '3')

    @patch('rdsreserve.rdsreservable.RdsReservable.get_offering_id_string')
    def test_get_cli_commands(self, mock_get_offering_id_string):
        mock_get_offering_id_string.return_value = '--reserved-db-instances-offering-id 0056db9a-7421-4207-8f54-92b563e53e19'
        reservation_data = ReservationData('test_csv.csv')
        command_output = self.rds_reservable.get_all_cli_commands(reservation_data)
        command_base = 'aws rds purchase-reserved-db-instances-offering'
        expected = [
            '{} --reserved-db-instances-offering-id 0056db9a-7421-4207-8f54-92b563e53e19 --db-instance-count 3'.format(command_base),
            '{} --reserved-db-instances-offering-id 0056db9a-7421-4207-8f54-92b563e53e19 --db-instance-count 1'.format(command_base),
            '{} --reserved-db-instances-offering-id 0056db9a-7421-4207-8f54-92b563e53e19 --db-instance-count 1'.format(command_base)
        ]

        self.assertEqual(command_output, expected)
