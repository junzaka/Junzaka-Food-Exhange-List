import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Thai Food Exchange Planner",
    page_icon="🥗",
    layout="wide"
)

# ==================================
# LOAD DATABASE
# ==================================

food_df = pd.read_csv("foods.csv")

# ==================================
# SESSION STATE
# ==================================

if "food_records" not in st.session_state:
    st.session_state.food_records = []

# ==================================
# HEADER
# ==================================

st.markdown("""
<h1 style='margin-bottom:0px;'>
🥗 Thai Food Exchange Planner
</h1>

<p style='font-size:11px;color:#888888;margin-top:-10px;'>
by Junzaka
</p>
""", unsafe_allow_html=True)

st.divider()

# ==================================
# FOOD FILTER
# ==================================

col1, col2 = st.columns(2)

with col1:

    group = st.selectbox(
        "หมวดอาหาร",
        sorted(
            food_df["group"]
            .dropna()
            .unique()
        )
    )

filtered_foods = food_df[
    food_df["group"] == group
]

filtered_foods["subcategory"] = (
    filtered_foods["subcategory"]
    .fillna("N/A")
)

if group == "เนื้อสัตว์":

    subcategory_list = [
        "ไขมันต่ำมาก",
        "ไขมันต่ำ",
        "ไขมันปานกลาง",
        "ไขมันสูง"
    ]

    subcategory_list = [
        x for x in subcategory_list
        if x in filtered_foods["subcategory"].unique()
    ]

else:

    subcategory_list = sorted(
        filtered_foods["subcategory"]
        .unique()
    )

with col2:

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
    f"พบอาหาร {len(filtered_foods)} รายการ"
)

food_name = st.selectbox(
    "เลือกอาหาร",
    filtered_foods["food_name"]
)

selected_food = filtered_foods[
    filtered_foods["food_name"]
    == food_name
].iloc[0]

# ==================================
# FOOD INFORMATION
# ==================================

st.divider()

st.markdown("## 🍽️ Food Information")

st.markdown(
    f"### {selected_food['food_name']}"
)

weight_value = (
    "-"
    if pd.isna(selected_food["weight_g"])
    else f"{selected_food['weight_g']} g"
)

st.markdown(
    f"""
    <style>
    .food-box {{
        border: 2px dashed #666666;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 5px;
    }}

    .green-bg {{
        background-color: #e8f5e9;
    }}

    .yellow-bg {{
        background-color: #fff9c4;
    }}

    .food-label {{
        font-size:14px;
        color:#555555;
    }}

    .food-value {{
        font-size:28px;
        font-weight:bold;
        color:#1f2c4f;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# แถวบน

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class="food-box green-bg">
        <div class="food-label">Serving Size</div>
        <div class="food-value">
        {selected_food['serving_size']}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="food-box green-bg">
        <div class="food-label">Weight</div>
        <div class="food-value">
        {weight_value}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="food-box green-bg">
        <div class="food-label">Exchange</div>
        <div class="food-value">
        {selected_food['exchange']}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# แถวล่าง

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="food-box yellow-bg">
        <div class="food-label">CHO</div>
        <div class="food-value">
        {selected_food['carb']} g
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="food-box yellow-bg">
        <div class="food-label">Protein</div>
        <div class="food-value">
        {selected_food['protein']} g
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="food-box yellow-bg">
        <div class="food-label">Fat</div>
        <div class="food-value">
        {selected_food['fat']} g
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="food-box yellow-bg">
        <div class="food-label">Kcal</div>
        <div class="food-value">
        {selected_food['kcal']} kcal
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ==================================
# ADD FOOD
# ==================================

st.divider()

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

# ==================================
# FOOD RECORDS
# ==================================

if len(st.session_state.food_records) > 0:

    st.divider()

    st.markdown("## 📝 Food Records")

    delete_index = None

    for idx, item in enumerate(
        st.session_state.food_records
    ):

        col1, col2 = st.columns([8,1])

        with col1:

            st.write(
                f"{item['Meal']} | {item['Food']} | {item['Exchange']} Exchange"
            )

        with col2:

            if st.button(
                "❌",
                key=f"delete_{idx}"
            ):
                delete_index = idx

    if delete_index is not None:

        st.session_state.food_records.pop(
            delete_index
        )

        st.rerun()

    df = pd.DataFrame(
        st.session_state.food_records
    )

    # ==========================
    # NUTRITION SUMMARY
    # ==========================

    cho = df["CHO"].sum()
    protein = df["Protein"].sum()
    fat = df["Fat"].sum()
    kcal = df["Energy"].sum()

    st.divider()

    st.markdown(
        "## 📊 Nutrition Summary"
    )

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
        "Kcal",
        round(kcal,0)
    )

    # ==========================
    # FOOD EXCHANGE SUMMARY
    # ==========================

    st.divider()

    st.markdown(
        "## 🔄 Food Exchange Summary"
    )

    exchange_summary = (
        df.groupby("Group")["Exchange"]
        .sum()
        .reset_index()
    )

    cols = st.columns(
        len(exchange_summary)
    )

    for i, row in exchange_summary.iterrows():

        cols[i].metric(
            row["Group"],
            round(row["Exchange"],1)
        )

    # ==========================
    # MEAL SUMMARY
    # ==========================

    st.divider()

    st.markdown(
        "## 🍱 Meal Summary"
    )

    meal_summary = (
        df.groupby("Meal")["Energy"]
        .sum()
        .reset_index()
    )

    cols = st.columns(
        len(meal_summary)
    )

    for i, row in meal_summary.iterrows():

        cols[i].metric(
            row["Meal"],
            f"{round(row['Energy'],0)} kcal"
        )

    # ==========================
    # PIE CHART
    # ==========================

    st.divider()

    pie_df = pd.DataFrame(
        {
            "Nutrient": [
                "CHO",
                "Protein",
                "Fat"
            ],
            "Gram": [
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
        width="stretch"
    )

# ==================================
# CLEAR
# ==================================

st.divider()

if st.button(
    "🗑️ Clear All"
):

    st.session_state.food_records = []

    st.rerun()
