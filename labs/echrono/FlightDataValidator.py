from .models import *
import datetime
from .ValidationResponse import *

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
            print(User.objects.filter(id=request.POST.get('instructor_id')).first())
            for user in User.objects.all():
                print(user.id)
            return Chronometer(
                instructor_id=User.objects.filter(id=request.POST.get('instructor_id')).first(),
                pilot_passenger_id=User.objects.filter(id=request.POST.get('pilot_passenger_id')).first(),
                start_type=request.POST.get('start_type'),
                winch_operator_id=User.objects.filter(id=request.POST.get('winch_pilot_id')).first(),
                tow_pilot_id=User.objects.filter(id=request.POST.get('tow_pilot')).first(),
                glider_id=Glider.objects.filter(id=request.POST.get('glider_id')).first(),
                airplane_id=Airplane.objects.filter(id=request.POST.get('airplane')).first()
            )

    @staticmethod
    def check_if_aircrafts_midair(flight) -> bool:
        """
        Function checks if aircrafts chosen for beginning flight arent curently midair.
        :param flight:
        :return: Boolean value either aircrafts are free or not
        """
        active_flights = Chronometer.query.filter(Chronometer.active == True).all()
        for af in active_flights:
            if af.airplane.id == flight.airplane.id or af.glider.id == flight.glider.id:
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
        active_flights = Chronometer.query.filter(Chronometer.active==True).all()
        airplane_flights = AirplaneFlight.query.all()
        for f in active_flights:
            mid_air_pilots.append(f.pilot_passenger)
            mid_air_pilots.append(f.instructor)
        for f in airplane_flights:
            mid_air_pilots.append(f.airplane_pilot)
        if flight.instructor in mid_air_pilots or flight.pilot_passenger in mid_air_pilots or flight.tow_pilot in mid_air_pilots:
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
        if flight.instructor:
            if not flight.instructor.instructor:
                return ValidationResponse(False, "User picked for instructor has no permissions to do that")
        if flight.pilot_passenger.id != 1:
            if not flight.pilot_passenger.glider_pilot:
                return ValidationResponse(False, "User picked for pilot has no permissions to do that")
        if flight.pilot_passenger.id == 1:
            if not flight.instructor:
                return ValidationResponse(False, "Passenger User cannot flight on his own")
        if flight.winch_operator:
            if not flight.winch_operator.winch_operator:
                return ValidationResponse(False, "User picked for winch operator has no permissions to do that")
        if flight.tow_pilot:
            if not flight.tow_pilot.airplane_pilot:
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
        if flight.start_type == 'W' and flight.tow_pilot:
            return ValidationResponse(False, "There cannot be tow pilot in Winch-Launched flight")
        if flight.start_type == 'W' and flight.airplane:
            return ValidationResponse(False, "There cannot be tow airplane in Winch-Launched flight")
        if flight.start_type == 'S' and flight.winch_operator:
            return ValidationResponse(False, "There cannot be winch operator in tow-type flight")
        if flight.start_type == 'S' and not flight.airplane:
            return ValidationResponse(False, "There must be a plane in tow-type flight")
        return ValidationResponse(True, "")

    @staticmethod
    def validate_operators(flight) -> bool:
        """
        Checks if there is one and only one staff member executing launch
        :param flight:
        :return: Boolean value
        """
        if (flight.tow_pilot and flight.winch_operator) or (not flight.tow_pilot and not flight.winch_operator):
            return ValidationResponse(False, "There cannot be both tow pilot and winch pilot in one flight")
        return ValidationResponse(True, "")

    @staticmethod
    def check_duplicate_ids(flight) -> bool:
        """
        Checks if there are any duplicate users taking part in flight
        :param flight:
        :return:
        """
        print(flight)
        crew = [flight.instructor_id,flight.pilot_passenger_id,flight.winch_operator,flight.tow_pilot_id]
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
    for key,value in arguments.items():
        if value == 'true':
            arguments[key] = True
        if value == 'false':
            arguments[key] = False


def time_difference(time1, time2):
    t1 = datetime.datetime.strptime(time1, "%H:%M")
    t2 = datetime.datetime.strptime(time2, "%H:%M")
    return str(t2 - t1)[0:4]


def chrono_to_airplane(chrono_object):
    """
    Function which converses one table record to another one for estetic purposes.
    :param chrono_object:
    :return:
    """
    return AirplaneFlight(
        flight_nr=chrono_object.flight_nr,
        time_of_start=chrono_object.time_of_start,
        airplane_pilot=chrono_object.tow_pilot.id,
        airplane=Airplane.query.filter(Airplane.id == chrono_object.airplane.id).first().name,
    )