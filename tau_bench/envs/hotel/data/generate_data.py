# Copyright Sierra
# Script to generate synthetic hotel booking data for tau-bench

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
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Timothy", "Deborah", "Raj", "Mei", "Wei", "Yuki", "Omar", "Fatima", "Chen",
    "Aisha", "Hiroshi", "Priya", "Akira", "Sana", "Ravi", "Yara", "Diego",
    "Sofia", "Lucas", "Emma", "Noah", "Olivia", "Liam", "Ava", "Ethan", "Mia",
    "Aarav", "Zara", "Ivan", "Elena", "Hassan", "Leila", "Kenji", "Sakura",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Kim", "Chen", "Patel", "Singh", "Li", "Wang", "Zhang",
    "Liu", "Muller", "Schmidt", "Fischer", "Weber", "Rossi", "Russo", "Ferrari",
    "Silva", "Santos", "Costa", "Tanaka", "Yamamoto", "Suzuki", "Sato", "Khan",
]

CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "San Francisco", "Seattle", "Miami", "Boston", "Denver",
    "San Diego", "Dallas", "Atlanta", "Las Vegas", "Orlando",
]

HOTEL_PREFIXES = [
    "Grand", "Royal", "Sunset", "Harbor", "Mountain", "Ocean", "City",
    "Park", "River", "Lake", "Crystal", "Golden", "Silver", "Diamond",
    "Pearl", "Emerald", "Sapphire", "Ruby", "Amber", "Ivory",
]

HOTEL_SUFFIXES = [
    "Hotel", "Inn", "Resort", "Suites", "Lodge", "Plaza", "Tower",
    "Palace", "Gardens", "Boutique Hotel",
]

ROOM_TYPES = {
    "standard": {"max_occupancy": 2, "base_rate_range": (80, 150)},
    "deluxe": {"max_occupancy": 3, "base_rate_range": (150, 280)},
    "suite": {"max_occupancy": 4, "base_rate_range": (280, 500)},
    "presidential_suite": {"max_occupancy": 4, "base_rate_range": (500, 1200)},
}

MEMBERSHIP_TIERS = ["regular", "regular", "regular", "silver", "silver", "gold", "platinum"]

EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com"]


def gen_email(first, last, uid_num):
    domain = random.choice(EMAIL_DOMAINS)
    return f"{first.lower()}.{last.lower()}{uid_num}@{domain}"


def gen_dob():
    year = random.randint(1955, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def gen_payment_methods():
    methods = []
    num_cc = random.randint(1, 3)
    for i in range(num_cc):
        last4 = "".join(random.choices(string.digits, k=4))
        methods.append({
            "payment_id": f"credit_card_{random.randint(1000000, 9999999)}",
            "type": "credit_card",
            "brand": random.choice(["visa", "mastercard", "amex"]),
            "last_four": last4,
        })
    num_gc = random.randint(0, 3)
    for i in range(num_gc):
        methods.append({
            "payment_id": f"gift_card_{random.randint(1000000, 9999999)}",
            "type": "gift_card",
            "balance": random.choice([25, 50, 75, 100, 150, 200, 250, 300, 500]),
        })
    return methods


def generate_hotels(num_hotels=30):
    hotels = {}
    used_names = set()
    for i in range(num_hotels):
        city = CITIES[i % len(CITIES)]
        while True:
            name = f"{random.choice(HOTEL_PREFIXES)} {random.choice(HOTEL_SUFFIXES)}"
            if name not in used_names:
                used_names.add(name)
                break
        hotel_id = f"hotel_{i+1:03d}"
        star = random.choice([3, 3, 4, 4, 4, 5, 5])
        star_mult = {3: 0.7, 4: 1.0, 5: 1.5}[star]

        rooms = {}
        for rt, info in ROOM_TYPES.items():
            low, high = info["base_rate_range"]
            rate = int(random.randint(low, high) * star_mult)
            rooms[rt] = {
                "nightly_rate": rate,
                "max_occupancy": info["max_occupancy"],
                "available": random.randint(2, 15),
                "amenities": _room_amenities(rt),
            }

        hotels[hotel_id] = {
            "hotel_id": hotel_id,
            "name": name,
            "city": city,
            "star_rating": star,
            "address": f"{random.randint(1, 999)} {random.choice(['Main', 'Broadway', 'Park', 'Ocean', 'Lake', 'Elm', 'Oak', 'Pine', 'Cedar', 'Maple'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr', 'Rd'])}",
            "rooms": rooms,
        }
    return hotels


def _room_amenities(room_type):
    base = ["wifi", "tv", "air_conditioning"]
    if room_type == "deluxe":
        base += ["mini_bar", "city_view"]
    elif room_type == "suite":
        base += ["mini_bar", "city_view", "living_room", "bathtub"]
    elif room_type == "presidential_suite":
        base += ["mini_bar", "panoramic_view", "living_room", "bathtub", "kitchen", "butler_service"]
    return base


def generate_users(num_users=200, hotels=None):
    users = {}
    for i in range(num_users):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        uid_num = random.randint(1000, 9999)
        user_id = f"{first.lower()}_{last.lower()}_{uid_num}"
        while user_id in users:
            uid_num = random.randint(1000, 9999)
            user_id = f"{first.lower()}_{last.lower()}_{uid_num}"

        users[user_id] = {
            "user_id": user_id,
            "name": {"first_name": first, "last_name": last},
            "email": gen_email(first, last, uid_num),
            "dob": gen_dob(),
            "phone": f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
            "membership": random.choice(MEMBERSHIP_TIERS),
            "payment_methods": gen_payment_methods(),
            "reservations": [],
            "address": {
                "street": f"{random.randint(1, 9999)} {random.choice(['Oak', 'Main', 'Elm', 'Park', 'Lake'])} {random.choice(['St', 'Ave', 'Rd'])}",
                "city": random.choice(CITIES),
                "state": random.choice(["NY", "CA", "IL", "TX", "FL", "WA", "MA", "CO"]),
                "zip": f"{random.randint(10000, 99999)}",
            },
        }
    return users


def generate_reservations(users, hotels, num_reservations=500):
    reservations = {}
    user_ids = list(users.keys())
    hotel_ids = list(hotels.keys())

    for i in range(num_reservations):
        res_id = "RES" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while res_id in reservations:
            res_id = "RES" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

        user_id = random.choice(user_ids)
        user = users[user_id]
        hotel_id = random.choice(hotel_ids)
        hotel = hotels[hotel_id]

        room_type = random.choice(list(hotel["rooms"].keys()))
        room_info = hotel["rooms"][room_type]
        max_occ = room_info["max_occupancy"]

        ci_offset = random.randint(-5, 30)
        ci_date = datetime(2024, 5, 15) + timedelta(days=ci_offset)
        nights = random.randint(1, 7)
        co_date = ci_date + timedelta(days=nights)

        num_guests = random.randint(1, min(max_occ, 3))
        guests = [
            {
                "first_name": user["name"]["first_name"],
                "last_name": user["name"]["last_name"],
                "dob": user["dob"],
            }
        ]
        for _ in range(num_guests - 1):
            guests.append({
                "first_name": random.choice(FIRST_NAMES),
                "last_name": user["name"]["last_name"],
                "dob": gen_dob(),
            })

        room_cost = room_info["nightly_rate"] * nights

        services = []
        service_cost = 0
        if random.random() < 0.4:
            services.append("breakfast")
            service_cost += 25 * nights * num_guests
        if random.random() < 0.3:
            services.append("parking")
            service_cost += 20 * nights
        if random.random() < 0.15:
            services.append("spa")
            service_cost += 50 * num_guests
        if random.random() < 0.1:
            services.append("late_checkout")
            service_cost += 30
        if random.random() < 0.08 and user["membership"] in ["silver", "gold", "platinum"]:
            services.append("early_checkin")
            service_cost += 30

        has_insurance = random.random() < 0.3
        insurance_cost = 40 if has_insurance else 0
        total = room_cost + service_cost + insurance_cost

        rate_type = random.choice(["refundable", "refundable", "refundable", "non_refundable"])

        if ci_offset < 0:
            status = random.choice(["checked_in", "checked_out", "checked_out"])
        elif ci_offset == 0:
            status = random.choice(["confirmed", "checked_in"])
        else:
            status = "confirmed"

        if random.random() < 0.05:
            status = "cancelled"

        created_offset = random.randint(1, 30)
        created_at = ci_date - timedelta(days=created_offset)

        payment_methods = []
        user_cc = [p for p in user["payment_methods"] if p["type"] == "credit_card"]
        if user_cc:
            cc = random.choice(user_cc)
            payment_methods.append({"payment_id": cc["payment_id"], "amount": total})

        reservations[res_id] = {
            "reservation_id": res_id,
            "user_id": user_id,
            "hotel_id": hotel_id,
            "room_type": room_type,
            "check_in_date": ci_date.strftime("%Y-%m-%d"),
            "check_out_date": co_date.strftime("%Y-%m-%d"),
            "guests": guests,
            "payment_methods": payment_methods,
            "services": services,
            "cancellation_insurance": has_insurance,
            "status": status,
            "created_at": created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "rate_type": rate_type,
            "room_cost": room_cost,
            "service_cost": service_cost,
            "insurance_cost": insurance_cost,
            "total_price": total,
        }

        user["reservations"].append(res_id)

    return reservations


def main():
    hotels = generate_hotels(30)
    users = generate_users(200, hotels)
    reservations = generate_reservations(users, hotels, 500)

    with open(os.path.join(FOLDER_PATH, "hotels.json"), "w") as f:
        json.dump(hotels, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "users.json"), "w") as f:
        json.dump(users, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "reservations.json"), "w") as f:
        json.dump(reservations, f, indent=2)

    print(f"Generated {len(hotels)} hotels, {len(users)} users, {len(reservations)} reservations")

    confirmed = sum(1 for r in reservations.values() if r["status"] == "confirmed")
    with_insurance = sum(1 for r in reservations.values() if r["cancellation_insurance"])
    non_refundable = sum(1 for r in reservations.values() if r["rate_type"] == "non_refundable")
    print(f"  Confirmed: {confirmed}, With insurance: {with_insurance}, Non-refundable: {non_refundable}")

    membership_counts = {}
    for u in users.values():
        m = u["membership"]
        membership_counts[m] = membership_counts.get(m, 0) + 1
    print(f"  Memberships: {membership_counts}")


if __name__ == "__main__":
    main()
