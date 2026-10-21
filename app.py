import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Thai Food Exchange Calculator",
    page_icon="🥗",
    layout="wide"
)

# ==========================
# LOAD DATABASE
# ==========================

food_df = pd.read_csv("foods.csv")

# ==========================
# SESSION STATE
# ==========================

if "food_records" not in st.session_state:
    st.session_state.food_records = []

# ==========================
# HEADER
# ==========================

st.title("🥗 Thai Food Exchange Planner")

st.markdown("Thai Food Exchange Lists Calculator")

# ==========================
# FOOD SELECTION
# ==========================

group_list = sorted(food_df["group"].dropna().unique())

group = st.selectbox(
    "หมวดอาหาร",
    group_list
)

filtered_foods = food_df[
    food_df["group"] == group
]

food_name = st.selectbox(
    "เลือกอาหาร",
    filtered_foods["food_name"]
)

selected_food = filtered_foods[
    filtered_foods["food_name"] == food_name
].iloc[0]

# ==========================
# FOOD DETAIL
# ==========================

st.subheader("Food Information")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Serving Size",
    selected_food["serving_size"]
)

c2.metric(
    "Weight (g)",
    selected_food["weight_g"]
)

c3.metric(
    "Exchange",
    selected_food["exchange"]
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "CHO",
    selected_food["carb"]
)

c2.metric(
    "Protein",
    selected_food["protein"]
)

c3.metric(
    "Fat",
    selected_food["fat"]
)

c4.metric(
    "Kcal",
    selected_food["kcal"]
)

# ==========================
# MEAL TYPE
# ==========================

meal = st.selectbox(
    "Meal",
    [
        "Breakfast",
        "Lunch",
        "Dinner",
        "Snack"
    ]
)

exchange = st.number_input(
    "Exchange",
    min_value=0.5,
    step=0.5,
    value=1.0
)

# ==========================
# ADD FOOD
# ==========================

if st.button("➕ Add Food"):

    st.session_state.food_records.append(
        {
            "Meal": meal,
            "Group": selected_food["group"],
            "Food": selected_food["food_name"],
            "Exchange": exchange,
            "CHO": selected_food["carb"] * exchange,
            "Protein": selected_food["protein"] * exchange,
            "Fat": selected_food["fat"] * exchange,
            "Energy": selected_food["kcal"] * exchange
        }
    )

# ==========================
# FOOD RECORD TABLE
# ==========================

if len(st.session_state.food_records) > 0:

    df = pd.DataFrame(
        st.session_state.food_records
    )

    st.subheader("Food Records")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ==========================
    # SUMMARY
    # ==========================

    cho = df["CHO"].sum()
    protein = df["Protein"].sum()
    fat = df["Fat"].sum()
    kcal = df["Energy"].sum()

    st.subheader("Nutrition Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "CHO (g)",
        round(cho,1)
    )

    c2.metric(
        "Protein (g)",
        round(protein,1)
    )

    c3.metric(
        "Fat (g)",
        round(fat,1)
    )

    c4.metric(
        "Energy (kcal)",
        round(kcal,0)
    )

    # ==========================
    # EXCHANGE SUMMARY
    # ==========================

    st.subheader("Exchange Summary")

    exchange_summary = (
        df.groupby("Group")["Exchange"]
        .sum()
        .reset_index()
    )

    st.dataframe(
        exchange_summary,
        use_container_width=True
    )

    # ==========================
    # MEAL SUMMARY
    # ==========================

    st.subheader("Meal Summary")

    meal_summary = (
        df.groupby("Meal")["Energy"]
        .sum()
        .reset_index()
    )

    st.dataframe(
        meal_summary,
        use_container_width=True
    )

    # ==========================
    # PIE CHART
    # ==========================

    pie_df = pd.DataFrame(
        {
            "Nutrient":[
                "CHO",
                "Protein",
                "Fat"
            ],
            "Gram":[
                cho,
                protein,
                fat
            ]
        }
    )

    fig = px.pie(
        pie_df,
        values="Gram",
        names="Nutrient",
        title="Macronutrient Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================
# CLEAR
# ==========================

if st.button("Clear All"):

    st.session_state.food_records = []

    st.rerun()
