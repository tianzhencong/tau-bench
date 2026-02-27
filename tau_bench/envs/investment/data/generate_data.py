# Copyright Sierra
# Generate investment portfolio data with 4-level nesting:
#   Client → Accounts → Holdings (with holding_ids) → Securities (with prices/lots)

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
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter",
    "Roberts", "Kim", "Chen", "Patel", "Singh", "Li", "Wang", "Zhang",
]

SECURITIES = [
    {"security_id": "AAPL", "name": "Apple Inc.", "type": "stock", "sector": "Technology", "current_price": 178.50},
    {"security_id": "MSFT", "name": "Microsoft Corp.", "type": "stock", "sector": "Technology", "current_price": 374.20},
    {"security_id": "GOOGL", "name": "Alphabet Inc.", "type": "stock", "sector": "Technology", "current_price": 141.80},
    {"security_id": "AMZN", "name": "Amazon.com Inc.", "type": "stock", "sector": "Technology", "current_price": 186.50},
    {"security_id": "NVDA", "name": "NVIDIA Corp.", "type": "stock", "sector": "Technology", "current_price": 484.00},
    {"security_id": "TSLA", "name": "Tesla Inc.", "type": "stock", "sector": "Automotive", "current_price": 255.70},
    {"security_id": "JPM", "name": "JPMorgan Chase", "type": "stock", "sector": "Finance", "current_price": 150.30},
    {"security_id": "V", "name": "Visa Inc.", "type": "stock", "sector": "Finance", "current_price": 260.40},
    {"security_id": "JNJ", "name": "Johnson & Johnson", "type": "stock", "sector": "Healthcare", "current_price": 156.80},
    {"security_id": "PG", "name": "Procter & Gamble", "type": "stock", "sector": "Consumer", "current_price": 153.20},
    {"security_id": "UNH", "name": "UnitedHealth Group", "type": "stock", "sector": "Healthcare", "current_price": 545.60},
    {"security_id": "MA", "name": "Mastercard Inc.", "type": "stock", "sector": "Finance", "current_price": 412.30},
    {"security_id": "DIS", "name": "Walt Disney Co.", "type": "stock", "sector": "Entertainment", "current_price": 84.50},
    {"security_id": "NFLX", "name": "Netflix Inc.", "type": "stock", "sector": "Entertainment", "current_price": 485.20},
    {"security_id": "KO", "name": "Coca-Cola Co.", "type": "stock", "sector": "Consumer", "current_price": 57.80},
    {"security_id": "SPY", "name": "SPDR S&P 500 ETF", "type": "etf", "sector": "Broad Market", "current_price": 455.80},
    {"security_id": "QQQ", "name": "Invesco QQQ Trust", "type": "etf", "sector": "Technology", "current_price": 385.90},
    {"security_id": "VTI", "name": "Vanguard Total Stock Market ETF", "type": "etf", "sector": "Broad Market", "current_price": 228.40},
    {"security_id": "BND", "name": "Vanguard Total Bond Market ETF", "type": "etf", "sector": "Bonds", "current_price": 72.30},
    {"security_id": "GLD", "name": "SPDR Gold Shares", "type": "etf", "sector": "Commodities", "current_price": 183.50},
    {"security_id": "AGG", "name": "iShares Core US Aggregate Bond", "type": "etf", "sector": "Bonds", "current_price": 97.60},
    {"security_id": "XOM", "name": "Exxon Mobil Corp.", "type": "stock", "sector": "Energy", "current_price": 107.20},
    {"security_id": "CVX", "name": "Chevron Corp.", "type": "stock", "sector": "Energy", "current_price": 154.80},
    {"security_id": "BOND01", "name": "US Treasury 10Y Bond", "type": "bond", "sector": "Government", "current_price": 95.50},
    {"security_id": "BOND02", "name": "Corporate Bond Fund AAA", "type": "bond", "sector": "Corporate", "current_price": 102.30},
    {"security_id": "BOND03", "name": "Municipal Bond Fund", "type": "bond", "sector": "Municipal", "current_price": 98.70},
    {"security_id": "HALT01", "name": "Suspended Trading Inc.", "type": "stock", "sector": "Technology", "current_price": 12.50, "status": "halted"},
    {"security_id": "DLIST01", "name": "Delisted Corp.", "type": "stock", "sector": "Finance", "current_price": 0.50, "status": "delisted"},
    {"security_id": "VFUND1", "name": "Vanguard Growth Fund", "type": "mutual_fund", "sector": "Growth", "current_price": 145.20},
    {"security_id": "FIDX1", "name": "Fidelity 500 Index Fund", "type": "mutual_fund", "sector": "Broad Market", "current_price": 178.90},
]

ACCOUNT_TYPES = ["brokerage", "ira", "savings"]
CLIENT_TIERS = ["standard", "standard", "standard", "premium", "premium"]
EMAIL_DOMAINS = ["email.com", "mail.com", "inbox.com"]


def gen_holding_id():
    return "H" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


def gen_order_id():
    return "ORD" + "".join(random.choices(string.ascii_uppercase + string.digits, k=7))


def gen_account_id(atype, idx):
    prefix = {"brokerage": "BRK", "ira": "IRA", "savings": "SAV"}[atype]
    return f"{prefix}{10000 + idx}"


def generate_securities():
    secs = {}
    for s in SECURITIES:
        sec = dict(s)
        if "status" not in sec:
            sec["status"] = "active"
        secs[sec["security_id"]] = sec
    return secs


def generate_clients(num_clients=200, securities=None):
    clients = {}
    accounts_all = {}
    sec_ids = [s for s, info in securities.items() if info["status"] == "active"]
    account_counter = 0

    for i in range(num_clients):
        cid = f"C{10000 + i}"
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        birth_year = random.randint(1955, 2000)
        dob = f"{birth_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        tier = random.choice(CLIENT_TIERS)

        account_ids = []
        # Every client gets a brokerage account
        acct_id = gen_account_id("brokerage", account_counter)
        account_counter += 1
        num_holdings = random.randint(2, 8)
        holdings = []
        used_secs = set()
        for _ in range(num_holdings):
            sid = random.choice(sec_ids)
            qty = random.randint(5, 200)
            sec = securities[sid]
            cost_basis = round(sec["current_price"] * random.uniform(0.6, 1.4), 2)
            days_ago = random.randint(30, 730)
            purchase_date = (datetime(2024, 10, 15) - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            hid = gen_holding_id()
            holdings.append({
                "holding_id": hid,
                "security_id": sid,
                "security_name": sec["name"],
                "quantity": qty,
                "average_cost_basis": cost_basis,
                "purchase_date": purchase_date,
            })
            # Sometimes add a second lot of the same security
            if sid not in used_secs and random.random() < 0.3:
                hid2 = gen_holding_id()
                cost2 = round(sec["current_price"] * random.uniform(0.5, 1.2), 2)
                date2 = (datetime(2024, 10, 15) - timedelta(days=random.randint(60, 900))).strftime("%Y-%m-%d")
                holdings.append({
                    "holding_id": hid2,
                    "security_id": sid,
                    "security_name": sec["name"],
                    "quantity": random.randint(10, 100),
                    "average_cost_basis": cost2,
                    "purchase_date": date2,
                })
            used_secs.add(sid)

        pending_orders = []
        if random.random() < 0.3:
            oid = gen_order_id()
            osid = random.choice(sec_ids)
            otype = random.choice(["buy", "sell"])
            pending_orders.append({
                "order_id": oid,
                "account_id": acct_id,
                "security_id": osid,
                "order_type": otype,
                "quantity": random.randint(5, 50),
                "price": securities[osid]["current_price"],
                "status": "pending",
                "created_at": "2024-10-15T13:30:00",
            })

        accounts_all[acct_id] = {
            "account_id": acct_id,
            "client_id": cid,
            "type": "brokerage",
            "cash_balance": round(random.uniform(500, 50000), 2),
            "holdings": holdings,
            "pending_orders": pending_orders,
            "settings": {
                "dividend_reinvestment": random.choice([True, False]),
                "default_order_type": "market",
            },
        }
        account_ids.append(acct_id)

        # 70% get an IRA
        if random.random() < 0.7:
            acct_id = gen_account_id("ira", account_counter)
            account_counter += 1
            ira_holdings = []
            for _ in range(random.randint(1, 4)):
                sid = random.choice(sec_ids)
                qty = random.randint(10, 100)
                sec = securities[sid]
                cost_basis = round(sec["current_price"] * random.uniform(0.7, 1.3), 2)
                purchase_date = (datetime(2024, 10, 15) - timedelta(days=random.randint(60, 1000))).strftime("%Y-%m-%d")
                ira_holdings.append({
                    "holding_id": gen_holding_id(),
                    "security_id": sid,
                    "security_name": sec["name"],
                    "quantity": qty,
                    "average_cost_basis": cost_basis,
                    "purchase_date": purchase_date,
                })

            contrib = random.choice([0, 0, 1000, 2500, 4000, 5500, 6500])
            accounts_all[acct_id] = {
                "account_id": acct_id,
                "client_id": cid,
                "type": "ira",
                "cash_balance": round(random.uniform(100, 10000), 2),
                "holdings": ira_holdings,
                "pending_orders": [],
                "ira_contributions_this_year": contrib,
                "settings": {
                    "dividend_reinvestment": random.choice([True, False]),
                    "default_order_type": "market",
                },
            }
            account_ids.append(acct_id)

        # 60% get a savings account
        if random.random() < 0.6:
            acct_id = gen_account_id("savings", account_counter)
            account_counter += 1
            accounts_all[acct_id] = {
                "account_id": acct_id,
                "client_id": cid,
                "type": "savings",
                "cash_balance": round(random.uniform(1000, 100000), 2),
                "holdings": [],
                "pending_orders": [],
                "settings": {},
            }
            account_ids.append(acct_id)

        clients[cid] = {
            "client_id": cid,
            "name": {"first_name": first, "last_name": last},
            "email": f"{first.lower()}.{last.lower()}{random.randint(10,99)}@{random.choice(EMAIL_DOMAINS)}",
            "dob": dob,
            "phone": f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
            "tier": tier,
            "account_ids": account_ids,
        }

    return clients, accounts_all


def main():
    securities = generate_securities()
    clients, accounts = generate_clients(200, securities)

    with open(os.path.join(FOLDER_PATH, "securities.json"), "w") as f:
        json.dump(securities, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "clients.json"), "w") as f:
        json.dump(clients, f, indent=2)
    with open(os.path.join(FOLDER_PATH, "accounts.json"), "w") as f:
        json.dump(accounts, f, indent=2)

    print(f"Generated {len(securities)} securities, {len(clients)} clients, {len(accounts)} accounts")
    type_counts = {}
    for a in accounts.values():
        type_counts[a["type"]] = type_counts.get(a["type"], 0) + 1
    print(f"  Account types: {type_counts}")
    total_holdings = sum(len(a["holdings"]) for a in accounts.values())
    print(f"  Total holdings: {total_holdings}")
    tier_counts = {}
    for c in clients.values():
        tier_counts[c["tier"]] = tier_counts.get(c["tier"], 0) + 1
    print(f"  Client tiers: {tier_counts}")
    with_pending = sum(1 for a in accounts.values() if a.get("pending_orders"))
    print(f"  Accounts with pending orders: {with_pending}")
    multi_lot = sum(1 for a in accounts.values() for i, h1 in enumerate(a["holdings"]) for h2 in a["holdings"][i+1:] if h1["security_id"] == h2["security_id"])
    print(f"  Multi-lot holdings (same security, different lots): {multi_lot}")


if __name__ == "__main__":
    main()
