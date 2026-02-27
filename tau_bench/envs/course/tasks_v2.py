# Copyright Sierra
# Expanded course tasks: 25 seeds + 75 variations (3 per seed)
# All data validated against generated JSON.

from tau_bench.types import Action, Task

TASKS = [
    # =================================================================
    # SEED 0: auth(name+dob) → student → reg → course × 2 → switch
    # Pattern: 6-action long chain with cross-referencing
    # =================================================================
    # Seed 0
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
    # Var 0a: Barbara Wang switches American Literature + checks Music History
    Task(
        user_id="S10002",
        instruction="You are Barbara Wang, born 2000-12-15. In registration REGQVAYXAR, you want to switch American Literature (ENG201) to a section that meets on Friday. Also check what other sections Music History (MUS220) has in your other registration. You are organized and brief.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Barbara", "last_name": "Wang", "dob": "2000-12-15"}),
            Action(name="get_student_details", kwargs={"student_id": "S10002"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGQVAYXAR"}),
            Action(name="get_course_details", kwargs={"course_id": "ENG201"}),
            Action(name="get_course_details", kwargs={"course_id": "MUS220"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGQVAYXAR", "switches": [{"course_id": "ENG201", "new_section_id": "ENG201-001"}]}),
        ],
        outputs=[],
    ),
    # Var 0b: Linda Chen switches 2 sections in one reg
    Task(
        user_id="S10007",
        instruction="You are Linda Chen, born 2002-04-10. In registration REGM21B07G, you want to switch Intro to Statistics (STAT111) to a section that doesn't meet in the afternoon, and switch Organic Chemistry (CHEM211) to section CHEM211-001. Check both courses first.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Linda", "last_name": "Chen", "dob": "2002-04-10"}),
            Action(name="get_student_details", kwargs={"student_id": "S10007"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGM21B07G"}),
            Action(name="get_course_details", kwargs={"course_id": "STAT111"}),
            Action(name="get_course_details", kwargs={"course_id": "CHEM211"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGM21B07G", "switches": [{"course_id": "STAT111", "new_section_id": "STAT111-001"}, {"course_id": "CHEM211", "new_section_id": "CHEM211-001"}]}),
        ],
        outputs=[],
    ),
    # Var 0c: Raj Sanchez switches in REGAWO778S, checks Physics sections
    Task(
        user_id="S10009",
        instruction="You are Raj Sanchez, born 2003-05-24. For registration REGAWO778S, you want to switch Electricity & Magnetism (PHYS221) to a morning section. Also check if Thermodynamics (ENGR201) has a TTh section. You don't remember the section IDs.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Raj", "last_name": "Sanchez", "dob": "2003-05-24"}),
            Action(name="get_student_details", kwargs={"student_id": "S10009"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAWO778S"}),
            Action(name="get_course_details", kwargs={"course_id": "PHYS221"}),
            Action(name="get_course_details", kwargs={"course_id": "ENGR201"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGAWO778S", "switches": [{"course_id": "PHYS221", "new_section_id": "PHYS221-001"}]}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 1: auth(email) → student → reg × 2 → course → drop + switch
    # Pattern: 7-action across 2 registrations with output
    # =================================================================
    # Seed 1
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
    # Var 1a: Linda Chen drops from one reg, switches in another
    Task(
        user_id="S10007",
        instruction="Your email is linda.chen78@university.edu. For registration REG2UGL6TB, drop Fundamentals of Nursing (NURS101) — you changed your major. For REGM21B07G, switch Mechanics (PHYS101) to section PHYS101-001. Tell me the NURS101 refund and the new REGM21B07G total.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "linda.chen78@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10007"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG2UGL6TB"}),
            Action(name="drop_courses", kwargs={"registration_id": "REG2UGL6TB", "course_ids": ["NURS101"], "payment_id": "financial_aid_624108"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGM21B07G"}),
            Action(name="get_course_details", kwargs={"course_id": "PHYS101"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGM21B07G", "switches": [{"course_id": "PHYS101", "new_section_id": "PHYS101-001"}]}),
        ],
        outputs=["700"],
    ),
    # Var 1b: Liam Williams across 2 regs
    Task(
        user_id="S10181",
        instruction="Your email is liam.williams69@campus.edu. You want to drop Intro to Psychology (PSYC120) from REG81DO6OU because you took it already. Then for REGGP15CA8, switch Databases (CS400) to section CS400-001. What's the PSYC120 refund amount? Use your credit card.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "liam.williams69@campus.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10181"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG81DO6OU"}),
            Action(name="drop_courses", kwargs={"registration_id": "REG81DO6OU", "course_ids": ["PSYC120"], "payment_id": "credit_card_1533803"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGGP15CA8"}),
            Action(name="get_course_details", kwargs={"course_id": "CS400"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGGP15CA8", "switches": [{"course_id": "CS400", "new_section_id": "CS400-001"}]}),
        ],
        outputs=["900"],
    ),
    # Var 1c: Barbara Wang, 3 regs involved
    Task(
        user_id="S10002",
        instruction="Your email is barbara.wang67@university.edu. Check all your confirmed Fall 2024 registrations. Drop Social Psychology (PSYC300) from REG77Z4ES3. Then switch Calculus I (MATH100) in REGRT28P6U to section MATH100-002. What's the total tuition across all remaining confirmed registrations?",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "barbara.wang67@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10002"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGQVAYXAR"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG08TV4RE"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGRT28P6U"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG77Z4ES3"}),
            Action(name="drop_courses", kwargs={"registration_id": "REG77Z4ES3", "course_ids": ["PSYC300"], "payment_id": "credit_card_7111929"}),
            Action(name="get_course_details", kwargs={"course_id": "MATH100"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGRT28P6U", "switches": [{"course_id": "MATH100", "new_section_id": "MATH100-002"}]}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 2: auth → student → reg → course × 2 → switch 2 at once
    # Pattern: 6-action, multi-switch in single call
    # =================================================================
    # Seed 2
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
    # Var 2a: Mary Perez switches 2 in REG71A57E8
    Task(
        user_id="S10006",
        instruction="You are Mary Perez, born 1999-12-21. In registration REG71A57E8, switch Linear Algebra (MATH300) to section MATH300-001 and Ecology (BIO301) to section BIO301-003. Check both courses for availability first.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Mary", "last_name": "Perez", "dob": "1999-12-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10006"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71A57E8"}),
            Action(name="get_course_details", kwargs={"course_id": "MATH300"}),
            Action(name="get_course_details", kwargs={"course_id": "BIO301"}),
            Action(name="switch_sections", kwargs={"registration_id": "REG71A57E8", "switches": [{"course_id": "MATH300", "new_section_id": "MATH300-001"}, {"course_id": "BIO301", "new_section_id": "BIO301-003"}]}),
        ],
        outputs=[],
    ),
    # Var 2b: Raj Sanchez switches Micro + Music Theory in REGGI3QUPX
    Task(
        user_id="S10009",
        instruction="You are Raj Sanchez, born 2003-05-24. For REGGI3QUPX, switch Microeconomics (ECON110) to ECON110-002 and Music Theory (MUS120) to MUS120-001. You want morning sections. Check availability first.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Raj", "last_name": "Sanchez", "dob": "2003-05-24"}),
            Action(name="get_student_details", kwargs={"student_id": "S10009"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGGI3QUPX"}),
            Action(name="get_course_details", kwargs={"course_id": "ECON110"}),
            Action(name="get_course_details", kwargs={"course_id": "MUS120"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGGI3QUPX", "switches": [{"course_id": "ECON110", "new_section_id": "ECON110-002"}, {"course_id": "MUS120", "new_section_id": "MUS120-001"}]}),
        ],
        outputs=[],
    ),
    # Var 2c: Liam Williams switches CS201 + PHYS221 in REGZJNNS9P
    Task(
        user_id="S10181",
        instruction="You are Liam Williams, born 2001-02-16. In REGZJNNS9P, switch Data Structures (CS201) to CS201-001 and Electricity & Magnetism (PHYS221) to PHYS221-001. Check if new sections are available.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Liam", "last_name": "Williams", "dob": "2001-02-16"}),
            Action(name="get_student_details", kwargs={"student_id": "S10181"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGZJNNS9P"}),
            Action(name="get_course_details", kwargs={"course_id": "CS201"}),
            Action(name="get_course_details", kwargs={"course_id": "PHYS221"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGZJNNS9P", "switches": [{"course_id": "CS201", "new_section_id": "CS201-001"}, {"course_id": "PHYS221", "new_section_id": "PHYS221-001"}]}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 3: auth → student → reg × 3+ → multi-reg inspection
    # Pattern: 5+ actions, multi-registration like retail multi-order
    # =================================================================
    # Seed 3
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
    # Var 3a: Noah Martinez - check all regs, find total tuition
    Task(
        user_id="S10196",
        instruction="Your email is noah.martinez87@student.edu. You have many registrations. You want to see all your Fall 2024 registrations (both confirmed and pending) and know: (1) total confirmed credits, (2) total confirmed tuition, (3) total pending credits, (4) total pending tuition. Be precise.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "noah.martinez87@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10196"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGHMLVHS2"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71K4FPL"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG5QBVNPY"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGTDKVUFF"}),
        ],
        outputs=[],
    ),
    # Var 3b: Yuki Harris - check 3 regs
    Task(
        user_id="S10190",
        instruction="You are Yuki Harris, born 2000-12-28. You have 3 Fall 2024 registrations (1 confirmed, 2 pending). Check all three and tell me the total credits and total tuition for each, plus the grand total. You want an organized breakdown.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Yuki", "last_name": "Harris", "dob": "2000-12-28"}),
            Action(name="get_student_details", kwargs={"student_id": "S10190"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGB45L6D1"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGDV1L303"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGIEMTMYJ"}),
        ],
        outputs=[],
    ),
    # Var 3c: Barbara Wang - 4 confirmed + 1 pending
    Task(
        user_id="S10002",
        instruction="You are Barbara Wang, born 2000-12-15. You want to check ALL your Fall 2024 registrations. For each one, tell me the courses, credits, and tuition. You want to know which registration is the most expensive and which has the fewest credits.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Barbara", "last_name": "Wang", "dob": "2000-12-15"}),
            Action(name="get_student_details", kwargs={"student_id": "S10002"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGQVAYXAR"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG08TV4RE"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGRT28P6U"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG77Z4ES3"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGRPRDVVK"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 4: auth → student → reg → course × 5 → drop 2
    # Pattern: 9-action chain (long), mirrors retail's item-level ops
    # =================================================================
    # Seed 4
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
    # Var 4a: Mary Perez drops 2 from 5-course reg REG71A57E8
    Task(
        user_id="S10006",
        instruction="You are Mary Perez, born 1999-12-21. For registration REG71A57E8, check all 5 courses. You want to drop Cell Biology (BIO110) and Accounting (BUS301) to reduce your course load. Tell me the per-course tuition for each dropped course, total refund, and remaining credits. Use your credit card.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Mary", "last_name": "Perez", "dob": "1999-12-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10006"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71A57E8"}),
            Action(name="get_course_details", kwargs={"course_id": "MATH300"}),
            Action(name="get_course_details", kwargs={"course_id": "BIO110"}),
            Action(name="get_course_details", kwargs={"course_id": "BIO301"}),
            Action(name="get_course_details", kwargs={"course_id": "BIO201"}),
            Action(name="get_course_details", kwargs={"course_id": "BUS301"}),
            Action(name="drop_courses", kwargs={"registration_id": "REG71A57E8", "course_ids": ["BIO110", "BUS301"], "payment_id": "credit_card_3308538"}),
        ],
        outputs=["800", "800", "1600"],
    ),
    # Var 4b: Mary Perez drops 2 from 5-course REGYMMQ8Q6
    Task(
        user_id="S10006",
        instruction="Your email is mary.perez77@student.edu. For REGYMMQ8Q6, look up all 5 courses first. Then drop Intro to Sociology (SOC111) and American Government (POLS120). How much is the total refund? Remaining credits? Use student account.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "mary.perez77@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10006"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGYMMQ8Q6"}),
            Action(name="get_course_details", kwargs={"course_id": "POLS120"}),
            Action(name="get_course_details", kwargs={"course_id": "CHEM300"}),
            Action(name="get_course_details", kwargs={"course_id": "CS201"}),
            Action(name="get_course_details", kwargs={"course_id": "HIST321"}),
            Action(name="get_course_details", kwargs={"course_id": "SOC111"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGYMMQ8Q6", "course_ids": ["SOC111", "POLS120"], "payment_id": "student_account_S10006"}),
        ],
        outputs=["1200"],
    ),
    # Var 4c: Noah Martinez drops from 5-course REG71K4FPL
    Task(
        user_id="S10196",
        instruction="Your email is noah.martinez87@student.edu. For REG71K4FPL (5 courses), look up every course. Then drop the two most expensive ones. Tell me which courses you're dropping, the refund amount for each, and remaining total. Use credit card.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "noah.martinez87@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10196"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71K4FPL"}),
            Action(name="get_course_details", kwargs={"course_id": "PHIL120"}),
            Action(name="get_course_details", kwargs={"course_id": "MUS120"}),
            Action(name="get_course_details", kwargs={"course_id": "POLS120"}),
            Action(name="get_course_details", kwargs={"course_id": "MATH420"}),
            Action(name="get_course_details", kwargs={"course_id": "MATH200"}),
            Action(name="drop_courses", kwargs={"registration_id": "REG71K4FPL", "course_ids": ["POLS120", "MATH420"], "payment_id": "credit_card_8432381"}),
        ],
        outputs=["1000", "900", "1900"],
    ),

    # =================================================================
    # SEED 5: Multi-registration management
    # =================================================================
    # Seed 5
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
    # Var 5a: Raj Sanchez - 3 confirmed regs
    Task(
        user_id="S10009",
        instruction="You are Raj Sanchez, born 2003-05-24. Check all your Fall 2024 confirmed registrations and give me a summary: which courses are in each, total credits per reg, and total tuition per reg. Also calculate the grand total tuition.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Raj", "last_name": "Sanchez", "dob": "2003-05-24"}),
            Action(name="get_student_details", kwargs={"student_id": "S10009"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGGI3QUPX"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAWO778S"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG50N97CJ"}),
        ],
        outputs=[],
    ),
    # Var 5b: Sandra Green - confirm + pending mix
    Task(
        user_id="S10193",
        instruction="Your email is sandra.green97@student.edu. List all your Fall 2024 registrations. For the confirmed one, tell me the courses. For the pending one, tell me the total tuition so I can decide whether to pay or cancel.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "sandra.green97@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10193"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGQI2CLP8"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAWWJNN4"}),
        ],
        outputs=[],
    ),
    # Var 5c: Matthew Perez - 2 confirmed
    Task(
        user_id="S10179",
        instruction="You are Matthew Perez, born 2005-05-28. You want to see both your confirmed Fall 2024 registrations side by side. Tell me which one costs more and which has more credits. You're trying to decide which one to drop.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Matthew", "last_name": "Perez", "dob": "2005-05-28"}),
            Action(name="get_student_details", kwargs={"student_id": "S10179"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG7G0L3RT"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG3NUPUY0"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 6: Credit limit / overloaded student → multi-reg drop
    # =================================================================
    # Seed 6
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
    # Var 6a: Betty White freshman - confirmed + pending, check total
    Task(
        user_id="S10189",
        instruction="Your email is betty.white39@university.edu. You're a freshman (max 16 credits). Check your confirmed registration REGQ08DNX8 and your pending REGBKG8B35. What's the combined total credits? If it exceeds 16, which courses should you drop from the confirmed reg? Tell me the savings.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "betty.white39@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10189"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGQ08DNX8"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGBKG8B35"}),
        ],
        outputs=[],
    ),
    # Var 6b: Linda Chen - way too many regs
    Task(
        user_id="S10007",
        instruction="You are Linda Chen, born 2002-04-10. You're a freshman. Check all your Fall 2024 registrations (confirmed and pending). Calculate your total credits. You need to get under 16 credits total. Cancel all pending registrations and drop courses from confirmed ones if needed. What's the minimum you need to drop?",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Linda", "last_name": "Chen", "dob": "2002-04-10"}),
            Action(name="get_student_details", kwargs={"student_id": "S10007"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG2UGL6TB"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGM21B07G"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGSLAYM0W"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGD4P7PP4"}),
        ],
        outputs=[],
    ),
    # Var 6c: Yuki Harris - 3 regs, calculate total
    Task(
        user_id="S10190",
        instruction="Your email is yuki.harris49@student.edu. You're a freshman (16 credit max). You have 3 Fall 2024 registrations. Check them all. Calculate total credits across confirmed + pending. If over 16, cancel one of the pending registrations. Which one should you cancel to stay closest to but not over 16 credits?",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "yuki.harris49@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10190"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGB45L6D1"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGDV1L303"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGIEMTMYJ"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 7: Switch if available, else drop (conditional)
    # =================================================================
    # Seed 7
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
    # Var 7a: Barbara Wang - switch if possible, else keep
    Task(
        user_id="S10002",
        instruction="Your email is barbara.wang67@university.edu. In REG77Z4ES3, your Operating Systems (CS520) section time is bad. Switch to another CS520 section if available. If not, just keep it and instead switch Macroeconomics (ECON200) to ECON200-002. You don't want to drop anything.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "barbara.wang67@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10002"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG77Z4ES3"}),
            Action(name="get_course_details", kwargs={"course_id": "CS520"}),
            Action(name="get_course_details", kwargs={"course_id": "ECON200"}),
            Action(name="switch_sections", kwargs={"registration_id": "REG77Z4ES3", "switches": [{"course_id": "CS520", "new_section_id": "CS520-003"}]}),
        ],
        outputs=[],
    ),
    # Var 7b: Matthew Perez - drop if can't switch
    Task(
        user_id="S10179",
        instruction="You are Matthew Perez, born 2005-05-28. In REG3NUPUY0, you want to switch Algorithms (CS300) to a different section. If no other section is available, drop it. Tell me the refund if dropped. Use your credit card.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Matthew", "last_name": "Perez", "dob": "2005-05-28"}),
            Action(name="get_student_details", kwargs={"student_id": "S10179"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG3NUPUY0"}),
            Action(name="get_course_details", kwargs={"course_id": "CS300"}),
        ],
        outputs=[],
    ),
    # Var 7c: Liam White - conditional switch or keep
    Task(
        user_id="S10013",
        instruction="You are Liam White, born 2004-05-21. In REGIIOH6CV, check if Social Psychology (PSYC300) has a section with a different instructor. If yes, switch to it. If no, just check what time English Composition (ENG111) meets in other sections.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Liam", "last_name": "White", "dob": "2004-05-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10013"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGIIOH6CV"}),
            Action(name="get_course_details", kwargs={"course_id": "PSYC300"}),
            Action(name="get_course_details", kwargs={"course_id": "ENG111"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGIIOH6CV", "switches": [{"course_id": "PSYC300", "new_section_id": "PSYC300-001"}]}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 8: Budget-based conditional drop
    # =================================================================
    # Seed 8
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
    # Var 8a: Noah Martinez, budget $3000
    Task(
        user_id="S10196",
        instruction="Your email is noah.martinez87@student.edu. Your budget for registration REG71K4FPL is $3000. If it exceeds that, drop the most expensive course. Tell me the final tuition and how much you saved. Credit card for refund.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "noah.martinez87@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10196"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71K4FPL"}),
            Action(name="drop_courses", kwargs={"registration_id": "REG71K4FPL", "course_ids": ["POLS120"], "payment_id": "credit_card_8432381"}),
        ],
        outputs=["3000"],
    ),
    # Var 8b: Betty White, budget $2000
    Task(
        user_id="S10189",
        instruction="You are Betty White, born 2001-06-12. Your budget for REGQ08DNX8 is $2000. Check the registration. If it's over budget, drop courses starting from the most expensive until you're at or under $2000. Tell me exactly which courses to drop and the final total.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Betty", "last_name": "White", "dob": "2001-06-12"}),
            Action(name="get_student_details", kwargs={"student_id": "S10189"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGQ08DNX8"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGQ08DNX8", "course_ids": ["MATH100", "PSYC220"], "payment_id": "credit_card_3839632"}),
        ],
        outputs=["1275"],
    ),
    # Var 8c: Raj Sanchez, budget $2500 for REGAWO778S
    Task(
        user_id="S10009",
        instruction="You are Raj Sanchez, born 2003-05-24. You can only afford $2500 for registration REGAWO778S. It's currently over budget. Drop courses starting with the most expensive. Tell me the final total tuition and which courses remain. Use credit card.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Raj", "last_name": "Sanchez", "dob": "2003-05-24"}),
            Action(name="get_student_details", kwargs={"student_id": "S10009"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAWO778S"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGAWO778S", "course_ids": ["MATH200", "HIST321", "ENGR201"], "payment_id": "credit_card_2133461"}),
        ],
        outputs=["1200"],
    ),

    # =================================================================
    # SEED 9: Change mind mid-conversation
    # =================================================================
    # Seed 9
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
    # Var 9a: Barbara Wang - wants to cancel all, then just one
    Task(
        user_id="S10002",
        instruction="Your email is barbara.wang67@university.edu. You're stressed and want to cancel ALL your registrations. After the agent checks, you realize REGRT28P6U has courses you need. Instead, cancel just the pending one (REGRPRDVVK) and keep everything else.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "barbara.wang67@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10002"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGQVAYXAR"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG08TV4RE"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGRT28P6U"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG77Z4ES3"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGRPRDVVK"}),
            Action(name="cancel_registration", kwargs={"registration_id": "REGRPRDVVK", "reason": "schedule change"}),
        ],
        outputs=[],
    ),
    # Var 9b: Raj Sanchez - wants upgrade, too expensive, just switch
    Task(
        user_id="S10009",
        instruction="You are Raj Sanchez, born 2003-05-24. You initially want to add more courses to REGGI3QUPX. But when you see you already have 10 credits and you're a freshman (max 16), you change your mind. Instead, just switch Data Structures (CS201) to section CS201-001. You are indecisive.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Raj", "last_name": "Sanchez", "dob": "2003-05-24"}),
            Action(name="get_student_details", kwargs={"student_id": "S10009"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGGI3QUPX"}),
            Action(name="get_course_details", kwargs={"course_id": "CS201"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGGI3QUPX", "switches": [{"course_id": "CS201", "new_section_id": "CS201-001"}]}),
        ],
        outputs=[],
    ),
    # Var 9c: Liam Williams - wants to drop, then just switch instead
    Task(
        user_id="S10181",
        instruction="Your email is liam.williams69@campus.edu. You want to drop Modern Europe (HIST321) from REGGP15CA8 because the time is bad. But when the agent shows you there's a Friday section HIST321-002 available, switch to that instead. Don't drop it.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "liam.williams69@campus.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10181"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGGP15CA8"}),
            Action(name="get_course_details", kwargs={"course_id": "HIST321"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGGP15CA8", "switches": [{"course_id": "HIST321", "new_section_id": "HIST321-002"}]}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 10: Tuition calculation across multiple regs
    # =================================================================
    # Seed 10
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
    # Var 10a: Mary Perez total across 3 confirmed
    Task(
        user_id="S10006",
        instruction="Your email is mary.perez77@student.edu. Calculate your total Fall 2024 tuition across all confirmed registrations. Also tell me how many courses and credits total. Give exact numbers.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "mary.perez77@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10006"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGTLVR7MG"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGYMMQ8Q6"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71A57E8"}),
        ],
        outputs=["9475"],
    ),
    # Var 10b: Noah Martinez total confirmed + pending
    Task(
        user_id="S10196",
        instruction="You are Noah Martinez, born 1998-06-14. Tell me: (1) total confirmed tuition, (2) total pending tuition, (3) grand total if all pending is paid. Be exact.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Noah", "last_name": "Martinez", "dob": "1998-06-14"}),
            Action(name="get_student_details", kwargs={"student_id": "S10196"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71K4FPL"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGTDKVUFF"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGHMLVHS2"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG5QBVNPY"}),
        ],
        outputs=["7275", "3875", "11150"],
    ),
    # Var 10c: Barbara Wang grand total
    Task(
        user_id="S10002",
        instruction="You are Barbara Wang, born 2000-12-15. What is your total Fall 2024 tuition across all confirmed registrations? How many credits total? Also tell me the per-registration breakdown.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Barbara", "last_name": "Wang", "dob": "2000-12-15"}),
            Action(name="get_student_details", kwargs={"student_id": "S10002"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGQVAYXAR"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG08TV4RE"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGRT28P6U"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG77Z4ES3"}),
        ],
        outputs=["8100"],
    ),

    # =================================================================
    # SEED 11: Drop + refund calculation
    # =================================================================
    # Seed 11
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
    # Var 11a: Linda Chen drops 2
    Task(
        user_id="S10007",
        instruction="Your email is linda.chen78@university.edu. For REGM21B07G, drop Mechanics (PHYS101, $900) and Organic Chemistry (CHEM211, $600). Tell me total refund and remaining tuition. Use financial aid for refund.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "linda.chen78@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10007"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGM21B07G"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGM21B07G", "course_ids": ["PHYS101", "CHEM211"], "payment_id": "financial_aid_624108"}),
        ],
        outputs=["1500", "2200"],
    ),
    # Var 11b: Betty Harris drops 1 expensive
    Task(
        user_id="S10015",
        instruction="You are Betty Harris, born 2005-02-19. For REGH9VGKY5, you want to drop Intro to Psychology (PSYC120). It's the most expensive at $800. What's the refund and what's the new total? Credit card for refund.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Betty", "last_name": "Harris", "dob": "2005-02-19"}),
            Action(name="get_student_details", kwargs={"student_id": "S10015"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGH9VGKY5"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGH9VGKY5", "course_ids": ["PSYC120"], "payment_id": "credit_card_7156398"}),
        ],
        outputs=["800", "2675"],
    ),
    # Var 11c: Raj Sanchez drops 1 from REGAWO778S
    Task(
        user_id="S10009",
        instruction="Your email is raj.sanchez52@university.edu. For REGAWO778S, drop Genetics (BIO201, $600). Tell me the refund and remaining total. Use credit card for refund.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "raj.sanchez52@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10009"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAWO778S"}),
            Action(name="drop_courses", kwargs={"registration_id": "REGAWO778S", "course_ids": ["BIO201"], "payment_id": "credit_card_2133461"}),
        ],
        outputs=["600", "3100"],
    ),

    # =================================================================
    # SEED 12: Search + compare sections
    # =================================================================
    # Seed 12
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
    # Var 12a: Search CS courses
    Task(
        user_id="S10009",
        instruction="You are Raj Sanchez, born 2003-05-24. You want to search for Computer Science courses. List all CS courses with their credit hours. Then check if Machine Learning (CS621) has an available section that doesn't conflict with your REGAWO778S schedule.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Raj", "last_name": "Sanchez", "dob": "2003-05-24"}),
            Action(name="get_student_details", kwargs={"student_id": "S10009"}),
            Action(name="search_courses_by_department", kwargs={"department": "Computer Science"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAWO778S"}),
            Action(name="get_course_details", kwargs={"course_id": "CS621"}),
        ],
        outputs=[],
    ),
    # Var 12b: Search Math department
    Task(
        user_id="S10007",
        instruction="Your email is linda.chen78@university.edu. You're interested in Math courses. Search the Mathematics department. Then check Calculus II (MATH200) sections - you want the cheapest one. Tell me the section ID, price per credit, and schedule.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "linda.chen78@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10007"}),
            Action(name="search_courses_by_department", kwargs={"department": "Mathematics"}),
            Action(name="get_course_details", kwargs={"course_id": "MATH200"}),
        ],
        outputs=[],
    ),
    # Var 12c: List departments then search
    Task(
        user_id="S10190",
        instruction="You are Yuki Harris, born 2000-12-28. First, list all available departments. Then search for Chemistry courses. You want to know what's available for next semester. Tell me the course names and credit hours.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Yuki", "last_name": "Harris", "dob": "2000-12-28"}),
            Action(name="get_student_details", kwargs={"student_id": "S10190"}),
            Action(name="list_departments", kwargs={}),
            Action(name="search_courses_by_department", kwargs={"department": "Chemistry"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEEDS 13-17: Policy compliance (credit limit, prereqs, status)
    # =================================================================
    # Seed 13: Credit limit
    Task(
        user_id="S10000",
        instruction="Your student id is S10000. You're Sofia Thompson. You want to check your registration REGAIH7WFR (14 credits). Then you want to add two more 4-credit courses. If the agent mentions a credit limit, insist you need them all. You are a freshman.",
        actions=[
            Action(name="get_student_details", kwargs={"student_id": "S10000"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAIH7WFR"}),
        ],
        outputs=[],
    ),
    # Var 13a: Liam White over limit
    Task(
        user_id="S10013",
        instruction="You are Liam White, born 2004-05-21. You're a freshman. Your registration REGIIOH6CV has 17 credits. You want to add a 3-credit course. If the agent says you're over the 16-credit limit, argue that other students have more. Be persistent.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Liam", "last_name": "White", "dob": "2004-05-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10013"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGIIOH6CV"}),
        ],
        outputs=[],
    ),
    # Var 13b: Linda Chen already at 18
    Task(
        user_id="S10007",
        instruction="Your email is linda.chen78@university.edu. You're a freshman with 18 credits in REG2UGL6TB. You want to add one more 3-credit Biology course. If the agent refuses due to credit limits, ask if there's an exception process.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "linda.chen78@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10007"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG2UGL6TB"}),
        ],
        outputs=[],
    ),

    # Seed 14: Prerequisites
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
    # Var 14a: Check prereqs for advanced courses
    Task(
        user_id="S10015",
        instruction="You are Betty Harris, born 2005-02-19. You want to take Machine Learning (CS621) and Quantum Physics (PHYS300). Check if you have the prerequisites. You've completed: BIO301, BUS211, PHYS101, CS120.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Betty", "last_name": "Harris", "dob": "2005-02-19"}),
            Action(name="get_student_details", kwargs={"student_id": "S10015"}),
            Action(name="get_course_details", kwargs={"course_id": "CS621"}),
            Action(name="get_course_details", kwargs={"course_id": "PHYS300"}),
        ],
        outputs=[],
    ),

    # Seed 15: Completed registration → can't modify
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
    # Var 15a: Another completed reg
    Task(
        user_id="S10003",
        instruction="You are Joshua Taylor, born 2002-08-27. You want to change a course in a Spring 2024 registration. If it's completed, ask if there's any way to get an adjustment. You are a sophomore.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Joshua", "last_name": "Taylor", "dob": "2002-08-27"}),
            Action(name="get_student_details", kwargs={"student_id": "S10003"}),
        ],
        outputs=[],
    ),

    # Seed 16: Senior gets compensation
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
    # Var 16a: Another senior compensation
    Task(
        user_id="S10196",
        instruction="You are Noah Martinez, born 1998-06-14. You're a senior. A section in your confirmed registration was cancelled by the university. The course was 4 credits. You want compensation ($50 per credit). Use add_credit to compensate.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Noah", "last_name": "Martinez", "dob": "1998-06-14"}),
            Action(name="get_student_details", kwargs={"student_id": "S10196"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71K4FPL"}),
            Action(name="add_credit", kwargs={"student_id": "S10196", "amount": 200}),
        ],
        outputs=["200"],
    ),

    # Seed 17: Freshman denied compensation
    Task(
        user_id="S10013",
        instruction="You are Liam White, born 2004-05-21. You're a freshman. A section you were enrolled in was cancelled by the university. You want a refund or compensation. Be persistent.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Liam", "last_name": "White", "dob": "2004-05-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10013"}),
        ],
        outputs=[],
    ),
    # Var 17a: Sophomore denied
    Task(
        user_id="S10015",
        instruction="Your email is betty.harris43@campus.edu. You're a sophomore. A section was cancelled and you want compensation. If denied, ask what you CAN get as a sophomore.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "betty.harris43@campus.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10015"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEEDS 18-20: Adversarial / info withholding
    # =================================================================
    # Seed 18: Doesn't remember reg ID
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
    # Var 18a
    Task(
        user_id="S10181",
        instruction="Your email is liam.williams69@campus.edu. You want to switch a course section but can't remember which registration it's in. You know you're taking Data Structures (CS201). Find it and switch to section CS201-001.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "liam.williams69@campus.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10181"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG81DO6OU"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGGP15CA8"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGZJNNS9P"}),
            Action(name="get_course_details", kwargs={"course_id": "CS201"}),
            Action(name="switch_sections", kwargs={"registration_id": "REGZJNNS9P", "switches": [{"course_id": "CS201", "new_section_id": "CS201-001"}]}),
        ],
        outputs=[],
    ),
    # Var 18b
    Task(
        user_id="S10006",
        instruction="You are Mary Perez, born 1999-12-21. You want to drop a Biology course but you don't remember which registration or which Biology course. You know you have multiple. Ask the agent to find all your Biology enrollments across all registrations and list them.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Mary", "last_name": "Perez", "dob": "1999-12-21"}),
            Action(name="get_student_details", kwargs={"student_id": "S10006"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGTLVR7MG"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGYMMQ8Q6"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG71A57E8"}),
        ],
        outputs=[],
    ),

    # Seed 19: Wrong info
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
    # Var 19a: Wrong email first
    Task(
        user_id="S10002",
        instruction="Your email is barbara.wang@university.edu. Wait, the agent can't find you? Try barbara.wang67@university.edu. Once found, check your registration REG77Z4ES3.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "barbara.wang67@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10002"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REG77Z4ES3"}),
        ],
        outputs=[],
    ),

    # Seed 20: Cancel then change mind
    Task(
        user_id="S10091",
        instruction="Your email is wei.clark32@campus.edu. You are very stressed and want to cancel ALL your registrations. But after the agent shows you the details of REGB3YYM33, you realize you need those courses for graduation. Instead, just cancel the pending registration REGSUSFH70.",
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
    # Var 20a: Sandra Green cancel pending
    Task(
        user_id="S10193",
        instruction="Your email is sandra.green97@student.edu. You want to cancel your pending registration REGAWWJNN4. You decided you can't afford it. What's the refund? If pending, you expect full refund.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "sandra.green97@student.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10193"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGAWWJNN4"}),
            Action(name="cancel_registration", kwargs={"registration_id": "REGAWWJNN4", "reason": "financial reasons"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEEDS 21-24: Auth, transfer, search
    # =================================================================
    # Seed 21: name+dob auth + summary
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
    # Var 21a
    Task(
        user_id="S10189",
        instruction="You are Betty White, born 2001-06-12. Show me all my Fall 2024 registrations with a complete breakdown: courses, credits, tuition per course, and total per registration.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Betty", "last_name": "White", "dob": "2001-06-12"}),
            Action(name="get_student_details", kwargs={"student_id": "S10189"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGQ08DNX8"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGBKG8B35"}),
        ],
        outputs=[],
    ),

    # Seed 22: email auth + complex
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

    # Seed 23: Grade appeal → transfer
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
    # Var 23a: Transcript request → transfer
    Task(
        user_id="S10007",
        instruction="Your email is linda.chen78@university.edu. You need an official transcript sent to another university for a transfer application. If the system can't do that, ask to speak with the registrar's office.",
        actions=[
            Action(name="find_student_by_email", kwargs={"email": "linda.chen78@university.edu"}),
            Action(name="get_student_details", kwargs={"student_id": "S10007"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Student needs official transcript for transfer application. Transcript requests are outside scope of registration system."}),
        ],
        outputs=[],
    ),

    # Seed 24: Modify completed → impossible
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
    # Var 24a
    Task(
        user_id="S10133",
        instruction="You are Yuki Perez, born 2004-02-13. You want to drop a course from your completed Spring 2024 registration REGS1ZL7P7 for a partial refund. If it can't be done, transfer me to someone who can help.",
        actions=[
            Action(name="find_student_by_name_dob", kwargs={"first_name": "Yuki", "last_name": "Perez", "dob": "2004-02-13"}),
            Action(name="get_student_details", kwargs={"student_id": "S10133"}),
            Action(name="get_registration_details", kwargs={"registration_id": "REGS1ZL7P7"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Student wants to drop a course from completed Spring 2024 registration for partial refund. Not possible through registration system."}),
        ],
        outputs=[],
    ),
]
