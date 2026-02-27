# Copyright Sierra
# Travel tasks: 25 seeds + 25 variations (1 per seed) = 50 total

from tau_bench.types import Action, Task
from tau_bench.envs.travel.tasks import TASKS as SEED_TASKS

VARIATIONS = [
    # Var 0 (F1: payment split - voucher+points+cc)
    Task(
        user_id="T10099",
        instruction="Your email is william.miller10@inbox.com. Search for Rome packages. Book the 3-night one for yourself (DOB 1999-12-19) and a friend (Amy Miller DOB 2001-05-10). Economy flight, standard hotel, compact car, include activity. With trip protection. Pay with $500 voucher, 500 points ($250 value), and credit card ending in 9700 for the rest. Calculate the exact split.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "william.miller10@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10099"}),
            Action(name="search_packages", kwargs={"destination": "Rome"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG024"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10099"}),
        ],
        outputs=[],
    ),
    # Var 1 (F1: voucher exceeds total, excess lost)
    Task(
        user_id="T10121",
        instruction="You are Sarah Clark, born 1965-06-13. Book the cheapest Costa Rica package for yourself only. Economy everything, skip activities, no protection. Pay entirely with your $1000 voucher. How much excess is wasted?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sarah", "last_name": "Clark", "dob": "1965-06-13"}),
            Action(name="get_client_details", kwargs={"client_id": "T10121"}),
            Action(name="search_packages", kwargs={"destination": "Costa Rica"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG017"}),
        ],
        outputs=[],
    ),
    # Var 2 (F1: points-only payment)
    Task(
        user_id="T10182",
        instruction="You are Liam Adams, born 1976-06-24. You have 15000 points ($7500). Book a Barcelona package for yourself only, economy flight, standard hotel, compact car, include activity. No protection. Pay entirely with points. How many points used?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Liam", "last_name": "Adams", "dob": "1976-06-24"}),
            Action(name="get_client_details", kwargs={"client_id": "T10182"}),
            Action(name="search_packages", kwargs={"destination": "Barcelona"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG005"}),
        ],
        outputs=[],
    ),
    # Var 3 (F1: triple split with exact math)
    Task(
        user_id="T10105",
        instruction="Your email is priya.carter95@email.com. Book a Bangkok 3-night package for yourself (DOB 1979-12-04). Business flight, deluxe hotel, skip activities. With protection. Pay: $500 voucher, 2000 points ($1000), credit card 4618 for rest. Calculate exact amounts.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "priya.carter95@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10105"}),
            Action(name="search_packages", kwargs={"destination": "Bangkok"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG013"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10105"}),
        ],
        outputs=[],
    ),
    # Var 4 (F1: modify payment to use voucher+points)
    Task(
        user_id="T10036",
        instruction="You are Sandra Carter, born 1978-09-23. For booking BK00286 (Bangkok, $3010), change payment to: $150 voucher, 2000 points ($1000), credit card 8736 for the remaining $1860. Confirm the split.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sandra", "last_name": "Carter", "dob": "1978-09-23"}),
            Action(name="get_client_details", kwargs={"client_id": "T10036"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00286"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10036"}),
            Action(name="calculate", kwargs={"expression": "3010 - 150 - 1000"}),
            Action(name="modify_booking_payment", kwargs={"booking_id": "BK00286", "new_payment_methods": [{"payment_id": "voucher_T10036_0", "amount": 150}, {"payment_id": "cc_T10036_7807", "amount": 1860}], "use_points": 2000}),
        ],
        outputs=["1860"],
    ),
    # Var 5 (F2: search+compare+pick cheapest+book)
    Task(
        user_id="T10017",
        instruction="You are Noah Adams, born 1974-08-08. Search for Dubai packages. Pick the cheapest. Book for yourself only, economy everything, include activity. With protection. Pay with 2000 points ($1000) and credit card 1475 for the rest. Tell me the total.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Noah", "last_name": "Adams", "dob": "1974-08-08"}),
            Action(name="get_client_details", kwargs={"client_id": "T10017"}),
            Action(name="search_packages", kwargs={"destination": "Dubai"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG010"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG030"}),
        ],
        outputs=[],
    ),
    # Var 6 (F2: search by duration+filter+book)
    Task(
        user_id="T10175",
        instruction="Your email is thomas.miller83@inbox.com. You want a 14-night trip. Search packages with 14+ nights. Find the one with the most components. Book for 2 travelers (yourself DOB 1960-01-13, wife Jane Miller DOB 1962-08-30). Business flight, deluxe hotel. No protection. Credit card ending in 7783.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "thomas.miller83@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10175"}),
            Action(name="search_packages", kwargs={"min_duration": 14}),
        ],
        outputs=[],
    ),
    # Var 7 (F2: search by component type)
    Task(
        user_id="T10036",
        instruction="Your email is sandra.carter63@mail.com. You want a trip with car rental in Bali or Hawaii. Search packages with car components in both destinations. Compare prices. Which is cheaper?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "sandra.carter63@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10036"}),
            Action(name="search_packages_by_component", kwargs={"component_type": "car", "destination": "Bali"}),
            Action(name="search_packages_by_component", kwargs={"component_type": "car", "destination": "Hawaii"}),
        ],
        outputs=[],
    ),
    # Var 8 (F3: multi-booking scan, cancel without protection)
    Task(
        user_id="T10121",
        instruction="Your email is sarah.clark91@email.com. Check all your confirmed bookings. Cancel any that do NOT have trip protection and cost more than $3000. Tell me which ones you cancel and total amount.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "sarah.clark91@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10121"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00083"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00148"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00285"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00285", "reason": "no protection, too expensive"}),
        ],
        outputs=[],
    ),
    # Var 9 (F3: scan bookings, upgrade flights on expensive ones)
    Task(
        user_id="T10175",
        instruction="You are Thomas Miller, born 1960-01-13. Check all confirmed bookings. For any over $5000, downgrade the hotel to standard to save money. Tell me which bookings changed and total savings. Credit card ending in 7783.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Thomas", "last_name": "Miller", "dob": "1960-01-13"}),
            Action(name="get_client_details", kwargs={"client_id": "T10175"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00043"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00103"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00152"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG011"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG035"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00043", "changes": [{"component_id": "PKG011_H", "new_option": "standard"}], "payment_id": "cc_T10175_7875"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00152", "changes": [{"component_id": "PKG035_H", "new_option": "standard"}], "payment_id": "cc_T10175_7875"}),
        ],
        outputs=[],
    ),
    # Var 10 (F3: scan by destination, downgrade Asian trips)
    Task(
        user_id="T10180",
        instruction="Your email is sofia.mitchell48@email.com. Check all confirmed bookings. For any in Europe (Paris, Santorini, Barcelona), skip all premium activities to save. Tell me savings per booking. Credit card ending in 4727.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "sofia.mitchell48@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10180"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00131"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00147"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00254"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG021"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG036"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00131", "changes": [{"component_id": "PKG021_A1", "new_option": "skip"}], "payment_id": "cc_T10180_9871"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00147", "changes": [{"component_id": "PKG036_A1", "new_option": "skip"}], "payment_id": "cc_T10180_9871"}),
        ],
        outputs=[],
    ),
    # Var 11 (F4: cancel+rebook cheaper)
    Task(
        user_id="T10036",
        instruction="You are Sandra Carter, born 1978-09-23. Cancel your Bali booking BK00295 ($7870, too pricey). Search for a cheaper Bali package. Book the cheapest for yourself only, economy everything, no protection. Credit card 8736. How much do you save?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sandra", "last_name": "Carter", "dob": "1978-09-23"}),
            Action(name="get_client_details", kwargs={"client_id": "T10036"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00295"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00295", "reason": "too expensive, rebooking cheaper"}),
            Action(name="search_packages", kwargs={"destination": "Bali"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG007"}),
        ],
        outputs=[],
    ),
    # Var 12 (F4: cancel+rebook different destination with voucher)
    Task(
        user_id="T10090",
        instruction="Your email is olivia.perez60@inbox.com. Cancel Barcelona booking BK00130 ($5130). Rebook a London trip instead. Search London packages. Book for yourself (DOB 1996-12-11) and partner (Alex Perez DOB 1995-04-22). Economy, standard hotel. With protection. Pay $1000 voucher + credit card 9433 for rest.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "olivia.perez60@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10090"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00130"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00130", "reason": "switching to London"}),
            Action(name="search_packages", kwargs={"destination": "London"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG003"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10090"}),
        ],
        outputs=[],
    ),
    # Var 13 (F4: cancel+rebook upgraded with points)
    Task(
        user_id="T10096",
        instruction="You are Ethan Brown, born 1968-09-07. Cancel Costa Rica BK00246 ($1780). Rebook a Swiss Alps 4-night trip with first class and suite. For yourself only. With protection. Use 4000 points ($2000) and credit card 8837. What's the cc amount?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Ethan", "last_name": "Brown", "dob": "1968-09-07"}),
            Action(name="get_client_details", kwargs={"client_id": "T10096"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00246"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00246", "reason": "upgrading to Swiss Alps"}),
            Action(name="search_packages", kwargs={"destination": "Swiss Alps"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG015"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10096"}),
        ],
        outputs=[],
    ),
    # Var 14 (F5: multi-component modify)
    Task(
        user_id="T10003",
        instruction="Your email is robert.torres27@mail.com. For booking BK00082 (Cancun, 14n), upgrade flight to business, downgrade hotel from deluxe to standard, and switch car from luxury to compact. Tell me the net change and new total. Credit card 5002.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "robert.torres27@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10003"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00082"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG008"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00082", "changes": [{"component_id": "PKG008_F", "new_option": "business"}, {"component_id": "PKG008_H", "new_option": "standard"}, {"component_id": "PKG008_C", "new_option": "compact"}], "payment_id": "cc_T10003_6718"}),
        ],
        outputs=[],
    ),
    # Var 15 (F5: downgrade multiple to save)
    Task(
        user_id="T10066",
        instruction="You are Andrew Hall, born 1971-01-08. For booking BK00225 (Swiss Alps, $10790), downgrade flight from first class to economy, hotel from presidential to deluxe, and skip the premium activity. Tell me total savings and new price. Credit card 9586.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Andrew", "last_name": "Hall", "dob": "1971-01-08"}),
            Action(name="get_client_details", kwargs={"client_id": "T10066"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00225"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG035"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00225", "changes": [{"component_id": "PKG035_F", "new_option": "economy"}, {"component_id": "PKG035_H", "new_option": "deluxe"}, {"component_id": "PKG035_A1", "new_option": "skip"}], "payment_id": "cc_T10066_8172"}),
        ],
        outputs=[],
    ),
    # Var 16 (F5: change travelers + modify component)
    Task(
        user_id="T10001",
        instruction="Your email is david.brown82@email.com. For booking BK00199 (Swiss Alps, 3 travelers), replace the second traveler with Lisa Brown (DOB 1995-07-18) and third with Mark Brown (DOB 2000-03-10). Also downgrade flight from first class to premium economy. Credit card 2113.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "david.brown82@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10001"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00199"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG035"}),
            Action(name="modify_booking_travelers", kwargs={"booking_id": "BK00199", "travelers": [{"first_name": "David", "last_name": "Brown", "dob": "1992-02-28"}, {"first_name": "Lisa", "last_name": "Brown", "dob": "1995-07-18"}, {"first_name": "Mark", "last_name": "Brown", "dob": "2000-03-10"}]}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00199", "changes": [{"component_id": "PKG035_F", "new_option": "premium_economy"}], "payment_id": "cc_T10001_2122"}),
        ],
        outputs=[],
    ),
    # Var 17 (POL: cancel no protection <3 days → no refund)
    Task(
        user_id="T10056",
        instruction="You are Wei Allen, born 1974-02-12. You want to cancel booking BK00096 (Maldives, starts June 14, has protection). You want a full refund. Check if you qualify.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Wei", "last_name": "Allen", "dob": "1974-02-12"}),
            Action(name="get_client_details", kwargs={"client_id": "T10056"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00096"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00096", "reason": "change of plans"}),
        ],
        outputs=[],
    ),
    # Var 18 (POL: add protection after booking → refuse)
    Task(
        user_id="T10027",
        instruction="Your email is michael.smith61@mail.com. You want to add trip protection to booking BK00309 (Sydney, no protection). Can you add it? If not, what refund would you get if you cancel?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "michael.smith61@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10027"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00309"}),
        ],
        outputs=[],
    ),
    # Var 19 (POL: gold member 50% guarantee)
    Task(
        user_id="T10066",
        instruction="You are Andrew Hall, born 1971-01-08. Gold member. Cancel booking BK00362 (Bali, no protection, starts June 21). As gold you expect at least 50% refund. Confirm the amount.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Andrew", "last_name": "Hall", "dob": "1971-01-08"}),
            Action(name="get_client_details", kwargs={"client_id": "T10066"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00362"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00362", "reason": "change of plans"}),
        ],
        outputs=["2400"],
    ),
    # Var 20 (ADV: wrong destination, corrects)
    Task(
        user_id="T10175",
        instruction="Your email is thomas.miller83@inbox.com. You have a booking in Australia but don't remember the ID. You first say it's in Melbourne, but actually it's Sydney. Ask the agent to find it and show details.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "thomas.miller83@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10175"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00043"}),
        ],
        outputs=[],
    ),
    # Var 21 (ADV: wants to cancel all, changes mind)
    Task(
        user_id="T10027",
        instruction="You are Michael Smith, born 1996-05-16. You're panicking and want to cancel ALL bookings. After the agent checks them, you realize the Costa Rica trip BK00015 has protection and is for your honeymoon. Just cancel BK00309 (Sydney) and BK00370 (Cancun).",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Michael", "last_name": "Smith", "dob": "1996-05-16"}),
            Action(name="get_client_details", kwargs={"client_id": "T10027"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00015"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00309"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00370"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00309", "reason": "change of plans"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00370", "reason": "change of plans"}),
        ],
        outputs=[],
    ),
    # Var 22 (COMP: gold member, past trip issue → points)
    Task(
        user_id="T10105",
        instruction="Your email is priya.carter95@email.com. Gold member. Your past Kyoto trip (BK00111) had 3 issues: hotel was dirty, activity was cancelled, and car broke down. That's 3 affected components. You want compensation (200 points each).",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "priya.carter95@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10105"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00111"}),
            Action(name="add_loyalty_points", kwargs={"client_id": "T10105", "points": 600}),
        ],
        outputs=["600"],
    ),
    # Var 23 (COMP: standard → transfer)
    Task(
        user_id="T10076",
        instruction="You are Thomas Johnson, born 1982-02-12. Standard tier. Your Barcelona trip (BK00238) had a terrible hotel. You want compensation. If the agent can't help, connect me to someone who can.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Thomas", "last_name": "Johnson", "dob": "1982-02-12"}),
            Action(name="get_client_details", kwargs={"client_id": "T10076"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00238"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Standard tier client requesting compensation for bad hotel experience on Barcelona trip BK00238. Per policy, standard members must be transferred."}),
        ],
        outputs=[],
    ),
    # Var 24 (COMP: complex end-to-end: scan → cancel → search → book with split payment)
    Task(
        user_id="T10182",
        instruction="Your email is liam.adams85@inbox.com. Check all confirmed bookings. Cancel the Barcelona one (BK00250). Then search for a Hawaii package. Book the 3-night one for yourself (DOB 1976-06-24) and spouse (Jane Adams DOB 1978-11-05). Economy flight, deluxe hotel, compact car. With protection. Pay: $1000 voucher, 4000 points ($2000), credit card 7510 for rest. Calculate exact split.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "liam.adams85@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10182"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00039"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00250"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00250", "reason": "switching to Hawaii"}),
            Action(name="search_packages", kwargs={"destination": "Hawaii"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG029"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10182"}),
        ],
        outputs=[],
    ),
]

VARIATIONS_2 = [
    # Var2-0 (F1: payment split voucher+points+cc)
    Task(
        user_id="T10149",
        instruction="You are Michael Perez, born 1983-05-05. Book a Dubai package for yourself only (DOB 1983-05-05). Business flight, deluxe hotel, include activity. No protection. Pay: $250 voucher, 2000 points ($1000), credit card 3340 for rest. Search Dubai packages first. Calculate exact split.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Michael", "last_name": "Perez", "dob": "1983-05-05"}),
            Action(name="get_client_details", kwargs={"client_id": "T10149"}),
            Action(name="search_packages", kwargs={"destination": "Dubai"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG030"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10149"}),
        ],
        outputs=[],
    ),
    # Var2-1 (F1: voucher exceeds total)
    Task(
        user_id="T10130",
        instruction="Your email is chen.young19@mail.com. Book the cheapest Marrakech package for yourself only. Economy everything, skip activity, no protection. Pay with your $750 voucher. How much excess is wasted?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "chen.young19@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10130"}),
            Action(name="search_packages", kwargs={"destination": "Marrakech"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG038"}),
        ],
        outputs=[],
    ),
    # Var2-2 (F1: points-only)
    Task(
        user_id="T10114",
        instruction="You are Anthony Taylor, born 1976-04-11. You have 15000 points ($7500). Book a New York 3-night package for yourself only. Economy everything, include activities. With protection. Pay entirely with points. How many points?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Anthony", "last_name": "Taylor", "dob": "1976-04-11"}),
            Action(name="get_client_details", kwargs={"client_id": "T10114"}),
            Action(name="search_packages", kwargs={"destination": "New York"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG026"}),
        ],
        outputs=[],
    ),
    # Var2-3 (F1: triple split exact math)
    Task(
        user_id="T10157",
        instruction="Your email is jessica.williams74@inbox.com. Book a Cancun 7-night package for 2 (yourself DOB 1990-06-13, friend Amy Williams DOB 1992-11-20). Premium economy, deluxe hotel, sedan car. Include activities. With protection. Pay: $500 voucher, credit card 7870 for rest. Calculate exact total and cc amount.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "jessica.williams74@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10157"}),
            Action(name="search_packages", kwargs={"destination": "Cancun"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG028"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10157"}),
        ],
        outputs=[],
    ),
    # Var2-4 (F1: modify payment with voucher+points)
    Task(
        user_id="T10188",
        instruction="You are David Moore, born 1965-05-01. For booking BK00354 (Cancun, $7150), change payment to: $250 voucher, 2000 points ($1000), credit card 4511 for $5900. Confirm the exact split.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "David", "last_name": "Moore", "dob": "1965-05-01"}),
            Action(name="get_client_details", kwargs={"client_id": "T10188"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00354"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10188"}),
            Action(name="calculate", kwargs={"expression": "7150 - 250 - 1000"}),
            Action(name="modify_booking_payment", kwargs={"booking_id": "BK00354", "new_payment_methods": [{"payment_id": "voucher_T10188_0", "amount": 250}, {"payment_id": "cc_T10188_1813", "amount": 5900}], "use_points": 2000}),
        ],
        outputs=["5900"],
    ),
    # Var2-5 (F2: search+compare+cheapest+book)
    Task(
        user_id="T10130",
        instruction="You are Chen Young, born 1973-08-26. Search Kyoto packages. Compare prices. Book the cheapest for yourself only. Economy everything, include activities. With protection. Pay with 3000 points ($1500) and credit card 9180 for rest.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Chen", "last_name": "Young", "dob": "1973-08-26"}),
            Action(name="get_client_details", kwargs={"client_id": "T10130"}),
            Action(name="search_packages", kwargs={"destination": "Kyoto"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG020"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG040"}),
        ],
        outputs=[],
    ),
    # Var2-6 (F2: search by duration + book)
    Task(
        user_id="T10102",
        instruction="Your email is sandra.rodriguez47@inbox.com. You want a 7-night trip. Search packages. Find one in Asia with car rental. Book for 2 travelers (yourself DOB 1992-08-09, partner Tom Rodriguez DOB 1990-12-01). Business flight, suite hotel. No protection. Credit card 3662.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "sandra.rodriguez47@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10102"}),
            Action(name="search_packages", kwargs={"min_duration": 7}),
        ],
        outputs=[],
    ),
    # Var2-7 (F2: search by component)
    Task(
        user_id="T10165",
        instruction="You are Liam Thomas, born 1968-04-27. You want a trip with activities in Hawaii or Bali. Search packages with activity components in both. Which has more activity options? Tell me the details.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Liam", "last_name": "Thomas", "dob": "1968-04-27"}),
            Action(name="get_client_details", kwargs={"client_id": "T10165"}),
            Action(name="search_packages_by_component", kwargs={"component_type": "activity", "destination": "Hawaii"}),
            Action(name="search_packages_by_component", kwargs={"component_type": "activity", "destination": "Bali"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG009"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG007"}),
        ],
        outputs=[],
    ),
    # Var2-8 (F3: multi-booking scan, cancel without protection)
    Task(
        user_id="T10157",
        instruction="Your email is jessica.williams74@inbox.com. Check all confirmed bookings. Cancel any WITHOUT trip protection. Tell me which you cancelled and the total amount.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "jessica.williams74@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10157"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00023"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00055"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00023", "reason": "no trip protection"}),
        ],
        outputs=[],
    ),
    # Var2-9 (F3: scan bookings, downgrade expensive ones)
    Task(
        user_id="T10102",
        instruction="You are Sandra Rodriguez, born 1992-08-09. Check all confirmed bookings. For any over $5000, downgrade hotel to standard. Tell me which changed and savings. Credit card 3662.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sandra", "last_name": "Rodriguez", "dob": "1992-08-09"}),
            Action(name="get_client_details", kwargs={"client_id": "T10102"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00101"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00166"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00247"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG004"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG040"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00166", "changes": [{"component_id": "PKG004_H", "new_option": "standard"}], "payment_id": "cc_T10102_2845"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00247", "changes": [{"component_id": "PKG040_H", "new_option": "standard"}], "payment_id": "cc_T10102_2845"}),
        ],
        outputs=[],
    ),
    # Var2-10 (F3: scan by region, skip activities)
    Task(
        user_id="T10165",
        instruction="Your email is liam.thomas35@inbox.com. Check all confirmed bookings. For any in Asia (Tokyo, Kyoto, Bangkok), skip all premium activities to save. What's the total savings? Credit card 2376.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "liam.thomas35@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10165"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00129"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00195"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG022"}),
        ],
        outputs=[],
    ),
    # Var2-11 (F4: cancel+rebook cheaper)
    Task(
        user_id="T10188",
        instruction="You are David Moore, born 1965-05-01. Cancel Cancun BK00354 ($7150, too pricey). Search for a cheaper Cancun package. Book cheapest for yourself only, economy everything. No protection. Credit card 4511. How much saved?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "David", "last_name": "Moore", "dob": "1965-05-01"}),
            Action(name="get_client_details", kwargs={"client_id": "T10188"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00354"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00354", "reason": "too expensive"}),
            Action(name="search_packages", kwargs={"destination": "Cancun"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG008"}),
        ],
        outputs=[],
    ),
    # Var2-12 (F4: cancel+rebook different dest with voucher)
    Task(
        user_id="T10192",
        instruction="Your email is chen.johnson97@inbox.com. Cancel Marrakech BK00189 ($5660). Rebook a Bali 10-night trip for yourself (DOB 1991-05-09). Economy, deluxe hotel. With protection. Pay $500 voucher + 1000 points ($500) + credit card 1578 for rest.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "chen.johnson97@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10192"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00189"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00189", "reason": "switching to Bali"}),
            Action(name="search_packages", kwargs={"destination": "Bali"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG027"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10192"}),
        ],
        outputs=[],
    ),
    # Var2-13 (F4: cancel+rebook upgraded)
    Task(
        user_id="T10137",
        instruction="You are Melissa Lopez, born 1979-10-19. Cancel Tokyo BK00281 ($1105). Rebook a Tokyo 14-night package with business flight, suite hotel. For yourself only. No protection. Use 5000 points ($2500) + credit card 2931 for rest. What's the cc amount?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Melissa", "last_name": "Lopez", "dob": "1979-10-19"}),
            Action(name="get_client_details", kwargs={"client_id": "T10137"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00281"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00281", "reason": "upgrading"}),
            Action(name="search_packages", kwargs={"destination": "Tokyo"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG002"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10137"}),
        ],
        outputs=[],
    ),
    # Var2-14 (F5: multi-component modify)
    Task(
        user_id="T10181",
        instruction="Your email is andrew.hill20@inbox.com. For BK00198 (London, 4n), upgrade flight to business, hotel to suite, switch car from luxury to compact. Net change and new total? Credit card 8357.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "andrew.hill20@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10181"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00198"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG003"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00198", "changes": [{"component_id": "PKG003_F", "new_option": "business"}, {"component_id": "PKG003_H", "new_option": "suite"}, {"component_id": "PKG003_C", "new_option": "compact"}], "payment_id": "cc_T10181_3415"}),
        ],
        outputs=[],
    ),
    # Var2-15 (F5: downgrade multiple to save)
    Task(
        user_id="T10102",
        instruction="You are Sandra Rodriguez, born 1992-08-09. For BK00166 (Rome, 14n, $6470), downgrade flight from business to economy, car from compact to compact (already), skip both premium activities. What's the new total? Credit card 3662.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sandra", "last_name": "Rodriguez", "dob": "1992-08-09"}),
            Action(name="get_client_details", kwargs={"client_id": "T10102"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00166"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG004"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00166", "changes": [{"component_id": "PKG004_F", "new_option": "economy"}, {"component_id": "PKG004_A1", "new_option": "skip"}, {"component_id": "PKG004_A2", "new_option": "skip"}], "payment_id": "cc_T10102_2845"}),
        ],
        outputs=[],
    ),
    # Var2-16 (F5: change travelers + modify)
    Task(
        user_id="T10192",
        instruction="Your email is chen.johnson97@inbox.com. For BK00156 (Bali, 4 travelers), replace 2nd/3rd/4th travelers with: Amy Johnson DOB 1993-02-14, Bob Johnson DOB 1995-08-30, Cara Johnson DOB 1997-12-05. Also upgrade flight to business. Credit card 1578.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "chen.johnson97@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10192"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00156"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG027"}),
            Action(name="modify_booking_travelers", kwargs={"booking_id": "BK00156", "travelers": [{"first_name": "Chen", "last_name": "Johnson", "dob": "1991-05-09"}, {"first_name": "Amy", "last_name": "Johnson", "dob": "1993-02-14"}, {"first_name": "Bob", "last_name": "Johnson", "dob": "1995-08-30"}, {"first_name": "Cara", "last_name": "Johnson", "dob": "1997-12-05"}]}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00156", "changes": [{"component_id": "PKG027_F", "new_option": "business"}], "payment_id": "cc_T10192_7628"}),
        ],
        outputs=[],
    ),
    # Var2-17 (POL: cancel with protection → full refund)
    Task(
        user_id="T10137",
        instruction="Your email is melissa.lopez86@email.com. Cancel Bangkok BK00386 (starts July 14, has trip protection). You want full refund. Check if you qualify (protection + >24h before trip).",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "melissa.lopez86@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10137"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00386"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00386", "reason": "change of plans"}),
        ],
        outputs=[],
    ),
    # Var2-18 (POL: add protection after booking → refuse)
    Task(
        user_id="T10165",
        instruction="You are Liam Thomas, born 1968-04-27. Add trip protection to booking BK00195 (Tokyo, no protection). If not possible, what are your options?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Liam", "last_name": "Thomas", "dob": "1968-04-27"}),
            Action(name="get_client_details", kwargs={"client_id": "T10165"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00195"}),
        ],
        outputs=[],
    ),
    # Var2-19 (POL: gold member 50% guarantee)
    Task(
        user_id="T10114",
        instruction="Your email is anthony.taylor95@inbox.com. Gold member. Cancel BK00095 (New York, $1715, no protection, starts June 10). As gold you get at least 50% refund. Confirm.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "anthony.taylor95@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10114"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00095"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00095", "reason": "change of plans"}),
        ],
        outputs=["857"],
    ),
    # Var2-20 (ADV: wrong info, corrects)
    Task(
        user_id="T10137",
        instruction="You are Melissa Lopez, born 1979-10-19. You have a booking in Tokyo but say it's BK99999. When not found, ask agent to look up your account. You want the one in Tokyo with 4 travelers.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Melissa", "last_name": "Lopez", "dob": "1979-10-19"}),
            Action(name="get_client_details", kwargs={"client_id": "T10137"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00281"}),
        ],
        outputs=[],
    ),
    # Var2-21 (ADV: cancel all → changes mind)
    Task(
        user_id="T10149",
        instruction="Your email is michael.perez88@inbox.com. You're stressed and want to cancel everything. After agent checks, realize your Dubai trip BK00249 is for a conference. Only cancel BK00053 (Costa Rica).",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "michael.perez88@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10149"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00053"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00249"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00053", "reason": "change of plans"}),
        ],
        outputs=[],
    ),
    # Var2-22 (COMP: gold + past trip issues → points)
    Task(
        user_id="T10154",
        instruction="You are Joshua Perez, born 1985-10-21. Gold member. Your Marrakech trip (BK00358) had 2 issues: hotel not as described and activity cancelled. 200 points per component. You want 400 points.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Joshua", "last_name": "Perez", "dob": "1985-10-21"}),
            Action(name="get_client_details", kwargs={"client_id": "T10154"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00358"}),
            Action(name="add_loyalty_points", kwargs={"client_id": "T10154", "points": 400}),
        ],
        outputs=["400"],
    ),
    # Var2-23 (COMP: standard → transfer)
    Task(
        user_id="T10157",
        instruction="Your email is jessica.williams74@inbox.com. Standard tier. Your Rome trip BK00055 had terrible service. Want compensation. If can't, transfer to someone who can.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "jessica.williams74@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10157"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00055"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Standard tier client requesting compensation for bad Rome trip BK00055. Must transfer per policy."}),
        ],
        outputs=[],
    ),
    # Var2-24 (COMP: complex end-to-end)
    Task(
        user_id="T10130",
        instruction="Your email is chen.young19@mail.com. Check all confirmed bookings. Cancel the Marrakech one (BK00323). Search Hawaii packages. Book the 3-night one for yourself (DOB 1973-08-26) and spouse (Lin Young DOB 1975-04-10). Economy, standard hotel, compact car. With protection. Pay: $750 voucher, 2000 points ($1000), credit card 9180 for rest.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "chen.young19@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10130"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00002"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00323"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00323", "reason": "switching to Hawaii"}),
            Action(name="search_packages", kwargs={"destination": "Hawaii"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG029"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10130"}),
        ],
        outputs=[],
    ),
]

TASKS = SEED_TASKS + VARIATIONS + VARIATIONS_2
