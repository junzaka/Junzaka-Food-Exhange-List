import streamlit as st
import pandas as pd
import plotly.express as px

from foods import foods

st.set_page_config(
    page_title="Thai Food Exchange Calculator",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 Thai Food Exchange Calculator")

if "items" not in st.session_state:
    st.session_state.items = []

group = st.selectbox(
    "หมวดอาหาร",
    list(foods.keys())
)

food = st.selectbox(
    "ชนิดอาหาร",
    list(foods[group].keys())
)

exchange = st.number_input(
    "จำนวน Exchange",
    min_value=0.5,
    value=1.0,
    step=0.5
)

if st.button("➕ เพิ่มอาหาร"):

    nutrient = foods[group][food]

    st.session_state.items.append({
        "หมวด": group,
        "อาหาร": food,
        "Exchange": exchange,
        "CHO": nutrient["carb"] * exchange,
        "PRO": nutrient["protein"] * exchange,
        "FAT": nutrient["fat"] * exchange,
        "KCAL": nutrient["kcal"] * exchange
    })

if len(st.session_state.items) > 0:

    df = pd.DataFrame(st.session_state.items)

    st.subheader("รายการอาหาร")

    st.dataframe(
        df,
        use_container_width=True
    )

    cho = df["CHO"].sum()
    pro = df["PRO"].sum()
    fat = df["FAT"].sum()
    kcal = df["KCAL"].sum()

    st.subheader("Nutrition Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Carbohydrate",
        f"{cho:.1f} g"
    )

    c2.metric(
        "Protein",
        f"{pro:.1f} g"
    )

    c3.metric(
        "Fat",
        f"{fat:.1f} g"
    )

    c4.metric(
        "Energy",
        f"{kcal:.0f} kcal"
    )

    chart_df = pd.DataFrame({
        "Nutrient": [
            "CHO",
            "PRO",
            "FAT"
        ],
        "Gram": [
            cho,
            pro,
            fat
        ]
    })

    fig = px.pie(
        chart_df,
        values="Gram",
        names="Nutrient"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

if st.button("Clear All"):
    st.session_state.items = []
    st.rerun()
