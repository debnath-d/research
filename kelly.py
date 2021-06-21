import random

INITIAL_CAPITAL = 1000
TRADES = 1000
SIMULATIONS = 1

WIN_PROBABILITY = 60/100
RISK_REWARD = 1
ALLOCATION = 1/100
COMMISSION = 10/100


PRECISION = 4
DISPLAY_EACH_TRADE = True if SIMULATIONS == 1 else False


commission_adjusted_risk_reward = (
    1 - COMMISSION) / (1/RISK_REWARD + COMMISSION)

expected_return_on_risk = round(
    100 * (WIN_PROBABILITY * (commission_adjusted_risk_reward + 1) - 1),
    PRECISION
)


def percentage(x):
    return round((x/INITIAL_CAPITAL - 1)*100, PRECISION)


def return_per_trade(capital, period):
    return round(((capital/INITIAL_CAPITAL)**(1/period) - 1) * 100, PRECISION)


def return_on_risk_per_trade(per_trade_return):
    return round(per_trade_return/ALLOCATION, PRECISION)


def print_result(winner, loser, current_capital, max_profit, biggest_drawdown, per_trade, return_on_risk, realized_rrr):
    print('---\n')
    print(
        f"(W, L) = ({winner}, {loser}), capital = {current_capital}")
    print()

    print(
        f"Return on capital (net) = {percentage(current_capital)}%"
    )
    print(
        f"Return on capital (per trade) = {per_trade}%"
    )
    print(
        f"Return on risk (net) = {return_on_risk}%"
    )
    print(
        f"Return on risk (per trade) = {return_on_risk_per_trade(per_trade_return=per_trade)}%"
    )
    print(
        f"Realized RR Ratio (net) = {realized_rrr}"
    )
    print(f"Highest profit = {max_profit} ({percentage(max_profit)}%)")
    print(
        f"Biggest drawdown = {biggest_drawdown} ({percentage(biggest_drawdown)}%)")


def simulate_trades():
    max_profit = biggest_drawdown = current_capital = INITIAL_CAPITAL
    winner = loser = total_risk = 0

    for x in range(TRADES):
        outcome = random.random() < WIN_PROBABILITY

        multiplier = commission_adjusted_risk_reward if outcome else -1
        if outcome:
            winner += 1
        else:
            loser += 1

        risk = round(current_capital * ALLOCATION, PRECISION)

        total_risk += risk

        profit = round(risk * multiplier, PRECISION)
        current_capital = round(current_capital + profit, PRECISION)

        if current_capital > max_profit:
            max_profit = current_capital
        elif current_capital < biggest_drawdown:
            biggest_drawdown = current_capital

        per_trade = return_per_trade(capital=current_capital, period=x+1)

        return_on_risk = round(
            100*(current_capital - INITIAL_CAPITAL)/total_risk, PRECISION)

        try:
            realized_rrr = round(
                -percentage(current_capital) / percentage(biggest_drawdown),
                PRECISION
            )
        except Exception as e:
            # print(e)
            realized_rrr = 'undefined'

        if DISPLAY_EACH_TRADE:
            arguments = {
                'winner': winner,
                'loser': loser,
                'current_capital': current_capital,
                'max_profit': max_profit,
                'biggest_drawdown': biggest_drawdown,
                'per_trade': per_trade,
                'return_on_risk': return_on_risk,
                'realized_rrr': realized_rrr,
            }

            print_result(**arguments)

    if not DISPLAY_EACH_TRADE:
        arguments = {
            'winner': winner,
            'loser': loser,
            'current_capital': current_capital,
            'max_profit': max_profit,
            'biggest_drawdown': biggest_drawdown,
            'per_trade': per_trade,
            'return_on_risk': return_on_risk,
            'realized_rrr': realized_rrr,
        }

        print_result(**arguments)


for x in range(SIMULATIONS):
    simulate_trades()


print(f'\nAdjusted RR = {commission_adjusted_risk_reward}')
print(f'Expected Return on Risk = {expected_return_on_risk}%')
