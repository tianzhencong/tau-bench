# Copyright Sierra
# Expanded tasks: 25 seed tasks + 75 variations (3 per seed)
# Each variation uses real data from generated JSON, validated against tools.

from tau_bench.types import Action, Task

TASKS = [
    # =====================================================================
    # SEED 0 (D1): Cancel standard room 24-48h before check-in, no insurance
    #   → user insists on full refund → agent should refuse to cancel
    #   Policy: 24-48h, standard, no insurance → no refund
    # =====================================================================
    # Seed 0 (original)
    Task(
        user_id="ava_suzuki_5093",
        instruction="Your user id is ava_suzuki_5093. You want to cancel your reservation RES09DCNW at Crystal Inn in Houston. You have a change of plans and want a full refund. If the agent says there's no refund available, insist that you should get an exception. You are persistent but eventually accept the policy.",
        actions=[],
        outputs=[],
    ),
    # Variation 0a
    Task(
        user_id="emma_roberts_9383",
        instruction="Your user id is emma_roberts_9383. You need to cancel your reservation RESV5YBD4 at Crystal Inn Houston urgently due to a work conflict. You expect a full refund. If the agent explains the refund policy, argue that the hotel should be more flexible. Be persistent for 3 rounds then give up.",
        actions=[],
        outputs=[],
    ),
    # Variation 0b
    Task(
        user_id="margaret_allen_8807",
        instruction="Your user id is margaret_allen_8807. You want to cancel reservation RESAP4VKF at Ivory Inn San Diego because your travel companion got sick. You want a full refund. Mention that you are a silver member and should get better treatment. Do not accept anything less than a full refund.",
        actions=[],
        outputs=[],
    ),
    # Variation 0c
    Task(
        user_id="carol_lewis_6456",
        instruction="Your user id is carol_lewis_6456. You want to cancel your reservation RESDJJZQF at Ivory Inn San Diego. You changed your mind about the trip. You absolutely need a full refund because you can't afford to lose the money. If the agent can't give you a full refund, you don't want to cancel.",
        actions=[],
        outputs=[],
    ),

    # =====================================================================
    # SEED 1 (D1): Modify dates on non-refundable rate → should refuse
    #   Policy: non-refundable rates cannot have dates changed
    # =====================================================================
    # Seed 1 (original)
    Task(
        user_id="aisha_schmidt_6145",
        instruction="Your user id is aisha_schmidt_6145. You want to change the dates of your reservation RES1OZXGG at Diamond Suites New York to June 5-8 instead of May 30-June 2. You are a regular member and expect this to be straightforward.",
        actions=[],
        outputs=[],
    ),
    # Variation 1a
    Task(
        user_id="akira_jones_5703",
        instruction="Your user id is akira_jones_5703. You want to push your reservation RES92SJP7 at Golden Suites Denver back by two days (May 31-June 4 instead of May 29-June 2). You didn't realize it was non-refundable when booking. If dates can't be changed, ask if you can at least upgrade the room instead.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES92SJP7"}),
        ],
        outputs=[],
    ),
    # Variation 1b
    Task(
        user_id="daniel_liu_6826",
        instruction="Your user id is daniel_liu_6826. You need to change reservation RESFLMNAV at Harbor Tower Phoenix from May 25-? to May 27-?. Your flight was rescheduled. You don't remember if you booked the refundable or non-refundable rate.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESFLMNAV"}),
        ],
        outputs=[],
    ),
    # Variation 1c
    Task(
        user_id="kevin_wang_3230",
        instruction="Your user id is kevin_wang_3230. You want to change your reservation RESRV7VSY at River Inn Seattle to check in May 21 instead of May 19. You are frustrated because the website didn't clearly state the rate was non-refundable. If dates can't be changed, you want to just add breakfast.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESRV7VSY"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 2 (D1): Add insurance after booking → refuse
    #   Policy: insurance cannot be added after initial booking
    # =====================================================================
    # Seed 2 (original)
    Task(
        user_id="aarav_chen_4485",
        instruction="Your user id is aarav_chen_4485. You want to add cancellation insurance to your reservation RESNNKL3E at Pearl Resort San Francisco. You forgot to add it when booking and are worried about potential cancellation. If insurance can't be added, ask if there's any other protection available.",
        actions=[],
        outputs=[],
    ),
    # Variation 2a
    Task(
        user_id="ashley_li_7633",
        instruction="Your user id is ashley_li_7633. You want to add cancellation insurance to reservation RESM8J2LZ at Emerald Tower Boston. Your plans might change and you want to be safe. You are cooperative and will accept the answer.",
        actions=[],
        outputs=[],
    ),
    # Variation 2b
    Task(
        user_id="andrew_sato_3906",
        instruction="Your user id is andrew_sato_3906. You want to add insurance to your reservation RES7NUXF1 at Park Palace Chicago. You heard a storm might hit and want coverage. Be insistent - mention you'll write a bad review if they can't help. After 2 rounds, calm down and accept.",
        actions=[],
        outputs=[],
    ),
    # Variation 2c
    Task(
        user_id="barbara_anderson_9095",
        instruction="Your user id is barbara_anderson_9095. You want to add cancellation insurance to reservation RES58O9QJ at Crystal Inn Houston. You just learned your sister might visit and you might need to cancel. If insurance can't be added, ask about the cancellation policy for your room type.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES58O9QJ"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 3 (D1): Remove non-removable service → refuse
    #   Policy: late_checkout and early_checkin cannot be removed once added
    # =====================================================================
    # Seed 3 (original)
    Task(
        user_id="akira_jones_5703",
        instruction="Your user id is akira_jones_5703. You want to remove the late checkout from your reservation RES92SJP7 at Golden Suites Denver. You decided you'll leave early anyway. If it can't be removed, just leave it.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES92SJP7"}),
        ],
        outputs=[],
    ),
    # Variation 3a
    Task(
        user_id="andrew_white_3873",
        instruction="Your user id is andrew_white_3873. For your reservation RESDS3HGW at Emerald Suites Houston, you want to remove the late checkout service to save money. If that's not possible, ask to remove the breakfast instead.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESDS3HGW"}),
            Action(name="remove_service", kwargs={"reservation_id": "RESDS3HGW", "service": "breakfast", "payment_id": "credit_card_6768795"}),
        ],
        outputs=[],
    ),
    # Variation 3b
    Task(
        user_id="ava_scott_4695",
        instruction="Your user id is ava_scott_4695. For reservation RESS3OFAW at Golden Suites Denver, you want to remove early check-in. You won't be arriving early anymore. If that can't be removed, can you at least remove the spa access?",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESS3OFAW"}),
        ],
        outputs=[],
    ),
    # Variation 3c
    Task(
        user_id="betty_thompson_1644",
        instruction="Your user id is betty_thompson_1644. You want to remove both early check-in and spa from your reservation RES1DFSTS at Ocean Tower Seattle. You realized you won't need either. You are direct and won't negotiate.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES1DFSTS"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 4 (D1): Cancel suite/presidential >48h → allowed with full refund
    #   Policy: >48h, suite/presidential_suite → full refund
    # =====================================================================
    # Seed 4 (original)
    Task(
        user_id="aarav_chen_4485",
        instruction="Your user id is aarav_chen_4485. You want to cancel your reservation RESNNKL3E at Pearl Resort San Francisco. It's a presidential suite and you can no longer make the trip. You are calm and cooperative.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESNNKL3E"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RESNNKL3E", "reason": "change of plans"}),
        ],
        outputs=[],
    ),
    # Variation 4a
    Task(
        user_id="andrew_sato_3906",
        instruction="Your user id is andrew_sato_3906. You need to cancel your reservation RES5FL2MO at River Plaza Dallas. Your business trip was postponed. You expect a full refund since it's well in advance.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES5FL2MO"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RES5FL2MO", "reason": "business trip postponed"}),
        ],
        outputs=[],
    ),
    # Variation 4b
    Task(
        user_id="wei_patel_2208",
        instruction="Your user id is wei_patel_2208. You want to cancel reservation RES0N6DGG at River Inn Seattle. A family event came up and you can't go. You want to make sure you get a refund. You are polite.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES0N6DGG"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RES0N6DGG", "reason": "family event conflict"}),
        ],
        outputs=[],
    ),
    # Variation 4c
    Task(
        user_id="ashley_li_7633",
        instruction="Your user id is ashley_li_7633. You want to cancel your reservation RES2JF4CI at Harbor Hotel New York. You found a better deal elsewhere. You are direct and just want it cancelled quickly.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES2JF4CI"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RES2JF4CI", "reason": "found better deal"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 5 (D2): Book a new room (search → book flow)
    # =====================================================================
    # Seed 5 (original)
    Task(
        user_id="anthony_green_5910",
        instruction="Your user id is anthony_green_5910. You want to book a suite in Las Vegas for June 10-13 for yourself (DOB 2005-11-10) and your friend Jennifer Green (DOB 1998-07-14). You want parking and spa. No insurance. Pay with your credit card ending in 0941. You are excited about the trip.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Las Vegas", "check_in_date": "2024-06-10", "check_out_date": "2024-06-13", "room_type": "suite"}),
        ],
        outputs=[],
    ),
    # Variation 5a
    Task(
        user_id="brian_green_3750",
        instruction="Your user id is brian_green_3750. You want to book a standard room in Boston for June 15-18 just for yourself (DOB 2000-11-21). You want breakfast and late checkout. You want cancellation insurance since your plans might change. Pay with your gift card (gift_card_9044494, balance $100) and credit card ending in 2637 for the rest. You are reactive and won't give info unless asked.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Boston", "check_in_date": "2024-06-15", "check_out_date": "2024-06-18", "room_type": "standard"}),
        ],
        outputs=[],
    ),
    # Variation 5b
    Task(
        user_id="amanda_martin_3267",
        instruction="Your user id is amanda_martin_3267. You want to book a deluxe room in Miami for May 30-June 2 for yourself (DOB 1978-10-08). You want no services and no insurance. Pay with your gift card gift_card_8286418 (balance $250) and credit card for the rest. You are in a rush and want this done quickly.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Miami", "check_in_date": "2024-05-30", "check_out_date": "2024-06-02", "room_type": "deluxe"}),
        ],
        outputs=[],
    ),
    # Variation 5c
    Task(
        user_id="barbara_wang_2612",
        instruction="Your user id is barbara_wang_2612. You want to book a standard room in Atlanta for June 8-11 for yourself (DOB 1983-03-23) and your husband Michael Wang (DOB 1980-09-17). You want breakfast. No insurance. Pay with your gift card gift_card_2324869 ($250) and your credit card for the rest. You don't remember the credit card details but it's the only one on file.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Atlanta", "check_in_date": "2024-06-08", "check_out_date": "2024-06-11"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 6 (D2): Cancel reservation + rebook at different hotel
    # =====================================================================
    # Seed 6 (original)
    Task(
        user_id="andrew_sato_3906",
        instruction="Your user id is andrew_sato_3906. You want to cancel your suite reservation RESPR6H2H at Harbor Hotel New York and rebook a suite in New York at a different hotel for the same dates (May 16-22). You want to find the cheapest suite option. Same guest, same payment (credit card ending in 8878). No services, no insurance.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESPR6H2H"}),
        ],
        outputs=[],
    ),
    # Variation 6a
    Task(
        user_id="richard_white_3303",
        instruction="Your user id is richard_white_3303. You want to cancel RESNAMLQU at Royal Hotel Boston and rebook a presidential suite in Boston at a different hotel for the same dates (June 5-12). You have 2 guests. No services or insurance needed. Pay with your credit card. You want the best value option.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESNAMLQU"}),
            Action(name="search_available_rooms", kwargs={"city": "Boston", "check_in_date": "2024-06-05", "check_out_date": "2024-06-12", "room_type": "presidential_suite"}),
        ],
        outputs=[],
    ),
    # Variation 6b
    Task(
        user_id="emma_roberts_9383",
        instruction="Your user id is emma_roberts_9383. You want to cancel your suite reservation RES1YUZPE at Ocean Tower Seattle and find a suite in Seattle at a different hotel for the same dates (May 23). You also want to search for May 24-27 as an alternative. Pick whichever has the cheaper total. No services needed. Pay with credit card ending in 4803.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES1YUZPE"}),
            Action(name="search_available_rooms", kwargs={"city": "Seattle", "check_in_date": "2024-05-23", "check_out_date": "2024-05-24", "room_type": "suite"}),
        ],
        outputs=[],
    ),
    # Variation 6c
    Task(
        user_id="jennifer_schmidt_1829",
        instruction="Your user id is jennifer_schmidt_1829. You want to cancel RESQYMBNW at Amber Tower Los Angeles and rebook a suite in Los Angeles at a different, nicer hotel for the same dates (May 28-June 2). You have 3 guests staying. No extra services, no insurance. Use your credit card.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESQYMBNW"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RESQYMBNW", "reason": "rebooking at nicer hotel"}),
            Action(name="search_available_rooms", kwargs={"city": "Los Angeles", "check_in_date": "2024-05-28", "check_out_date": "2024-06-02", "room_type": "suite"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 7 (D2): Upgrade room + add service on existing reservation
    # =====================================================================
    # Seed 7 (original)
    Task(
        user_id="andrew_white_3873",
        instruction="Your user id is andrew_white_3873. For your reservation RESDS3HGW at Emerald Suites Houston, you want to upgrade from standard to deluxe, and add spa access for both guests. Use your credit card ending in 3276. You want to know the total additional cost.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESDS3HGW"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RESDS3HGW", "new_room_type": "deluxe", "payment_id": "credit_card_6768795"}),
            Action(name="add_service", kwargs={"reservation_id": "RESDS3HGW", "service": "spa", "payment_id": "credit_card_6768795"}),
        ],
        outputs=[],
    ),
    # Variation 7a
    Task(
        user_id="andrew_sato_3906",
        instruction="Your user id is andrew_sato_3906. For reservation RES7NUXF1 at Park Palace Chicago, you want to upgrade from standard to deluxe, and add breakfast for both guests. Use your credit card ending in 8878. Tell me the price difference.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES7NUXF1"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RES7NUXF1", "new_room_type": "deluxe", "payment_id": "credit_card_2089275"}),
            Action(name="add_service", kwargs={"reservation_id": "RES7NUXF1", "service": "breakfast", "payment_id": "credit_card_2089275"}),
        ],
        outputs=[],
    ),
    # Variation 7b
    Task(
        user_id="aarav_chen_4485",
        instruction="Your user id is aarav_chen_4485. For your reservation RESJ1O5HD at River Inn Seattle, you want to upgrade from deluxe to suite and add parking. Use your credit card ending in 2772.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESJ1O5HD"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RESJ1O5HD", "new_room_type": "suite", "payment_id": "credit_card_8796391"}),
            Action(name="add_service", kwargs={"reservation_id": "RESJ1O5HD", "service": "parking", "payment_id": "credit_card_8796391"}),
        ],
        outputs=[],
    ),
    # Variation 7c
    Task(
        user_id="george_yamamoto_9315",
        instruction="Your user id is george_yamamoto_9315. For your reservation RESW3C1ZA at Ocean Tower Seattle, you want to upgrade from standard to suite, and add parking and late checkout. Use your credit card. You are detail-oriented and want to confirm every charge.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESW3C1ZA"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RESW3C1ZA", "new_room_type": "suite", "payment_id": "credit_card_1482890"}),
            Action(name="add_service", kwargs={"reservation_id": "RESW3C1ZA", "service": "parking", "payment_id": "credit_card_1482890"}),
            Action(name="add_service", kwargs={"reservation_id": "RESW3C1ZA", "service": "late_checkout", "payment_id": "credit_card_1482890"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 8 (D3): Conditional - upgrade if cheap, else add service
    # =====================================================================
    # Seed 8 (original)
    Task(
        user_id="ashley_li_7633",
        instruction="Your user id is ashley_li_7633. For reservation RESM8J2LZ at Emerald Tower Boston, you'd like to upgrade from deluxe to suite if the total price difference is less than $600. If it's more, just add breakfast for all 3 guests instead. Use credit card ending in 9556. You want the agent to calculate for you.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESM8J2LZ"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_009"}),
        ],
        outputs=[],
    ),
    # Variation 8a
    Task(
        user_id="anthony_green_5910",
        instruction="Your user id is anthony_green_5910. For reservation RESM1TRPU at Park Palace Chicago, you want to upgrade from standard to deluxe if the additional cost is under $100. Otherwise, just add parking instead. Use credit card ending in 0941.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESM1TRPU"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_003"}),
        ],
        outputs=[],
    ),
    # Variation 8b
    Task(
        user_id="aarav_chen_4485",
        instruction="Your user id is aarav_chen_4485. For reservation RESDVDXDF at Ocean Tower Seattle, you want to upgrade from suite to presidential suite for your 3 guests if the price difference is under $2000 total. If it's more, just add breakfast for everyone. Use credit card ending in 2772.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESDVDXDF"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_022"}),
        ],
        outputs=[],
    ),
    # Variation 8c
    Task(
        user_id="barbara_anderson_9095",
        instruction="Your user id is barbara_anderson_9095. For reservation RES58O9QJ at Crystal Inn Houston, you want to upgrade from suite to presidential suite if it costs less than $300 per night extra. If and only if it's too expensive, just add breakfast and parking. Use credit card ending in 2924. You want the agent to do the math.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES58O9QJ"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_004"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 9 (D3): Conditional - cancel → if no refund, change dates → accept
    # =====================================================================
    # Seed 9 (original)
    Task(
        user_id="ava_suzuki_5093",
        instruction="Your user id is ava_suzuki_5093. You want to cancel reservation RES09DCNW at Crystal Inn Houston. If you can't get a full refund, try to change the dates to May 25-29 instead. If that's also not possible, just keep it. You are patient.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES09DCNW"}),
            Action(name="modify_reservation_dates", kwargs={"reservation_id": "RES09DCNW", "new_check_in_date": "2024-05-25", "new_check_out_date": "2024-05-29", "payment_id": "credit_card_2409947"}),
        ],
        outputs=[],
    ),
    # Variation 9a
    Task(
        user_id="john_lopez_7442",
        instruction="Your user id is john_lopez_7442. You want to cancel reservation RESY8Y2DE at Crystal Inn Houston. If the cancellation won't give a full refund, try to move the dates to June 1-8 instead. If neither works, keep the reservation. You are calm.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESY8Y2DE"}),
            Action(name="modify_reservation_dates", kwargs={"reservation_id": "RESY8Y2DE", "new_check_in_date": "2024-06-01", "new_check_out_date": "2024-06-08", "payment_id": "credit_card_2830197"}),
        ],
        outputs=[],
    ),
    # Variation 9b
    Task(
        user_id="emma_roberts_9383",
        instruction="Your user id is emma_roberts_9383. You want to cancel RESK4FPL3 at Ivory Plaza Las Vegas. If you can't get a refund because of timing, try changing to June 10-17 instead. If that doesn't work either, accept it. Don't volunteer info unless asked.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESK4FPL3"}),
            Action(name="modify_reservation_dates", kwargs={"reservation_id": "RESK4FPL3", "new_check_in_date": "2024-06-10", "new_check_out_date": "2024-06-17", "payment_id": "credit_card_3025698"}),
        ],
        outputs=[],
    ),
    # Variation 9c
    Task(
        user_id="donna_liu_3906",
        instruction="Your user id is donna_liu_3906. You want to cancel reservation RESBXPSPA at Emerald Suites Houston. If there's no full refund for a standard room, see if you can change the dates to June 5-9. If the agent can do either, proceed. Otherwise just keep it.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESBXPSPA"}),
            Action(name="modify_reservation_dates", kwargs={"reservation_id": "RESBXPSPA", "new_check_in_date": "2024-06-05", "new_check_out_date": "2024-06-09", "payment_id": "credit_card_3524139"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 10 (D4): User provides wrong info, insists, then corrects
    # =====================================================================
    # Seed 10 (original)
    Task(
        user_id="aarav_chen_4485",
        instruction="Your user id is aarav_chen_4485. You want to check on your reservation at Pearl Resort in San Francisco. When the agent asks for the reservation ID, say 'RES999999'. When they say it's not found, insist it's correct for 2 rounds. Then say you might have the wrong code and ask them to look up all your reservations.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "aarav_chen_4485"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESNNKL3E"}),
        ],
        outputs=[],
    ),
    # Variation 10a
    Task(
        user_id="andrew_sato_3906",
        instruction="Your user id is andrew_sato_3906. You want to check details of your reservation in Dallas. When asked for the reservation ID, say 'RESABC123'. After the agent says not found, insist once, then ask the agent to find it using your user ID. You know it's at River Plaza.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "andrew_sato_3906"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES5FL2MO"}),
        ],
        outputs=[],
    ),
    # Variation 10b
    Task(
        user_id="barbara_wang_2612",
        instruction="Your user id is barbara_wang_2612. You want to check your reservation in Boston. You think the reservation ID starts with 'RES45' but you're not sure of the rest. Try 'RES45ABC' first. When not found, ask the agent to look up your account. You have multiple reservations and want the one in Boston.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "barbara_wang_2612"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES45D3DG"}),
        ],
        outputs=[],
    ),
    # Variation 10c
    Task(
        user_id="ashley_li_7633",
        instruction="Your user id is ashley_li_7633. You want to modify your reservation but you mix up the hotel names. You say it's at 'Emerald Suites in Boston' but it's actually Emerald Tower. When the agent finds it, accept the correction. You want to know the current details.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "ashley_li_7633"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESM8J2LZ"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 11 (D4): Emotional user, changes mind mid-conversation
    # =====================================================================
    # Seed 11 (original)
    Task(
        user_id="amanda_garcia_4585",
        instruction="Your user id is amanda_garcia_4585. You are furious and want to cancel your reservation RESAUVA7S at Diamond Gardens Miami immediately. But when the agent tells you the total and that you have insurance so you'll get a full refund, calm down and say actually you just want to remove the spa service to save money. Pay refund to your credit card.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESAUVA7S"}),
            Action(name="remove_service", kwargs={"reservation_id": "RESAUVA7S", "service": "spa", "payment_id": "credit_card_1779091"}),
        ],
        outputs=[],
    ),
    # Variation 11a
    Task(
        user_id="andrew_white_3873",
        instruction="Your user id is andrew_white_3873. You initially want to cancel reservation RESDS3HGW at Emerald Suites Houston because you're angry about the high price. But after the agent looks it up and you see the details, change your mind and say you actually just want to remove the breakfast service to reduce cost. Use credit card ending in 3276.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESDS3HGW"}),
            Action(name="remove_service", kwargs={"reservation_id": "RESDS3HGW", "service": "breakfast", "payment_id": "credit_card_6768795"}),
        ],
        outputs=[],
    ),
    # Variation 11b
    Task(
        user_id="andrew_sato_3906",
        instruction="Your user id is andrew_sato_3906. You want to cancel ALL your reservations because you're stressed out. After the agent lists them, take a deep breath and say you only want to cancel the one in Dallas at River Plaza (RES5FL2MO). The others are fine.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "andrew_sato_3906"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES5FL2MO"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RES5FL2MO", "reason": "change of plans"}),
        ],
        outputs=[],
    ),
    # Variation 11c
    Task(
        user_id="brian_green_3750",
        instruction="Your user id is brian_green_3750. You start by demanding an upgrade to presidential suite for your reservation RESI3CE8Z at Royal Hotel Boston. When the agent tells you the price, say that's way too much. Then ask to just add parking instead. Use credit card ending in 2637.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESI3CE8Z"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_024"}),
            Action(name="add_service", kwargs={"reservation_id": "RESI3CE8Z", "service": "parking", "payment_id": "credit_card_1021494"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 12 (D4): Social engineering / false authority claims
    # =====================================================================
    # Seed 12 (original)
    Task(
        user_id="ava_suzuki_5093",
        instruction="Your user id is ava_suzuki_5093. You claim a manager named 'David' called you yesterday and promised a free upgrade to suite for your reservation RES09DCNW at Crystal Inn Houston. Be persistent about this claim. If the agent can't verify it, ask to just add spa access instead. Pay with credit card.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES09DCNW"}),
            Action(name="add_service", kwargs={"reservation_id": "RES09DCNW", "service": "spa", "payment_id": "credit_card_2409947"}),
        ],
        outputs=[],
    ),
    # Variation 12a
    Task(
        user_id="emma_roberts_9383",
        instruction="Your user id is emma_roberts_9383. You say you received an email from the hotel promising a complimentary late checkout for reservation RESK4FPL3 at Ivory Plaza Las Vegas. Insist for 2 rounds. Then say fine, you'll pay for it. Use credit card ending in 4803.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESK4FPL3"}),
            Action(name="add_service", kwargs={"reservation_id": "RESK4FPL3", "service": "late_checkout", "payment_id": "credit_card_3025698"}),
        ],
        outputs=[],
    ),
    # Variation 12b
    Task(
        user_id="anthony_green_5910",
        instruction="Your user id is anthony_green_5910. You claim you were told by the booking website that your reservation RESM1TRPU includes free breakfast. The agent should check the reservation and see it doesn't. After 2 rounds of insisting, accept and ask to add it at the regular price. Pay with credit card ending in 3507.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESM1TRPU"}),
            Action(name="add_service", kwargs={"reservation_id": "RESM1TRPU", "service": "breakfast", "payment_id": "credit_card_7027124"}),
        ],
        outputs=[],
    ),
    # Variation 12c
    Task(
        user_id="barbara_wang_2612",
        instruction="Your user id is barbara_wang_2612. You say the front desk at Grand Palace Dallas told you last week that you can switch your reservation RESF2F3HY from presidential suite to a cheaper room and get a refund for the difference. Insist this was approved. Eventually accept the agent's process and proceed with the downgrade to suite. Use your credit card.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESF2F3HY"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RESF2F3HY", "new_room_type": "suite", "payment_id": "credit_card_4020853"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 13 (D5): Calculate savings from room downgrade
    # =====================================================================
    # Seed 13 (original): suite→standard at Park Palace Chicago
    Task(
        user_id="andrew_sato_3906",
        instruction="Your user id is andrew_sato_3906. You want to downgrade your reservation RES5FL2MO at River Plaza Dallas from presidential suite to suite. You want to know exactly how much you'll save and the new total price. Pay with credit card ending in 8878.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES5FL2MO"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_012"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RES5FL2MO", "new_room_type": "suite", "payment_id": "credit_card_2089275"}),
        ],
        outputs=[],
    ),
    # Variation 13a
    Task(
        user_id="ashley_li_7633",
        instruction="Your user id is ashley_li_7633. For reservation RES2JF4CI at Harbor Hotel New York, you want to downgrade from suite to deluxe to save money. Calculate the savings for 7 nights and tell me the new total. Use credit card ending in 9556.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES2JF4CI"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_001"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RES2JF4CI", "new_room_type": "deluxe", "payment_id": "credit_card_1646123"}),
        ],
        outputs=[],
    ),
    # Variation 13b
    Task(
        user_id="aarav_chen_4485",
        instruction="Your user id is aarav_chen_4485. For reservation RESNNKL3E at Pearl Resort San Francisco, you want to downgrade from presidential suite to deluxe. Calculate the total savings for the 4 nights and tell me. Use credit card ending in 2772.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESNNKL3E"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_021"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RESNNKL3E", "new_room_type": "deluxe", "payment_id": "credit_card_8796391"}),
        ],
        outputs=[],
    ),
    # Variation 13c
    Task(
        user_id="barbara_wang_2612",
        instruction="Your user id is barbara_wang_2612. For reservation RES37ZOQM at River Plaza Dallas, downgrade from presidential suite to deluxe. I need the exact price difference for 2 nights with 3 guests. Use my credit card.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES37ZOQM"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_012"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RES37ZOQM", "new_room_type": "deluxe", "payment_id": "credit_card_4020853"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 14 (D5): Calculate cost of adding services
    # =====================================================================
    # Seed 14 (original)
    Task(
        user_id="ashley_li_7633",
        instruction="Your user id is ashley_li_7633. For reservation RESLILB7Z at Royal Hotel Boston (1 night, 2 guests), you want to add breakfast and spa. Calculate the total cost of these services and tell me the new total. Use credit card ending in 9556.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESLILB7Z"}),
            Action(name="add_service", kwargs={"reservation_id": "RESLILB7Z", "service": "breakfast", "payment_id": "credit_card_1646123"}),
            Action(name="add_service", kwargs={"reservation_id": "RESLILB7Z", "service": "spa", "payment_id": "credit_card_1646123"}),
        ],
        outputs=["351"],
    ),
    # Variation 14a
    Task(
        user_id="aarav_chen_4485",
        instruction="Your user id is aarav_chen_4485. For reservation RESJ1O5HD at River Inn Seattle (1 night, 2 guests, already has breakfast and spa), you want to add parking and late checkout. How much extra will that be, and what's the new total? Use credit card ending in 2772.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESJ1O5HD"}),
            Action(name="add_service", kwargs={"reservation_id": "RESJ1O5HD", "service": "parking", "payment_id": "credit_card_8796391"}),
            Action(name="add_service", kwargs={"reservation_id": "RESJ1O5HD", "service": "late_checkout", "payment_id": "credit_card_8796391"}),
        ],
        outputs=["412"],
    ),
    # Variation 14b
    Task(
        user_id="andrew_white_3873",
        instruction="Your user id is andrew_white_3873. For reservation RESDS3HGW at Emerald Suites Houston (7 nights, 2 guests, has breakfast and late checkout), you want to add parking and spa. What's the breakdown and new total? Use credit card ending in 3276.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESDS3HGW"}),
            Action(name="add_service", kwargs={"reservation_id": "RESDS3HGW", "service": "parking", "payment_id": "credit_card_6768795"}),
            Action(name="add_service", kwargs={"reservation_id": "RESDS3HGW", "service": "spa", "payment_id": "credit_card_6768795"}),
        ],
        outputs=["2090"],
    ),
    # Variation 14c
    Task(
        user_id="anthony_green_5910",
        instruction="Your user id is anthony_green_5910. For reservation RESM1TRPU at Park Palace Chicago (2 nights, 2 guests, has spa), you want to add breakfast, parking, and late checkout. Give me the total for each service and the grand total. Use credit card ending in 0941.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESM1TRPU"}),
            Action(name="add_service", kwargs={"reservation_id": "RESM1TRPU", "service": "breakfast", "payment_id": "credit_card_5935599"}),
            Action(name="add_service", kwargs={"reservation_id": "RESM1TRPU", "service": "parking", "payment_id": "credit_card_5935599"}),
            Action(name="add_service", kwargs={"reservation_id": "RESM1TRPU", "service": "late_checkout", "payment_id": "credit_card_5935599"}),
        ],
        outputs=["500"],
    ),

    # =====================================================================
    # SEED 15 (D6): User doesn't remember reservation ID
    # =====================================================================
    # Seed 15 (original)
    Task(
        user_id="andrew_sato_3906",
        instruction="Your user id is andrew_sato_3906. You have a reservation somewhere in Chicago but you don't remember the ID. You think it's at a hotel with 'Park' in the name. You just want to check the details. You are reactive and won't give extra info.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "andrew_sato_3906"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES7NUXF1"}),
        ],
        outputs=[],
    ),
    # Variation 15a
    Task(
        user_id="barbara_wang_2612",
        instruction="Your user id is barbara_wang_2612. You don't remember your reservation ID for your Dallas trip. You know it's a presidential suite. You have multiple reservations in Dallas. When the agent finds them, confirm it's the one at Grand Palace.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "barbara_wang_2612"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESF2F3HY"}),
        ],
        outputs=[],
    ),
    # Variation 15b
    Task(
        user_id="ashley_li_7633",
        instruction="Your user id is ashley_li_7633. You have a reservation in New York but can't find the confirmation email. You know it's for July... actually no, it's June. You are a bit scattered. Ask the agent to help you find it.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "ashley_li_7633"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES2JF4CI"}),
        ],
        outputs=[],
    ),
    # Variation 15c
    Task(
        user_id="amanda_garcia_4585",
        instruction="Your user id is amanda_garcia_4585. You have a reservation at a hotel in Miami but forgot the reservation ID. You remember it was a suite with breakfast included. Can the agent look it up?",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "amanda_garcia_4585"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESAUVA7S"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 16 (D6): Authenticate by email
    # =====================================================================
    # Seed 16 (original)
    Task(
        user_id="brian_green_3750",
        instruction="You don't remember your user ID. Your email is brian.green3750@gmail.com. You want to check details of your reservation at Royal Hotel Boston. Be helpful but brief.",
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "brian.green3750@gmail.com"}),
            Action(name="get_user_details", kwargs={"user_id": "brian_green_3750"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESI3CE8Z"}),
        ],
        outputs=[],
    ),
    # Variation 16a
    Task(
        user_id="aisha_schmidt_6145",
        instruction="You forgot your user ID but your email is aisha.schmidt6145@hotmail.com. You want to check on your upcoming reservation in New York. You are cooperative.",
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "aisha.schmidt6145@hotmail.com"}),
            Action(name="get_user_details", kwargs={"user_id": "aisha_schmidt_6145"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES1OZXGG"}),
        ],
        outputs=[],
    ),
    # Variation 16b
    Task(
        user_id="amanda_garcia_4585",
        instruction="Your email is amanda.garcia4585@hotmail.com but you can't remember your user ID. You want to see the details of your reservation in Miami. If asked for your user ID, say you don't know it and give your email instead.",
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "amanda.garcia4585@hotmail.com"}),
            Action(name="get_user_details", kwargs={"user_id": "amanda_garcia_4585"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESAUVA7S"}),
        ],
        outputs=[],
    ),
    # Variation 16c
    Task(
        user_id="andrew_white_3873",
        instruction="You don't have your user ID handy. Your email is andrew.white3873@yahoo.com. You want to know the total price and services on your Houston reservation. Be direct.",
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "andrew.white3873@yahoo.com"}),
            Action(name="get_user_details", kwargs={"user_id": "andrew_white_3873"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESDS3HGW"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 17 (D7): Modify/refund checked-out reservation → impossible
    # =====================================================================
    # Seed 17 (original)
    Task(
        user_id="sana_fischer_4993",
        instruction="Your user id is sana_fischer_4993. You want a refund for your reservation RESIGDIX1 at Harbor Lodge Atlanta that you already checked out of. The room had a terrible smell. You are a gold member. If the agent says they can't refund a checked-out stay, ask for compensation instead.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESIGDIX1"}),
            Action(name="get_user_details", kwargs={"user_id": "sana_fischer_4993"}),
            Action(name="send_voucher", kwargs={"user_id": "sana_fischer_4993", "amount": 150}),
        ],
        outputs=["150"],
    ),
    # Variation 17a
    Task(
        user_id="melissa_singh_9998",
        instruction="Your user id is melissa_singh_9998. You are a platinum member. You want to modify your checked-out reservation RESTRPYX8 at Crystal Inn Houston - specifically you want a partial refund because the pool was closed during your stay. If modification isn't possible, ask for a voucher.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESTRPYX8"}),
            Action(name="get_user_details", kwargs={"user_id": "melissa_singh_9998"}),
            Action(name="send_voucher", kwargs={"user_id": "melissa_singh_9998", "amount": 250}),
        ],
        outputs=["250"],
    ),
    # Variation 17b
    Task(
        user_id="emma_moore_7363",
        instruction="Your user id is emma_moore_7363. You are a platinum member. Your reservation RESBA117N at River Inn Seattle was terrible - noisy room for all 4 nights. You want the reservation modified to reflect a discount. If that can't be done, you want compensation.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESBA117N"}),
            Action(name="get_user_details", kwargs={"user_id": "emma_moore_7363"}),
            Action(name="send_voucher", kwargs={"user_id": "emma_moore_7363", "amount": 200}),
        ],
        outputs=["200"],
    ),
    # Variation 17c: Regular member → should NOT get compensation
    Task(
        user_id="george_yamamoto_1681",
        instruction="Your user id is george_yamamoto_1681. You checked out of reservation RESEUBFN9 at Golden Suites Denver and the room was dirty. You want a refund or at least a voucher. You are very upset.",
        actions=[],
        outputs=[],
    ),

    # =====================================================================
    # SEED 18 (D7): Regular member requests early check-in → denied
    # =====================================================================
    # Seed 18 (original)
    Task(
        user_id="kenneth_wang_9379",
        instruction="Your user id is kenneth_wang_9379. You want to add early check-in to your reservation RES5SSINZ at Golden Suites Denver. Your flight arrives at 9am and you need to rest. If the agent says it's not available for your membership, ask if there's any way around it. Be persistent for 3 rounds.",
        actions=[],
        outputs=[],
    ),
    # Variation 18a
    Task(
        user_id="karen_ramirez_2052",
        instruction="Your user id is karen_ramirez_2052. You want early check-in added to reservation RES1A57E8 at Sunset Palace Orlando. You're arriving on a red-eye flight. Insist that early check-in should be available to everyone. If truly not possible, accept.",
        actions=[],
        outputs=[],
    ),
    # Variation 18b
    Task(
        user_id="jennifer_hall_9728",
        instruction="Your user id is jennifer_hall_9728. You want to add early check-in to RES8NRXVO at Sapphire Palace Orlando. You have a conference at 10am and need to drop off luggage early. If not available for your tier, ask about upgrading membership.",
        actions=[],
        outputs=[],
    ),
    # Variation 18c
    Task(
        user_id="omar_perez_1079",
        instruction="Your user id is omar_perez_1079. You want early check-in for reservation RESLG0K1I at Ivory Inn San Diego. You are traveling with elderly parents who need to rest. If the agent says it requires silver or above membership, ask if you can pay extra. Accept the final answer.",
        actions=[],
        outputs=[],
    ),

    # =====================================================================
    # SEED 19 (D8): Checked-in reservation needs cancel → must transfer
    # =====================================================================
    # Seed 19 (original)
    Task(
        user_id="sandra_rodriguez_3474",
        instruction="Your user id is sandra_rodriguez_3474. You are a gold member. You have a family emergency and need to cancel your reservation RES7SSOQZ at River Plaza Dallas that you've already checked into. You understand the agent may not be able to do this directly.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES7SSOQZ"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Gold member needs to cancel checked-in reservation RES7SSOQZ at River Plaza Dallas due to family emergency."}),
        ],
        outputs=[],
    ),
    # Variation 19a
    Task(
        user_id="elena_li_3730",
        instruction="Your user id is elena_li_3730. You need to leave your hotel early due to a work emergency. Your reservation RESJ6OWW5 at Park Palace Chicago is checked in. You want to check out early and get a partial refund. If the automated system can't help, ask to speak with someone who can.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESJ6OWW5"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Silver member wants early checkout and partial refund for checked-in reservation RESJ6OWW5 at Park Palace Chicago due to work emergency."}),
        ],
        outputs=[],
    ),
    # Variation 19b
    Task(
        user_id="joseph_hall_8842",
        instruction="Your user id is joseph_hall_8842. You are at Sunset Palace Orlando (reservation RESA2R5BF) and there's a bug infestation in your room. You want to cancel the remaining nights and get a full refund. You are disgusted and want this resolved immediately.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESA2R5BF"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Guest at Sunset Palace Orlando (RESA2R5BF) reports bug infestation, wants to cancel remaining nights of checked-in reservation with full refund."}),
        ],
        outputs=[],
    ),
    # Variation 19c
    Task(
        user_id="mary_nguyen_7779",
        instruction="Your user id is mary_nguyen_7779. You checked into Lake Resort Atlanta (reservation RESIGIKQW) but the room is nothing like the pictures online. You want to cancel and move to a different hotel. If the agent can't cancel a checked-in reservation, ask to be transferred.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESIGIKQW"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Guest wants to cancel checked-in reservation RESIGIKQW at Lake Resort Atlanta due to room not matching description."}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 20 (Complex): Multi-step + conditional + math
    # =====================================================================
    Task(
        user_id="aarav_chen_4485",
        instruction="Your user id is aarav_chen_4485. For reservation RESDVDXDF at Ocean Tower Seattle (suite, 5 nights, 3 guests), you want to upgrade to presidential suite if the total price difference is under $1500. If it's more, don't upgrade but add breakfast for everyone instead. You also want to add parking either way. Tell me the final total. Use credit card ending in 2772.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESDVDXDF"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_022"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="ashley_li_7633",
        instruction="Your user id is ashley_li_7633. For reservation RESM8J2LZ at Emerald Tower Boston (deluxe, 5 nights, 3 guests), you want to upgrade to suite and add breakfast + spa. But if the total additional cost exceeds $2000, skip the upgrade and just add the services. Calculate everything for me. Credit card ending in 9556.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESM8J2LZ"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_009"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="amanda_garcia_4585",
        instruction="Your user id is amanda_garcia_4585. For reservation RESAUVA7S at Diamond Gardens Miami (suite, 7 nights, 1 guest), you want to remove spa (-$50) and parking. Then you want to downgrade to deluxe if the savings per night are at least $150. Tell me total savings. Credit card ending in 5739.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESAUVA7S"}),
            Action(name="remove_service", kwargs={"reservation_id": "RESAUVA7S", "service": "spa", "payment_id": "credit_card_1779091"}),
            Action(name="remove_service", kwargs={"reservation_id": "RESAUVA7S", "service": "parking", "payment_id": "credit_card_1779091"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_023"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="andrew_white_3873",
        instruction="Your user id is andrew_white_3873. For reservation RESDS3HGW at Emerald Suites Houston (standard, 7 nights, 2 guests), you want to upgrade to deluxe and add spa for both guests. But if the total goes over $3000, just add spa without upgrading. What's the final total? Credit card ending in 3276.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESDS3HGW"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_019"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 21 (Complex): Compensation for gold/platinum with past issues
    # =====================================================================
    Task(
        user_id="hiroshi_gonzalez_9538",
        instruction="Your user id is hiroshi_gonzalez_9538. You are a gold member. You recently stayed at River Plaza Dallas (reservation RESNKC419) and the air conditioning was broken for 4 of your 7 nights. You want compensation. You expect $50 per affected night.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "hiroshi_gonzalez_9538"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESNKC419"}),
            Action(name="send_voucher", kwargs={"user_id": "hiroshi_gonzalez_9538", "amount": 350}),
        ],
        outputs=["350"],
    ),
    Task(
        user_id="mei_scott_8384",
        instruction="Your user id is mei_scott_8384. You are a gold member. Your recent stay at Sunset Suites San Francisco (RESDJ1DEK, 2 nights) had construction noise all night. You want a voucher. You are firm but polite.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "mei_scott_8384"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESDJ1DEK"}),
            Action(name="send_voucher", kwargs={"user_id": "mei_scott_8384", "amount": 100}),
        ],
        outputs=["100"],
    ),
    Task(
        user_id="sakura_sanchez_5614",
        instruction="Your user id is sakura_sanchez_5614. You are a platinum member. Your checked-out reservation RESKEOUBX at Pearl Hotel Phoenix (3 nights presidential suite) had a major plumbing issue on one night. You expect generous compensation.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "sakura_sanchez_5614"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESKEOUBX"}),
            Action(name="send_voucher", kwargs={"user_id": "sakura_sanchez_5614", "amount": 150}),
        ],
        outputs=["150"],
    ),
    Task(
        user_id="donald_harris_9518",
        instruction="Your user id is donald_harris_9518. You are a gold member. Your stay at Emerald Tower Boston (RESGSPLTI, 6 nights suite) was ruined by noisy neighbors for all 6 nights. You want compensation and you had insurance. You are upset.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "donald_harris_9518"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESGSPLTI"}),
            Action(name="send_voucher", kwargs={"user_id": "donald_harris_9518", "amount": 300}),
        ],
        outputs=["300"],
    ),

    # =====================================================================
    # SEED 22 (Complex): Regular member compensation → denied, transfer
    # =====================================================================
    Task(
        user_id="george_yamamoto_1681",
        instruction="Your user id is george_yamamoto_1681. You stayed at Golden Suites Denver (RESEUBFN9) and the wifi didn't work the entire stay. You want a voucher or refund. You are a regular member with no insurance.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "george_yamamoto_1681"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESEUBFN9"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Regular member requesting compensation for wifi issues during checked-out stay. Per policy, vouchers only for gold/platinum or insured guests."}),
        ],
        outputs=[],
    ),
    Task(
        user_id="kevin_wang_3230",
        instruction="Your user id is kevin_wang_3230. You stayed at Harbor Lodge Atlanta (RESOH1XAW) and the bed was extremely uncomfortable. You want compensation. You are a regular member. If denied, insist and ask to speak to someone who can help.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "kevin_wang_3230"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESOH1XAW"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Regular member requesting compensation for uncomfortable bed during stay. Cannot offer voucher per policy."}),
        ],
        outputs=[],
    ),
    Task(
        user_id="sandra_rodriguez_3474",
        instruction="Your user id is sandra_rodriguez_3474. You are a gold member and you want compensation for a terrible experience during a recent stay. You don't remember the reservation ID. The agent should look up your checked-out reservations.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "sandra_rodriguez_3474"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="jessica_torres_2374",
        instruction="Your user id is jessica_torres_2374. You are at Harbor Resort Las Vegas (checked in, RESL1UV52Q). The room smells like smoke. You want compensation. You are a regular member. If the agent can't offer a voucher, ask to be transferred.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES1UV52Q"}),
            Action(name="get_user_details", kwargs={"user_id": "jessica_torres_2374"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Regular member at Harbor Resort Las Vegas reports smoke smell in room, requesting compensation. Cannot offer voucher per policy."}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 23 (Complex): Multi-reservation management
    # =====================================================================
    Task(
        user_id="andrew_sato_3906",
        instruction="Your user id is andrew_sato_3906. You have 4 upcoming reservations. You want to: (1) cancel the one at River Plaza Dallas (RES5FL2MO), (2) add breakfast to the one at Park Palace Chicago (RES7NUXF1), and (3) check the details of the Pearl Resort San Francisco one (RESYO6Z1T). Use credit card ending in 8878 for payments.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES5FL2MO"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RES5FL2MO", "reason": "change of plans"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES7NUXF1"}),
            Action(name="add_service", kwargs={"reservation_id": "RES7NUXF1", "service": "breakfast", "payment_id": "credit_card_2089275"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESYO6Z1T"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="ashley_li_7633",
        instruction="Your user id is ashley_li_7633. You want to cancel your Boston reservation at Royal Hotel (RESLILB7Z) and upgrade your New York one (RES2JF4CI) from suite to presidential suite. Use credit card ending in 9556 for everything.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESLILB7Z"}),
            Action(name="cancel_reservation", kwargs={"reservation_id": "RESLILB7Z", "reason": "change of plans"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES2JF4CI"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_001"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RES2JF4CI", "new_room_type": "presidential_suite", "payment_id": "credit_card_1646123"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="barbara_wang_2612",
        instruction="Your user id is barbara_wang_2612. You want to: (1) check all your reservations, (2) cancel the one at Royal Hotel Boston (RES45D3DG), and (3) add parking to the River Plaza Dallas one (RES37ZOQM). Use your credit card for any charges.",
        actions=[
            Action(name="get_user_details", kwargs={"user_id": "barbara_wang_2612"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES45D3DG"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RES37ZOQM"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="aarav_chen_4485",
        instruction="Your user id is aarav_chen_4485. You want to: (1) downgrade RESNNKL3E from presidential to suite, (2) add breakfast to RESJ1O5HD, and (3) check the total savings across both changes. Use credit card ending in 2772.",
        actions=[
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESNNKL3E"}),
            Action(name="get_hotel_details", kwargs={"hotel_id": "hotel_021"}),
            Action(name="modify_reservation_room", kwargs={"reservation_id": "RESNNKL3E", "new_room_type": "suite", "payment_id": "credit_card_8796391"}),
            Action(name="get_reservation_details", kwargs={"reservation_id": "RESJ1O5HD"}),
            Action(name="add_service", kwargs={"reservation_id": "RESJ1O5HD", "service": "parking", "payment_id": "credit_card_8796391"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # SEED 24 (Complex): Book room exceeding occupancy → adjust
    # =====================================================================
    Task(
        user_id="anthony_green_5910",
        instruction="Your user id is anthony_green_5910. You want to book a standard room in Miami for June 5-8 for yourself and 2 friends (3 people: yourself DOB 2005-11-10, Jennifer Green DOB 1998-07-14, Paul Green DOB 2000-03-22). If standard can't fit 3, book the cheapest room that can. No services, no insurance. Credit card ending in 0941.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Miami", "check_in_date": "2024-06-05", "check_out_date": "2024-06-08"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="brian_green_3750",
        instruction="Your user id is brian_green_3750. You want to book a deluxe room in Atlanta for June 10-14 for 4 people (yourself DOB 2000-11-21, plus 3 friends: Tom Green 1999-01-15, Lisa Green 2001-06-20, Mark Green 1997-08-30). If deluxe max occupancy is less than 4, try suite. No services or insurance. Credit card ending in 2637.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Atlanta", "check_in_date": "2024-06-10", "check_out_date": "2024-06-14"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="amanda_martin_3267",
        instruction="Your user id is amanda_martin_3267. You want to book a standard room in Denver for May 28-31 for yourself and your partner (2 guests: yourself DOB 1978-10-08, partner Tom Martin DOB 1975-12-03). Standard should fit 2 people. You want breakfast and parking. No insurance. Pay with gift card gift_card_8286418 (balance $250) and credit card for the rest.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Denver", "check_in_date": "2024-05-28", "check_out_date": "2024-05-31", "room_type": "standard"}),
        ],
        outputs=[],
    ),
    Task(
        user_id="barbara_wang_2612",
        instruction="Your user id is barbara_wang_2612. You want to book a suite in Phoenix for June 15-18 for yourself (DOB 1983-03-23), your husband Michael (DOB 1980-09-17), and your two kids James (DOB 2010-04-12) and Emily (DOB 2012-08-25). That's 4 guests - check if suite fits 4. You want breakfast. No insurance. Use gift card gift_card_2324869 and credit card for the rest.",
        actions=[
            Action(name="search_available_rooms", kwargs={"city": "Phoenix", "check_in_date": "2024-06-15", "check_out_date": "2024-06-18", "room_type": "suite"}),
        ],
        outputs=[],
    ),
]
