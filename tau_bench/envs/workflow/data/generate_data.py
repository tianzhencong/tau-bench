# Copyright Sierra
# Generate office workflow data: employees, projects, databases, files
# Key difference from CRUD domains: data has cross-references that require chaining

import json
import os
import random
from datetime import datetime, timedelta

random.seed(42)
FOLDER_PATH = os.path.dirname(__file__)

FIRST_NAMES = ["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","David","Barbara",
    "William","Elizabeth","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Christopher","Karen",
    "Daniel","Nancy","Matthew","Betty","Anthony","Emily","Mark","Donna","Steven","Michelle",
    "Raj","Mei","Wei","Yuki","Omar","Sofia","Lucas","Emma","Noah","Olivia","Liam","Ava","Ethan","Mia"]
LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson",
    "White","Harris","Sanchez","Clark","Lewis","Robinson","Walker","Young","Allen","King"]

DEPARTMENTS = ["Engineering","Marketing","Sales","Finance","HR","Operations","Product","Design","Legal","Support"]

PROJECT_NAMES = [
    "Q4 Product Launch","Website Redesign","Customer Migration","Budget Review","Hiring Sprint",
    "Performance Optimization","Brand Campaign","Security Audit","Data Pipeline","Mobile App v2",
    "Annual Report","Client Onboarding","Cost Reduction","Market Research","Compliance Update",
    "Infrastructure Upgrade","Training Program","Partnership Deal","Feature Rollout","Incident Response",
]

def generate_employees(num=100):
    employees = {}
    for i in range(num):
        eid = f"EMP{i+1:03d}"
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        dept = random.choice(DEPARTMENTS)
        role = random.choice(["Manager","Senior","Lead","Associate","Director","VP"]) + " " + random.choice(["Engineer","Analyst","Specialist","Coordinator","Designer"])
        employees[eid] = {
            "employee_id": eid,
            "name": {"first_name": first, "last_name": last},
            "email": f"{first.lower()}.{last.lower()}{random.randint(10,99)}@company.com",
            "department": dept,
            "role": role,
            "manager_id": f"EMP{random.randint(1,10):03d}" if i >= 10 else None,
            "team_members": [f"EMP{random.randint(11,100):03d}" for _ in range(random.randint(2,6))],
        }
    return employees

def generate_projects(employees):
    projects = {}
    emp_ids = list(employees.keys())
    for i, name in enumerate(PROJECT_NAMES):
        pid = f"PRJ{i+1:03d}"
        owner = random.choice(emp_ids[:20])
        members = random.sample(emp_ids, random.randint(3,8))
        if owner not in members:
            members.append(owner)
        
        tasks = []
        for t in range(random.randint(5,15)):
            status = random.choice(["todo","in_progress","in_progress","done","done","done","blocked"])
            assignee = random.choice(members)
            tasks.append({
                "task_id": f"{pid}_T{t+1:02d}",
                "title": random.choice(["Implement","Design","Review","Test","Deploy","Document","Research","Analyze","Fix","Update"]) + " " + random.choice(["feature","component","module","integration","API","UI","report","config","schema","pipeline"]),
                "assignee": assignee,
                "status": status,
                "priority": random.choice(["low","medium","medium","high","high","critical"]),
                "due_date": (datetime(2024,11,15) + timedelta(days=random.randint(-10,30))).strftime("%Y-%m-%d"),
                "hours_logged": random.randint(0,40) if status in ("in_progress","done") else 0,
            })
        
        projects[pid] = {
            "project_id": pid,
            "name": name,
            "owner": owner,
            "members": members,
            "status": random.choice(["active","active","active","on_hold","completed"]),
            "budget": random.choice([10000,25000,50000,75000,100000,150000]),
            "spent": random.randint(5000,80000),
            "start_date": (datetime(2024,11,15) - timedelta(days=random.randint(30,180))).strftime("%Y-%m-%d"),
            "deadline": (datetime(2024,11,15) + timedelta(days=random.randint(15,90))).strftime("%Y-%m-%d"),
            "tasks": tasks,
        }
    return projects

def generate_sales_data():
    """Simulated sales database - agent can query this"""
    records = []
    regions = ["North","South","East","West","Central"]
    products = ["Widget A","Widget B","Service X","Service Y","Enterprise Plan","Basic Plan","Pro Plan"]
    for i in range(200):
        date = (datetime(2024,11,15) - timedelta(days=random.randint(0,90))).strftime("%Y-%m-%d")
        records.append({
            "record_id": f"SALE{i+1:04d}",
            "date": date,
            "region": random.choice(regions),
            "product": random.choice(products),
            "amount": round(random.uniform(100, 50000), 2),
            "quantity": random.randint(1, 100),
            "customer_id": f"CUST{random.randint(1,50):03d}",
            "sales_rep": f"EMP{random.randint(1,30):03d}",
        })
    return records

def generate_hr_data(employees):
    """HR records - leave requests, performance reviews"""
    records = []
    for eid, emp in employees.items():
        records.append({
            "employee_id": eid,
            "leave_balance": random.randint(0, 20),
            "leave_taken_this_year": random.randint(0, 15),
            "performance_rating": random.choice([3.0, 3.5, 4.0, 4.0, 4.5, 5.0]),
            "last_review_date": (datetime(2024,11,15) - timedelta(days=random.randint(30,180))).strftime("%Y-%m-%d"),
            "salary_band": random.choice(["L3","L4","L4","L5","L5","L6","L7"]),
        })
    return {r["employee_id"]: r for r in records}

def generate_files():
    """Shared file system"""
    files = {}
    for i in range(50):
        fid = f"FILE{i+1:03d}"
        ftype = random.choice(["spreadsheet","document","presentation","csv","pdf"])
        files[fid] = {
            "file_id": fid,
            "name": random.choice(["Q3 Report","Budget Summary","Team Roster","Meeting Notes","Project Plan","Sales Data","Org Chart","Policy Doc","Expense Report","KPI Dashboard"]) + f" {random.randint(1,5)}.{ftype[:3]}",
            "type": ftype,
            "owner": f"EMP{random.randint(1,50):03d}",
            "department": random.choice(DEPARTMENTS),
            "size_kb": random.randint(10, 5000),
            "last_modified": (datetime(2024,11,15) - timedelta(days=random.randint(0,60))).strftime("%Y-%m-%d"),
            "content_preview": f"Contains {random.choice(['financial','sales','HR','project','operational'])} data for {random.choice(['Q3','Q4','2024','November','October'])}.",
        }
    return files

def generate_calendar_events(employees):
    """Calendar events for next 2 weeks"""
    events = []
    emp_ids = list(employees.keys())
    for i in range(100):
        day_offset = random.randint(0, 14)
        date = (datetime(2024,11,15) + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        hour = random.randint(9, 16)
        attendees = random.sample(emp_ids[:30], random.randint(2,6))
        events.append({
            "event_id": f"EVT{i+1:03d}",
            "title": random.choice(["Sprint Planning","1:1","Team Standup","Design Review","Budget Meeting","All Hands","Client Call","Retrospective","Demo Day","Strategy Session"]),
            "date": date,
            "start_time": f"{hour:02d}:00",
            "end_time": f"{hour+1:02d}:00",
            "organizer": random.choice(attendees),
            "attendees": attendees,
            "location": random.choice(["Room A","Room B","Virtual","Room C","Main Hall"]),
        })
    return events

def generate_sent_messages():
    """Internal message log"""
    messages = []
    for i in range(50):
        messages.append({
            "message_id": f"MSG{i+1:03d}",
            "from": f"EMP{random.randint(1,50):03d}",
            "to": f"EMP{random.randint(1,50):03d}",
            "subject": random.choice(["Re: Project update","FYI: New policy","Action needed","Meeting recap","Quick question"]),
            "date": (datetime(2024,11,15) - timedelta(days=random.randint(0,14))).strftime("%Y-%m-%d"),
            "read": random.choice([True, True, False]),
        })
    return messages

def main():
    employees = generate_employees(100)
    projects = generate_projects(employees)
    sales_data = generate_sales_data()
    hr_data = generate_hr_data(employees)
    files = generate_files()
    calendar = generate_calendar_events(employees)
    messages = generate_sent_messages()

    data = {
        "employees": employees,
        "projects": projects,
        "sales_database": sales_data,
        "hr_records": hr_data,
        "files": files,
        "calendar_events": calendar,
        "messages": messages,
        "generated_reports": {},
        "sent_emails": [],
        "created_tasks": [],
    }
    
    with open(os.path.join(FOLDER_PATH, "workspace_data.json"), "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated: {len(employees)} employees, {len(projects)} projects, {len(sales_data)} sales records")
    print(f"  {len(hr_data)} HR records, {len(files)} files, {len(calendar)} calendar events")
    total_tasks = sum(len(p["tasks"]) for p in projects.values())
    print(f"  {total_tasks} project tasks, {len(messages)} messages")

if __name__ == "__main__":
    main()
