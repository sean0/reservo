import abc


class Reservable(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def format_cli_command(self, instance_count_string, offering_id_string):
        raise NotImplementedError('users must define format_cli_command to use this base class')

    @abc.abstractmethod
    def get_all_cli_commands(self, reservation_data):
        raise NotImplementedError('users must define get_all_cli_commands to use this base class')

    @abc.abstractmethod
    def get_offering_id_string(self, reservation):
        raise NotImplementedError('users must define get_offering_id_string to use this base class')
