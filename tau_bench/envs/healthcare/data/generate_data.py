# Copyright Sierra
# Generate healthcare data with retail-like nesting:
#   Patient → Appointments → Procedure (from catalog) → Specialist → TimeSlot

import json
import os
import random
import hashlib
from datetime import datetime, timedelta

random.seed(42)
FOLDER_PATH = os.path.dirname(__file__)

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Daniel", "Nancy", "Matthew", "Betty",
    "Anthony", "Emily", "Mark", "Donna", "Steven", "Michelle", "Paul", "Sandra",
    "Andrew", "Ashley", "Kevin", "Amanda", "Brian", "Melissa", "Raj", "Mei",
    "Wei", "Yuki", "Omar", "Fatima", "Chen", "Aisha", "Sofia", "Lucas",
    "Emma", "Noah", "Olivia", "Liam", "Ava", "Ethan", "Mia", "Zara",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
    "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez",
    "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright",
    "Scott", "Torres", "Nguyen", "Hill", "Green", "Adams", "Nelson", "Baker",
    "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts", "Kim", "Chen",
]

DEPARTMENTS = ["Cardiology", "Orthopedics", "Dermatology", "Neurology", "Gastroenterology",
               "Ophthalmology", "ENT", "General Practice", "Pediatrics", "Psychiatry"]

PROCEDURES = [
    {"procedure_id": "PROC001", "name": "Annual Physical Exam", "department": "General Practice", "duration_minutes": 30, "base_cost": 150, "requires_referral": False},
    {"procedure_id": "PROC002", "name": "Blood Work Panel", "department": "General Practice", "duration_minutes": 15, "base_cost": 80, "requires_referral": False},
    {"procedure_id": "PROC003", "name": "Cardiology Consultation", "department": "Cardiology", "duration_minutes": 45, "base_cost": 300, "requires_referral": True},
    {"procedure_id": "PROC004", "name": "Echocardiogram", "department": "Cardiology", "duration_minutes": 60, "base_cost": 500, "requires_referral": True},
    {"procedure_id": "PROC005", "name": "Stress Test", "department": "Cardiology", "duration_minutes": 90, "base_cost": 750, "requires_referral": True},
    {"procedure_id": "PROC006", "name": "Knee X-Ray", "department": "Orthopedics", "duration_minutes": 30, "base_cost": 200, "requires_referral": False},
    {"procedure_id": "PROC007", "name": "MRI Scan", "department": "Orthopedics", "duration_minutes": 60, "base_cost": 800, "requires_referral": True},
    {"procedure_id": "PROC008", "name": "Physical Therapy Session", "department": "Orthopedics", "duration_minutes": 45, "base_cost": 120, "requires_referral": True},
    {"procedure_id": "PROC009", "name": "Skin Cancer Screening", "department": "Dermatology", "duration_minutes": 30, "base_cost": 180, "requires_referral": False},
    {"procedure_id": "PROC010", "name": "Dermatology Consultation", "department": "Dermatology", "duration_minutes": 30, "base_cost": 200, "requires_referral": False},
    {"procedure_id": "PROC011", "name": "Neurology Consultation", "department": "Neurology", "duration_minutes": 45, "base_cost": 350, "requires_referral": True},
    {"procedure_id": "PROC012", "name": "EEG Test", "department": "Neurology", "duration_minutes": 60, "base_cost": 600, "requires_referral": True},
    {"procedure_id": "PROC013", "name": "Colonoscopy", "department": "Gastroenterology", "duration_minutes": 90, "base_cost": 1200, "requires_referral": True},
    {"procedure_id": "PROC014", "name": "GI Consultation", "department": "Gastroenterology", "duration_minutes": 30, "base_cost": 250, "requires_referral": True},
    {"procedure_id": "PROC015", "name": "Eye Exam", "department": "Ophthalmology", "duration_minutes": 30, "base_cost": 120, "requires_referral": False},
    {"procedure_id": "PROC016", "name": "LASIK Consultation", "department": "Ophthalmology", "duration_minutes": 45, "base_cost": 400, "requires_referral": True},
    {"procedure_id": "PROC017", "name": "Hearing Test", "department": "ENT", "duration_minutes": 30, "base_cost": 150, "requires_referral": False},
    {"procedure_id": "PROC018", "name": "Sinus Surgery Consultation", "department": "ENT", "duration_minutes": 45, "base_cost": 350, "requires_referral": True},
    {"procedure_id": "PROC019", "name": "Well-Child Visit", "department": "Pediatrics", "duration_minutes": 30, "base_cost": 130, "requires_referral": False},
    {"procedure_id": "PROC020", "name": "Psychiatric Evaluation", "department": "Psychiatry", "duration_minutes": 60, "base_cost": 300, "requires_referral": True},
]

SPECIALIST_FIRST = ["Robert", "Sarah", "James", "Emily", "David", "Lisa", "Michael", "Jennifer", "Chen", "Raj", "Yuki", "Maria", "Omar", "Priya", "William"]
SPECIALIST_LAST = ["Chen", "Patel", "Kim", "Smith", "Johnson", "Garcia", "Williams", "Brown", "Lee", "Wilson", "Anderson", "Taylor", "Martinez", "Thomas", "Moore"]

INSURANCE_PLANS = ["basic", "basic", "standard", "standard", "standard", "premium", "premium"]
EMAIL_DOMAINS = ["email.com", "mail.com", "inbox.com"]


def generate_procedures():
    return {p["procedure_id"]: p for p in PROCEDURES}


def generate_specialists(procedures):
    specialists = {}
    dept_procs = {}
    for p in procedures.values():
        dept_procs.setdefault(p["department"], []).append(p["procedure_id"])

    sid = 0
    for dept in DEPARTMENTS:
        num = random.randint(3, 5)
        for _ in range(num):
            spec_id = f"DR{sid+1:03d}"
            sid += 1
            name = f"Dr. {random.choice(SPECIALIST_FIRST)} {random.choice(SPECIALIST_LAST)}"
            slots = []
            for day_offset in range(1, 30):
                date = (datetime(2024, 9, 15) + timedelta(days=day_offset)).strftime("%Y-%m-%d")
                num_slots = random.randint(3, 6)
                hours = sorted(random.sample(range(8, 17), num_slots))
                for h in hours:
                    slots.append({
                        "date": date,
                        "start_time": f"{h:02d}:00",
                        "end_time": f"{h:02d}:45",
                        "available": random.random() > 0.3,
                    })
            specialists[spec_id] = {
                "specialist_id": spec_id,
                "name": name,
                "department": dept,
                "procedures": dept_procs.get(dept, []),
                "available_slots": slots,
            }
    return specialists


def generate_patients(num=200, procedures=None, specialists=None):
    patients = {}
    proc_ids = list(procedures.keys())

    for i in range(num):
        pid = f"P{10000+i}"
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        dob = f"{random.randint(1955,2005)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        plan = random.choice(INSURANCE_PLANS)

        payments = [{
            "payment_id": f"cc_{pid}_{random.randint(1000,9999)}",
            "type": "credit_card",
            "last_four": f"{random.randint(1000,9999)}",
        }]
        hsa_bal = random.choice([0, 0, 200, 500, 1000, 1500, 2000])
        if hsa_bal > 0:
            payments.append({
                "payment_id": f"hsa_{pid}",
                "type": "hsa",
                "balance": hsa_bal,
            })

        deductible_met = random.choice([0, 0, 200, 500, 800, 1000, 1500, 2000])
        medical_history = random.sample(proc_ids, random.randint(0, 6))

        referrals = []
        if random.random() < 0.5:
            ref_procs = [p for p in proc_ids if procedures[p]["requires_referral"]]
            for rp in random.sample(ref_procs, min(random.randint(1, 3), len(ref_procs))):
                referrals.append({
                    "referral_id": f"REF_{pid}_{rp}",
                    "procedure_id": rp,
                    "valid_until": "2024-12-31",
                })

        pcp_dept_specs = [s for s in specialists.values() if s["department"] == "General Practice"]
        pcp = random.choice(pcp_dept_specs)["specialist_id"] if pcp_dept_specs else "DR001"

        dependents = []
        if random.random() < 0.3:
            num_dep = random.randint(1, 2)
            for d in range(num_dep):
                dependents.append({
                    "name": {"first_name": random.choice(FIRST_NAMES), "last_name": last},
                    "dob": f"{random.randint(2008,2020)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                    "relationship": random.choice(["child", "spouse"]),
                })

        patients[pid] = {
            "patient_id": pid,
            "name": {"first_name": first, "last_name": last},
            "email": f"{first.lower()}.{last.lower()}{random.randint(10,99)}@{random.choice(EMAIL_DOMAINS)}",
            "dob": dob,
            "phone": f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
            "insurance_plan": plan,
            "payment_methods": payments,
            "deductible_met_this_year": deductible_met,
            "primary_care_doctor": pcp,
            "medical_history": medical_history,
            "referrals": referrals,
            "dependents": dependents,
            "appointments": [],
        }
    return patients


def generate_appointments(patients, procedures, specialists, num=400):
    appointments = {}
    patient_ids = list(patients.keys())
    proc_ids = list(procedures.keys())

    for i in range(num):
        appt_id = f"APT{i+1:05d}"
        pid = random.choice(patient_ids)
        patient = patients[pid]
        proc_id = random.choice(proc_ids)
        proc = procedures[proc_id]

        dept_specs = [s for s in specialists.values() if s["department"] == proc["department"]]
        spec = random.choice(dept_specs)

        day_offset = random.randint(-10, 28)
        date = (datetime(2024, 9, 15) + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        hour = random.randint(8, 16)
        start = f"{hour:02d}:00"
        end_min = hour * 60 + proc["duration_minutes"]
        end = f"{end_min // 60:02d}:{end_min % 60:02d}"

        if day_offset < 0:
            status = random.choice(["completed", "completed", "no_show"])
        else:
            status = random.choice(["scheduled", "scheduled", "scheduled", "cancelled"])

        plan = patient["insurance_plan"]
        copay = {"basic": 40, "standard": 25, "premium": 10}[plan]
        coverage = {"basic": 0.6, "standard": 0.8, "premium": 0.9}[plan]
        base_cost = proc["base_cost"]
        insurance_covered = round(coverage * max(0, base_cost - copay), 2)
        total_cost = round(base_cost - insurance_covered, 2)

        ref_id = None
        if proc["requires_referral"]:
            matching = [r for r in patient["referrals"] if r["procedure_id"] == proc_id]
            ref_id = matching[0]["referral_id"] if matching else None

        cc = [p for p in patient["payment_methods"] if p["type"] == "credit_card"]
        payment_method = cc[0]["payment_id"] if cc else None

        appointments[appt_id] = {
            "appointment_id": appt_id,
            "patient_id": pid,
            "procedure_id": proc_id,
            "procedure_name": proc["name"],
            "specialist_id": spec["specialist_id"],
            "specialist_name": spec["name"],
            "department": proc["department"],
            "date": date,
            "start_time": start,
            "end_time": end,
            "status": status,
            "copay_amount": copay,
            "insurance_covered": insurance_covered,
            "total_cost": total_cost,
            "payment_method": payment_method,
            "referral_id": ref_id,
            "created_at": (datetime(2024, 9, 15) - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%dT%H:%M:%S"),
        }
        patient["appointments"].append(appt_id)

    return appointments


def main():
    procedures = generate_procedures()
    specialists = generate_specialists(procedures)
    patients = generate_patients(200, procedures, specialists)
    appointments = generate_appointments(patients, procedures, specialists, 400)

    with open(os.path.join(FOLDER_PATH, "procedures.json"), "w") as f:
        json.dump(procedures, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "specialists.json"), "w") as f:
        json.dump(specialists, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "patients.json"), "w") as f:
        json.dump(patients, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "appointments.json"), "w") as f:
        json.dump(appointments, f, indent=2)

    print(f"Generated {len(procedures)} procedures, {len(specialists)} specialists, {len(patients)} patients, {len(appointments)} appointments")
    scheduled = sum(1 for a in appointments.values() if a["status"] == "scheduled")
    completed = sum(1 for a in appointments.values() if a["status"] == "completed")
    with_referral = sum(1 for a in appointments.values() if a["referral_id"])
    plans = {}
    for p in patients.values():
        plans[p["insurance_plan"]] = plans.get(p["insurance_plan"], 0) + 1
    print(f"  Scheduled: {scheduled}, Completed: {completed}, With referral: {with_referral}")
    print(f"  Plans: {plans}")
    with_deps = sum(1 for p in patients.values() if p["dependents"])
    with_refs = sum(1 for p in patients.values() if p["referrals"])
    with_hsa = sum(1 for p in patients.values() if any(pm["type"] == "hsa" for pm in p["payment_methods"]))
    multi_appt = sum(1 for p in patients.values() if len(p["appointments"]) >= 3)
    print(f"  With dependents: {with_deps}, With referrals: {with_refs}, With HSA: {with_hsa}")
    print(f"  Patients with 3+ appointments: {multi_appt}")


if __name__ == "__main__":
    main()
