# Copyright Sierra
# Investment tasks: 25 seeds + 75 variations (3 per seed)
# Focus: 8-15 action chains, cross-account, multi-lot, precise math

from tau_bench.types import Action, Task

TASKS = [
    # =================================================================
    # SEED 0: Sell brokerage → transfer to IRA → buy (11 actions)
    # =================================================================
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
    # Var 0a: Noah Young sells XOM → transfer to IRA → buy QQQ
    Task(
        user_id="C10006",
        instruction="Your email is noah.young98@email.com. You want to sell your Exxon Mobil (XOM) holding in brokerage, transfer as much as possible to your IRA (you're 61, so limit is $7500), and buy QQQ in the IRA. Check your IRA contributions first. How much can you still contribute? How many QQQ shares can you buy?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "noah.young98@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10006"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10014"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10015"}),
            Action(name="calculate", kwargs={"expression": "7500 - 1000"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10014", "holding_id": "HM43D8W3Z", "quantity": 99}),
            Action(name="transfer_funds", kwargs={"from_account_id": "BRK10014", "to_account_id": "IRA10015", "amount": 6500}),
            Action(name="get_security_details", kwargs={"security_id": "QQQ"}),
            Action(name="calculate", kwargs={"expression": "6500 / 385.90"}),
            Action(name="place_buy_order", kwargs={"account_id": "IRA10015", "security_id": "QQQ", "quantity": 16}),
        ],
        outputs=["6500"],
    ),
    # Var 0b: Karen Jackson sell MA profit lot → transfer → buy VTI in IRA
    Task(
        user_id="C10187",
        instruction="You are Karen Jackson, born 1972-02-25. Sell the profitable Mastercard lot (the older one from 2022) in your brokerage. Transfer $7500 to your IRA (you're 52, limit is $7500, check contributions). Buy VTI with the transferred amount. How many shares?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Karen", "last_name": "Jackson", "dob": "1972-02-25"}),
            Action(name="get_client_details", kwargs={"client_id": "C10187"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10447"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10448"}),
            Action(name="calculate", kwargs={"expression": "7500 - 0"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10447", "holding_id": "H8VI5WL0J", "quantity": 45}),
            Action(name="transfer_funds", kwargs={"from_account_id": "BRK10447", "to_account_id": "IRA10448", "amount": 7500}),
            Action(name="get_security_details", kwargs={"security_id": "VTI"}),
            Action(name="calculate", kwargs={"expression": "7500 / 228.40"}),
            Action(name="place_buy_order", kwargs={"account_id": "IRA10448", "security_id": "VTI", "quantity": 32}),
        ],
        outputs=["7500", "32"],
    ),
    # Var 0c: William Zhang sell AMZN older lot → transfer to IRA → buy BOND01
    Task(
        user_id="C10199",
        instruction="Your email is william.zhang61@email.com. Sell your older Amazon lot (from Nov 2022, 80 shares) in brokerage. Transfer $6500 to your IRA (you're 52, limit $7500, check contrib). Buy US Treasury bonds (BOND01) with IRA cash. Remember $1 bond fee. How many bonds and total cost?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "william.zhang61@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10199"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10476"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10477"}),
            Action(name="calculate", kwargs={"expression": "7500 - 0"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10476", "holding_id": "HS9URXIJA", "quantity": 80}),
            Action(name="transfer_funds", kwargs={"from_account_id": "BRK10476", "to_account_id": "IRA10477", "amount": 6500}),
            Action(name="get_security_details", kwargs={"security_id": "BOND01"}),
            Action(name="calculate", kwargs={"expression": "(6500 + 1077) / 95.50"}),
            Action(name="place_buy_order", kwargs={"account_id": "IRA10477", "security_id": "BOND01", "quantity": 79}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 1: Sell multi-lot, pick profitable one, transfer to savings
    # =================================================================
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
    # Var 1a: Brian Martinez sell oldest GOOGL lot
    Task(
        user_id="C10015",
        instruction="You are Brian Martinez, born 1998-08-12. You have 2 GOOGL lots in brokerage. Sell the older one (from Jan 2023, 26 shares - it's profitable). Then transfer $2000 to savings. What's the gain on the GOOGL sale?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Brian", "last_name": "Martinez", "dob": "1998-08-12"}),
            Action(name="get_client_details", kwargs={"client_id": "C10015"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10034"}),
            Action(name="get_security_details", kwargs={"security_id": "GOOGL"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10034", "holding_id": "HNI92IRMU", "quantity": 26}),
            Action(name="calculate", kwargs={"expression": "(141.80 - 117.29) * 26"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "BRK10034", "to_account_id": "SAV10036", "amount": 2000}),
        ],
        outputs=["637.26"],
    ),
    # Var 1b: Elizabeth Miller sell cheaper AMZN lot (older, more profitable)
    Task(
        user_id="C10026",
        instruction="Your email is elizabeth.miller99@mail.com. Check your AMZN holdings - you have 2 lots. Sell the older one (from June 2023) which has a lower cost basis. Transfer the proceeds to savings. What's the total gain and total proceeds?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "elizabeth.miller99@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10026"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10061"}),
            Action(name="get_security_details", kwargs={"security_id": "AMZN"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10061", "holding_id": "H4FZ8OBK3", "quantity": 67}),
            Action(name="calculate", kwargs={"expression": "(186.50 - 115.95) * 67"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "BRK10061", "to_account_id": "SAV10063", "amount": 12495.50}),
        ],
        outputs=["4726.85"],
    ),
    # Var 1c: Sarah White sell profitable GLD lot
    Task(
        user_id="C10194",
        instruction="You are Sarah White, born 1979-04-09. You have 2 GLD (gold) lots. Sell the older one (from Oct 2022) - it should be very profitable. Then transfer $5000 to your savings. Tell me the gain.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sarah", "last_name": "White", "dob": "1979-04-09"}),
            Action(name="get_client_details", kwargs={"client_id": "C10194"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10464"}),
            Action(name="get_security_details", kwargs={"security_id": "GLD"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10464", "holding_id": "HZVWT0Y5K", "quantity": 48}),
            Action(name="calculate", kwargs={"expression": "(183.50 - 116.12) * 48"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "BRK10464", "to_account_id": "SAV10466", "amount": 5000}),
        ],
        outputs=["3234.24"],
    ),

    # =================================================================
    # SEED 2: IRA withdrawal with penalty (under 59.5)
    # =================================================================
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
    # Var 2a: Brian Martinez IRA withdrawal (age 26)
    Task(
        user_id="C10015",
        instruction="Your email is brian.martinez23@mail.com. You need $2000 from your IRA for rent. You're 26. What's the 10% early withdrawal penalty? Transfer it to savings anyway.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "brian.martinez23@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10015"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10035"}),
            Action(name="calculate", kwargs={"expression": "2000 * 0.10"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "IRA10035", "to_account_id": "SAV10036", "amount": 2000}),
        ],
        outputs=["200"],
    ),
    # Var 2b: Emily Wang (age 24) withdrawal
    Task(
        user_id="C10191",
        instruction="You are Emily Wang, born 2000-01-08. Emergency: need $5000 from IRA. You're 24 so there's a penalty. Check IRA balance, calculate penalty, transfer to savings. What are the exact numbers?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Emily", "last_name": "Wang", "dob": "2000-01-08"}),
            Action(name="get_client_details", kwargs={"client_id": "C10191"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10458"}),
            Action(name="calculate", kwargs={"expression": "5000 * 0.10"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "IRA10458", "to_account_id": "SAV10459", "amount": 5000}),
        ],
        outputs=["500", "4500"],
    ),
    # Var 2c: No penalty - Susan Williams age 66
    Task(
        user_id="C10025",
        instruction="Your email is susan.williams19@email.com. You want to withdraw $4000 from IRA to savings. You're 66 so no penalty. Check IRA balance and transfer. Confirm no penalty applies.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "susan.williams19@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10025"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10059"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "IRA10059", "to_account_id": "SAV10060", "amount": 4000}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 3: IRA contribution limit (age-based: <50 → $6500, ≥50 → $7500)
    # =================================================================
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
    # Var 3a: Noah Young (61, $1000 contributed, limit $7500)
    Task(
        user_id="C10006",
        instruction="You are Noah Young, born 1963-10-18. Maximize your IRA contribution. Check how much you've contributed this year and what the limit is (you're over 50). Transfer the remaining from savings. Give exact numbers.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Noah", "last_name": "Young", "dob": "1963-10-18"}),
            Action(name="get_client_details", kwargs={"client_id": "C10006"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10015"}),
            Action(name="get_account_details", kwargs={"account_id": "SAV10016"}),
            Action(name="calculate", kwargs={"expression": "7500 - 1000"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "SAV10016", "to_account_id": "IRA10015", "amount": 6500}),
        ],
        outputs=["1000", "7500", "6500"],
    ),
    # Var 3b: Daniel Davis (54, $1000 contributed, limit $7500)
    Task(
        user_id="C10023",
        instruction="Your email is daniel.davis21@inbox.com. You want to max out your IRA. You're 54. Check contributions so far and calculate remaining room. Transfer from savings. How much can you add?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "daniel.davis21@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10023"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10055"}),
            Action(name="get_account_details", kwargs={"account_id": "SAV10056"}),
            Action(name="calculate", kwargs={"expression": "7500 - 1000"}),
        ],
        outputs=["1000", "7500", "6500"],
    ),
    # Var 3c: Already maxed out (Susan Sanchez, $6500 contributed, under 50 limit $6500)
    Task(
        user_id="C10045",
        instruction="You are Susan Sanchez, born 1990-12-09. You want to transfer $3000 from savings to IRA. Check if you have room under the annual limit. You're under 50 so limit is $6500.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Susan", "last_name": "Sanchez", "dob": "1990-12-09"}),
            Action(name="get_client_details", kwargs={"client_id": "C10045"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10105"}),
            Action(name="calculate", kwargs={"expression": "6500 - 6500"}),
        ],
        outputs=["0"],
    ),

    # =================================================================
    # SEED 4: Tax-loss harvesting - sell losing lot
    # =================================================================
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
    # Var 4a: Patricia Hall sell biggest loser
    Task(
        user_id="C10014",
        instruction="Your email is patricia.hall92@mail.com. Check your brokerage portfolio summary. Identify the holding with the largest unrealized loss. Sell it entirely. Tell me which security, the loss amount, and the proceeds.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "patricia.hall92@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10014"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10031"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10031", "holding_id": "HDFQS3D63", "quantity": 137}),
            Action(name="calculate", kwargs={"expression": "(178.90 - 229.16) * 137"}),
        ],
        outputs=["FIDX1", "6885.62"],
    ),
    # Var 4b: James Moore sell worst holding
    Task(
        user_id="C10018",
        instruction="You are James Moore, born 1979-04-15. Review your brokerage. Sell the holding with the worst performance (biggest unrealized loss %). Tell me the security name, shares, and total loss.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "James", "last_name": "Moore", "dob": "1979-04-15"}),
            Action(name="get_client_details", kwargs={"client_id": "C10018"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10042"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10042"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10042", "holding_id": "H31YV2STN", "quantity": 125}),
            Action(name="calculate", kwargs={"expression": "(228.40 - 275.42) * 125"}),
        ],
        outputs=["VTI", "5877.50"],
    ),
    # Var 4c: Amanda Rodriguez sell worst
    Task(
        user_id="C10184",
        instruction="Your email is amanda.rodriguez34@inbox.com. Check your brokerage portfolio. Your UNH position has a massive loss. Sell it entirely. What are the proceeds and the loss?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "amanda.rodriguez34@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10184"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10439"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10439", "holding_id": "HV08KTRPW", "quantity": 184}),
            Action(name="calculate", kwargs={"expression": "(545.60 - 734.06) * 184"}),
        ],
        outputs=["34676.64"],
    ),

    # =================================================================
    # SEED 5: Sell specific lot by date
    # =================================================================
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
    # Var 5a: Amanda Adams sell TSLA lot by date
    Task(
        user_id="C10004",
        instruction="You are Amanda Adams, born 1957-10-03. You have 2 TSLA lots. Sell the one from November 2023 (117 shares, the losing one). Keep the profitable April 2023 lot. Tell me the exact loss.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Amanda", "last_name": "Adams", "dob": "1957-10-03"}),
            Action(name="get_client_details", kwargs={"client_id": "C10004"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10008"}),
            Action(name="get_security_details", kwargs={"security_id": "TSLA"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10008", "holding_id": "HW9XA3KX7", "quantity": 117}),
            Action(name="calculate", kwargs={"expression": "(255.70 - 323.97) * 117"}),
        ],
        outputs=["7987.59"],
    ),
    # Var 5b: Noah Thomas sell specific DIS lot (Oct 2023)
    Task(
        user_id="C10181",
        instruction="Your email is noah.thomas48@email.com. You have 3 DIS lots. Sell the one from October 2023 (28 shares, it's a loss). Check all DIS lots first. What's the loss amount?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "noah.thomas48@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10181"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10433"}),
            Action(name="get_security_details", kwargs={"security_id": "DIS"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10433", "holding_id": "H46N05FL0", "quantity": 28}),
            Action(name="calculate", kwargs={"expression": "(84.50 - 91.86) * 28"}),
        ],
        outputs=["206.08"],
    ),
    # Var 5c: Daniel Davis sell specific CVX lot
    Task(
        user_id="C10023",
        instruction="You are Daniel Davis, born 1970-05-04. You have 2 CVX lots. Sell the profitable one (bought Jan 2023, cost $119). Keep the other. Tell me gain and proceeds.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Daniel", "last_name": "Davis", "dob": "1970-05-04"}),
            Action(name="get_client_details", kwargs={"client_id": "C10023"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10054"}),
            Action(name="get_security_details", kwargs={"security_id": "CVX"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10054", "holding_id": "HKG4W58RH", "quantity": 74}),
            Action(name="calculate", kwargs={"expression": "(154.80 - 119.00) * 74"}),
        ],
        outputs=["2649.20"],
    ),

    # =================================================================
    # SEED 6: Full portfolio review across all accounts
    # =================================================================
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
    # Var 6a: Amanda Adams full review (3 accounts)
    Task(
        user_id="C10004",
        instruction="Your email is amanda.adams89@mail.com. Give me a complete portfolio summary: brokerage total value, IRA total value, savings balance. What's my total net worth in investments? Break it down.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "amanda.adams89@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10004"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10008"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "IRA10009"}),
            Action(name="get_account_details", kwargs={"account_id": "SAV10010"}),
        ],
        outputs=[],
    ),
    # Var 6b: Sarah White review
    Task(
        user_id="C10194",
        instruction="You are Sarah White, born 1979-04-09. I want to see all my accounts. For each, show me total holdings value, cash, and total. Then calculate grand total. I need exact numbers.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sarah", "last_name": "White", "dob": "1979-04-09"}),
            Action(name="get_client_details", kwargs={"client_id": "C10194"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10464"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "IRA10465"}),
            Action(name="get_account_details", kwargs={"account_id": "SAV10466"}),
        ],
        outputs=[],
    ),
    # Var 6c: Karen Jackson review (premium)
    Task(
        user_id="C10187",
        instruction="Your email is karen.jackson44@mail.com. Full portfolio review please. All three accounts: values, cash, holdings count. Grand total. I'm a premium client and expect detailed numbers.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "karen.jackson44@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10187"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10447"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "IRA10448"}),
            Action(name="get_account_details", kwargs={"account_id": "SAV10449"}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEED 7: Sell worst → buy bonds (long chain)
    # =================================================================
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
    # Var 7a: David Brown sell worst → buy Corporate Bond
    Task(
        user_id="C10028",
        instruction="You are David Brown, born 1961-06-07. Check brokerage portfolio. Sell the holding with the largest dollar loss. Buy Corporate Bond Fund AAA (BOND02) with the proceeds. How many bonds? $1 fee per bond trade.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "David", "last_name": "Brown", "dob": "1961-06-07"}),
            Action(name="get_client_details", kwargs={"client_id": "C10028"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10066"}),
            Action(name="get_security_details", kwargs={"security_id": "NVDA"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10066", "holding_id": "HDMT8VT43", "quantity": 197}),
            Action(name="get_security_details", kwargs={"security_id": "BOND02"}),
            Action(name="calculate", kwargs={"expression": "(197 * 484.00) / 102.30"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10066", "security_id": "BOND02", "quantity": 932}),
        ],
        outputs=["NVDA", "14985.79"],
    ),
    # Var 7b: Emily Wang sell SPY loss → buy BND
    Task(
        user_id="C10191",
        instruction="Your email is emily.wang11@email.com. Your SPY position has a huge loss. Sell it all. Then buy BND (Vanguard Bond ETF) with the proceeds. BND is an ETF so no trade fee. How many shares?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "emily.wang11@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10191"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10457"}),
            Action(name="get_security_details", kwargs={"security_id": "SPY"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10457", "holding_id": "H08GSG8UE", "quantity": 175}),
            Action(name="get_security_details", kwargs={"security_id": "BND"}),
            Action(name="calculate", kwargs={"expression": "(175 * 455.80) / 72.30"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10457", "security_id": "BND", "quantity": 1102}),
        ],
        outputs=["SPY", "25849.25"],
    ),
    # Var 7c: James Moore rebalance - sell PG loss → buy BOND01
    Task(
        user_id="C10018",
        instruction="You are James Moore, born 1979-04-15. Sell your Procter & Gamble (PG) position (it's losing). Then buy US Treasury bonds (BOND01). Bond fee is $1. How many bonds can you get? What's the PG loss?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "James", "last_name": "Moore", "dob": "1979-04-15"}),
            Action(name="get_client_details", kwargs={"client_id": "C10018"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10042"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10042", "holding_id": "HJMIYQFY7", "quantity": 154}),
            Action(name="get_security_details", kwargs={"security_id": "BOND01"}),
            Action(name="calculate", kwargs={"expression": "(154 * 153.20) / 95.50"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10042", "security_id": "BOND01", "quantity": 247}),
        ],
        outputs=["4207.28"],
    ),

    # =================================================================
    # SEEDS 8-11: Policy compliance (buy halted, savings, IRA limits)
    # =================================================================
    Task(  # Seed 8: Buy halted → refuse
        user_id="C10014",
        instruction="You are Patricia Hall, born 1985-06-18. You heard about Suspended Trading Inc (HALT01). Buy 100 shares in brokerage. Insist for 2 rounds if told it's not possible.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Patricia", "last_name": "Hall", "dob": "1985-06-18"}),
            Action(name="get_client_details", kwargs={"client_id": "C10014"}),
            Action(name="get_security_details", kwargs={"security_id": "HALT01"}),
        ],
        outputs=[],
    ),
    Task(  # Var 8a
        user_id="C10029",
        instruction="Your email is sofia.martin94@mail.com. Buy 50 shares of Delisted Corp (DLIST01) in your brokerage. If told it's delisted, ask if there's any way to buy it. Then accept.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "sofia.martin94@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10029"}),
            Action(name="get_security_details", kwargs={"security_id": "DLIST01"}),
        ],
        outputs=[],
    ),
    Task(  # Var 8b: Buy in savings → redirect to transfer + buy
        user_id="C10025",
        instruction="Your email is susan.williams19@email.com. Buy 50 AAPL in your savings account. If told you can't trade in savings, transfer money to brokerage first, then buy.",
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
    Task(  # Var 8c: IRA maxed out → can't contribute
        user_id="C10026",
        instruction="You are Elizabeth Miller, born 1965-08-15. Transfer $2000 from savings to IRA. You're 59, limit $7500. Check if you have room. If already maxed, don't transfer.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Elizabeth", "last_name": "Miller", "dob": "1965-08-15"}),
            Action(name="get_client_details", kwargs={"client_id": "C10026"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10062"}),
            Action(name="calculate", kwargs={"expression": "7500 - 6500"}),
            Action(name="transfer_funds", kwargs={"from_account_id": "SAV10063", "to_account_id": "IRA10062", "amount": 1000}),
        ],
        outputs=["1000"],
    ),

    # =================================================================
    # SEEDS 12-13: Cancel pending + reorganize
    # =================================================================
    Task(  # Seed 12
        user_id="C10023",
        instruction="You are Daniel Davis, born 1970-05-04. Cancel your pending GLD buy order. Then buy NVDA instead. How many NVDA shares with the freed cash?",
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
    Task(  # Var 12a: Olivia Li cancel pending BND buy, buy AAPL instead
        user_id="C10037",
        instruction="Your email is olivia.li77@mail.com. Cancel your pending buy order in brokerage. Then buy AAPL instead. How many shares can you afford with just the freed amount?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "olivia.li77@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10037"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10087"}),
            Action(name="cancel_order", kwargs={"order_id": "ORD4ABUFWB", "account_id": "BRK10087"}),
            Action(name="get_security_details", kwargs={"security_id": "AAPL"}),
            Action(name="calculate", kwargs={"expression": "(8 * 72.30) / 178.50"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10087", "security_id": "AAPL", "quantity": 3}),
        ],
        outputs=[],
    ),
    Task(  # Seed 13: Cancel sell + sell different lot
        user_id="C10015",
        instruction="Your email is brian.martinez23@mail.com. Cancel your pending sell order. Then sell your older XOM lot (March 2023, 137 shares). What's the gain?",
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
    Task(  # Var 13a: Noah Thomas cancel pending AGG buy, buy SPY
        user_id="C10181",
        instruction="You are Noah Thomas, born 1957-08-14. Cancel your pending AGG buy order. Use the freed cash to buy SPY instead. How many SPY shares?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Noah", "last_name": "Thomas", "dob": "1957-08-14"}),
            Action(name="get_client_details", kwargs={"client_id": "C10181"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10433"}),
            Action(name="cancel_order", kwargs={"order_id": "ORDV1RDNF4", "account_id": "BRK10433"}),
            Action(name="get_security_details", kwargs={"security_id": "SPY"}),
            Action(name="calculate", kwargs={"expression": "(47 * 97.60) / 455.80"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10433", "security_id": "SPY", "quantity": 10}),
        ],
        outputs=["10"],
    ),

    # =================================================================
    # SEEDS 14-15: Search + compare + buy chains
    # =================================================================
    Task(  # Seed 14
        user_id="C10039",
        instruction="You are Sofia Mitchell, born 1965-02-07. Search all bonds. Buy the cheapest one (50 shares). Bond fee $1. Tell me which, price, and total cost.",
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
    Task(  # Var 14a: Search ETFs, buy cheapest in IRA
        user_id="C10006",
        instruction="Your email is noah.young98@email.com. Search all ETFs. Buy the cheapest one (max shares you can afford) in your IRA. ETFs have no fee. Which ETF and how many shares?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "noah.young98@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10006"}),
            Action(name="search_securities", kwargs={"type": "etf"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10015"}),
            Action(name="get_security_details", kwargs={"security_id": "BND"}),
            Action(name="calculate", kwargs={"expression": "2382.33 / 72.30"}),
            Action(name="place_buy_order", kwargs={"account_id": "IRA10015", "security_id": "BND", "quantity": 32}),
        ],
        outputs=["BND", "32"],
    ),
    Task(  # Var 14b: Search Energy stocks
        user_id="C10194",
        instruction="You are Sarah White, born 1979-04-09. Search Energy sector stocks. Which ones are available? Check their prices. Buy 20 shares of the cheaper one in brokerage. No fee for stocks.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sarah", "last_name": "White", "dob": "1979-04-09"}),
            Action(name="get_client_details", kwargs={"client_id": "C10194"}),
            Action(name="search_securities", kwargs={"sector": "Energy"}),
            Action(name="get_security_details", kwargs={"security_id": "XOM"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10464"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10464", "security_id": "XOM", "quantity": 20}),
        ],
        outputs=[],
    ),
    Task(  # Seed 15
        user_id="C10037",
        instruction="Your email is olivia.li77@mail.com. Search Technology sector stocks. Buy the most expensive one (highest price) in your IRA. Max whole shares. How many?",
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
    Task(  # Var 15a: Search mutual funds, buy in brokerage
        user_id="C10199",
        instruction="You are William Zhang, born 1972-06-05. Search for mutual funds. Buy 30 shares of the cheapest one in your brokerage. No fee for mutual funds. What's the total cost?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "William", "last_name": "Zhang", "dob": "1972-06-05"}),
            Action(name="get_client_details", kwargs={"client_id": "C10199"}),
            Action(name="search_securities", kwargs={"type": "mutual_fund"}),
            Action(name="get_security_details", kwargs={"security_id": "VFUND1"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10476"}),
            Action(name="calculate", kwargs={"expression": "30 * 145.20"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10476", "security_id": "VFUND1", "quantity": 30}),
        ],
        outputs=["4356"],
    ),

    # =================================================================
    # SEEDS 16-18: Adversarial / change mind
    # =================================================================
    Task(  # Seed 16: Wrong account
        user_id="C10028",
        instruction="You are David Brown, born 1961-06-07. Sell your NVIDIA. Say it's in your IRA. When not found there, realize it's in brokerage. Sell all.",
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
    Task(  # Var 16a: Patricia Hall wrong lot ID
        user_id="C10014",
        instruction="Your email is patricia.hall92@mail.com. You want to sell your Mastercard stock. You think it's holding 'H123456'. When the agent says that ID doesn't exist, ask them to find your MA holdings. Sell the losing lot (from March 2023).",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "patricia.hall92@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10014"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10031"}),
            Action(name="get_security_details", kwargs={"security_id": "MA"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10031", "holding_id": "HS9TOQW9J", "quantity": 22}),
        ],
        outputs=[],
    ),
    Task(  # Seed 17: Panic sell → change mind
        user_id="C10039",
        instruction="Your email is sofia.mitchell83@mail.com. Market is crashing! Sell EVERYTHING in brokerage. But after seeing portfolio, keep the bonds. Just sell the TSLA lots.",
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
    Task(  # Var 17a: Want to sell, then just switch to bonds
        user_id="C10018",
        instruction="You are James Moore, born 1979-04-15. You're nervous. Initially want to sell all stocks. But after checking, decide to only sell AMZN (losing) and buy Municipal bonds (BOND03) with proceeds. $1 bond fee.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "James", "last_name": "Moore", "dob": "1979-04-15"}),
            Action(name="get_client_details", kwargs={"client_id": "C10018"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10042"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10042", "holding_id": "HHTF4PYZR", "quantity": 20}),
            Action(name="get_security_details", kwargs={"security_id": "BOND03"}),
            Action(name="calculate", kwargs={"expression": "(20 * 186.50) / 98.70"}),
            Action(name="place_buy_order", kwargs={"account_id": "BRK10042", "security_id": "BOND03", "quantity": 37}),
        ],
        outputs=[],
    ),
    Task(  # Seed 18: Don't remember which account
        user_id="C10026",
        instruction="Your email is elizabeth.miller99@mail.com. Sell some Amazon stock. Don't know which account. Agent should check all. Sell the lot with higher cost basis (losing more).",
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
    Task(  # Var 18a: Mary Clark can't find GOOGL
        user_id="C10180",
        instruction="You are Mary Clark, born 1997-12-09. You want to sell your Alphabet (GOOGL) stock. You don't remember if it's in your brokerage or IRA. Check both accounts. Sell the more profitable lot.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Mary", "last_name": "Clark", "dob": "1997-12-09"}),
            Action(name="get_client_details", kwargs={"client_id": "C10180"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10430"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10431"}),
            Action(name="get_security_details", kwargs={"security_id": "GOOGL"}),
            Action(name="place_sell_order", kwargs={"account_id": "BRK10430", "holding_id": "HEOL0TA8R", "quantity": 190}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEEDS 19-20: Compensation
    # =================================================================
    Task(  # Seed 19: Premium gets credit
        user_id="C10004",
        instruction="Your email is amanda.adams89@mail.com. Premium client. Two trades failed last week due to system error. $50 per trade. Credit my brokerage. What's new balance?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "amanda.adams89@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10004"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10008"}),
            Action(name="add_account_credit", kwargs={"account_id": "BRK10008", "amount": 100}),
        ],
        outputs=["100"],
    ),
    Task(  # Var 19a: Another premium client
        user_id="C10187",
        instruction="You are Karen Jackson, born 1972-02-25. Premium client. Three trades had excessive fees totaling $80. I want a refund credited to my brokerage.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Karen", "last_name": "Jackson", "dob": "1972-02-25"}),
            Action(name="get_client_details", kwargs={"client_id": "C10187"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10447"}),
            Action(name="add_account_credit", kwargs={"account_id": "BRK10447", "amount": 80}),
        ],
        outputs=["80"],
    ),
    Task(  # Seed 20: Standard denied → transfer
        user_id="C10014",
        instruction="You are Patricia Hall, born 1985-06-18. Standard tier. Trade executed at wrong price. Want compensation. If can't get it automatically, transfer to human.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Patricia", "last_name": "Hall", "dob": "1985-06-18"}),
            Action(name="get_client_details", kwargs={"client_id": "C10014"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Standard tier client requesting compensation for trade execution issue. Per policy, standard clients must be transferred to human advisor."}),
        ],
        outputs=[],
    ),
    Task(  # Var 20a: Another standard denied
        user_id="C10028",
        instruction="Your email is david.brown22@email.com. Standard client. System glitch caused you to miss a trade. Want $200 compensation. If denied, speak to someone.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "david.brown22@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10028"}),
            Action(name="transfer_to_human_agents", kwargs={"summary": "Standard tier client requesting $200 compensation for system glitch. Per policy, must transfer to human advisor."}),
        ],
        outputs=[],
    ),

    # =================================================================
    # SEEDS 21-24: Complex calculations + planning
    # =================================================================
    Task(  # Seed 21: Total unrealized P&L
        user_id="C10029",
        instruction="You are Sofia Martin, born 1989-06-14. Calculate total unrealized gain/loss across brokerage and IRA combined. Break down winners vs losers.",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Sofia", "last_name": "Martin", "dob": "1989-06-14"}),
            Action(name="get_client_details", kwargs={"client_id": "C10029"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10069"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "IRA10070"}),
        ],
        outputs=[],
    ),
    Task(  # Var 21a: Amanda Adams full P&L
        user_id="C10004",
        instruction="Your email is amanda.adams89@mail.com. What's my total unrealized gain/loss across ALL accounts? Which individual holding has the biggest loss? Biggest gain?",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "amanda.adams89@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10004"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10008"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "IRA10009"}),
        ],
        outputs=[],
    ),
    Task(  # Seed 22: Raise specific cash amount
        user_id="C10023",
        instruction="Your email is daniel.davis21@inbox.com. Need exactly $15000 in brokerage cash for a down payment. Check balance. Calculate shortfall. Sell the holding with smallest loss to cover it.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "daniel.davis21@inbox.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10023"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10054"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10054"}),
            Action(name="get_security_details", kwargs={"security_id": "CVX"}),
        ],
        outputs=[],
    ),
    Task(  # Var 22a: Mary Clark needs $30000
        user_id="C10180",
        instruction="You are Mary Clark, born 1997-12-09. You need $30000 total cash in brokerage. Check current cash. If not enough, sell the most profitable holding to make up the difference. How much more do you need? What do you sell?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Mary", "last_name": "Clark", "dob": "1997-12-09"}),
            Action(name="get_client_details", kwargs={"client_id": "C10180"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10430"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10430"}),
        ],
        outputs=[],
    ),
    Task(  # Seed 23: Settings modification
        user_id="C10039",
        instruction="You are Sofia Mitchell, born 1965-02-07. Turn ON dividend reinvestment for brokerage, OFF for IRA. Check current settings first.",
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
    Task(  # Var 23a
        user_id="C10014",
        instruction="Your email is patricia.hall92@mail.com. Change both your brokerage and IRA to have dividend reinvestment OFF. Check current settings first.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "patricia.hall92@mail.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10014"}),
            Action(name="get_account_details", kwargs={"account_id": "BRK10031"}),
            Action(name="get_account_details", kwargs={"account_id": "IRA10032"}),
            Action(name="modify_account_settings", kwargs={"account_id": "BRK10031", "settings": {"dividend_reinvestment": False}}),
            Action(name="modify_account_settings", kwargs={"account_id": "IRA10032", "settings": {"dividend_reinvestment": False}}),
        ],
        outputs=[],
    ),
    Task(  # Seed 24: Tax planning - list all losses
        user_id="C10028",
        instruction="Your email is david.brown22@email.com. Year-end tax planning. Check brokerage and IRA portfolios. List ALL holdings with unrealized losses. Calculate total potential tax-loss amount. Don't sell yet, just plan.",
        actions=[
            Action(name="find_client_by_email", kwargs={"email": "david.brown22@email.com"}),
            Action(name="get_client_details", kwargs={"client_id": "C10028"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10066"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "IRA10067"}),
        ],
        outputs=[],
    ),
    Task(  # Var 24a: Susan Williams tax planning
        user_id="C10025",
        instruction="You are Susan Williams, born 1958-07-17. Check your brokerage portfolio. List all losing positions. What's the total potential tax-loss harvest? Which lots would you sell?",
        actions=[
            Action(name="find_client_by_name_dob", kwargs={"first_name": "Susan", "last_name": "Williams", "dob": "1958-07-17"}),
            Action(name="get_client_details", kwargs={"client_id": "C10025"}),
            Action(name="get_portfolio_summary", kwargs={"account_id": "BRK10058"}),
        ],
        outputs=[],
    ),
]
