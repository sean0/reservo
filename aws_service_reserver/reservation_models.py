import csv


class ReservationData:
    def __init__(self, input_csv):
        self.reservations = import_reservation_from_csv(input_csv)


class Reservation:
    def __init__(self, instance_type, db_class, multi_region, offering_type, number_of_reservations, duration_in_months):
        self.instance_type = instance_type
        self.db_class = db_class
        self.multi_region = yes_no_to_bool(multi_region)
        self.offering_type = offering_type
        self.number_of_reservations = number_of_reservations
        self.duration = str(convert_months_to_years(duration_in_months))


def import_reservation_from_csv(input_csv):
    reservations = []
    with open(input_csv, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            reservations.append(
                Reservation(
                    instance_type=row[4],
                    db_class=row[5],
                    multi_region=row[6],
                    duration_in_months=row[7],
                    offering_type=row[11],
                    number_of_reservations=row[12]
                )
            )
    return reservations


def yes_no_to_bool(yes_no_string):
    if type(yes_no_string) is bool:
        return yes_no_string
    if yes_no_string == 'Yes':
        return True
    elif yes_no_string == 'No':
        return False


def convert_months_to_years(duration_in_months):
    return int(int(duration_in_months) / 12)
