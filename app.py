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

st.markdown("""
<h1 style='margin-bottom:0px;'>
🥗 Thai Food Exchange Planner
</h1>

<p style='font-size:11px;color:#888888;margin-top:-10px;'>
by Junzaka
</p>
""",
unsafe_allow_html=True)

# ==========================
# FOOD SELECTION
# ==========================

group_list = sorted(
    food_df["group"].dropna().unique()
)

group = st.selectbox(
    "หมวดอาหาร",
    group_list
)

filtered_foods = food_df[
    food_df["group"] == group
]

subcategory_list = sorted(
    filtered_foods["subcategory"]
    .fillna("")
    .unique()
)

subcategory = st.selectbox(
    "หมวดย่อย",
    subcategory_list
)

if subcategory != "":
    filtered_foods = filtered_foods[
        filtered_foods["subcategory"]
        == subcategory
    ]

st.caption(
    f"พบ {len(filtered_foods)} รายการ"
)

food_name = st.selectbox(
    "เลือกอาหาร",
    filtered_foods["food_name"]
)

selected_food = filtered_foods[
    filtered_foods["food_name"]
    == food_name
].iloc[0]
# ==========================
# FOOD DETAIL
# ==========================

st.markdown("### 🍽️ Food Information")

st.markdown(
f"""
**🍴 {selected_food['food_name']}**

• Serving Size : {selected_food['serving_size']}

• Weight : {selected_food['weight_g']} g

• Exchange : {selected_food['exchange']}
"""
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

    st.divider()
st.markdown("## 📝 Food Records")

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

    st.divider()
st.markdown("## 📊 Nutrition Summary")

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

    st.divider()
st.markdown("## 🔄 Exchange Summary")

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

    st.divider()
st.markdown("## 🍱 Meal Summary")

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
