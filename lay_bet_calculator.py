import streamlit as st

def calculate_maximum_stake_and_profit(bank_size, losing_streak, odds, winning_streak, min_risk_percentage=0.01):
    # Minimum stake amount based on the minimum risk percentage
    min_stake = bank_size * (min_risk_percentage / 100)
    
    # Total liability to recover after a losing streak
    total_loss = 0
    for _ in range(losing_streak):
        total_loss += max(min_stake, (bank_size * 0.01)) * (odds - 1)  # Liability per bet

    # Maximum suggested stake based on anticipated winning streak
    maximum_suggested_stake = total_loss / winning_streak if winning_streak > 0 else 0
    maximum_suggested_stake = max(maximum_suggested_stake, min_stake)  # Ensure stake is above the minimum

    # Calculate possible profit after a complete cycle (losing streak + winning streak)
    total_winnings = winning_streak * maximum_suggested_stake  # Total winnings from winning bets
    total_liability = losing_streak * maximum_suggested_stake * (odds - 1)  # Total liability from losing bets
    possible_profit = total_winnings - total_liability

    return maximum_suggested_stake, possible_profit


# Streamlit App Layout
st.set_page_config(page_title="Lay Bet Calculator", page_icon="💰", layout="centered")

# Header Section
st.title("💰 Lay Bet Stake Calculator")
st.markdown(
    """
    Welcome to the **Lay Bet Calculator**! This tool helps you manage your lay bets effectively by:
    - Calculating the **maximum suggested stake**.
    - Estimating the **possible profit** after a full betting cycle.
    """
)
st.divider()

# Input Section with Columns
reset = st.button("🔄 Reset")

if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = False

if reset:
    st.session_state.reset_flag = True

# Default values for inputs
default_bank_size = 1000.0
default_losing_streak = 10
default_odds = 4.0
default_winning_streak = 5
default_min_risk_percentage = 0.01

if st.session_state.reset_flag:
    bank_size = st.number_input("Enter your bank size:", min_value=0.0, step=1.0, value=default_bank_size, key="bank_size_reset")
    losing_streak = st.number_input("Anticipated losing streak:", min_value=1, step=1, value=default_losing_streak, key="losing_streak_reset")
    odds = st.number_input("Odds you are laying at:", min_value=1.01, step=0.01, value=default_odds, key="odds_reset")
    winning_streak = st.number_input("Expected winning streak:", min_value=1, step=1, value=default_winning_streak, key="winning_streak_reset")
    min_risk_percentage = st.slider("Minimum risk percentage of bank:", min_value=0.01, max_value=10.0, value=default_min_risk_percentage, step=0.01, key="min_risk_reset")
else:
    bank_size = st.number_input("Enter your bank size:", min_value=0.0, step=1.0, value=default_bank_size)
    losing_streak = st.number_input("Anticipated losing streak:", min_value=1, step=1, value=default_losing_streak)
    odds = st.number_input("Odds you are laying at:", min_value=1.01, step=0.01, value=default_odds)
    winning_streak = st.number_input("Expected winning streak:", min_value=1, step=1, value=default_winning_streak)
    min_risk_percentage = st.slider("Minimum risk percentage of bank:", min_value=0.01, max_value=10.0, value=default_min_risk_percentage, step=0.01)

# Calculate Button
if st.button("💡 Calculate Maximum Stake and Profit"):
    # Perform Calculation
    maximum_suggested_stake, possible_profit = calculate_maximum_stake_and_profit(
        bank_size, losing_streak, odds, winning_streak, min_risk_percentage
    )

    # Display Results
    st.subheader("📊 Results")
    st.write(f"**Maximum Suggested Stake:** {maximum_suggested_stake:.2f}")
    st.write(f"**Possible Profit (after {losing_streak + winning_streak} bets):** {possible_profit:.2f}")
    st.success(
        "The maximum suggested stake ensures recovery from losses during the losing streak, "
        "while the profit estimation considers both the losing and winning streaks."
    )
else:
    st.info("Enter your details and click **Calculate Maximum Stake and Profit** to see results!")

# Footer
st.divider()
st.markdown(
    """
    **Disclaimer:** This tool is for informational purposes only. Losing streaks may not follow clear patterns. Always gamble responsibly.
    """
)
