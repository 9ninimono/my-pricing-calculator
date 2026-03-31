import streamlit as st

# 1. 網頁基本設定
st.set_page_config(page_title="Foodie Pricing Calculator", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# 定義數學公式解析函數
def parse_math(expression):
    try:
        allowed_chars = "0123456789+-*/.() "
        if all(c in allowed_chars for c in str(expression)):
            return float(eval(str(expression)))
        return 0.0
    except:
        return 0.0

# --- 第一部分：側邊欄參數 (全域共用) ---
st.sidebar.header("⚙️ 核心參數設定")
ex_rate = st.sidebar.slider("即時匯率 (TWD/SGD)", 20.0, 26.0, 23.5, step=0.1)
ship_kg_rate = st.sidebar.slider("重量運費成本 (SGD/kg)", 0.0, 20.0, 8.0, step=0.5)
ship_gap_global = st.sidebar.number_input("賣家負擔運費差額 (SGD)", value=2.30, step=0.1)

st.sidebar.divider()
p_type = st.sidebar.radio("選擇計算平台", ["Shopee", "Lazada"])
f_rate_raw = st.sidebar.slider(f"{p_type} 抽成率 (%)", 0.0, 30.0, 14.75, step=0.01)
f_rate = f_rate_raw / 100.0

# --- 第二部分：功能頁籤 ---
tab1, tab2 = st.tabs(["🚀 售價逆推", "📝 帳單回測"])

# === Tab 1: 售價逆推 ===
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 成本輸入")
        t1_c_raw = st.text_input("商品台幣成本 (支援公式如: 180/3)", value="150", key="t1_c_raw")
        t1_c_twd = parse_math(t1_c_raw)
        st.caption(f"解析後台幣成本：{t1_c_twd:.2f}")
        t1_w = st.number_input("商品重量 (kg)", value=0.5, key="t1_w")
        t1_m = st.number_input("雜項/包材 (SGD)", value=0.5, key="t1_m")
        base_cost = (t1_c_twd / ex_rate) + (t1_w * ship_kg_rate) + t1_m
    with col2:
        st.subheader("💰 獲利目標")
        t1_target_p = st.slider("期望純利潤率 (%)", 5.0, 50.0, 13.0, key="t1_t") / 100.0

    st.divider()
    denom = 1.0 - f_rate - t1_target_p
