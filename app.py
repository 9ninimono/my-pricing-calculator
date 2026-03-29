import streamlit as st

# 1. 網頁基本設定
st.set_page_config(page_title="Foodie Pricing Calculator 🍔具", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# --- 第一部分：側邊欄參數調節 (全域共用) ---
st.sidebar.header("⚙️ 平台與匯率設定")
exchange_rate = st.sidebar.slider("即時匯率 (TWD/SGD)", 20.0, 26.0, 23.5, step=0.1)
shipping_rate_per_kg = st.sidebar.slider("重量運費成本 (SGD/kg)", 0.0, 20.0, 8.0, step=0.5)
shipping_gap_global = st.sidebar.number_input("賣家負擔運費差額 (SGD)", value=2.30, step=0.1)

st.sidebar.divider()
platform_type = st.sidebar.radio("選擇目前計算平台", ["Shopee", "Lazada"])

if platform_type == "Shopee":
    fee_rate = st.sidebar.slider("Shopee 總抽成率 (%)", 0.0, 30.0, 14.75, step=0.05) / 100
else:
    fee_rate = st.sidebar.slider("Lazada 總抽成率 (%)", 0.0, 30.0, 12.0, step=0.05) / 100

# --- 第二部分：功能切換頁籤 ---
tab1, tab2 = st.tabs(["🚀 售價逆推 (我要標多少？)", "📝 帳單回測 (這單賺多少？)"])

# === Tab 1: 售價逆推功能 ===
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 成本輸入")
        t1_cost_twd = st.number_input("商品台幣成本", value=150.0, key="t1_c")
        t1_weight = st.number_input("商品重量 (kg)", value=0.5, key="t1_w")
        t1_cost_sgd = t1_cost_twd / exchange_rate
        t1_ship_sgd = t1_weight * shipping_rate_per_kg
        st.write(f"折合成本：{t1_cost_sgd:.2f} SGD | 運費：{t1_ship_sgd:.2f} SGD")
        
    with col2:
        st.subheader("💰 目標設定")
        t1_misc = st.number_input("雜項/包材 (SGD)", value=0.5, key="t1_m")
        t1_target = st.slider("期望純利潤率 (%)", 5, 50, 20, key="t1_target") / 100

    st.divider()
    t1_total_c = t1
