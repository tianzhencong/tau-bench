# Copyright Sierra

from .find_employee_by_email import FindEmployeeByEmail
from .get_employee_details import GetEmployeeDetails
from .get_project_details import GetProjectDetails
from .list_employee_projects import ListEmployeeProjects
from .query_sales_data import QuerySalesData
from .get_hr_record import GetHrRecord
from .search_files import SearchFiles
from .get_calendar import GetCalendar
from .aggregate_data import AggregateData
from .filter_data import FilterData
from .generate_report import GenerateReport
from .format_table import FormatTable
from .send_email import SendEmail
from .post_message import PostMessage
from .create_task import CreateTask
from .update_task_status import UpdateTaskStatus
from .calculate import Calculate
from .get_current_date import GetCurrentDate
from .transfer_to_human import TransferToHuman
from .list_departments import ListDepartments


ALL_TOOLS = [
    FindEmployeeByEmail,
    GetEmployeeDetails,
    GetProjectDetails,
    ListEmployeeProjects,
    QuerySalesData,
    GetHrRecord,
    SearchFiles,
    GetCalendar,
    AggregateData,
    FilterData,
    GenerateReport,
    FormatTable,
    SendEmail,
    PostMessage,
    CreateTask,
    UpdateTaskStatus,
    Calculate,
    GetCurrentDate,
    TransferToHuman,
    ListDepartments,
]
