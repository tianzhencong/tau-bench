# Copyright Sierra

from .add_hsa_credit import AddHsaCredit
from .book_appointment import BookAppointment
from .calculate import Calculate
from .cancel_appointment import CancelAppointment
from .find_patient_by_email import FindPatientByEmail
from .find_patient_by_name_dob import FindPatientByNameDob
from .get_appointment_details import GetAppointmentDetails
from .get_insurance_summary import GetInsuranceSummary
from .get_patient_details import GetPatientDetails
from .get_procedure_details import GetProcedureDetails
from .get_specialist_details import GetSpecialistDetails
from .list_departments import ListDepartments
from .modify_appointment_procedure import ModifyAppointmentProcedure
from .reschedule_appointment import RescheduleAppointment
from .search_procedures import SearchProcedures
from .search_specialists import SearchSpecialists
from .transfer_to_human_agents import TransferToHumanAgents

ALL_TOOLS = [
    AddHsaCredit,
    BookAppointment,
    Calculate,
    CancelAppointment,
    FindPatientByEmail,
    FindPatientByNameDob,
    GetAppointmentDetails,
    GetInsuranceSummary,
    GetPatientDetails,
    GetProcedureDetails,
    GetSpecialistDetails,
    ListDepartments,
    ModifyAppointmentProcedure,
    RescheduleAppointment,
    SearchProcedures,
    SearchSpecialists,
    TransferToHumanAgents,
]
