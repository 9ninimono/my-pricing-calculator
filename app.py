import streamlit as st

# 1. 網頁基本設定
st.set_page_config(page_title="Foodie Pricing Calculator 🍔", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# --- 第一部分：側邊欄參數調節 ---
st.sidebar.header("⚙️ 平台與匯率設定")
ex_rate = st.sidebar.slider("即時匯率 (TWD/SGD)", 20.0, 26.0, 23.5, step=0.1)
ship_kg = st.sidebar.slider("重量運費成本 (SGD/kg)", 0.0, 20.0, 8.0, step=0.5)
ship_gap = st.sidebar.number_input("賣家負擔運費差額 (SGD)", value=2.30, step=0.1)

st.sidebar.divider()
p_type = st.sidebar.radio("選擇目前計算平台", ["Shopee", "Lazada"])
f_rate = (st.sidebar.slider(f"{p_type} 預期抽成率 (%)", 0.0, 30.0, 14.75 if p_type=="Shopee" else 12.0, step=0.05)) / 100

# --- 第二部分：功能切換頁籤 ---
tab1, tab2 = st.tabs(["🚀 售價逆推", "📝 帳單回測"])

# === Tab 1: 售價逆推 ===
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 成本輸入")
        t1_c_twd = st.number_input("商品台幣成本", value=150.0, key="t1_c")
        t1_w = st.number_input("商品重量 (kg)", value=0.5, key="t1_w")
        t1_c_sgd = t1_c_twd / ex_rate
        t1_s_sgd = t1_w * ship_kg
    with col2:
        st.subheader("💰 目標設定")
        t1_m = st.number_input("雜項/包材 (SGD)", value=0.5, key="t1_m")
        t1_target = st.slider("期望純利潤率 (%)", 5, 50, 20, key="t1_t") / 100

    st.divider()
    t1_total_c = t1_c_sgd + t1_s_sgd + t1_m + ship_gap
    t1_denom = 1 - f_rate - t1_target
    
    if t1_denom > 0:
        t1_sp = t1_total_c / t1_denom
        t1_pay = t1_sp * (1 - f_rate)
