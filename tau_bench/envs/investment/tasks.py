# Copyright Sierra
# Investment portfolio tasks: complex, 8-15 action chains
# Key patterns: cross-account ops, multi-lot sell, IRA rules, long info chains

from tau_bench.types import Action, Task

TASKS = [
    # =================================================================
    # PATTERN A: Cross-account sell → transfer → buy chains (10-12 actions)
    # This is the signature complexity: actions span multiple accounts
    # =================================================================

    # Task 0: Sell in brokerage → transfer to IRA → buy ETF in IRA (11 actions)
    Task(
        user_id="C10014",
        instruction="You are Patricia Hall, born 1985-06-18. You want to sell your Apple stock (the older, cheaper lot from 2023-04-20) in your brokerage account to fund your IRA. First check your brokerage holdings to find the right Apple lot. Then sell it. Transfer the proceeds to your IRA (but stay within the annual contribution limit - check how much you've contributed so far). Then buy SPY ETF with whatever you can transfer. Tell me the exact contribution limit remaining and how many shares of SPY you can buy.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Patricia", "last_name": "Hall", "dob": "1985-06-18"}),
            Action(name="get_client_details", kwargs={"client_id": "C10014"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10031"}),
            Action(name="get_security_details", kwargs={"security_id": "AAPL"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10031", "holding_id": "HNNCILDZM", "quantity": 111}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10032"}),
            Action(name="calculate", kwargs={"expression": "6500 - 0"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "BRK10031", "to_account_id": "IRA10032", "amount": 6500}),
            Action(name="get_security_details", kwargs={"security_id": "SPY"}),
            Action(name="calculate", kwargs={"expression": "6500 / 455.80"}),
            Action(name="place_buy_order", kwargs={"account_id": "IRA10032", "security_id": "SPY", "quantity": 14}),
        ],
        outputs=["6500"],
    ),

    # Task 1: Sell multi-lot, pick the profitable one, transfer to savings (10 actions)
    Task(
        user_id="C10025",
        instruction="Your email is susan.williams19@email.com. You want to sell some of your Exxon Mobil stock from your brokerage. You have 3 lots - sell the one bought earliest (should have the lowest cost basis and highest gain). Check all XOM lots first. After selling, transfer $5000 to your savings account. Tell me the total gain from this sale.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "susan.williams19@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10025"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10058"}),
            Action(name="get_security_details", kwargs={"security_id": "XOM"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10058"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10058", "holding_id": "H98CQK4LT", "quantity": 18}),
            Action(name="calculate", kwargs={"expression": "(107.20 - 79.70) * 18"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "BRK10058", "to_account_id": "SAV10060", "amount": 5000}),
        ],
        outputs=["495"],
    ),

    # Task 2: IRA withdrawal with age check (under 59.5 → penalty) (9 actions)
    Task(
        user_id="C10029",
        instruction="You are Sofia Martin, born 1989-06-14. You need to withdraw $3000 from your IRA to your savings account for an emergency. You know there might be a penalty since you're under 59.5. Check your IRA balance first. Tell me: how much penalty you'll pay, and how much will actually arrive in savings.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sofia", "last_name": "Martin", "dob": "1989-06-14"}),
            Action(name="get_client_details", kwargs={"client_id": "C10029"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10070"}),
            Action(name="calculate", kwargs={"expression": "3000 * 0.10"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "IRA10070", "to_account_id": "SAV10071", "amount": 3000}),
        ],
        outputs=["300", "2700"],
    ),

    # Task 3: IRA contribution limit check + transfer (age >= 50 gets $7500) (10 actions)
    Task(
        user_id="C10004",
        instruction="Your email is amanda.adams89@mail.com. You want to maximize your IRA contribution this year. You're 67 years old. Check: (1) how much you've already contributed, (2) what the limit is for your age, (3) how much more you can contribute. Transfer the remaining amount from your savings to IRA. Tell me exact numbers.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "amanda.adams89@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10004"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10009"}),
            Action(name="get_account_details", kwargs={"account_id": "SAV10010"}),
            Action(name="calculate", kwargs={"expression": "7500 - 6500"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "SAV10010", "to_account_id": "IRA10009", "amount": 1000}),
        ],
        outputs=["6500", "7500", "1000"],
    ),

    # =================================================================
    # PATTERN B: Multi-lot sell selection (like retail item_id selection)
    # Agent must find the correct holding_id from multiple lots
    # =================================================================

    # Task 4: Sell the losing lot of a multi-lot holding for tax-loss harvesting (9 actions)
    Task(
        user_id="C10037",
        instruction="You are Olivia Li, born 1994-11-06. You want to do some tax-loss harvesting. Check your brokerage holdings. Find any stock where you have a LOSING position (current price < cost basis). Sell the lot with the biggest loss. Tell me which stock, how many shares, and the total loss.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Olivia", "last_name": "Li", "dob": "1994-11-06"}),
            Action(name="get_client_details", kwargs={"client_id": "C10037"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10087"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10087"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10087", "holding_id": "HRRVSFFCX", "quantity": 95}),
        ],
        outputs=["DIS", "95", "2037.75"],
    ),

    # Task 5: Sell specific lot by date (10 actions)
    Task(
        user_id="C10015",
        instruction="Your email is brian.martinez23@mail.com. You have multiple lots of GOOGL in your brokerage. You want to sell the lot you bought in October 2023 (the larger position). First check all your GOOGL holdings, then sell just that lot. Tell me the proceeds and the gain/loss.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "brian.martinez23@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10015"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10034"}),
            Action(name="get_security_details", kwargs={"security_id": "GOOGL"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10034", "holding_id": "HYZTKKFZZ", "quantity": 179}),
            Action(name="calculate", kwargs={"expression": "(141.80 - 194.84) * 179"}),
        ],
        outputs=["9494.16"],
    ),

    # =================================================================
    # PATTERN C: Portfolio analysis + rebalancing (12-15 actions)
    # Long info-gathering chains: check all accounts, calculate values
    # =================================================================

    # Task 6: Full portfolio review across all 3 accounts (10 actions)
    Task(
        user_id="C10026",
        instruction="You are Elizabeth Miller, born 1965-08-15. You want a complete portfolio review. For each account (brokerage, IRA, savings), tell me: total value, cash balance, and number of holdings. Then tell me the grand total across all accounts. Be precise.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Elizabeth", "last_name": "Miller", "dob": "1965-08-15"}),
            Action(name="get_client_details", kwargs={"client_id": "C10026"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10061"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "IRA10062"}),
            Action(name="get_account_details", kwargs={"account_id": "SAV10063"}),
        ],
        outputs=[],
    ),

    # Task 7: Check portfolio + sell worst performers + buy bonds (12 actions)
    Task(
        user_id="C10006",
        instruction="Your email is noah.young98@email.com. Review your brokerage portfolio. Find the holding with the worst unrealized loss (biggest negative). Sell it entirely. Then use the proceeds to buy US Treasury 10Y Bond (BOND01). Tell me what you sold, the loss, and how many bonds you can buy. Remember bond trades have a $1 fee.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "noah.young98@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10006"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10014"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10014"}),
            Action(name="get_security_details", kwargs={"security_id": "GLD"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10014", "holding_id": "H2FLU7U6N", "quantity": 160}),
            Action(name="get_security_details", kwargs={"security_id": "BOND01"}),
            Action(name="calculate", kwargs={"expression": "(160 * 183.50) / 95.50"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10014", "security_id": "BOND01", "quantity": 307}),
        ],
        outputs=["GLD", "10892.80"],
    ),

    # =================================================================
    # PATTERN D: Policy compliance (API doesn't check)
    # =================================================================

    # Task 8: Try to buy halted security → agent must refuse
    Task(
        user_id="C10014",
        instruction="You are Patricia Hall, born 1985-06-18. You heard about a great deal on Suspended Trading Inc (HALT01). You want to buy 100 shares in your brokerage. Insist for 2 rounds if the agent says it's not possible.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Patricia", "last_name": "Hall", "dob": "1985-06-18"}),
            Action(name="get_client_details", kwargs={"client_id": "C10014"}),
            Action(name="get_security_details", kwargs={"security_id": "HALT01"}),
        ],
        outputs=[],
    ),

    # Task 9: Try to buy in savings account → agent must refuse
    Task(
        user_id="C10025",
        instruction="Your email is susan.williams19@email.com. You want to buy 50 shares of Apple in your savings account. You have plenty of cash there. If the agent says you can't trade in savings, ask to transfer the money to brokerage first, then buy.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "susan.williams19@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10025"}),
            Action(name="get_account_details", kwargs={"account_id": "SAV10060"}),
            Action(name="get_security_details", kwargs={"security_id": "AAPL"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "SAV10060", "to_account_id": "BRK10058", "amount": 8925}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10058", "security_id": "AAPL", "quantity": 50}),
        ],
        outputs=[],
    ),

    # Task 10: IRA over-contribution attempt → agent must check limit
    Task(
        user_id="C10045",
        instruction="You are Susan Sanchez, born 1990-12-09. You want to transfer $5000 from savings to your IRA. You're under 50 so the limit is $6500. Check how much you've already contributed this year before transferring. If you can't transfer the full $5000, transfer whatever is allowed.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Susan", "last_name": "Sanchez", "dob": "1990-12-09"}),
            Action(name="get_client_details", kwargs={"client_id": "C10045"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10105"}),
            Action(name="get_account_details", kwargs={"account_id": "SAV10106"}),
            Action(name="calculate", kwargs={"expression": "6500 - 6500"}),
        ],
        outputs=["0"],
    ),

    # Task 11: IRA withdrawal under 59.5 → must warn about penalty
    Task(
        user_id="C10015",
        instruction="Your email is brian.martinez23@mail.com. You want to withdraw $2000 from your IRA to your savings for rent. You're 26 years old. If the agent mentions a penalty, ask exactly how much it is and proceed anyway.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "brian.martinez23@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10015"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10035"}),
            Action(name="calculate", kwargs={"expression": "2000 * 0.10"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "IRA10035", "to_account_id": "SAV10036", "amount": 2000}),
        ],
        outputs=["200"],
    ),

    # =================================================================
    # PATTERN E: Cancel pending orders + reorganize (8-10 actions)
    # =================================================================

    # Task 12: Cancel pending buy, use cash differently
    Task(
        user_id="C10023",
        instruction="You are Daniel Davis, born 1970-05-04. You have a pending buy order for GLD in your brokerage. Cancel it. Then use that freed-up cash to buy NVDA instead. How many shares of NVDA can you afford with the freed cash? Tell me the exact amount freed and shares.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Daniel", "last_name": "Davis", "dob": "1970-05-04"}),
            Action(name="get_client_details", kwargs={"client_id": "C10023"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10054"}),
            Action(name="cancel_order", kwargs={"order_id": "ORD3H0Y4VP", "account_id": "BRK10054"}),
            Action(name="get_security_details", kwargs={"security_id": "NVDA"}),
            Action(name="calculate", kwargs={"expression": "(18 * 183.50) / 484.00"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10054", "security_id": "NVDA", "quantity": 6}),
        ],
        outputs=["3303"],
    ),

    # Task 13: Cancel pending sell, then sell from different lot
    Task(
        user_id="C10015",
        instruction="Your email is brian.martinez23@mail.com. You have a pending sell order in your brokerage. Cancel it. Instead, you want to sell your older XOM lot (from 2023-03-01). Check both XOM lots first. Tell me the gain on the one you're selling.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "brian.martinez23@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10015"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10034"}),
            Action(name="cancel_order", kwargs={"order_id": "ORD8R2YKCC", "account_id": "BRK10034"}),
            Action(name="get_security_details", kwargs={"security_id": "XOM"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10034", "holding_id": "HXG8P6BEF", "quantity": 137}),
            Action(name="calculate", kwargs={"expression": "(107.20 - 93.87) * 137"}),
        ],
        outputs=["1826.21"],
    ),

    # =================================================================
    # PATTERN F: Search + compare + buy (long info chain)
    # =================================================================

    # Task 14: Search for bonds, compare prices, buy cheapest
    Task(
        user_id="C10039",
        instruction="You are Sofia Mitchell, born 1965-02-07. You want to buy bonds in your brokerage. Search all available bonds. Find the cheapest one. Buy 50 shares. Remember bond trades have a $1 fee. Tell me which bond, the price, and total cost including fee.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sofia", "last_name": "Mitchell", "dob": "1965-02-07"}),
            Action(name="get_client_details", kwargs={"client_id": "C10039"}),
            Action(name="search_securities", kwargs={"type": "bond"}),
            Action(name="get_security_details", kwargs={"security_id": "BOND01"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10091"}),
            Action(name="calculate", kwargs={"expression": "50 * 95.50 + 1"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10091", "security_id": "BOND01", "quantity": 50}),
        ],
        outputs=["BOND01", "95.50", "4776"],
    ),

    # Task 15: Search tech stocks, find best performer, buy in IRA
    Task(
        user_id="C10037",
        instruction="Your email is olivia.li77@mail.com. Search for Technology sector stocks. You want to buy the one with the highest current price in your IRA. Check your IRA cash first. How many shares can you afford? Buy the maximum whole shares possible.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "olivia.li77@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10037"}),
            Action(name="search_securities", kwargs={"sector": "Technology"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10088"}),
            Action(name="get_security_details", kwargs={"security_id": "NVDA"}),
            Action(name="calculate", kwargs={"expression": "6527.39 / 484.00"}),
            Action(name="place_buy_order", kwargs={"account_id": "IRA10088", "security_id": "NVDA", "quantity": 13}),
        ],
        outputs=["13"],
    ),

    # =================================================================
    # PATTERN G: Adversarial / change mind / info withholding
    # =================================================================

    # Task 16: Wrong account, then correct
    Task(
        user_id="C10028",
        instruction="You are David Brown, born 1961-06-07. You want to sell your NVIDIA holdings. When the agent asks which account, say your IRA. But NVIDIA is actually in your brokerage (you got confused). When the agent doesn't find it in IRA, realize your mistake. Sell all NVIDIA from brokerage. Tell me the total proceeds.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "David", "last_name": "Brown", "dob": "1961-06-07"}),
            Action(name="get_client_details", kwargs={"client_id": "C10028"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10067"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10066"}),
            Action(name="get_security_details", kwargs={"security_id": "NVDA"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10066", "holding_id": "HDMT8VT43", "quantity": 197}),
        ],
        outputs=[],
    ),

    # Task 17: Initially wants to sell everything, changes mind
    Task(
        user_id="C10039",
        instruction="Your email is sofia.mitchell83@mail.com. You're panicking about the market and want to sell EVERYTHING in your brokerage. But after the agent shows your portfolio summary, you realize your US Treasury bonds (BOND01) are actually doing well. Just sell the TSLA positions (both lots) and keep everything else. Tell me the total TSLA proceeds.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "sofia.mitchell83@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10039"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10091"}),
            Action(name="get_security_details", kwargs={"security_id": "TSLA"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10091", "holding_id": "HHX2KBVSI", "quantity": 168}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10091", "holding_id": "HBIAF92MO", "quantity": 11}),
        ],
        outputs=[],
    ),

    # Task 18: Doesn't remember which account or lot
    Task(
        user_id="C10026",
        instruction="Your email is elizabeth.miller99@mail.com. You want to sell some Amazon stock but don't remember which account it's in or how many lots you have. Ask the agent to find all your Amazon positions across all accounts. Then sell the lot with the higher cost basis (since it's losing money) from whichever account it's in.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "elizabeth.miller99@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10026"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10061"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10062"}),
            Action(name="get_security_details", kwargs={"security_id": "AMZN"}),
            Action(name="place_sell_order", kwargs={"account_id": "IRA10062", "holding_id": "HT2018U9N", "quantity": 41}),
        ],
        outputs=[],
    ),

    # =================================================================
    # PATTERN H: Compensation + transfer to human
    # =================================================================

    # Task 19: Premium client gets compensation for failed trade
    Task(
        user_id="C10004",
        instruction="Your email is amanda.adams89@mail.com. You are a premium client. Two of your trades last week failed due to a system error and you want compensation. The policy is $50 per affected trade. After getting the credit, tell me your new brokerage cash balance.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "amanda.adams89@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10004"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10008"}),
            Action(name="add_account_credit", kwargs={"account_id": "BRK10008", "amount": 100}),
        ],
        outputs=["100"],
    ),

    # Task 20: Standard client denied → transfer
    Task(
        user_id="C10014",
        instruction="You are Patricia Hall, born 1985-06-18. You are a standard tier client. You want compensation because a trade you placed was executed at a worse price than expected. If the agent says standard clients can't get compensation through the automated system, ask to speak with a human advisor.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Patricia", "last_name": "Hall", "dob": "1985-06-18"}),
            Action(name="get_client_details", kwargs={"client_id": "C10014"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Standard tier client requesting compensation for trade execution issue. Per policy, standard clients must be transferred to human advisor for compensation requests."}),
        ],
        outputs=[],
    ),

    # =================================================================
    # PATTERN I: Complex multi-step calculation tasks
    # =================================================================

    # Task 21: Calculate total unrealized gains across all accounts
    Task(
        user_id="C10029",
        instruction="You are Sofia Martin, born 1989-06-14. Calculate your total unrealized gain/loss across your brokerage and IRA accounts combined. Break it down: which holdings are winners and which are losers? What's the net unrealized position? Be exact.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sofia", "last_name": "Martin", "dob": "1989-06-14"}),
            Action(name="get_client_details", kwargs={"client_id": "C10029"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10069"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "IRA10070"}),
        ],
        outputs=[],
    ),

    # Task 22: Calculate how much to sell to raise a specific cash amount
    Task(
        user_id="C10023",
        instruction="Your email is daniel.davis21@inbox.com. You need exactly $15000 in cash in your brokerage for a down payment. Check your current cash balance. Calculate how much more you need. Then find the holding with the smallest loss to sell. Tell me exactly how many shares you need to sell to raise the difference.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "daniel.davis21@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10023"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10054"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10054"}),
            Action(name="get_security_details", kwargs={"security_id": "CVX"}),
        ],
        outputs=[],
    ),

    # Task 23: Modify settings across multiple accounts
    Task(
        user_id="C10039",
        instruction="You are Sofia Mitchell, born 1965-02-07. You want to turn ON dividend reinvestment for your brokerage and turn it OFF for your IRA. Check the current settings for both accounts first. Confirm the changes.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sofia", "last_name": "Mitchell", "dob": "1965-02-07"}),
            Action(name="get_client_details", kwargs={"client_id": "C10039"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10091"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10092"}),
            Action(name="modify_account_settings", kwargs={"account_id": "BRK10091", "settings": {"dividend_reinvestment": True}}),
            Action(name="modify_account_settings", kwargs={"account_id": "IRA10092", "settings": {"dividend_reinvestment": False}}),
        ],
        outputs=[],
    ),

    # Task 24: Tax planning - find all losses across accounts for harvesting
    Task(
        user_id="C10028",
        instruction="Your email is david.brown22@email.com. You want to do year-end tax planning. Check your brokerage and IRA portfolios. List ALL holdings with unrealized losses. Calculate the total potential tax-loss harvesting amount (sum of all losses). Which specific holdings would you sell? Don't actually sell yet, just give me the plan.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "david.brown22@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10028"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10066"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "IRA10067"}),
        ],
        outputs=[],
    ),
]
