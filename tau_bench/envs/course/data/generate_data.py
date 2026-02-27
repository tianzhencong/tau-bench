# Copyright Sierra
# Generate synthetic course registration data with retail-like nesting:
#   Student → Registrations → Courses (with section_ids) → Course Catalog → Sections

import json
import os
import random
import string
from datetime import datetime, timedelta

random.seed(42)
FOLDER_PATH = os.path.dirname(__file__)

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Daniel", "Nancy", "Matthew", "Betty",
    "Anthony", "Emily", "Mark", "Donna", "Steven", "Michelle", "Paul", "Sandra",
    "Andrew", "Ashley", "Joshua", "Kimberly", "Kevin", "Amanda", "Brian", "Melissa",
    "Raj", "Mei", "Wei", "Yuki", "Omar", "Fatima", "Chen", "Aisha", "Hiroshi", "Priya",
    "Sofia", "Lucas", "Emma", "Noah", "Olivia", "Liam", "Ava", "Ethan", "Mia", "Zara",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Kim", "Chen", "Patel", "Singh", "Li", "Wang", "Zhang",
]

DEPARTMENTS = [
    "Computer Science", "Mathematics", "Physics", "Chemistry", "Biology",
    "English", "History", "Psychology", "Economics", "Business",
    "Art", "Music", "Philosophy", "Sociology", "Political Science",
    "Engineering", "Statistics", "Linguistics", "Nursing", "Education",
]

DEPT_CODES = {
    "Computer Science": "CS", "Mathematics": "MATH", "Physics": "PHYS",
    "Chemistry": "CHEM", "Biology": "BIO", "English": "ENG", "History": "HIST",
    "Psychology": "PSYC", "Economics": "ECON", "Business": "BUS",
    "Art": "ART", "Music": "MUS", "Philosophy": "PHIL", "Sociology": "SOC",
    "Political Science": "POLS", "Engineering": "ENGR", "Statistics": "STAT",
    "Linguistics": "LING", "Nursing": "NURS", "Education": "EDUC",
}

COURSE_NAMES = {
    "CS": ["Intro to Programming", "Data Structures", "Algorithms", "Databases", "Operating Systems", "Machine Learning"],
    "MATH": ["Calculus I", "Calculus II", "Linear Algebra", "Differential Equations", "Probability"],
    "PHYS": ["Mechanics", "Electricity & Magnetism", "Quantum Physics"],
    "CHEM": ["General Chemistry", "Organic Chemistry", "Biochemistry"],
    "BIO": ["Cell Biology", "Genetics", "Ecology"],
    "ENG": ["English Composition", "American Literature", "Creative Writing"],
    "HIST": ["World History", "US History", "Modern Europe"],
    "PSYC": ["Intro to Psychology", "Cognitive Psychology", "Social Psychology"],
    "ECON": ["Microeconomics", "Macroeconomics"],
    "BUS": ["Principles of Management", "Marketing", "Accounting"],
    "ART": ["Drawing Fundamentals", "Art History"],
    "MUS": ["Music Theory", "Music History"],
    "PHIL": ["Intro to Philosophy", "Ethics"],
    "SOC": ["Intro to Sociology"],
    "POLS": ["American Government", "International Relations"],
    "ENGR": ["Engineering Design", "Thermodynamics"],
    "STAT": ["Intro to Statistics", "Regression Analysis"],
    "LING": ["Intro to Linguistics"],
    "NURS": ["Fundamentals of Nursing"],
    "EDUC": ["Educational Psychology"],
}

INSTRUCTOR_FIRST = ["Robert", "Sarah", "James", "Emily", "David", "Lisa", "Michael", "Jennifer", "William", "Maria", "Chen", "Raj", "Yuki", "Omar", "Priya"]
INSTRUCTOR_LAST = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Chen", "Patel", "Kim", "Lee", "Wilson", "Taylor", "Anderson", "Thomas", "Martinez"]

DAYS_PATTERNS = ["MWF", "TTh", "MW", "MWF", "TTh", "MW", "F"]
TIME_SLOTS = [
    ("08:00", "08:50"), ("09:00", "09:50"), ("10:00", "10:50"), ("11:00", "11:50"),
    ("12:00", "12:50"), ("13:00", "13:50"), ("14:00", "14:50"), ("15:00", "15:50"),
    ("16:00", "16:50"),
    ("08:00", "09:15"), ("09:30", "10:45"), ("10:30", "11:45"),
    ("13:00", "14:15"), ("14:30", "15:45"), ("16:00", "17:15"),
]

BUILDINGS = ["Science", "Liberal Arts", "Engineering", "Business", "Health Sciences", "Fine Arts", "Main Hall", "Technology"]
LEVELS = ["freshman", "sophomore", "junior", "senior"]
EMAIL_DOMAINS = ["university.edu", "student.edu", "campus.edu"]


def generate_courses(num_courses=50):
    courses = {}
    course_list = []
    for dept, names in COURSE_NAMES.items():
        for i, name in enumerate(names):
            num = (i + 1) * 100 + random.choice([0, 1, 2]) * 10 + random.randint(0, 1)
            course_id = f"{dept}{num}"
            course_list.append((course_id, dept, name))

    random.shuffle(course_list)
    course_list = course_list[:num_courses]

    existing_ids = set()
    for course_id, dept_code, name in course_list:
        dept = [d for d, c in DEPT_CODES.items() if c == dept_code][0]
        credits = random.choice([3, 3, 3, 4, 4])

        prereqs = []
        course_num_str = course_id[len(dept_code):]
        if course_num_str and course_num_str[0].isdigit() and int(course_num_str[0]) >= 2:
            possible = [c for c in existing_ids if c.startswith(dept_code) and c[len(dept_code):][0].isdigit() and int(c[len(dept_code):][0]) < 2]
            if possible:
                prereqs = [random.choice(possible)]

        num_sections = random.randint(2, 5)
        sections = {}
        used_slots = set()
        for s in range(num_sections):
            section_id = f"{course_id}-{s+1:03d}"
            days = random.choice(DAYS_PATTERNS)
            while True:
                time_slot = random.choice(TIME_SLOTS)
                slot_key = (days, time_slot)
                if slot_key not in used_slots:
                    used_slots.add(slot_key)
                    break

            instructor = f"Dr. {random.choice(INSTRUCTOR_FIRST)} {random.choice(INSTRUCTOR_LAST)}"
            room = f"{random.choice(BUILDINGS)} {random.randint(100, 499)}"
            capacity = random.choice([25, 30, 35, 40, 50])
            enrolled = random.randint(max(0, capacity - 15), capacity)
            tuition_per_credit = random.choice([150, 150, 175, 200, 200, 225, 250])

            sections[section_id] = {
                "section_id": section_id,
                "instructor": instructor,
                "days": days,
                "start_time": time_slot[0],
                "end_time": time_slot[1],
                "room": room,
                "capacity": capacity,
                "enrolled": enrolled,
                "available": enrolled < capacity,
                "tuition_per_credit": tuition_per_credit,
            }

        courses[course_id] = {
            "course_id": course_id,
            "name": name,
            "department": dept,
            "credits": credits,
            "prerequisites": prereqs,
            "sections": sections,
        }
        existing_ids.add(course_id)

    return courses


def generate_students(num_students=200, courses=None):
    students = {}
    for i in range(num_students):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        sid = f"S{10000 + i}"
        dob_year = random.randint(1998, 2006)
        dob = f"{dob_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        level = random.choice(LEVELS)
        major_dept = random.choice(DEPARTMENTS)

        payment_methods = []
        payment_methods.append({
            "payment_id": f"credit_card_{random.randint(1000000, 9999999)}",
            "type": "credit_card",
            "brand": random.choice(["visa", "mastercard"]),
            "last_four": f"{random.randint(1000, 9999)}",
        })
        payment_methods.append({
            "payment_id": f"student_account_{sid}",
            "type": "student_account",
            "balance": random.choice([0, 0, 500, 1000, 1500, 2000, 3000, 5000]),
        })
        if random.random() < 0.4:
            payment_methods.append({
                "payment_id": f"financial_aid_{random.randint(100000, 999999)}",
                "type": "financial_aid",
                "balance": random.choice([2000, 3000, 4000, 5000, 8000]),
            })

        completed_courses = []
        if level in ("sophomore", "junior", "senior"):
            available = list(courses.keys())
            num_completed = {"sophomore": random.randint(3, 6), "junior": random.randint(6, 10), "senior": random.randint(8, 14)}.get(level, 0)
            completed_courses = random.sample(available, min(num_completed, len(available)))

        email = f"{first.lower()}.{last.lower()}{random.randint(10,99)}@{random.choice(EMAIL_DOMAINS)}"
        students[sid] = {
            "student_id": sid,
            "name": {"first_name": first, "last_name": last},
            "email": email,
            "dob": dob,
            "major": major_dept,
            "level": level,
            "payment_methods": payment_methods,
            "completed_courses": completed_courses,
            "registrations": [],
        }
    return students


def time_overlap(s1, e1, s2, e2):
    return s1 < e2 and s2 < e1


def generate_registrations(students, courses, num_registrations=500):
    registrations = {}
    student_ids = list(students.keys())
    course_ids = list(courses.keys())

    for i in range(num_registrations):
        reg_id = "REG" + "".join(random.choices(string.ascii_uppercase + string.digits, k=7))
        while reg_id in registrations:
            reg_id = "REG" + "".join(random.choices(string.ascii_uppercase + string.digits, k=7))

        sid = random.choice(student_ids)
        student = students[sid]
        num_courses = random.randint(2, 5)
        selected = random.sample(course_ids, min(num_courses, len(course_ids)))

        enrolled_courses = []
        for cid in selected:
            course = courses[cid]
            available_sections = [s for s in course["sections"].values() if s["enrolled"] < s["capacity"]]
            if not available_sections:
                available_sections = list(course["sections"].values())
            section = random.choice(available_sections)
            tuition = section["tuition_per_credit"] * course["credits"]
            enrolled_courses.append({
                "course_id": cid,
                "course_name": course["name"],
                "section_id": section["section_id"],
                "credits": course["credits"],
                "tuition": tuition,
                "instructor": section["instructor"],
                "days": section["days"],
                "start_time": section["start_time"],
                "end_time": section["end_time"],
                "room": section["room"],
            })

        total_credits = sum(c["credits"] for c in enrolled_courses)
        total_tuition = sum(c["tuition"] for c in enrolled_courses)

        semester = random.choice(["Fall 2024", "Fall 2024", "Fall 2024", "Spring 2024"])
        if semester == "Spring 2024":
            status = random.choice(["completed", "completed", "cancelled"])
        else:
            status = random.choice(["confirmed", "confirmed", "confirmed", "pending", "cancelled"])

        created_days_ago = random.randint(1, 60)
        created = datetime(2024, 8, 15) - timedelta(days=created_days_ago)

        cc = [p for p in student["payment_methods"] if p["type"] == "credit_card"]
        payment_history = []
        if cc and status != "cancelled":
            payment_history.append({
                "transaction_type": "payment",
                "amount": total_tuition,
                "payment_method_id": cc[0]["payment_id"],
            })

        registrations[reg_id] = {
            "registration_id": reg_id,
            "student_id": sid,
            "semester": semester,
            "courses": enrolled_courses,
            "status": status,
            "total_credits": total_credits,
            "total_tuition": total_tuition,
            "payment_history": payment_history,
            "created_at": created.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        student["registrations"].append(reg_id)

    return registrations


def main():
    courses = generate_courses(50)
    students = generate_students(200, courses)
    registrations = generate_registrations(students, courses, 500)

    with open(os.path.join(FOLDER_PATH, "courses.json"), "w") as f:
        json.dump(courses, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "students.json"), "w") as f:
        json.dump(students, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "registrations.json"), "w") as f:
        json.dump(registrations, f, indent=2)

    print(f"Generated {len(courses)} courses, {len(students)} students, {len(registrations)} registrations")
    confirmed = sum(1 for r in registrations.values() if r["status"] == "confirmed")
    pending = sum(1 for r in registrations.values() if r["status"] == "pending")
    completed = sum(1 for r in registrations.values() if r["status"] == "completed")
    avg_courses = sum(len(r["courses"]) for r in registrations.values()) / len(registrations)
    total_sections = sum(len(c["sections"]) for c in courses.values())
    print(f"  Sections: {total_sections}, Confirmed: {confirmed}, Pending: {pending}, Completed: {completed}")
    print(f"  Avg courses per registration: {avg_courses:.1f}")
    levels = {}
    for s in students.values():
        levels[s["level"]] = levels.get(s["level"], 0) + 1
    print(f"  Student levels: {levels}")


if __name__ == "__main__":
    main()
