# Copyright Sierra

from .add_loyalty_points import AddLoyaltyPoints
from .book_package import BookPackage
from .calculate import Calculate
from .cancel_booking import CancelBooking
from .find_client_by_email import FindClientByEmail
from .find_client_by_name_dob import FindClientByNameDob
from .get_booking_details import GetBookingDetails
from .get_client_details import GetClientDetails
from .get_package_details import GetPackageDetails
from .get_payment_summary import GetPaymentSummary
from .list_destinations import ListDestinations
from .modify_booking_options import ModifyBookingOptions
from .modify_booking_payment import ModifyBookingPayment
from .modify_booking_travelers import ModifyBookingTravelers
from .search_packages import SearchPackages
from .search_packages_by_component import SearchPackagesByComponent
from .transfer_to_human_agents import TransferToHumanAgents

ALL_TOOLS = [
    AddLoyaltyPoints,
    BookPackage,
    Calculate,
    CancelBooking,
    FindClientByEmail,
    FindClientByNameDob,
    GetBookingDetails,
    GetClientDetails,
    GetPackageDetails,
    GetPaymentSummary,
    ListDestinations,
    ModifyBookingOptions,
    ModifyBookingPayment,
    ModifyBookingTravelers,
    SearchPackages,
    SearchPackagesByComponent,
    TransferToHumanAgents,
]
