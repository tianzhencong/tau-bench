# Copyright Sierra
# Workflow orchestration tasks — fundamentally different from CRUD domains
# Each task requires CHAINING: tool A's output feeds into tool B
# Targets: MCP-Atlas/MCP-Bench style tool orchestration

from tau_bench.types import Action, Task

TASKS = [
    # =================================================================
    # PATTERN 1: Query → Aggregate → Report → Email (full pipeline)
    # This is the canonical MCP-Atlas pattern
    # =================================================================

    # Task 0: Sales pipeline (7 actions)
    # query → aggregate by product → generate report → email to manager
    Task(
        user_id="EMP001",
        instruction="Your email is liam.brown41@company.com. Query all sales data from the North region. Aggregate the results by product, summing the amount. Generate a summary report titled 'North Region Sales Summary'. Then email it to your manager at EMP004's email. Tell me the top product by total sales.",
        actions=[
            Action(name="find_employee_by_email", kwargs={"email": "liam.brown41@company.com"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP001"}),
            Action(name="query_sales_data", kwargs={"region": "North"}),
            Action(name="aggregate_data", kwargs={"data_ref": "latest_query", "group_by": "product", "metric": "amount", "operation": "sum"}),
            Action(name="generate_report", kwargs={"title": "North Region Sales Summary", "data_ref": "998562a02cd0", "format": "summary", "author_id": "EMP001"}),
        ],
        outputs=[],
    ),

    # Task 1: Full pipeline with filter step
    # query → filter high-value → aggregate by region → report → email
    Task(
        user_id="EMP005",
        instruction="You are Anthony Brown, employee EMP005. Query all sales data. Filter to only records with amount greater than 5000. Then aggregate by region, summing the amounts. Generate a detailed report. Email the report to mary.perez38@company.com with subject 'High-Value Sales by Region'. How many regions have over $50,000 in high-value sales?",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP005"}),
            Action(name="query_sales_data", kwargs={}),
            Action(name="filter_data", kwargs={"data_ref": "latest_query", "field": "amount", "operator": "greater_than", "value": "5000"}),
            Action(name="aggregate_data", kwargs={"data_ref": "2be3cb8f2563", "group_by": "region", "metric": "amount", "operation": "sum"}),
            Action(name="generate_report", kwargs={"title": "High-Value Sales by Region", "data_ref": "0beea620f863", "format": "detailed", "author_id": "EMP005"}),
        ],
        outputs=[],
    ),

    # Task 2: Sales analysis → format table → email with attachment
    Task(
        user_id="EMP010",
        instruction="Your email is mia.wilson50@company.com. Query sales for product 'Enterprise Plan'. Aggregate by sales_rep, counting records. Format the result as a table showing sales_rep and count columns. Email the table to your manager with subject 'Enterprise Plan Sales Activity'. Include the report as attachment.",
        actions=[
            Action(name="find_employee_by_email", kwargs={"email": "mia.wilson50@company.com"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP010"}),
            Action(name="query_sales_data", kwargs={"product": "Enterprise Plan"}),
            Action(name="aggregate_data", kwargs={"data_ref": "latest_query", "group_by": "sales_rep", "metric": "record_id", "operation": "count"}),
            Action(name="generate_report", kwargs={"title": "Enterprise Plan Sales Activity", "data_ref": "043ea81cb28a", "format": "table", "author_id": "EMP010"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # PATTERN 2: Project analysis → task creation (cross-domain chain)
    # =================================================================

    # Task 3: Check project → find overdue tasks → create follow-up tasks
    Task(
        user_id="EMP005",
        instruction="You are EMP005. Check project PRJ003 details. Find all tasks that are 'blocked' or overdue (due_date before 2024-11-15). For each blocked task, create a new task assigned to the same person with title 'Unblock: [original title]' and priority 'critical', due 2024-11-22. How many new tasks do you need to create?",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP005"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ003"}),
        ],
        outputs=[],
    ),

    # Task 4: Check all my projects → summarize status → email report
    Task(
        user_id="EMP010",
        instruction="Your email is mia.wilson50@company.com. List all your projects. For each project, count tasks by status (todo, in_progress, done, blocked). Generate a report titled 'My Projects Status Summary'. Email it to yourself as a record. Tell me which project has the most blocked tasks.",
        actions=[
            Action(name="find_employee_by_email", kwargs={"email": "mia.wilson50@company.com"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP010"}),
            Action(name="list_employee_projects", kwargs={"employee_id": "EMP010"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ007"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ008"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ013"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ018"}),
        ],
        outputs=[],
    ),

    # Task 5: Project budget check → alert if over → email finance
    Task(
        user_id="EMP003",
        instruction="You are Wei Thompson, EMP003. Check project PRJ001. If the project has spent more than 80% of its budget, generate a report titled 'Budget Alert: [project name]' and email it to the Finance department head. Calculate the percentage spent and remaining budget.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP003"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ001"}),
            Action(name="calculate", kwargs={"expression": "100 * 1.0"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # PATTERN 3: Multi-source query → merge → analyze (data analyst workflow)
    # =================================================================

    # Task 6: HR + project data → identify top performers → notify
    Task(
        user_id="EMP005",
        instruction="You are EMP005 (Operations). Check your team members' HR records. Find anyone with performance_rating >= 4.5. Also check which projects they're on. For each top performer, send them a message saying 'Congratulations on your excellent review!' Tell me how many top performers you found.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP005"}),
        ],
        outputs=[],
    ),

    # Task 7: Calendar + project → find scheduling conflicts
    Task(
        user_id="EMP010",
        instruction="Your email is mia.wilson50@company.com. Check your calendar for November 18 (Monday). Also check project PRJ008 for tasks assigned to you that are due this week. If you have a meeting during a time when you planned to work on a critical task, let me know the conflict. List your meetings and critical tasks.",
        actions=[
            Action(name="find_employee_by_email", kwargs={"email": "mia.wilson50@company.com"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP010"}),
            Action(name="get_calendar", kwargs={"employee_id": "EMP010", "date": "2024-11-18"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ008"}),
        ],
        outputs=[],
    ),

    # Task 8: File search + data query → merge context → compose email
    Task(
        user_id="EMP020",
        instruction="You are Mary Perez, EMP020 (Legal). Search for files in the Legal department. Also query sales data for the West region. You need to email the Sales VP about compliance issues. Compose an email that references the legal policy document and the West region sales figures. Send to anthony.brown43@company.com with subject 'West Region Compliance Review'.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP020"}),
            Action(name="search_files", kwargs={"department": "Legal"}),
            Action(name="query_sales_data", kwargs={"region": "West"}),
            Action(name="aggregate_data", kwargs={"data_ref": "latest_query", "group_by": "product", "metric": "amount", "operation": "sum"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # PATTERN 4: Conditional workflow (decide based on data)
    # =================================================================

    # Task 9: Query → check threshold → branch action
    Task(
        user_id="EMP015",
        instruction="You are William Moore, EMP015. Query sales data for the South region. Aggregate by product, summing amounts. If any product has total sales under $10,000, create a task on project PRJ010 titled 'Investigate low sales: [product name]' with high priority, due 2024-11-25, assigned to you. Tell me which products are underperforming.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP015"}),
            Action(name="query_sales_data", kwargs={"region": "South"}),
            Action(name="aggregate_data", kwargs={"data_ref": "latest_query", "group_by": "product", "metric": "amount", "operation": "sum"}),
        ],
        outputs=[],
    ),

    # Task 10: Check HR data → conditional compensation → notify
    Task(
        user_id="EMP001",
        instruction="Your email is liam.brown41@company.com. You are a manager. Check the HR record for employee EMP015. If their performance rating is 4.0 or above and they haven't had a review in over 90 days, create a task for yourself on PRJ004 to schedule a review, priority high, due 2024-11-22. If rating is below 4.0, send them a message asking to schedule a 1:1.",
        actions=[
            Action(name="find_employee_by_email", kwargs={"email": "liam.brown41@company.com"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP001"}),
            Action(name="get_hr_record", kwargs={"employee_id": "EMP015"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP015"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # PATTERN 5: Multi-step task management workflow
    # =================================================================

    # Task 11: Scan project → update statuses → notify team
    Task(
        user_id="EMP005",
        instruction="You are EMP005. In project PRJ003, find all tasks with status 'in_progress' that have logged more than 30 hours. Update their status to 'done'. Then send a message to each task's assignee saying 'Your task [task_id] has been marked complete.' Count how many tasks you completed.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP005"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ003"}),
        ],
        outputs=[],
    ),

    # Task 12: Create weekly status report from project data
    Task(
        user_id="EMP003",
        instruction="You are Wei Thompson, EMP003. Create a weekly status report for project PRJ001. Get project details, count tasks by status, calculate total hours logged this sprint. Generate a report titled 'PRJ001 Weekly Status - Nov 15'. Email to all project members. What percentage of tasks are done?",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP003"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ001"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # PATTERN 6: Complex multi-source orchestration (10+ actions)
    # =================================================================

    # Task 13: Full analyst workflow
    Task(
        user_id="EMP005",
        instruction="You are Anthony Brown, EMP005. Complete this analysis: (1) Query all sales data for October (date_from 2024-10-01, date_to 2024-10-31). (2) Aggregate by region, summing amounts. (3) Filter to regions with total > $50,000. (4) Generate a detailed report titled 'October High-Performance Regions'. (5) Email the report to liam.brown41@company.com with subject 'October Sales Analysis'. Tell me the total sales across all high-performance regions.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP005"}),
            Action(name="query_sales_data", kwargs={"date_from": "2024-10-01", "date_to": "2024-10-31"}),
            Action(name="aggregate_data", kwargs={"data_ref": "latest_query", "group_by": "region", "metric": "amount", "operation": "sum"}),
            Action(name="filter_data", kwargs={"data_ref": "2123fe685590", "field": "sum_amount", "operator": "greater_than", "value": "50000"}),
            Action(name="generate_report", kwargs={"title": "October High-Performance Regions", "data_ref": "937398e90393", "format": "detailed", "author_id": "EMP005"}),
        ],
        outputs=[],
    ),

    # Task 14: Cross-source dashboard
    Task(
        user_id="EMP001",
        instruction="Your email is liam.brown41@company.com. Build me a dashboard: (1) Get my project PRJ004 status. (2) Query sales data for my team (I'm in Engineering). (3) Check my calendar for next Monday Nov 18. (4) Get my HR record. Compile all this into a report titled 'Weekly Dashboard - Liam Brown'. Email it to yourself. Summarize the key findings.",
        actions=[
            Action(name="find_employee_by_email", kwargs={"email": "liam.brown41@company.com"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP001"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ004"}),
            Action(name="query_sales_data", kwargs={}),
            Action(name="get_calendar", kwargs={"employee_id": "EMP001", "date": "2024-11-18"}),
            Action(name="get_hr_record", kwargs={"employee_id": "EMP001"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # POLICY / EDGE CASES
    # =================================================================

    # Task 15: Try to access other employee's HR data → should only show own
    Task(
        user_id="EMP020",
        instruction="You are Mary Perez, EMP020. You want to see the performance ratings of everyone in the Legal department to prepare for annual reviews. Check HR records for EMP020, EMP045, and EMP067. If you can access them, compile a summary.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP020"}),
            Action(name="get_hr_record", kwargs={"employee_id": "EMP020"}),
            Action(name="get_hr_record", kwargs={"employee_id": "EMP045"}),
            Action(name="get_hr_record", kwargs={"employee_id": "EMP067"}),
        ],
        outputs=[],
    ),

    # Task 16: Send email without confirming → should ask for confirmation
    Task(
        user_id="EMP003",
        instruction="You are Wei Thompson, EMP003. Send an email to all PRJ001 members about the upcoming deadline. First get the project details to find the members. Compose a professional email about the deadline. The subject should be 'Deadline Reminder: [project name]'.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP003"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ001"}),
        ],
        outputs=[],
    ),

    # Task 17: Transfer when task is outside scope
    Task(
        user_id="EMP020",
        instruction="You are Mary Perez, EMP020. You need to submit a formal legal brief to the court. This requires document notarization and official filing. If the system can't handle court filings, ask to be transferred to the legal operations team.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP020"}),
            Action(name="transfer_to_human", kwargs={"summary": "Employee needs to submit a formal legal brief to court. This requires document notarization and official filing, which is outside the scope of the workflow automation system."}),
        ],
        outputs=[],
    ),

    # =================================================================
    # ADVERSARIAL / CHANGE MIND
    # =================================================================

    # Task 18: Wrong project, corrects
    Task(
        user_id="EMP010",
        instruction="Your email is mia.wilson50@company.com. You want to check your project about the mobile app. You first say it's PRJ005 but that's actually 'Hiring Sprint'. Ask the agent to find your actual projects and identify the right one.",
        actions=[
            Action(name="find_employee_by_email", kwargs={"email": "mia.wilson50@company.com"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP010"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ005"}),
            Action(name="list_employee_projects", kwargs={"employee_id": "EMP010"}),
        ],
        outputs=[],
    ),

    # Task 19: Starts with email, changes to report generation
    Task(
        user_id="EMP015",
        instruction="You are William Moore, EMP015. You initially want to just email a quick update to your team. But after checking project PRJ016 details, you realize there are too many blocked tasks. Instead of a simple email, generate a formal report and email that. Title: 'PRJ016 Blocked Tasks Alert'.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP015"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ016"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # COMPLEX END-TO-END
    # =================================================================

    # Task 20: Full management workflow (8+ tool calls)
    Task(
        user_id="EMP005",
        instruction="You are Anthony Brown, EMP005 (Operations). Your weekly workflow: (1) Check PRJ008 for blocked tasks. (2) For each blocked task, update status to 'in_progress' and create a follow-up task. (3) Query this week's sales data. (4) Aggregate by product. (5) Generate a report. (6) Email the report to your manager. Complete all steps and tell me the summary.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP005"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ008"}),
            Action(name="query_sales_data", kwargs={"date_from": "2024-11-11", "date_to": "2024-11-15"}),
            Action(name="aggregate_data", kwargs={"data_ref": "latest_query", "group_by": "product", "metric": "amount", "operation": "sum"}),
        ],
        outputs=[],
    ),

    # Task 21: Executive summary from multiple sources
    Task(
        user_id="EMP001",
        instruction="Your email is liam.brown41@company.com. Prepare an executive summary: (1) Query total sales by region for November. (2) Get PRJ004 status. (3) Check upcoming calendar events this week. (4) Compile everything into a report titled 'Executive Weekly Brief - Nov 15'. (5) Email to mary.perez38@company.com (Legal head). Tell me the total November sales across all regions.",
        actions=[
            Action(name="find_employee_by_email", kwargs={"email": "liam.brown41@company.com"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP001"}),
            Action(name="query_sales_data", kwargs={"date_from": "2024-11-01", "date_to": "2024-11-15"}),
            Action(name="aggregate_data", kwargs={"data_ref": "latest_query", "group_by": "region", "metric": "amount", "operation": "sum"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ004"}),
            Action(name="get_calendar", kwargs={"employee_id": "EMP001"}),
            Action(name="generate_report", kwargs={"title": "Executive Weekly Brief - Nov 15", "data_ref": "2123fe685590", "format": "detailed", "author_id": "EMP001"}),
        ],
        outputs=[],
    ),

    # Task 22: Quarterly review preparation
    Task(
        user_id="EMP010",
        instruction="Your email is mia.wilson50@company.com. Prepare for your quarterly review: (1) Get your HR record. (2) List all your projects and their statuses. (3) Query sales data where you are the sales_rep. (4) Calculate your total sales amount. (5) Generate a self-assessment report. Tell me your performance rating and total sales.",
        actions=[
            Action(name="find_employee_by_email", kwargs={"email": "mia.wilson50@company.com"}),
            Action(name="get_employee_details", kwargs={"employee_id": "EMP010"}),
            Action(name="get_hr_record", kwargs={"employee_id": "EMP010"}),
            Action(name="list_employee_projects", kwargs={"employee_id": "EMP010"}),
            Action(name="query_sales_data", kwargs={}),
        ],
        outputs=[],
    ),

    # Task 23: Incident response workflow
    Task(
        user_id="EMP003",
        instruction="You are Wei Thompson, EMP003 (Engineering). Project PRJ001 has critical blocked tasks. (1) Get project details. (2) Find all critical and blocked tasks. (3) Create an urgent task assigned to yourself: 'Incident: Unblock PRJ001 critical path', priority critical, due today (2024-11-15). (4) Send a message to the project owner about the situation. (5) Generate an incident report.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP003"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ001"}),
            Action(name="get_current_date", kwargs={}),
        ],
        outputs=[],
    ),

    # Task 24: End-of-day wrap-up
    Task(
        user_id="EMP005",
        instruction="You are Anthony Brown, EMP005. End-of-day wrap-up: (1) Check today's calendar for any meetings you missed. (2) Check all your projects for tasks due today. (3) Update any 'in_progress' tasks that have >20 hours logged to 'done'. (4) Send a daily summary message to your manager EMP001 listing completed work. (5) Generate a daily log report.",
        actions=[
            Action(name="get_employee_details", kwargs={"employee_id": "EMP005"}),
            Action(name="get_calendar", kwargs={"employee_id": "EMP005", "date": "2024-11-15"}),
            Action(name="list_employee_projects", kwargs={"employee_id": "EMP005"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ003"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ008"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ010"}),
            Action(name="get_project_details", kwargs={"project_id": "PRJ014"}),
        ],
        outputs=[],
    ),
]
