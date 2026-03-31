import streamlit as st

# 1. 網頁基本設定
st.set_page_config(page_title="Foodie Pricing Calculator", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# 公式解析函式
def parse_expression(expression):
    try:
        allowed_chars = "0123456789+-*/.() "
        if all(c in allowed_chars for c in str(expression)):
            return float(eval(str(expression)))
        return 0.0
    except:
        return 0.0

# --- 側邊欄參數 ---
st.sidebar.header("⚙️ 核心參數")
ex_rate = st.sidebar.slider("匯率 (TWD/SGD)", 20.0, 26.0, 23.5, 0.1)
ship_kg = st.sidebar.slider("重量運費 (SGD/kg)", 0.0, 20.0, 8.0, 0.5)
ship_gap = st.sidebar.number_input("賣家負擔運費差額 (SGD)", value=2.30)

st.sidebar.divider()
p_type = st.sidebar.radio("平台選擇", ["Shopee", "Lazada"])
f_rate = st.sidebar.slider(f"{p_type} 預期抽成 (%)", 0.0, 30.0, 14.75, 0.01) / 100.0

# --- 功能分頁 ---
tab1, tab2 = st.tabs(["🚀 售價逆推", "📝 帳單回測"])

# === Tab 1: 售價逆推 ===
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📦 成本")
        t1_c_twd = parse_expression(st.text_input("台幣成本 (可輸入公式)", "150", key="t1c"))
        st.caption(f"計算結果: NT$ {t1_c_twd:.2f}")
        t1_w = st.number_input("重量 (kg)", 0.5, key="t1w")
        t1_m = st.number_input("雜項 (SGD)", 0.5, key="t1m")
    with c2:
        st.subheader("💰 目標")
        target = st.slider("期望純利潤率 (%)", 5.0, 50.0, 13.0, key="t1t") / 100.0

    st.divider()
    base_cost = (t1_c_twd / ex_rate) + (t1_w * ship_kg) + t1_m
    denom = 1.0 - f_rate - target
    
    if denom > 0:
        sp = (base_cost + ship_gap) / denom
        pay = sp * (1.0 - f_rate) - ship_gap
        r1, r2, r3 = st.columns(3)
        r1.success(f"### 🎯 建議售價\n## {sp:.2f}")
        r2.info(f"### 💵 預估撥款\n## {pay:.2f}")
        res_pure = target
