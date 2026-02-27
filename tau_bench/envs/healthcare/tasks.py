# Copyright Sierra
# Healthcare tasks targeting airline's 5 failure patterns:
# F1: Insurance/payment calculation (copay + HSA + deductible + coverage%)
# F2: Search specialist → compare slots → select → book
# F3: Multi-appointment scan + selective action
# F4: Cancel + rebook chain
# F5: Multi-field modification (specialist + time + procedure)

from tau_bench.types import Action, Task

TASKS = [
    # =================================================================
    # F1: INSURANCE/PAYMENT CALCULATION (like airline payment split)
    # Agent must compute: copay + deductible + coverage% → patient cost
    # =================================================================

    # Task 0: Full insurance calc for premium patient (8 actions)
    Task(
        user_id="P10012",
        instruction="Your email is sofia.garcia58@inbox.com. You want to book an Echocardiogram (PROC004). You have a referral. Search for a Cardiology specialist with availability on Sep 25. Book the earliest slot. You're premium plan with $0 deductible met. Calculate your exact out-of-pocket cost including copay. Pay with HSA.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "sofia.garcia58@inbox.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10012"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC004"}),
            Action(name="get_insurance_summary", kwargs={"patient_id": "P10012"}),
            Action(name="search_specialists", kwargs={"procedure_id": "PROC004", "date": "2024-09-25"}),
        ],
        outputs=[],
    ),

    # Task 1: Basic plan with partial deductible (complex calc)
    Task(
        user_id="P10010",
        instruction="You are Sarah Thomas, born 1996-10-24. You want to book a Cardiology Consultation (PROC003). You have a referral (REF_P10010_PROC003). Search cardiology specialists available Sep 26. Calculate your cost: basic plan, $40 copay, $200 deductible already met out of $2000. Use HSA for payment. Tell me exact out-of-pocket.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Sarah", "last_name": "Thomas", "dob": "1996-10-24"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10010"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC003"}),
            Action(name="get_insurance_summary", kwargs={"patient_id": "P10010"}),
            Action(name="search_specialists", kwargs={"department": "Cardiology", "date": "2024-09-26"}),
        ],
        outputs=[],
    ),

    # Task 2: HSA + credit card split
    Task(
        user_id="P10042",
        instruction="Your email is william.nguyen84@mail.com. Book an Echocardiogram (PROC004, referral REF_P10042_PROC004). Search Cardiology on Oct 1. You're basic plan, $0 deductible met. Calculate cost. Your HSA has $500. Use HSA first, credit card for the rest. What's the credit card amount?",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "william.nguyen84@mail.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10042"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC004"}),
            Action(name="get_insurance_summary", kwargs={"patient_id": "P10042"}),
            Action(name="search_specialists", kwargs={"procedure_id": "PROC004", "date": "2024-10-01"}),
        ],
        outputs=[],
    ),

    # Task 3: Compare costs across different procedures
    Task(
        user_id="P10015",
        instruction="You are Paul Rodriguez, born 1984-10-11. You need either a Neurology Consultation (PROC011) or an EEG Test (PROC012). You have a referral for PROC011. Check both procedures. Calculate your out-of-pocket for each with standard plan, $0 deductible met. Which is cheaper for you? Tell me both amounts.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Paul", "last_name": "Rodriguez", "dob": "1984-10-11"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10015"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC011"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC012"}),
            Action(name="get_insurance_summary", kwargs={"patient_id": "P10015"}),
        ],
        outputs=[],
    ),

    # Task 4: Calculate total cost for multiple upcoming appointments
    Task(
        user_id="P10058",
        instruction="Your email is liam.torres45@inbox.com. You have 3 scheduled appointments. Check each one. Calculate your total out-of-pocket across all three. Standard plan, $0 deductible met. Tell me per-appointment and total cost.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "liam.torres45@inbox.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10058"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00006"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00246"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00350"}),
            Action(name="get_insurance_summary", kwargs={"patient_id": "P10058"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # F2: SEARCH → COMPARE → SELECT → BOOK (like airline flight search)
    # =================================================================

    # Task 5: Search specialist by date, pick earliest slot
    Task(
        user_id="P10066",
        instruction="You are Noah Johnson, born 1967-12-24. You want to book a Stress Test (PROC005). You have a referral (REF_P10066_PROC005). Search Cardiology specialists available on Sep 30. Pick the earliest available slot. Book it. Pay with HSA.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Noah", "last_name": "Johnson", "dob": "1967-12-24"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10066"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC005"}),
            Action(name="search_specialists", kwargs={"department": "Cardiology", "date": "2024-09-30"}),
        ],
        outputs=[],
    ),

    # Task 6: Compare multiple specialists, pick by name preference
    Task(
        user_id="P10076",
        instruction="Your email is andrew.roberts78@mail.com. You need an EEG Test (PROC012, referral REF_P10076_PROC012). Search Neurology specialists. Compare who has availability on Oct 5 vs Oct 6. Book with whichever specialist has the earliest slot. Pay with credit card.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "andrew.roberts78@mail.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10076"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC012"}),
            Action(name="search_specialists", kwargs={"department": "Neurology", "date": "2024-10-05"}),
            Action(name="search_specialists", kwargs={"department": "Neurology", "date": "2024-10-06"}),
        ],
        outputs=[],
    ),

    # Task 7: Search procedures by department, then find specialist
    Task(
        user_id="P10031",
        instruction="You are Daniel Clark, born 1995-02-22. You want a GI procedure but don't know which one. Search Gastroenterology procedures. You want the one that's NOT a colonoscopy. Then search for specialists. Book the first available after Oct 1. You have referral for PROC013. Pay with HSA.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Daniel", "last_name": "Clark", "dob": "1995-02-22"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10031"}),
            Action(name="search_procedures", kwargs={"department": "Gastroenterology"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC014"}),
            Action(name="search_specialists", kwargs={"department": "Gastroenterology"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # F3: MULTI-APPOINTMENT SCAN + SELECTIVE ACTION (like airline multi-reservation)
    # =================================================================

    # Task 8: Check all appointments, cancel ones without referral
    Task(
        user_id="P10010",
        instruction="Your email is sarah.thomas74@email.com. Check all your scheduled appointments. Some procedures require a referral. Cancel any appointment for a procedure that requires a referral but you DON'T have one. Tell me which ones you cancelled.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "sarah.thomas74@email.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10010"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00026"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00044"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00256"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC017"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC006"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC018"}),
        ],
        outputs=[],
    ),

    # Task 9: Scan all, reschedule the expensive ones to cheaper specialist
    Task(
        user_id="P10079",
        instruction="You are Jessica White, born 1989-06-03. Check all your scheduled appointments. For any appointment costing more than $50, find if the same procedure has a cheaper time slot with another specialist. Tell me which could be cheaper.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Jessica", "last_name": "White", "dob": "1989-06-03"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10079"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00302"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00323"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00389"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC005"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC003"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC014"}),
        ],
        outputs=[],
    ),

    # Task 10: Scan all, find total cost, cancel most expensive
    Task(
        user_id="P10077",
        instruction="Your email is michael.perez38@email.com. You're on a budget. Check all scheduled appointments. Calculate total cost. If over $200 total, cancel the most expensive one. What's remaining total?",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "michael.perez38@email.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10077"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00078"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00224"}),
            Action(name="cancel_appointment", kwargs={"appointment_id": "APT00224", "reason": "over budget"}),
        ],
        outputs=["90"],
    ),

    # =================================================================
    # F4: CANCEL + REBOOK CHAIN (like airline cancel + rebook)
    # =================================================================

    # Task 11: Cancel + rebook with different specialist
    Task(
        user_id="P10031",
        instruction="You are Daniel Clark, born 1995-02-22. Cancel your MRI appointment APT00121 (Oct 3). You want to rebook the same MRI (PROC007) but with a different Orthopedics specialist on Oct 8 instead. Search for availability. Pay with HSA.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Daniel", "last_name": "Clark", "dob": "1995-02-22"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10031"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00121"}),
            Action(name="cancel_appointment", kwargs={"appointment_id": "APT00121", "reason": "rescheduling with different specialist"}),
            Action(name="search_specialists", kwargs={"department": "Orthopedics", "date": "2024-10-08"}),
        ],
        outputs=[],
    ),

    # Task 12: Cancel + rebook different procedure entirely
    Task(
        user_id="P10059",
        instruction="Your email is elizabeth.jackson24@email.com. Cancel your Colonoscopy APT00064 ($504). You'd rather have a GI Consultation (PROC014, $250) first. You have referral REF_P10059_PROC012 but need one for PROC014 too. If no referral for PROC014, just do a general checkup (PROC001) instead. Search General Practice specialists for Oct 10.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "elizabeth.jackson24@email.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10059"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00064"}),
            Action(name="cancel_appointment", kwargs={"appointment_id": "APT00064", "reason": "switching to less invasive option"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC014"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC001"}),
            Action(name="search_specialists", kwargs={"department": "General Practice", "date": "2024-10-10"}),
        ],
        outputs=[],
    ),

    # Task 13: Cancel + rebook + recalculate insurance
    Task(
        user_id="P10071",
        instruction="You are Omar Martin, born 1977-02-01. Cancel your Neurology appointment APT00391 ($164). Rebook it as a Dermatology Consultation (PROC010, no referral needed) instead - cheaper. Search Dermatology specialists Oct 5. Calculate new cost with basic plan, deductible already met. Pay with HSA. How much do you save?",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Omar", "last_name": "Martin", "dob": "1977-02-01"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10071"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00391"}),
            Action(name="cancel_appointment", kwargs={"appointment_id": "APT00391", "reason": "switching to cheaper procedure"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC010"}),
            Action(name="get_insurance_summary", kwargs={"patient_id": "P10071"}),
            Action(name="search_specialists", kwargs={"department": "Dermatology", "date": "2024-10-05"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # F5: MULTI-FIELD MODIFICATION (like airline multi-update)
    # =================================================================

    # Task 14: Reschedule + change procedure
    Task(
        user_id="P10076",
        instruction="Your email is andrew.roberts78@mail.com. For APT00261 (MRI, Sep 16), reschedule to Oct 7 with a different Orthopedics specialist. Also, you want to change the procedure from MRI to Physical Therapy (PROC008, referral REF_P10076_PROC008). Tell me the cost difference.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "andrew.roberts78@mail.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10076"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00261"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC008"}),
            Action(name="search_specialists", kwargs={"department": "Orthopedics", "date": "2024-10-07"}),
            Action(name="modify_appointment_procedure", kwargs={"appointment_id": "APT00261", "new_procedure_id": "PROC008", "payment_method": "cc_P10076_9818"}),
        ],
        outputs=[],
    ),

    # Task 15: Reschedule to different date + different specialist
    Task(
        user_id="P10057",
        instruction="You are Emily Thomas, born 1968-07-19. Reschedule your Neurology appointment APT00320 (Sep 30) to Oct 8. You want a different neurologist. Search Neurology availability on Oct 8. Pick a morning slot.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Emily", "last_name": "Thomas", "dob": "1968-07-19"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10057"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00320"}),
            Action(name="search_specialists", kwargs={"department": "Neurology", "date": "2024-10-08"}),
        ],
        outputs=[],
    ),

    # Task 16: Change procedure + recalculate + pay difference
    Task(
        user_id="P10023",
        instruction="Your email is donna.hill68@mail.com. For your Cardiology Consultation APT00393 ($39), you want to upgrade to an Echocardiogram (PROC004) instead since you have referral REF_P10023_PROC003 (which also covers cardiology). Check the cost difference. Premium plan, $1000 deductible met. Pay with credit card.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "donna.hill68@mail.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10023"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00393"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC004"}),
            Action(name="get_insurance_summary", kwargs={"patient_id": "P10023"}),
            Action(name="modify_appointment_procedure", kwargs={"appointment_id": "APT00393", "new_procedure_id": "PROC004", "payment_method": "cc_P10023_2310"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # POLICY COMPLIANCE (API doesn't check)
    # =================================================================

    # Task 17: Book without referral → agent must refuse
    Task(
        user_id="P10011",
        instruction="You are Barbara Allen, born 1957-05-20. You want to book a Colonoscopy (PROC013, requires referral). You have a referral for PROC013 (REF_P10011_PROC013). Search Gastroenterology on Oct 3. Book the first slot. Pay with credit card.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Barbara", "last_name": "Allen", "dob": "1957-05-20"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10011"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC013"}),
            Action(name="search_specialists", kwargs={"department": "Gastroenterology", "date": "2024-10-03"}),
        ],
        outputs=[],
    ),

    # Task 18: Cancel <24h → fee applies (unless premium)
    Task(
        user_id="P10030",
        instruction="Your email is emma.perez55@email.com. Cancel your Stress Test APT00240 (Sep 17). It's less than 48 hours away. You're basic plan. The agent should inform you about the $50 cancellation fee. Proceed anyway.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "emma.perez55@email.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10030"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00240"}),
            Action(name="cancel_appointment", kwargs={"appointment_id": "APT00240", "reason": "scheduling conflict"}),
        ],
        outputs=["50"],
    ),

    # Task 19: Premium cancel → free regardless
    Task(
        user_id="P10012",
        instruction="You are Sofia Garcia, born 1966-06-19. Premium plan. Cancel APT00027 (Sep 20, less than a week away). Premium members get free cancellation. Confirm no fee.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Sofia", "last_name": "Garcia", "dob": "1966-06-19"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10012"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00027"}),
            Action(name="cancel_appointment", kwargs={"appointment_id": "APT00027", "reason": "schedule change"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # ADVERSARIAL + COMPENSATION
    # =================================================================

    # Task 20: Doesn't remember appointment, gives wrong date
    Task(
        user_id="P10066",
        instruction="Your email is noah.johnson29@inbox.com. You have an orthopedics appointment but think it's on Oct 5. It's actually Oct 6. When agent can't find one on Oct 5, ask to check all your appointments. You want the knee X-ray one.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "noah.johnson29@inbox.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10066"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00037"}),
        ],
        outputs=[],
    ),

    # Task 21: Premium patient complains → gets HSA credit
    Task(
        user_id="P10012",
        instruction="You are Sofia Garcia, born 1966-06-19. Premium plan. Your past Stress Test (APT00227, completed) had a 2-hour wait. You want compensation. Policy says $50 per affected appointment. Credit to my HSA.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Sofia", "last_name": "Garcia", "dob": "1966-06-19"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10012"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00227"}),
            Action(name="add_hsa_credit", kwargs={"patient_id": "P10012", "amount": 50}),
        ],
        outputs=["50"],
    ),

    # Task 22: Basic plan patient complains → transfer
    Task(
        user_id="P10030",
        instruction="Your email is emma.perez55@email.com. Basic plan. Your past appointment had terrible service. You want compensation. If the agent can't help basic plan patients, ask to speak to someone who can.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "emma.perez55@email.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10030"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Basic plan patient requesting compensation for poor service. Per policy, basic/standard plan patients must be transferred for compensation."}),
        ],
        outputs=[],
    ),

    # Task 23: Book for dependent (family member)
    Task(
        user_id="P10015",
        instruction="You are Paul Rodriguez, born 1984-10-11. You want to book a Well-Child Visit (PROC019) for your child (check dependents in your profile). Search Pediatrics specialists available Oct 4. Book the earliest slot. No referral needed. Pay with credit card.",
        actions=[
            Action(name="find_patient_by_name_dob", kwargs={"first_name": "Paul", "last_name": "Rodriguez", "dob": "1984-10-11"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10015"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC019"}),
            Action(name="search_specialists", kwargs={"department": "Pediatrics", "date": "2024-10-04"}),
        ],
        outputs=[],
    ),

    # Task 24: Complex: scan all → cancel one → rebook → calculate insurance → pay split
    Task(
        user_id="P10079",
        instruction="Your email is jessica.white83@email.com. Premium plan, $500 deductible met. Check all your scheduled appointments. Cancel the GI Consultation (APT00389). Instead, book a Colonoscopy (PROC013, you DON'T have a referral for it - if needed, just book the GI Consultation with a different specialist on Oct 5 instead). Calculate exact cost with insurance. Pay HSA first ($2000), credit card for rest.",
        actions=[
            Action(name="find_patient_by_email", kwargs={"email": "jessica.white83@email.com"}),
            Action(name="get_patient_details", kwargs={"patient_id": "P10079"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00302"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00323"}),
            Action(name="get_appointment_details", kwargs={"appointment_id": "APT00389"}),
            Action(name="cancel_appointment", kwargs={"appointment_id": "APT00389", "reason": "rebooking with different specialist"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC013"}),
            Action(name="get_procedure_details", kwargs={"procedure_id": "PROC014"}),
            Action(name="get_insurance_summary", kwargs={"patient_id": "P10079"}),
            Action(name="search_specialists", kwargs={"department": "Gastroenterology", "date": "2024-10-05"}),
        ],
        outputs=[],
    ),
]
