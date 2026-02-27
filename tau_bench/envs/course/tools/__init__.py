# Copyright Sierra

from .add_credit import AddCredit
from .calculate import Calculate
from .cancel_registration import CancelRegistration
from .drop_courses import DropCourses
from .find_student_by_email import FindStudentByEmail
from .find_student_by_name_dob import FindStudentByNameDob
from .get_course_details import GetCourseDetails
from .get_registration_details import GetRegistrationDetails
from .get_student_details import GetStudentDetails
from .list_departments import ListDepartments
from .modify_registration_courses import ModifyRegistrationCourses
from .modify_registration_payment import ModifyRegistrationPayment
from .search_courses_by_department import SearchCoursesByDepartment
from .switch_sections import SwitchSections
from .transfer_to_human_agents import TransferToHumanAgents


ALL_TOOLS = [
    AddCredit,
    Calculate,
    CancelRegistration,
    DropCourses,
    FindStudentByEmail,
    FindStudentByNameDob,
    GetCourseDetails,
    GetRegistrationDetails,
    GetStudentDetails,
    ListDepartments,
    ModifyRegistrationCourses,
    ModifyRegistrationPayment,
    SearchCoursesByDepartment,
    SwitchSections,
    TransferToHumanAgents,
]
