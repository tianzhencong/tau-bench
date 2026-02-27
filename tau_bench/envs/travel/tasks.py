# Copyright Sierra
# Travel agency tasks targeting airline's 5 failure patterns:
# F1: Complex payment splitting (voucher + points + credit card)
# F2: Search → compare → select → book
# F3: Multi-booking scan + selective action
# F4: Cancel + rebook chain
# F5: Multi-component modification

from tau_bench.types import Action, Task

TASKS = [
    # =================================================================
    # F1: COMPLEX PAYMENT SPLITTING (airline tasks 0, 8, 9 always fail)
    # Voucher (max 1) + loyalty points + credit card must sum to exact total
    # =================================================================

    # Task 0: Book with voucher + points + credit card split (8 actions)
    Task(
        user_id="T10002",
        instruction="Your email is melissa.garcia19@email.com. You want to book a trip to Bali. Search for Bali packages. Pick the cheapest one. Book for yourself (DOB 1986-11-19) with economy flight, standard hotel, compact car if available. No trip protection. For payment, use your $1000 voucher first, then 2000 loyalty points ($1000 value), then credit card ending in 5272 for the rest. Calculate the exact split.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "melissa.garcia19@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10002"}),
            Action(name="search_packages", kwargs={"destination": "Bali"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG007"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10002"}),
        ],
        outputs=[],
    ),

    # Task 1: Book with voucher that exceeds total (excess is lost)
    Task(
        user_id="T10076",
        instruction="You are Thomas Johnson, born 1982-02-12. You want to book a cheap trip. Search for Bangkok packages. Pick the cheapest. Book for yourself only, economy everything, skip activities. No protection. Pay entirely with your $1000 voucher. You know the excess is lost but that's fine. Tell me how much you'll waste from the voucher.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Thomas", "last_name": "Johnson", "dob": "1982-02-12"}),
            Action(name="get_client_details", kwargs={"client_id": "T10076"}),
            Action(name="search_packages", kwargs={"destination": "Bangkok"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG013"}),
        ],
        outputs=[],
    ),

    # Task 2: Points-only payment for small booking
    Task(
        user_id="T10096",
        instruction="Your email is ethan.brown53@inbox.com. You have 10000 loyalty points ($5000 value). Book a Costa Rica trip for yourself (DOB 1968-09-07). Economy flight, standard hotel, compact car. No activities. No protection. Pay entirely with points. How many points will it cost?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "ethan.brown53@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10096"}),
            Action(name="search_packages", kwargs={"destination": "Costa Rica"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG017"}),
        ],
        outputs=[],
    ),

    # Task 3: Triple split: voucher + points + credit card with exact math
    Task(
        user_id="T10033",
        instruction="You are Amanda Robinson, born 2000-08-03. Book a Paris trip for yourself and a friend (Lisa Robinson DOB 1999-03-15). Search Paris packages. Pick the 14-night one. Economy flight, deluxe hotel, compact car, skip all activities. With trip protection. Pay with: $750 voucher, 1000 points ($500), and credit card 6460 for the rest. Calculate exact amounts.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Amanda", "last_name": "Robinson", "dob": "2000-08-03"}),
            Action(name="get_client_details", kwargs={"client_id": "T10033"}),
            Action(name="search_packages", kwargs={"destination": "Paris"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG001"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10033"}),
            Action(name="calculate", kwargs={"expression": "2800 + 80*14 + 0 - 50 - 75 + 100"}),
        ],
        outputs=[],
    ),

    # Task 4: Modify payment on existing booking to use voucher + points
    Task(
        user_id="T10010",
        instruction="Your email is wei.davis95@mail.com. For booking BK00107 (Santorini, $6000), you want to change the payment to use your $250 voucher, 3000 points ($1500 value), and credit card for the remaining $4250. Confirm the exact split.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "wei.davis95@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10010"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00107"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10010"}),
            Action(name="calculate", kwargs={"expression": "6000 - 250 - 1500"}),
            Action(name="modify_booking_payment", kwargs={"booking_id": "BK00107", "new_payment_methods": [{"payment_id": "voucher_T10010_0", "amount": 250}, {"payment_id": "cc_T10010_7691", "amount": 4250}], "use_points": 3000}),
        ],
        outputs=["4250"],
    ),

    # =================================================================
    # F2: SEARCH → COMPARE → SELECT → BOOK (airline tasks 0,3,14,19,22)
    # Must search, compare options, pick by criteria, then book correctly
    # =================================================================

    # Task 5: Search + compare + pick cheapest + book (9 actions)
    Task(
        user_id="T10019",
        instruction="You are Matthew Thomas, born 1964-11-02. You want the cheapest Hawaii trip. Search Hawaii packages, compare prices. Book the cheapest one for yourself only. Economy everything, include all activities. With trip protection. Pay with credit card. Tell me the total including protection.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Matthew", "last_name": "Thomas", "dob": "1964-11-02"}),
            Action(name="get_client_details", kwargs={"client_id": "T10019"}),
            Action(name="search_packages", kwargs={"destination": "Hawaii"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG009"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG029"}),
        ],
        outputs=[],
    ),

    # Task 6: Search + pick by duration + book with upgrades
    Task(
        user_id="T10003",
        instruction="Your email is robert.torres27@mail.com. You want a 7-night trip. Search packages with at least 7 nights. Compare all destinations. Book the one that includes car rental AND has the lowest base price. Book for 2 travelers (yourself DOB 1973-09-09, and wife Maria Torres DOB 1975-03-22). Business flight, suite hotel, SUV car. Include activities. No protection. Credit card ending in 5002.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "robert.torres27@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10003"}),
            Action(name="search_packages", kwargs={"min_duration": 7}),
        ],
        outputs=[],
    ),

    # Task 7: Search by component type (activity) + destination
    Task(
        user_id="T10073",
        instruction="You are Jennifer Harris, born 1974-01-11. You want a trip that includes a cooking class or food tasting. Search packages that have activity components in Kyoto or Tokyo. Compare options. Tell me which packages have food-related activities and their prices.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Jennifer", "last_name": "Harris", "dob": "1974-01-11"}),
            Action(name="get_client_details", kwargs={"client_id": "T10073"}),
            Action(name="search_packages_by_component", kwargs={"component_type": "activity", "destination": "Kyoto"}),
            Action(name="search_packages_by_component", kwargs={"component_type": "activity", "destination": "Tokyo"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG020"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG002"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # F3: MULTI-BOOKING SCAN + SELECTIVE ACTION (airline tasks 28, 33)
    # Client has many bookings, must check each, apply filter, act on some
    # =================================================================

    # Task 8: Cancel all bookings without trip protection (scan + filter + cancel)
    Task(
        user_id="T10003",
        instruction="Your email is robert.torres27@mail.com. You want to cancel all your confirmed bookings that do NOT have trip protection. Check each booking. For each one without protection, cancel it. Tell me how many you cancelled and the total money involved.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "robert.torres27@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10003"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00021"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00082"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00265"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00021", "reason": "no trip protection"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00082", "reason": "no trip protection"}),
        ],
        outputs=[],
    ),

    # Task 9: Check all bookings, upgrade flights on the expensive ones
    Task(
        user_id="T10076",
        instruction="You are Thomas Johnson, born 1982-02-12. Check all your confirmed bookings. For any booking that costs more than $3000, upgrade the flight to business class. For bookings under $3000, leave them. Tell me which bookings you modified and the new totals. Use credit card ending in 6447.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Thomas", "last_name": "Johnson", "dob": "1982-02-12"}),
            Action(name="get_client_details", kwargs={"client_id": "T10076"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00077"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00128"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG001"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG033"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00077", "changes": [{"component_id": "PKG001_F", "new_option": "business"}], "payment_id": "cc_T10076_2698"}),
        ],
        outputs=[],
    ),

    # Task 10: Scan all bookings, find ones in specific destinations
    Task(
        user_id="T10099",
        instruction="Your email is william.miller10@inbox.com. Check all your confirmed bookings. Which ones are in Asia (Kyoto, Tokyo, Bangkok, Bali)? For those Asian bookings, downgrade hotels to standard to save money. Tell me total savings. Use credit card ending in 9700.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "william.miller10@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10099"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00032"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00182"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00343"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG020"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00343", "changes": [{"component_id": "PKG020_H", "new_option": "standard"}], "payment_id": "cc_T10099_4972"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # F4: CANCEL + REBOOK CHAIN (airline tasks 8, 9, 10, 25)
    # Cancel existing booking → search alternatives → book new
    # =================================================================

    # Task 11: Cancel expensive booking, rebook cheaper in same destination
    Task(
        user_id="T10078",
        instruction="Your email is aisha.walker20@mail.com. Your Bangkok booking BK00398 ($6610) is too expensive. Cancel it. Then search for a cheaper Bangkok package. Book the cheapest one for yourself only (DOB 1984-06-06), economy everything, skip activities. No protection. Pay with credit card ending in 9507. How much do you save?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "aisha.walker20@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10078"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00398"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00398", "reason": "too expensive, rebooking cheaper"}),
            Action(name="search_packages", kwargs={"destination": "Bangkok"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG013"}),
        ],
        outputs=[],
    ),

    # Task 12: Cancel + rebook with different options + voucher payment
    Task(
        user_id="T10027",
        instruction="You are Michael Smith, born 1996-05-16. Cancel your Cancun booking BK00370 ($4680). Then search for a Sydney 3-night package and rebook with economy flight, deluxe hotel. For 2 travelers (yourself and Sarah Smith DOB 1998-02-14). With protection. Pay with $1000 voucher and credit card for the rest. Tell me the new total and credit card amount.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Michael", "last_name": "Smith", "dob": "1996-05-16"}),
            Action(name="get_client_details", kwargs={"client_id": "T10027"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00370"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00370", "reason": "switching destination"}),
            Action(name="search_packages", kwargs={"destination": "Sydney"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG031"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10027"}),
        ],
        outputs=[],
    ),

    # Task 13: Cancel + rebook at higher tier with points
    Task(
        user_id="T10019",
        instruction="Your email is matthew.thomas95@email.com. Cancel your Santorini booking BK00394 ($2965). You want to rebook Santorini but with business flight and suite hotel. Search Santorini packages. Book the 10-night one for yourself (DOB 1964-11-02). Use 4000 points ($2000) and credit card for the rest. With protection. What's the credit card amount?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "matthew.thomas95@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10019"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00394"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00394", "reason": "upgrading to better options"}),
            Action(name="search_packages", kwargs={"destination": "Santorini"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG016"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10019"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # F5: MULTI-COMPONENT MODIFICATION (airline tasks 3, 4, 19)
    # Change multiple components in one booking sequentially
    # =================================================================

    # Task 14: Upgrade flight + hotel + add activity (3 changes at once)
    Task(
        user_id="T10001",
        instruction="You are David Brown, born 1992-02-28. For booking BK00307 (New York), you want to: (1) upgrade flight from economy to business, (2) upgrade hotel from deluxe to suite, (3) change car from luxury to compact to save money. Make all changes. Tell me the net price difference and new total. Use credit card ending in 2113.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "David", "last_name": "Brown", "dob": "1992-02-28"}),
            Action(name="get_client_details", kwargs={"client_id": "T10001"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00307"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG026"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00307", "changes": [{"component_id": "PKG026_F", "new_option": "business"}, {"component_id": "PKG026_H", "new_option": "suite"}, {"component_id": "PKG026_C", "new_option": "compact"}], "payment_id": "cc_T10001_2122"}),
        ],
        outputs=[],
    ),

    # Task 15: Downgrade multiple components to save money
    Task(
        user_id="T10002",
        instruction="Your email is melissa.garcia19@email.com. For booking BK00363 (Rome, $10910), downgrade: flight to economy (already economy, skip), hotel from presidential to standard, car from SUV to compact, and skip both activities. Tell me the savings and new total. Credit card ending in 5272.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "melissa.garcia19@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10002"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00363"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG004"}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00363", "changes": [{"component_id": "PKG004_H", "new_option": "standard"}, {"component_id": "PKG004_C", "new_option": "compact"}, {"component_id": "PKG004_A1", "new_option": "skip"}, {"component_id": "PKG004_A2", "new_option": "skip"}], "payment_id": "cc_T10002_9565"}),
        ],
        outputs=[],
    ),

    # Task 16: Change travelers + change components
    Task(
        user_id="T10010",
        instruction="You are Wei Davis, born 1979-09-10. For booking BK00326 (Dubai, 3 travelers), replace the second traveler with James Davis (DOB 2005-08-20) and the third with Emily Davis (DOB 2008-11-03). Also upgrade the flight from business to first class. Use credit card ending in 7592.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Wei", "last_name": "Davis", "dob": "1979-09-10"}),
            Action(name="get_client_details", kwargs={"client_id": "T10010"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00326"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG030"}),
            Action(name="modify_booking_travelers", kwargs={"booking_id": "BK00326", "travelers": [{"first_name": "Wei", "last_name": "Davis", "dob": "1979-09-10"}, {"first_name": "James", "last_name": "Davis", "dob": "2005-08-20"}, {"first_name": "Emily", "last_name": "Davis", "dob": "2008-11-03"}]}),
            Action(name="modify_booking_options", kwargs={"booking_id": "BK00326", "changes": [{"component_id": "PKG030_F", "new_option": "first_class"}], "payment_id": "cc_T10010_7691"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # POLICY COMPLIANCE (API doesn't check)
    # =================================================================

    # Task 17: Cancel without protection, <3 days → no refund (agent must check)
    Task(
        user_id="T10078",
        instruction="Your email is aisha.walker20@mail.com. You want to cancel your Bangkok booking BK00398. It starts June 12 and has no trip protection. You want a full refund. If the agent explains the refund policy, insist for 2 rounds then accept.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "aisha.walker20@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10078"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00398"}),
        ],
        outputs=[],
    ),

    # Task 18: Try to add trip protection after booking → refuse
    Task(
        user_id="T10003",
        instruction="You are Robert Torres, born 1973-09-09. You forgot to add trip protection to booking BK00082 (Cancun). Can you add it now? If not, what are your cancellation options?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Robert", "last_name": "Torres", "dob": "1973-09-09"}),
            Action(name="get_client_details", kwargs={"client_id": "T10003"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00082"}),
        ],
        outputs=[],
    ),

    # Task 19: Gold member cancellation → at least 50% refund guaranteed
    Task(
        user_id="T10010",
        instruction="Your email is wei.davis95@mail.com. You're a gold member. Cancel booking BK00107 (Santorini, no protection, starts June 23). As a gold member you should get at least 50% refund. Confirm the refund amount.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "wei.davis95@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10010"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00107"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00107", "reason": "change of plans"}),
        ],
        outputs=["3000"],
    ),

    # =================================================================
    # ADVERSARIAL / CHANGE MIND / INFO WITHHOLDING
    # =================================================================

    # Task 20: Doesn't know booking ID, gives wrong destination first
    Task(
        user_id="T10099",
        instruction="Your email is william.miller10@inbox.com. You have a booking in Japan but don't remember the ID. You initially say it's Tokyo but actually it's Kyoto. When the agent can't find a Tokyo booking, correct yourself. You want to check the details.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "william.miller10@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10099"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00343"}),
        ],
        outputs=[],
    ),

    # Task 21: Wants to cancel everything, then changes mind
    Task(
        user_id="T10096",
        instruction="You are Ethan Brown, born 1968-09-07. You're stressed and want to cancel ALL your bookings. After the agent checks them, you realize the Swiss Alps trip BK00181 is your anniversary trip. Just cancel the Costa Rica ones (BK00161 and BK00246). Keep the Swiss Alps.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Ethan", "last_name": "Brown", "dob": "1968-09-07"}),
            Action(name="get_client_details", kwargs={"client_id": "T10096"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00161"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00181"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00246"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00161", "reason": "change of plans"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00246", "reason": "change of plans"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # COMPENSATION + TRANSFER
    # =================================================================

    # Task 22: Gold member complains about past trip → gets points
    Task(
        user_id="T10066",
        instruction="Your email is andrew.hall46@mail.com. You're a gold member. Your recent Bali trip (BK00362) was terrible - the hotel was nothing like the pictures and the activity was cancelled. That's 2 affected components. You want compensation (200 points per component).",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "andrew.hall46@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10066"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00362"}),
            Action(name="add_loyalty_points", kwargs={"client_id": "T10066", "points": 400}),
        ],
        outputs=["400"],
    ),

    # Task 23: Standard member requests compensation → transfer
    Task(
        user_id="T10001",
        instruction="You are David Brown, born 1992-02-28. Standard tier. Your Swiss Alps trip (BK00199) had a terrible hotel experience. You want compensation. If the agent says standard members can't get automated compensation, ask to speak with someone who can help.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "David", "last_name": "Brown", "dob": "1992-02-28"}),
            Action(name="get_client_details", kwargs={"client_id": "T10001"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00199"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Standard tier client requesting compensation for bad hotel experience on Swiss Alps trip BK00199. Per policy, standard members must be transferred for compensation."}),
        ],
        outputs=[],
    ),

    # Task 24: Complex end-to-end: check all → cancel some → rebook → pay with split
    Task(
        user_id="T10033",
        instruction="Your email is amanda.robinson14@mail.com. Check all your confirmed bookings. Cancel the Santorini one (BK00251). Then search for a Maldives 7-night package. Book it for yourself (DOB 2000-08-03), business flight, deluxe hotel. With protection. Pay with $300 voucher, 1000 points ($500), and credit card 6460 for the rest. Calculate everything.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "amanda.robinson14@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "T10033"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00251"}),
            Action(name="get_booking_details", kwargs={"booking_id": "BK00257"}),
            Action(name="cancel_booking", kwargs={"booking_id": "BK00251", "reason": "switching to Maldives"}),
            Action(name="search_packages", kwargs={"destination": "Maldives"}),
            Action(name="get_package_details", kwargs={"package_id": "PKG034"}),
            Action(name="get_payment_summary", kwargs={"client_id": "T10033"}),
        ],
        outputs=[],
    ),
]
