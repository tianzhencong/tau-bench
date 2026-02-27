# Copyright Sierra

from tau_bench.envs.hotel.tools.get_user_details import GetUserDetails
from tau_bench.envs.hotel.tools.find_user_id_by_email import FindUserIdByEmail
from tau_bench.envs.hotel.tools.get_reservation_details import GetReservationDetails
from tau_bench.envs.hotel.tools.get_hotel_details import GetHotelDetails
from tau_bench.envs.hotel.tools.search_available_rooms import SearchAvailableRooms
from tau_bench.envs.hotel.tools.book_reservation import BookReservation
from tau_bench.envs.hotel.tools.cancel_reservation import CancelReservation
from tau_bench.envs.hotel.tools.modify_reservation_dates import ModifyReservationDates
from tau_bench.envs.hotel.tools.modify_reservation_room import ModifyReservationRoom
from tau_bench.envs.hotel.tools.modify_reservation_guests import ModifyReservationGuests
from tau_bench.envs.hotel.tools.modify_reservation_payment import ModifyReservationPayment
from tau_bench.envs.hotel.tools.add_service import AddService
from tau_bench.envs.hotel.tools.remove_service import RemoveService
from tau_bench.envs.hotel.tools.send_voucher import SendVoucher
from tau_bench.envs.hotel.tools.calculate import Calculate
from tau_bench.envs.hotel.tools.transfer_to_human_agents import TransferToHumanAgents
from tau_bench.envs.hotel.tools.think import Think

ALL_TOOLS = [
    BookReservation,
    Calculate,
    CancelReservation,
    GetReservationDetails,
    GetUserDetails,
    GetHotelDetails,
    FindUserIdByEmail,
    SearchAvailableRooms,
    ModifyReservationDates,
    ModifyReservationRoom,
    ModifyReservationGuests,
    ModifyReservationPayment,
    AddService,
    RemoveService,
    SendVoucher,
    TransferToHumanAgents,
    Think,
]
