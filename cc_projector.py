# Forrit sem áætlar kreditkortareikninginn minn um hver mánaðarmót
# Streamlit útgáfa
# Guðjón Emilsson
# 23. apríl 2025

import datetime
import streamlit as st

# Sækja dagsetningu dagsins í dag
current_date = datetime.datetime.now()

# Reikna upphaf og endi tímabils
if current_date.day > 26:
    billing_start = datetime.datetime(current_date.year, current_date.month, 27)
else:
    if current_date.month == 1:
        billing_start = datetime.datetime(current_date.year - 1, 12, 27)
    else:
        billing_start = datetime.datetime(current_date.year, current_date.month - 1, 27)

if current_date.month == 11:
    billing_end = datetime.datetime(current_date.year, 12, 26)
elif current_date.month == 12:
    billing_end = datetime.datetime(current_date.year + 1, 1, 26)
elif current_date.day > 26:
    billing_end = datetime.datetime(current_date.year, current_date.month + 1, 26)
else:
    billing_end = datetime.datetime(current_date.year, current_date.month, 26)

# Sýna upplýsingar um tímabilið
st.title("📊 Kreditkortareikningsspá")
st.markdown(f"**Tímabil:** {billing_start.date()} - {billing_end.date()}")
st.markdown(f"**Dagsetning í dag:** {current_date.date()}")

# Innsláttur notanda
credit_card_amount1 = st.number_input("Staða á kreditkorti Arion Banka:", min_value=0.0, step=100.0)
credit_card_amount2 = st.number_input("Staða á kreditkorti Landsbankanum:", min_value=0.0, step=100.0)
goal = st.number_input("Markmið fyrir tímabilið (kr.):", min_value=0.0, step=1000.0)

# Reikna út
bill_now = credit_card_amount1 + credit_card_amount2
total_days = (billing_end - billing_start).days + 1
days_elapsed = (current_date - billing_start).days

if days_elapsed == 0:
    st.warning("Tímabilið hófst í dag – ekki hægt að reikna áætlun.")
else:
    projected_bill1 = credit_card_amount1 * total_days / days_elapsed
    projected_bill2 = credit_card_amount2 * total_days / days_elapsed
    projected_total_bill = bill_now * total_days / days_elapsed
    total_bill_per_day = projected_total_bill / total_days

    goal_per_day = goal / total_days
    to_get_goal = goal - bill_now
    days_remaining = total_days - days_elapsed

    if days_remaining > 0:
        to_get_goal_per_day = to_get_goal / days_remaining
    else:
        to_get_goal_per_day = 0.0

    # Sýna niðurstöður
    st.markdown("---")
    st.subheader("📈 Niðurstöður")
    st.metric("Samtals kortanotkun til dagsins í dag", f"{bill_now:,.0f} kr.")
    st.metric("Áætlaður Arionbankareikningur", f"{projected_bill1:,.0f} kr.")
    st.metric("Áætlaður Landsbankareikningur", f"{projected_bill2:,.0f} kr.")
    st.metric("Áætlaður heildarkortareikningur", f"{projected_total_bill:,.0f} kr.")
    st.metric("Fjöldi daga liðnir", f"{days_elapsed} dagar")
    st.metric("Notkun á dag", f"{total_bill_per_day:,.0f} kr./dag")
    st.metric("Markmið á dag", f"{goal_per_day:,.0f} kr./dag")
    st.metric("Leyfileg dagleg notkun til að ná markmiði", f"{to_get_goal_per_day:,.0f} kr./dag")
