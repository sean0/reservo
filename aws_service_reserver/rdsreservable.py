from aws_service_reserver.rds_helper import RdsHelper
from aws_service_reserver.reservable import Reservable

OFFERING_ID_FLAG = '--reserved-db-instances-offering-id'
INSTANCE_COUNT_FLAG = '--db-instance-count'


class RdsReservable(Reservable):

    def format_cli_command(self, instance_count_string, offering_id_string):
        command_base = 'aws rds purchase-reserved-db-instances-offering'
        single_reservation_command = '{base} {offering_id} {instance_count}'.format(
            base=command_base,
            offering_id=offering_id_string,
            instance_count=instance_count_string
        )
        return single_reservation_command

    def get_offering_id_string(self, reservation):
        rds_helper = RdsHelper()
        instance_offering_id = rds_helper.get_rds_instance_offering(reservation)
        return '{offering_id_flag} {offering_id}'.format(
            offering_id_flag=OFFERING_ID_FLAG,
            offering_id=instance_offering_id
        )

    def get_instance_count_string(self, reservation):
        return '{instance_count_flag} {instance_count}'.format(
            instance_count_flag=INSTANCE_COUNT_FLAG,
            instance_count=reservation.number_of_reservations
        )

    def get_all_cli_commands(self, reservation_data):
        all_reservation_commands = []
        for reservation in reservation_data.reservations:
            instance_count_string = self.get_instance_count_string(reservation)
            offering_id_string = self.get_offering_id_string(reservation)
            single_reservation_command = self.format_cli_command(instance_count_string, offering_id_string)
            all_reservation_commands.append(single_reservation_command)
        return all_reservation_commands
