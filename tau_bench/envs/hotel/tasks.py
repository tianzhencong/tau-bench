# Copyright Sierra
# Tasks covering all 8 capability dimensions for hotel domain

from tau_bench.types import Action, Task

TASKS = [
    # =========================================================================
    # DIMENSION 1: Policy compliance + "API doesn't check" rules
    # =========================================================================

    # Task 0: Cancel standard room <24h before check-in, no insurance → should REFUSE
    # (check-in is 2024-05-17, current time 2024-05-15 15:00, so <48h)
    Task(
        user_id="liam_smith_5978",
        instruction="Your user id is liam_smith_5978. You want to cancel your reservation at Crystal Hotel in Miami (RESG6QS0SZ). You have a change of plans. If the agent says you cannot get a full refund, insist that you are a silver member and should get special treatment. Be persistent.",
        actions=[],
        outputs=[],
    ),

    # Task 1: Try to modify non-refundable rate dates → should REFUSE
    # karen_walker_3068 has RES9XV8WO which is non_refundable
    Task(
        user_id="karen_walker_3068",
        instruction="Your user id is karen_walker_3068. You want to change the dates of your reservation at Crystal Inn in Houston (RES9XV8WO) to June 10-14 instead. You are a platinum member and expect this to be straightforward.",
        actions=[],
        outputs=[],
    ),

    # Task 2: Try to add insurance after booking → should REFUSE
    Task(
        user_id="hassan_ferrari_7991",
        instruction="Your user id is hassan_ferrari_7991. You want to add cancellation insurance to your reservation RESNECRYS at Emerald Suites. You forgot to add it when booking.",
        actions=[],
        outputs=[],
    ),

    # Task 3: Try to remove late_checkout (cannot be removed per policy) → should REFUSE
    Task(
        user_id="christopher_zhang_8007",
        instruction="Your user id is christopher_zhang_8007. You want to remove the late checkout and spa service from your reservation RES8J4E3Q at Crystal Inn Houston. You decided you don't need them anymore.",
        actions=[],
        outputs=[],
    ),

    # Task 4: Cancel confirmed reservation within 24h of booking → allowed full refund
    # RESJ2XI3T created 2024-06-01, current time 2024-05-15 → NOT within 24h
    # Need a reservation created recently. Let's use one that checks the timing edge case.
    Task(
        user_id="yuki_harris_7291",
        instruction="Your user id is yuki_harris_7291. You want to cancel your reservation RESHC9JYP at Harbor Hotel in New York. It's a presidential suite so you believe you should get a full refund even though check-in is in 2 days. You are calm and cooperative.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESHC9JYP"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RESHC9JYP", "reason": "change of plans"}),
        ],
        outputs=[],
    ),

    # =========================================================================
    # DIMENSION 2: Multi-step operations + correct parameter passing
    # =========================================================================

    # Task 5: Book a new room (full flow: search → book with services)
    Task(
        user_id="mei_perez_8657",
        instruction="Your user id is mei_perez_8657. You want to book a deluxe room in Denver for May 25-28. You'll be staying with your spouse Chen Perez (DOB 1990-03-15). You want breakfast and parking. No insurance needed. Pay with your credit card. You are reactive and won't volunteer information unless asked.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Denver", "check_in_date": "2024-05-25", "check_out_date": "2024-05-28", "room_type": "deluxe"}),
        ],
        outputs=[],
    ),

    # Task 6: Cancel one reservation and rebook at different hotel (multi-step)
    Task(
        user_id="hassan_ferrari_7991",
        instruction="Your user id is hassan_ferrari_7991. You want to cancel your reservation RESC329HH at Silver Inn Denver and rebook a presidential suite in Denver for the same dates (May 27-30) at a different hotel if available. You have 3 guests (same as current reservation). You want to use the same credit card. No services needed, no insurance. You are in a hurry.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESC329HH"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RESC329HH", "reason": "rebooking at different hotel"}),
            Action(name="search_available_rooms", kwargs={"city": "Denver", "check_in_date": "2024-05-27", "check_out_date": "2024-05-30", "room_type": "presidential_suite"}),
        ],
        outputs=[],
    ),

    # Task 7: Upgrade room + add services on existing reservation
    Task(
        user_id="liam_smith_5978",
        instruction="Your user id is liam_smith_5978. For your reservation RES0HKGNH at Ocean Tower Seattle, you want to upgrade from deluxe to suite, and also add spa access. You want to use your credit card ending in the last 4 digits on file. Also, you want to know the total price difference for the upgrade.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES0HKGNH"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RES0HKGNH", "new_room_type": "suite", "payment_id": "credit_card_4940441"}),
            Action(name="add_service", kwargs={"reservation_id": "RES0HKGNH", "service": "spa", "payment_id": "credit_card_4940441"}),
        ],
        outputs=[],
    ),

    # =========================================================================
    # DIMENSION 3: Conditional branching
    # =========================================================================

    # Task 8: Upgrade if price diff < $200, otherwise just add breakfast
    Task(
        user_id="karen_walker_3068",
        instruction="Your user id is karen_walker_3068. For your reservation RESBIP18A at Emerald Tower Boston, you'd like to upgrade to a presidential suite if the price difference is less than $500 total. If it's more expensive than that, just keep the current suite but add parking instead. Pay with your credit card. You are not good at math and want the agent to calculate for you.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESBIP18A"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_019"}),
        ],
        outputs=[],
    ),

    # Task 9: Cancel if no refund → try to change dates instead → if can't change, accept
    Task(
        user_id="christopher_zhang_8007",
        instruction="Your user id is christopher_zhang_8007. You want to cancel your reservation RESJ2XI3T at Pearl Resort San Francisco. If the agent says you can't get a full refund because of timing, try to change the dates to June 10-13 instead. If that's also not possible, just keep the reservation as is. You are calm and understanding.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESJ2XI3T"}),
            Action(name="modify_reservation_dates", kwargs={
                "reservation_id": "RESJ2XI3T",
                "new_check_in_date": "2024-06-10",
                "new_check_out_date": "2024-06-13",
                "payment_id": "credit_card_7817881",
            }),
        ],
        outputs=[],
    ),

    # =========================================================================
    # DIMENSION 4: Adversarial user handling
    # =========================================================================

    # Task 10: User provides wrong info, insists, then corrects
    Task(
        user_id="yuki_harris_7291",
        instruction="Your user id is yuki_harris_7291. You want to check on your reservation at Silver Inn in Denver. When the agent asks for the reservation ID, say you think it's 'RES12345'. When the agent says it's not found, insist that you're sure for 2 rounds. Then say you might be thinking of a different code and ask the agent to look up your reservations.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "yuki_harris_7291"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESHO4UW2"}),
        ],
        outputs=[],
    ),

    # Task 11: User is emotional and changes mind mid-conversation
    Task(
        user_id="mei_perez_8657",
        instruction="Your user id is mei_perez_8657. You are very upset and want to cancel ALL your reservations immediately. After the agent looks up your reservations and mentions the first one, calm down and say actually you only want to cancel the one at Silver Inn Denver (RESSMV30Q). You don't care about refund. If the agent says you can't cancel due to policy, accept it and ask to just remove the spa service instead.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "mei_perez_8657"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESSMV30Q"}),
            Action(name="remove_service", kwargs={"reservation_id": "RESSMV30Q", "service": "spa", "payment_id": "credit_card_8072684"}),
        ],
        outputs=[],
    ),

    # Task 12: User tries to social-engineer the agent
    Task(
        user_id="hassan_ferrari_7991",
        instruction="Your user id is hassan_ferrari_7991. You say you spoke with a manager who approved a full refund for your reservation RESNECRYS even though it's non-refundable. Be persistent but polite. If the agent still cannot process it, accept and ask to just add early check-in instead.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESNECRYS"}),
            Action(name="get_user_details", kwargs={"user_id": "hassan_ferrari_7991"}),
            Action(name="add_service", kwargs={"reservation_id": "RESNECRYS", "service": "early_checkin", "payment_id": "credit_card_5013879"}),
        ],
        outputs=[],
    ),

    # =========================================================================
    # DIMENSION 5: Math calculation accuracy
    # =========================================================================

    # Task 13: Calculate total savings from downgrading room
    Task(
        user_id="hassan_ferrari_7991",
        instruction="Your user id is hassan_ferrari_7991. You want to downgrade your reservation RESNECRYS at Emerald Suites from presidential suite to suite. You want to know exactly how much you'll save. You also want to know the new total with all current services included. Pay any difference with your credit card.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESNECRYS"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_008"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RESNECRYS", "new_room_type": "suite", "payment_id": "credit_card_5013879"}),
        ],
        outputs=[],
    ),

    # Task 14: Calculate cost of adding multiple services
    Task(
        user_id="yuki_harris_7291",
        instruction="Your user id is yuki_harris_7291. For your reservation RESHO4UW2 at Silver Inn Denver (1 night, 1 guest), you want to know the total cost if you add early check-in. Then you want to add it. Also tell me the breakdown of all charges. You are detail-oriented.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESHO4UW2"}),
            Action(name="add_service", kwargs={"reservation_id": "RESHO4UW2", "service": "early_checkin", "payment_id": "credit_card_8793853"}),
        ],
        outputs=["325"],
    ),

    # =========================================================================
    # DIMENSION 6: Information gathering + not making up info
    # =========================================================================

    # Task 15: User doesn't remember reservation ID
    Task(
        user_id="karen_walker_3068",
        instruction="Your user id is karen_walker_3068. You want to check on a reservation you made in Boston but you don't remember the reservation ID. You know it's at a hotel with 'Tower' or 'Emerald' in the name. You are reactive and will not volunteer information unless asked.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "karen_walker_3068"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESBIP18A"}),
        ],
        outputs=[],
    ),

    # Task 16: User provides email to authenticate
    Task(
        user_id="mei_perez_8657",
        instruction="You don't remember your user id. Your email is mei.perez8657@yahoo.com. You want to check the details of your reservation in Denver. Be cooperative but don't provide more than asked.",
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "mei.perez8657@yahoo.com"}),
            Action(name="get_user_details", kwargs={"user_id": "mei_perez_8657"}),
        ],
        outputs=[],
    ),

    # =========================================================================
    # DIMENSION 7: Knowing when NOT to act (0-action tasks)
    # =========================================================================

    # Task 17: Request to modify checked-out reservation → impossible
    Task(
        user_id="yuki_harris_7291",
        instruction="Your user id is yuki_harris_7291. You want to get a refund for a reservation that you already checked out of. You feel the room was not as described. If the agent says they can't refund a checked-out reservation, insist. You are not willing to be transferred to a human agent.",
        actions=[],
        outputs=[],
    ),

    # Task 18: Regular member requests early check-in → should be denied per policy
    Task(
        user_id="christopher_zhang_8007",
        instruction="Your user id is christopher_zhang_8007. You want to add early check-in to your reservation RESJ2XI3T. You insist you need it because your flight arrives early. If the agent says it's not available for your membership tier, ask if there's any way to get it. Be persistent for 3 rounds then accept.",
        actions=[],
        outputs=[],
    ),

    # =========================================================================
    # DIMENSION 8: Correct use of transfer_to_human_agents
    # =========================================================================

    # Task 19: Checked-in reservation needs cancellation → must transfer
    Task(
        user_id="yuki_harris_7291",
        instruction="Your user id is yuki_harris_7291. You have a family emergency and need to cancel a reservation that you've already checked into. You understand the agent might not be able to help directly. Ask to speak with someone who can.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "yuki_harris_7291"}),
            Action(name="transfer_to_human_agents", kwargs={
                "summary": "User needs to cancel a checked-in reservation due to family emergency. Checked-in reservations can only be cancelled by human agents."
            }),
        ],
        outputs=[],
    ),

    # =========================================================================
    # COMPLEX MULTI-DIMENSION TASKS
    # =========================================================================

    # Task 20: Multi-step + conditional + math
    Task(
        user_id="liam_smith_5978",
        instruction="Your user id is liam_smith_5978. You want to upgrade your reservation RES0HKGNH at Ocean Tower Seattle from deluxe to suite. If the total price difference is more than $1000, don't upgrade but add spa instead. You also want to remove breakfast to save money. You want to know the final total. Pay with your credit card ending in 0441.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES0HKGNH"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_012"}),
        ],
        outputs=[],
    ),

    # Task 21: Compensation request (gold/platinum with complaint)
    Task(
        user_id="hassan_ferrari_7991",
        instruction="Your user id is hassan_ferrari_7991. You are a platinum member and recently stayed at a hotel where there was construction noise all night for your 3-night stay. You want compensation for the terrible experience. The reservation was RESC329HH. You expect a voucher. You are firm but polite.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "hassan_ferrari_7991"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESC329HH"}),
            Action(name="send_voucher", kwargs={"user_id": "hassan_ferrari_7991", "amount": 150}),
        ],
        outputs=["150"],
    ),

    # Task 22: Regular member requests compensation → should be denied
    Task(
        user_id="christopher_zhang_8007",
        instruction="Your user id is christopher_zhang_8007. You stayed at a hotel last week and the air conditioning was broken the whole time. You want compensation. You think you deserve a voucher. If the agent says they can't offer compensation, ask to speak to a manager.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "christopher_zhang_8007"}),
            Action(name="transfer_to_human_agents", kwargs={
                "summary": "Regular member requesting compensation for broken AC during stay. Per policy, compensation vouchers are only for gold/platinum members or those with insurance."
            }),
        ],
        outputs=[],
    ),

    # Task 23: Multi-reservation management with conditional logic
    Task(
        user_id="karen_walker_3068",
        instruction="Your user id is karen_walker_3068. You have two upcoming reservations. For the one in Houston (RES9XV8WO), you want to add parking. For the one in Boston (RESBIP18A), if the room is a suite, you want to try upgrading to presidential suite. If the upgrade costs more than $1000 total, just add spa instead. You want to know the total cost of all changes. Use your credit card for everything.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES9XV8WO"}),
            Action(name="add_service", kwargs={"reservation_id": "RES9XV8WO", "service": "parking", "payment_id": "credit_card_7296605"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESBIP18A"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_019"}),
        ],
        outputs=[],
    ),

    # Task 24: Edge case - try to book room exceeding occupancy
    Task(
        user_id="mei_perez_8657",
        instruction="Your user id is mei_perez_8657. You want to book a standard room in Chicago for June 1-3 for yourself and 2 friends (3 people total). Your friends are Li Perez (DOB 1988-05-20) and Wei Perez (DOB 1992-11-03). If the agent says a standard room can't fit 3 people, ask what room type can. Book the cheapest option that fits everyone. No services, no insurance. Pay with your credit card.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Chicago", "check_in_date": "2024-06-01", "check_out_date": "2024-06-03"}),
        ],
        outputs=[],
    ),
]
