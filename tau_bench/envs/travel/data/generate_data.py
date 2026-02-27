# Copyright Sierra
# Generate travel agency data with composite bookings:
#   Client → Bookings → Package → Components (flight+hotel+car+activity)

import json
import os
import random
import string
import hashlib
from datetime import datetime, timedelta

random.seed(42)
FOLDER_PATH = os.path.dirname(__file__)

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Daniel", "Nancy", "Matthew", "Betty",
    "Anthony", "Emily", "Mark", "Donna", "Steven", "Michelle", "Paul", "Sandra",
    "Andrew", "Ashley", "Joshua", "Kimberly", "Kevin", "Amanda", "Brian", "Melissa",
    "Raj", "Mei", "Wei", "Yuki", "Omar", "Fatima", "Chen", "Aisha", "Sofia", "Lucas",
    "Emma", "Noah", "Olivia", "Liam", "Ava", "Ethan", "Mia", "Zara", "Hiroshi", "Priya",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter",
]

DESTINATIONS = [
    "Paris", "Tokyo", "London", "Rome", "Barcelona", "New York", "Bali",
    "Cancun", "Hawaii", "Dubai", "Sydney", "Reykjavik", "Bangkok", "Maldives",
    "Swiss Alps", "Santorini", "Costa Rica", "Marrakech", "Patagonia", "Kyoto",
]

FLIGHT_OPTIONS = {
    "economy": {"price_mod": 0, "desc": "Economy class flight"},
    "premium_economy": {"price_mod": 200, "desc": "Premium economy with extra legroom"},
    "business": {"price_mod": 600, "desc": "Business class flight"},
    "first_class": {"price_mod": 1500, "desc": "First class flight"},
}
HOTEL_OPTIONS = {
    "standard": {"price_mod": 0, "desc": "Standard room"},
    "deluxe": {"price_mod": 80, "desc": "Deluxe room with city view"},
    "suite": {"price_mod": 200, "desc": "Suite with living area"},
    "presidential": {"price_mod": 500, "desc": "Presidential suite"},
}
CAR_OPTIONS = {
    "compact": {"price_mod": 0, "desc": "Compact car"},
    "sedan": {"price_mod": 30, "desc": "Mid-size sedan"},
    "suv": {"price_mod": 60, "desc": "Full-size SUV"},
    "luxury": {"price_mod": 120, "desc": "Luxury vehicle"},
}
ACTIVITY_TYPES = [
    ("City walking tour", 50), ("Museum pass", 40), ("Food tasting tour", 75),
    ("Snorkeling excursion", 90), ("Cooking class", 65), ("Sunset cruise", 110),
    ("Hiking adventure", 55), ("Spa day", 120), ("Wine tasting", 85),
    ("Cultural show", 60), ("Zip-line adventure", 95), ("Scuba diving", 130),
    ("Hot air balloon", 200), ("Surfing lesson", 70), ("Temple tour", 45),
]

TIERS = ["standard", "standard", "standard", "silver", "silver", "gold"]
EMAIL_DOMAINS = ["email.com", "mail.com", "inbox.com"]


def det_id(prefix, seed_str):
    h = hashlib.md5(seed_str.encode()).hexdigest()[:8].upper()
    return f"{prefix}{h}"


def generate_packages(num=40):
    packages = {}
    for i in range(num):
        dest = DESTINATIONS[i % len(DESTINATIONS)]
        duration = random.choice([3, 4, 5, 7, 10, 14])
        pkg_id = f"PKG{i+1:03d}"
        base_price = random.choice([800, 1000, 1200, 1500, 1800, 2200, 2800, 3500])

        components = []
        # Every package has a flight
        comp_flight = {
            "component_id": f"{pkg_id}_F",
            "type": "flight",
            "description": f"Round-trip flight to {dest}",
            "options": {k: {"price_modifier": v["price_mod"], "description": v["desc"]}
                       for k, v in FLIGHT_OPTIONS.items()},
            "default_option": "economy",
        }
        components.append(comp_flight)

        # Every package has a hotel
        comp_hotel = {
            "component_id": f"{pkg_id}_H",
            "type": "hotel",
            "description": f"{duration}-night hotel in {dest}",
            "options": {k: {"price_modifier": v["price_mod"] * duration, "description": v["desc"]}
                       for k, v in HOTEL_OPTIONS.items()},
            "default_option": "standard",
        }
        components.append(comp_hotel)

        # 70% have car rental
        if random.random() < 0.7:
            comp_car = {
                "component_id": f"{pkg_id}_C",
                "type": "car",
                "description": f"{duration}-day car rental in {dest}",
                "options": {k: {"price_modifier": v["price_mod"] * duration, "description": v["desc"]}
                           for k, v in CAR_OPTIONS.items()},
                "default_option": "compact",
            }
            components.append(comp_car)

        # 1-2 activities
        num_activities = random.randint(1, 2)
        used = set()
        for a in range(num_activities):
            while True:
                act_name, act_price = random.choice(ACTIVITY_TYPES)
                if act_name not in used:
                    used.add(act_name)
                    break
            comp_act = {
                "component_id": f"{pkg_id}_A{a+1}",
                "type": "activity",
                "description": act_name,
                "options": {
                    "included": {"price_modifier": 0, "description": f"{act_name} (included)"},
                    "premium": {"price_modifier": act_price, "description": f"Premium {act_name} with private guide"},
                    "skip": {"price_modifier": -act_price, "description": f"Skip {act_name} (save ${act_price})"},
                },
                "default_option": "included",
            }
            components.append(comp_act)

        packages[pkg_id] = {
            "package_id": pkg_id,
            "destination": dest,
            "duration_nights": duration,
            "components": components,
            "base_price": base_price,
            "available": random.randint(3, 20),
        }
    return packages


def generate_clients(num=200, packages=None):
    clients = {}
    for i in range(num):
        cid = f"T{10000+i}"
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        dob_year = random.randint(1960, 2000)
        dob = f"{dob_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        tier = random.choice(TIERS)

        payments = []
        payments.append({
            "payment_id": f"cc_{cid}_{random.randint(1000,9999)}",
            "type": "credit_card",
            "brand": random.choice(["visa", "mastercard", "amex"]),
            "last_four": f"{random.randint(1000,9999)}",
        })
        if random.random() < 0.4:
            payments.append({
                "payment_id": f"cc2_{cid}_{random.randint(1000,9999)}",
                "type": "credit_card",
                "brand": random.choice(["visa", "mastercard"]),
                "last_four": f"{random.randint(1000,9999)}",
            })

        num_vouchers = random.randint(0, 3)
        for v in range(num_vouchers):
            payments.append({
                "payment_id": f"voucher_{cid}_{v}",
                "type": "travel_voucher",
                "amount": random.choice([100, 150, 200, 250, 300, 500, 750, 1000]),
            })

        points = random.choice([0, 0, 500, 1000, 2000, 3000, 5000, 8000, 10000, 15000])

        clients[cid] = {
            "client_id": cid,
            "name": {"first_name": first, "last_name": last},
            "email": f"{first.lower()}.{last.lower()}{random.randint(10,99)}@{random.choice(EMAIL_DOMAINS)}",
            "dob": dob,
            "phone": f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
            "tier": tier,
            "payment_methods": payments,
            "loyalty_points": points,
            "bookings": [],
        }
    return clients


def generate_bookings(clients, packages, num=400):
    bookings = {}
    client_ids = list(clients.keys())
    pkg_ids = list(packages.keys())

    for i in range(num):
        bid = f"BK{i+1:05d}"
        cid = random.choice(client_ids)
        client = clients[cid]
        pkg_id = random.choice(pkg_ids)
        pkg = packages[pkg_id]

        num_travelers = random.randint(1, 4)
        travelers = [{
            "first_name": client["name"]["first_name"],
            "last_name": client["name"]["last_name"],
            "dob": client["dob"],
        }]
        for _ in range(num_travelers - 1):
            travelers.append({
                "first_name": random.choice(FIRST_NAMES),
                "last_name": client["name"]["last_name"],
                "dob": f"{random.randint(1965,2005)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            })

        selected_options = {}
        total_modifier = 0
        for comp in pkg["components"]:
            opts = list(comp["options"].keys())
            chosen = random.choice(opts)
            selected_options[comp["component_id"]] = chosen
            total_modifier += comp["options"][chosen]["price_modifier"]

        has_protection = random.random() < 0.35
        protection_cost = 50 * num_travelers if has_protection else 0
        total_price = pkg["base_price"] + total_modifier + protection_cost

        trip_offset = random.randint(-10, 45)
        trip_start = datetime(2024, 6, 1) + timedelta(days=trip_offset)
        created_offset = random.randint(7, 60)
        created = trip_start - timedelta(days=created_offset)

        if trip_offset < 0:
            status = random.choice(["completed", "completed", "cancelled"])
        else:
            status = random.choice(["confirmed", "confirmed", "confirmed", "pending", "cancelled"])

        cc_list = [p for p in client["payment_methods"] if p["type"] == "credit_card"]
        payment_methods = []
        if cc_list:
            payment_methods.append({"payment_id": cc_list[0]["payment_id"], "amount": total_price})

        bookings[bid] = {
            "booking_id": bid,
            "client_id": cid,
            "package_id": pkg_id,
            "destination": pkg["destination"],
            "duration_nights": pkg["duration_nights"],
            "selected_options": selected_options,
            "travelers": travelers,
            "total_price": total_price,
            "payment_methods": payment_methods,
            "status": status,
            "trip_protection": has_protection,
            "trip_start_date": trip_start.strftime("%Y-%m-%d"),
            "created_at": created.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        client["bookings"].append(bid)

    return bookings


def main():
    packages = generate_packages(40)
    clients = generate_clients(200, packages)
    bookings = generate_bookings(clients, packages, 400)

    with open(os.path.join(FOLDER_PATH, "packages.json"), "w") as f:
        json.dump(packages, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "clients.json"), "w") as f:
        json.dump(clients, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "bookings.json"), "w") as f:
        json.dump(bookings, f, indent=2)

    print(f"Generated {len(packages)} packages, {len(clients)} clients, {len(bookings)} bookings")
    confirmed = sum(1 for b in bookings.values() if b["status"] == "confirmed")
    pending = sum(1 for b in bookings.values() if b["status"] == "pending")
    completed = sum(1 for b in bookings.values() if b["status"] == "completed")
    with_protection = sum(1 for b in bookings.values() if b["trip_protection"])
    avg_components = sum(len(packages[b["package_id"]]["components"]) for b in bookings.values()) / len(bookings)
    print(f"  Confirmed: {confirmed}, Pending: {pending}, Completed: {completed}")
    print(f"  With trip protection: {with_protection}")
    print(f"  Avg components per booking: {avg_components:.1f}")
    tiers = {}
    for c in clients.values():
        tiers[c["tier"]] = tiers.get(c["tier"], 0) + 1
    print(f"  Client tiers: {tiers}")
    voucher_clients = sum(1 for c in clients.values() if any(p["type"] == "travel_voucher" for p in c["payment_methods"]))
    print(f"  Clients with vouchers: {voucher_clients}")
    multi_booking = sum(1 for c in clients.values() if len(c["bookings"]) >= 3)
    print(f"  Clients with 3+ bookings: {multi_booking}")


if __name__ == "__main__":
    main()
