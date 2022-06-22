from .models import *
from .ValidationResponse import *
from django.utils import timezone

crew_roles = ["instructor_id", "pilot_passenger_id", "winch_operator_id", "tow_pilot_id"]


class FlightDataValidator:

    @staticmethod
    def validate_add_flight_request(request) -> bool:
        required_data = ['instructor', 'pilot_passenger', 'start_type', 'winch_pilot',
                         'airplane_pilot', 'glider', 'airplane']
        if request.method != "POST":
            return ValidationResponse(False, "Invalid request method")
        if not any(required_data) not in request.POST.keys():
            return ValidationResponse(False, "Incorrect data provided")
        return ValidationResponse(True, "")

    @staticmethod
    def validate_start_flight_request(request) -> bool:
        pass

    @staticmethod
    def create_chronometer_object(request):
        if FlightDataValidator.validate_add_flight_request(request):
            chrono = Chronometer(
                instructor_id=User.objects.filter(id=request.POST.get('instructor_id')).first(),
                pilot_passenger_id=User.objects.filter(id=request.POST.get('pilot_passenger_id')).first(),
                start_type=request.POST.get('start_type'),
                winch_operator_id=User.objects.filter(id=request.POST.get('winch_pilot_id')).first(),
                tow_pilot_id=User.objects.filter(id=request.POST.get('tow_pilot')).first(),
                glider_id=Glider.objects.filter(id=request.POST.get('glider_id')).first(),
                airplane_id=Airplane.objects.filter(id=request.POST.get('airplane')).first()
            )
            return chrono

    @staticmethod
    def check_if_aircrafts_midair(flight) -> bool:
        """
        Function checks if aircrafts chosen for beginning flight arent curently midair.
        :param flight:
        :return: Boolean value either aircrafts are free or not
        """
        active_flights = Chronometer.objects.filter(active=True).all()
        for af in active_flights:
            if af.airplane.id == flight.airplane_id.id or af.glider.id == flight.glider.id:
                return ValidationResponse(False, "Some of chosen aircrafts are mid-air")
        return ValidationResponse(True, "")

    @staticmethod
    def check_if_pilots_midair(flight) -> bool:
        """
        Function checks if pilot in flight beeing executed arent actually midair
        :param flight:
        :return:
        """
        mid_air_pilots = []
        active_flights = Chronometer.objects.filter(active=True).all()
        airplane_flights = AirplaneFlight.objects.all()
        for f in active_flights:
            mid_air_pilots.append(f.pilot_passenger_id)
            mid_air_pilots.append(f.instructor_id)
        for f in airplane_flights:
            mid_air_pilots.append(f.airplane_pilot_id)
        if flight.instructor_id in mid_air_pilots or flight.pilot_passenger_id in mid_air_pilots or flight.tow_pilot_id in mid_air_pilots:
            return ValidationResponse(False, "Some of chosen pilots are mid-air")
        return ValidationResponse(True, "")

    @staticmethod
    def check_users_permissions(flight) -> bool:
        """
        Checks if user is permitted to contribute in given way for example if
        instructor in flight record has instructor permission
        :param flight:
        :return: Boolean value either users fit or not
        """
        if flight.instructor_id:
            if flight.instructor_id:
                if not flight.instructor_id.instructor:
                    return ValidationResponse(False, "User picked for instructor has no permissions to do that")
        if hasattr(flight, 'pilot_passenger_id'):
            if flight.pilot_passenger_id.id != 1:
                if not flight.pilot_passenger_id.glider_pilot:
                    return ValidationResponse(False, "User picked for pilot has no permissions to do that")
        if hasattr(flight, 'pilot_passenger_id'):
            if flight.pilot_passenger_id.id == 1:
                if not flight.instructor_id:
                    return ValidationResponse(False, "Passenger User cannot flight on his own")
        if flight.winch_operator_id:
            if flight.winch_operator_id:
                if not flight.winch_operator_id.winch_operator:
                    return ValidationResponse(False, "User picked for winch operator has no permissions to do that")
        if flight.tow_pilot_id:
            if flight.tow_pilot_id:
                if not flight.tow_pilot_id.airplane_pilot:
                    return ValidationResponse(False, "User picked for tow pilot has no permissions to do that")
        return ValidationResponse(True, "")

    @staticmethod
    def check_start_type(flight) -> bool:
        """
        Function checks if start type matches with other fields
        for example if start type is winch launch field flight.airplane should be
        none
        W - winch start
        S - tow pull start (S for samolot in pol.)
        :param flight:
        :return:
        """
        if flight.start_type == 'W' and flight.tow_pilot_id:
            return ValidationResponse(False, "There cannot be tow pilot in Winch-Launched flight")

        if flight.start_type == 'W' and flight.airplane_id:
            return ValidationResponse(False, "There cannot be tow airplane in Winch-Launched flight")

        if flight.start_type == 'S' and flight.winch_operator_id:
            return ValidationResponse(False, "There cannot be winch operator in tow-type flight")

        if flight.start_type == 'S' and not flight.airplane_id:
            return ValidationResponse(False, "There must be a plane in tow-type flight")

        return ValidationResponse(True, "")

    @staticmethod
    def validate_operators(flight) -> bool:
        """
        Checks if there is one and only one staff member executing launch
        :param flight:
        :return: Boolean value
        """
        if (flight.tow_pilot_id and flight.winch_operator_id) or (
                not flight.tow_pilot_id and not flight.winch_operator_id):
            return ValidationResponse(False, "There cannot be both tow pilot and winch pilot in one flight")
        return ValidationResponse(True, "")

    @staticmethod
    def check_duplicate_ids(flight) -> bool:
        """
        Checks if there are any duplicate users taking part in flight
        :param flight:
        :return:
        """
        crew = [getattr(flight, role) for role in crew_roles if hasattr(flight, role)]
        for member in crew:
            if member and crew.count(member) > 1:
                return ValidationResponse(False, "Same user cannot take more than one role in flight crew")
        return ValidationResponse(True, "")

    @staticmethod
    def validate_chrono_table(flight) -> bool:
        """
        Wraps together previous functions to one.
        :param flight:
        :return:
        """

        check_duplicate_response = FlightDataValidator.check_duplicate_ids(flight)
        if not check_duplicate_response.value:
            return check_duplicate_response
        check_users_permissions_response = FlightDataValidator.check_users_permissions(flight)
        if not check_users_permissions_response.value:
            return check_users_permissions_response
        check_start_type_response = FlightDataValidator.check_start_type(flight)
        if not check_start_type_response.value:
            return check_start_type_response
        validate_operators_response = FlightDataValidator.validate_operators(flight)
        if not validate_operators_response.value:
            return validate_operators_response
        return ValidationResponse(True, "")

    @staticmethod
    def validate_chrono_for_start(flight):

        check_if_pilots_midair_response = FlightDataValidator.check_if_pilots_midair(flight)
        if not check_if_pilots_midair_response.value:
            return check_if_pilots_midair_response
        check_if_aircrafts_midair_response = FlightDataValidator.check_if_aircrafts_midair(flight)
        if not check_if_aircrafts_midair_response.value:
            return check_if_aircrafts_midair_response
        return ValidationResponse(True, "")


def flip_booleans(arguments):
    """
    In html you cannot simply state boolean value as tag value so this is function
    which swaps string 'True' to boolean value
    :param arguments:
    :return:
    """
    for key, value in arguments.items():
        if value == 'true':
            arguments[key] = True
        if value == 'false':
            arguments[key] = False


def time_difference(time1, time2):
    # t1 = datetime.datetime.strptime(time1, "%H:%M")
    # t2 = datetime.datetime.strptime(time2, "%H:%M")
    return time2 - time1


def chrono_to_airplane(chrono_object):
    """
    Function which converses one table record to another one for estetic purposes.
    :param chrono_object:
    :return:
    """
    return AirplaneFlight(
        id=chrono_object.id,
        time_of_start=chrono_object.time_of_start,
        airplane_pilot=chrono_object.tow_pilot_id,
        airplane=Airplane.objects.filter(id=chrono_object.airplane_id.id).first(),
    )
