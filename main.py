from optparse import OptionParser
from warnings import warn

from aws_service_reserver.reservation_models import ReservationData
from aws_service_reserver.rdsreservable import RdsReservable


def main():
    parser = OptionParser(usage="usage: %prog [options] input_csv")
    parser.add_option("-a", "--aws-service",
                      action="store",
                      type='choice',
                      dest="aws_service",
                      choices=['rds', 'elasticache'],
                      default='rds',
                      help="The name of a (supported) reservable AWS service",
                      )
    (opts, args) = parser.parse_args()
    if len(args) >= 1:
        csv_file_path = args[0]
    else:
        csv_file_path = 'aws_service_reserver/tests/test_csv.csv'
        warn('No input_csv supplied. Falling back to test csv: {}'.format(csv_file_path))

    choose_aws_service_flow(csv_file_path, opts.aws_service)


def choose_aws_service_flow(csv_file_path, aws_service):
    if aws_service == 'rds':
        reservation_data = ReservationData(csv_file_path)
        rds_reservable = RdsReservable()

        print('Running these commands with a user with proper privileges will purchase these reservations.')
        for item in rds_reservable.get_all_cli_commands(reservation_data):
            print(item)
    elif aws_service == 'elasticache':
        raise Exception("This isn't implemented yet for elasticache.")


if __name__ == '__main__':
    main()
