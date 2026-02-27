# Copyright Sierra
# Course registration tasks designed to match retail's structural complexity:
#   - Long action chains (6-12 steps): auth → lookup → lookup → ... → action
#   - Item-level cross-referencing: registration → course → sections → switch
#   - Multi-object management: multiple registrations per student
#   - Precise numeric outputs: tuition calculations, credit totals
#   - All 8 capability dimensions covered

from tau_bench.types import Action, Task

TASKS = [
    # =====================================================================
    # PATTERN A: Long chains with item-level cross-referencing
    # Mirrors retail's: auth → get_user → get_order → get_product × N → action
    # =====================================================================

    # Task 0: auth(name+dob) → get_student → get_reg → get_course × 2 → switch_sections
    # 6 actions, mirrors the canonical retail exchange pattern
    Task(
        user_id="S10006",
        instruction="You are Mary Perez, born 1999-12-21. You want to switch the section for American Government in your Fall 2024 registration REGTLVR7MG to a section that meets on Tuesday/Thursday instead of your current TTh 15:00 slot. You also want to check if Ecology has a section with a different instructor. You are reactive and won't volunteer info unless asked.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Mary", "last_name": "Perez", "dob": "1999-12-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10006"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGTLVR7MG"}),
            Action(name="get_course_details", kwargs={"course_id": "POLS120"}),
            Action(name="get_course_details", kwargs={"course_id": "BIO301"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGTLVR7MG", "switches": [{"course_id": "POLS120", "new_section_id": "POLS120-004"}]}),
        ],
        outputs=[],
    ),

    # Task 1: auth(email) → get_student → get_reg → get_reg → get_course × 2 → drop + switch
    # 8 actions across 2 registrations
    Task(
        user_id="S10006",
        instruction="Your email is mary.perez77@student.edu. You have multiple Fall 2024 registrations. For REGTLVR7MG, you want to drop Intro to Programming (CS120) because you already took it. For REGYMMQ8Q6, you want to switch Modern Europe (HIST321) to a section that meets on Friday. You want to know the tuition refund for dropping CS120.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "mary.perez77@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10006"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGTLVR7MG"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGTLVR7MG", "course_ids": ["CS120"], "payment_id": "credit_card_3308538"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGYMMQ8Q6"}),
            Action(name="get_course_details", kwargs={"course_id": "HIST321"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGYMMQ8Q6", "switches": [{"course_id": "HIST321", "new_section_id": "HIST321-001"}]}),
        ],
        outputs=["450"],
    ),

    # Task 2: auth → get_student → get_reg → get_course × 3 → switch 2 sections at once
    # 7 actions, switch multiple courses in one call
    Task(
        user_id="S10015",
        instruction="You are Betty Harris, born 2005-02-19. In your registration REGH9VGKY5, you want to switch Macroeconomics (ECON200) to section ECON200-001 and Intro to Psychology (PSYC120) to section PSYC120-003. First check if those sections have seats. Tell me the new total tuition.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Betty", "last_name": "Harris", "dob": "2005-02-19"}),
            Action(name="get_student_details", kwargs={"student_id": "S10015"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGH9VGKY5"}),
            Action(name="get_course_details", kwargs={"course_id": "ECON200"}),
            Action(name="get_course_details", kwargs={"course_id": "PSYC120"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGH9VGKY5", "switches": [{"course_id": "ECON200", "new_section_id": "ECON200-001"}, {"course_id": "PSYC120", "new_section_id": "PSYC120-003"}]}),
        ],
        outputs=[],
    ),

    # Task 3: auth → student → reg → reg → reg → drop from one + course detail → switch in another
    # 9 actions across 3 registrations, mirrors retail's multi-order pattern
    Task(
        user_id="S10097",
        instruction="Your email is richard.miller33@student.edu. You don't remember which registration has your Statistics course. Can the agent check all your Fall 2024 registrations? Once found, you want to switch the Statistics section to one that meets earlier in the day. You also want to drop any History courses across all registrations. You want the total credits remaining after all changes.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "richard.miller33@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10097"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGDQLOVYV"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG2BVPDCB"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG6ZCHHXA"}),
        ],
        outputs=[],
    ),

    # Task 4: 10-action chain: auth → student → reg → course × 4 → drop 2 courses
    Task(
        user_id="S10007",
        instruction="You are Linda Chen, born 2002-04-10. For registration REG2UGL6TB, you want to drop Fundamentals of Nursing (NURS101) and American Government (POLS120). Before dropping, you want to check the details of all courses in the registration to make sure you're dropping the right ones. You want to know the total refund amount and remaining credits.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Linda", "last_name": "Chen", "dob": "2002-04-10"}),
            Action(name="get_student_details", kwargs={"student_id": "S10007"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG2UGL6TB"}),
            Action(name="get_course_details", kwargs={"course_id": "NURS101"}),
            Action(name="get_course_details", kwargs={"course_id": "BIO201"}),
            Action(name="get_course_details", kwargs={"course_id": "STAT200"}),
            Action(name="get_course_details", kwargs={"course_id": "BIO301"}),
            Action(name="get_course_details", kwargs={"course_id": "POLS120"}),
            Action(name="drop_courses", kwargs={"registration_id": "REG2UGL6TB", "course_ids": ["NURS101", "POLS120"], "payment_id": "financial_aid_624108"}),
        ],
        outputs=["1500"],
    ),

    # =====================================================================
    # PATTERN B: Multi-registration management (like retail multi-order)
    # =====================================================================

    # Task 5: Student with 3+ registrations, actions across multiple
    Task(
        user_id="S10075",
        instruction="Your email is christopher.nelson65@university.edu. You have multiple Fall 2024 registrations. You want to: (1) check all of them, (2) cancel the cancelled one if it's not already cancelled, (3) for each confirmed one, tell me the total credits and tuition. You want the combined total tuition across all confirmed registrations.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "christopher.nelson65@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10075"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG2QSQ0P8"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG5T82DDL"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGZTO7D83"}),
        ],
        outputs=[],
    ),

    # Task 6: Student wants to consolidate - drop courses from one reg, figure out schedule
    Task(
        user_id="S10080",
        instruction="You are Joseph Torres, born 2003-11-27. You have too many registrations for Fall 2024. You want to see all of them and figure out your total credits. If you're over 16 credits total (you're a freshman), you need to drop courses until you're at or under 16. Drop the most expensive courses first. Tell me which courses you recommend dropping and the total savings.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Joseph", "last_name": "Torres", "dob": "2003-11-27"}),
            Action(name="get_student_details", kwargs={"student_id": "S10080"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGRSBZB7T"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGD20J1OU"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGJ74NL03"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG2HOQ5E7"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # PATTERN C: Conditional + multi-step (like retail's complex tasks)
    # =====================================================================

    # Task 7: Switch section if available, otherwise drop the course
    Task(
        user_id="S10009",
        instruction="You are Raj Sanchez, born 2003-05-24. In registration REGAWO778S, your Calculus II (MATH200) section conflicts with a new job schedule. You want to switch to another section. If no other section is available, drop the course and tell me the refund. You also want to check if there's a different time for Electricity & Magnetism.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Raj", "last_name": "Sanchez", "dob": "2003-05-24"}),
            Action(name="get_student_details", kwargs={"student_id": "S10009"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAWO778S"}),
            Action(name="get_course_details", kwargs={"course_id": "MATH200"}),
            Action(name="get_course_details", kwargs={"course_id": "PHYS221"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGAWO778S", "course_ids": ["MATH200"], "payment_id": "credit_card_2133461"}),
        ],
        outputs=["900"],
    ),

    # Task 8: Complex conditional - if tuition over budget, drop expensive courses
    Task(
        user_id="S10013",
        instruction="You are Liam White, born 2004-05-21. Your budget for Fall 2024 is $2500. Check your registration REGIIOH6CV. If total tuition exceeds $2500, drop the most expensive course. If it's still over budget after that, drop the next most expensive. Tell me the final total. Use your credit card for refunds.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Liam", "last_name": "White", "dob": "2004-05-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10013"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGIIOH6CV"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGIIOH6CV", "course_ids": ["BIO110"], "payment_id": "credit_card_7815076"}),
        ],
        outputs=["2375"],
    ),

    # Task 9: Change mind mid-conversation
    Task(
        user_id="S10014",
        instruction="Your email is yuki.patel96@student.edu. You initially want to cancel registration REGTLT4Q9B entirely. But after the agent looks up the courses, you realize you need Mechanics (PHYS101) for your major. Instead of cancelling, just drop all courses EXCEPT PHYS101. Tell me the refund amount. Use credit card ending in 7272.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "yuki.patel96@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10014"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGTLT4Q9B"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGTLT4Q9B", "course_ids": ["CHEM211", "PHIL120", "PHYS300"], "payment_id": "credit_card_7145971"}),
        ],
        outputs=["1875"],
    ),

    # =====================================================================
    # PATTERN D: Precise numeric outputs (like retail's price calculations)
    # =====================================================================

    # Task 10: Calculate total tuition across multiple registrations
    Task(
        user_id="S10092",
        instruction="You are James Campbell, born 2004-10-02. You want to know the total tuition you're paying across ALL your Fall 2024 confirmed registrations. Also tell me the total number of credits. You want the exact numbers.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "James", "last_name": "Campbell", "dob": "2004-10-02"}),
            Action(name="get_student_details", kwargs={"student_id": "S10092"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGGLL42JZ"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGUV1FKHN"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG3YF15Z0"}),
        ],
        outputs=[],
    ),

    # Task 11: Calculate refund after dropping with tuition breakdown
    Task(
        user_id="S10000",
        instruction="Your email is sofia.thompson72@university.edu. For registration REGAIH7WFR, you want to drop Databases (CS400) and Calculus I (MATH100). Tell me: (1) the per-course tuition for each, (2) the total refund, (3) the remaining total tuition. Use your student account for the refund.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "sofia.thompson72@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10000"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAIH7WFR"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGAIH7WFR", "course_ids": ["CS400", "MATH100"], "payment_id": "student_account_S10000"}),
        ],
        outputs=["600", "600", "1200", "1400"],
    ),

    # Task 12: Search course + compare section prices
    Task(
        user_id="S10002",
        instruction="You are Barbara Wang, born 2000-12-15. You want to find the cheapest section for American Literature (ENG201) and tell me its section ID, instructor, and tuition for 3 credits. Also check if there's a time conflict with your current registration REG77Z4ES3.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Barbara", "last_name": "Wang", "dob": "2000-12-15"}),
            Action(name="get_student_details", kwargs={"student_id": "S10002"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG77Z4ES3"}),
            Action(name="get_course_details", kwargs={"course_id": "ENG201"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # PATTERN E: Policy compliance (API doesn't check)
    # =====================================================================

    # Task 13: Freshman over 16 credit limit → agent must refuse
    Task(
        user_id="S10000",
        instruction="Your student id is S10000. You're Sofia Thompson. You want to check your registration REGAIH7WFR (14 credits). Then you want to add two more 4-credit courses. If the agent mentions a credit limit, insist you need them all. You are a freshman.",
        actions=[
            Action(name="get_student_details", kwargs={"student_id": "S10000"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAIH7WFR"}),
        ],
        outputs=[],
    ),

    # Task 14: Missing prerequisites → agent must check and refuse
    Task(
        user_id="S10000",
        instruction="Your email is sofia.thompson72@university.edu. You want to check what courses require prerequisites that you haven't completed. You're interested in taking Data Structures (CS201) and Organic Chemistry (CHEM211). Check if you meet the prerequisites for each.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "sofia.thompson72@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10000"}),
            Action(name="get_course_details", kwargs={"course_id": "CS201"}),
            Action(name="get_course_details", kwargs={"course_id": "CHEM211"}),
        ],
        outputs=[],
    ),

    # Task 15: Try to drop from a completed registration → should refuse
    Task(
        user_id="S10079",
        instruction="You are Lucas Scott, born 1998-07-03. You want a refund for a course in your Spring 2024 registration REGG7UELN0 because the instructor was terrible. If the agent says it's completed, insist you deserve compensation. You are a senior.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Lucas", "last_name": "Scott", "dob": "1998-07-03"}),
            Action(name="get_student_details", kwargs={"student_id": "S10079"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGG7UELN0"}),
        ],
        outputs=[],
    ),

    # Task 16: Senior complains about cancelled section → compensation
    Task(
        user_id="S10119",
        instruction="Your email is sarah.wang97@campus.edu. You are a senior. Your registration REGYEJHDZX was supposed to include a course whose section was cancelled by the university. You want compensation. The affected course was 3 credits.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "sarah.wang97@campus.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10119"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGYEJHDZX"}),
            Action(name="add_credit", kwargs={"student_id": "S10119", "amount": 150}),
        ],
        outputs=["150"],
    ),

    # Task 17: Freshman asks for compensation → should be denied per policy
    Task(
        user_id="S10013",
        instruction="You are Liam White, born 2004-05-21. You're a freshman. A section you were enrolled in was cancelled by the university. You want a refund or compensation. Be persistent.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Liam", "last_name": "White", "dob": "2004-05-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10013"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # PATTERN F: Adversarial / information withholding
    # =====================================================================

    # Task 18: Student doesn't remember registration ID
    Task(
        user_id="S10081",
        instruction="Your email is elizabeth.mitchell94@university.edu. You need to modify something in one of your registrations but can't remember which one. You know it has an Economics course in it. Ask the agent to find it. Once found, switch the Economics section to one that meets on MWF.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "elizabeth.mitchell94@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10081"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGOEFUKPV"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG5QF0N85"}),
        ],
        outputs=[],
    ),

    # Task 19: Student gives wrong info then corrects
    Task(
        user_id="S10006",
        instruction="You are Mary Perez, born 1999-12-21. You want to check your registration but initially give the wrong ID 'REG12345'. When the agent says not found, say you might be confused and ask them to look up your registrations. You want to see the one with Biology courses.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Mary", "last_name": "Perez", "dob": "1999-12-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10006"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71A57E8"}),
        ],
        outputs=[],
    ),

    # Task 20: Student wants to cancel but changes mind after seeing courses
    Task(
        user_id="S10091",
        instruction="Your email is wei.clark32@campus.edu. You are very stressed and want to cancel ALL your registrations. But after the agent shows you the details of REGB3YYM33, you realize you need those courses for graduation. Instead, just drop the most expensive course from REGB3YYM33 and cancel the pending registration REGSUSFH70 instead.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "wei.clark32@campus.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10091"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGB3YYM33"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGO2LNGIX"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGSUSFH70"}),
            Action(name="cancel_registration", kwargs={"registration_id": "REGSUSFH70", "reason": "schedule change"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # PATTERN G: Auth flow diversity (mirroring retail's name+zip pattern)
    # =====================================================================

    # Task 21: Auth by name+dob, simple lookup
    Task(
        user_id="S10140",
        instruction="You are Mei Taylor, born 1999-05-20. You want to check all your Fall 2024 registrations and know the total credits and total tuition across all of them. You are organized and want a neat summary.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Mei", "last_name": "Taylor", "dob": "1999-05-20"}),
            Action(name="get_student_details", kwargs={"student_id": "S10140"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGU4SE2KY"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG6FHRXJP"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG0FT1AFD"}),
        ],
        outputs=[],
    ),

    # Task 22: Email auth, then complex operation
    Task(
        user_id="S10170",
        instruction="Your email is matthew.martin38@student.edu. You are a senior. For registration REG0224WK0, you want to check all courses, then drop any course that costs more than $800. Tell me the total savings. Refund to credit card.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "matthew.martin38@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10170"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG0224WK0"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG9B7LNKZ"}),
        ],
        outputs=[],
    ),

    # =====================================================================
    # PATTERN H: Transfer to human + zero-action
    # =====================================================================

    # Task 23: Request beyond system scope → transfer
    Task(
        user_id="S10009",
        instruction="You are Raj Sanchez, born 2003-05-24. You want to appeal a grade you received in a Spring 2024 course. You believe the grading was unfair. If the agent can't handle grade appeals, ask to be connected to an academic advisor.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Raj", "last_name": "Sanchez", "dob": "2003-05-24"}),
            Action(name="get_student_details", kwargs={"student_id": "S10009"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Student wants to appeal a grade from Spring 2024. Grade appeals are outside the scope of the registration system."}),
        ],
        outputs=[],
    ),

    # Task 24: Modify completed registration → impossible
    Task(
        user_id="S10095",
        instruction="Your email is mary.perez62@campus.edu. You want to modify your Spring 2024 registration REG66YA6BA to change a course. If the agent says it's completed, insist you should be able to modify it retroactively. If truly impossible, ask to be transferred.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "mary.perez62@campus.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10095"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG66YA6BA"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Student wants to retroactively modify a completed Spring 2024 registration. This is not possible through the registration system."}),
        ],
        outputs=[],
    ),
]
