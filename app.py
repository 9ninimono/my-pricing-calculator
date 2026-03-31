import streamlit as st

# 1. 基本設定
st.set_page_config(page_title="Foodie Pricing Calculator", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

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
ship_kg = st.sidebar.slider("運費 (SGD/kg)", 0.0, 20.0, 8.0, 0.5)
ship_gap = st.sidebar.number_input("運費差額 (SGD)", value=2.30)

p_type = st.sidebar.radio("平台", ["Shopee", "Lazada"])
f_rate = st.sidebar.slider(f"{p_type} 抽成 (%)", 0.0, 30.0, 14.75, 0.01) / 100.0

# --- 分頁設定 ---
tab1, tab2 = st.tabs(["🚀 售價逆推", "📝 帳單回測"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        t1_c_twd = parse_expression(st.text_input("台幣成本", "150", key="t1c"))
        t1_w = st.number_input("重量 (kg)", 0.5, key="t1w")
        t1_m = st.number_input("雜項 (SGD)", 0.5, key="t1m")
        base = (t1_c_twd / ex_rate) + (t1_w * ship_kg) + t1_m
    with c2:
        target = st.slider("期望利潤 (%)", 5.0, 50.0, 13.0) / 100.0
    
    denom = 1.0 - f_rate - target
    if denom > 0:
        sp = (base + ship_gap) / denom
        pay = sp * (1.0 - f_rate) - ship_gap
        st.divider()
        r1, r2, r3 = st.columns(3)
        r1.success(f"建議售價: {sp:.2f}")
        r2.info(f"預估撥款: {pay:.2f}")
        r3.warning(f"純利: {target*100:.1f}% | 到手: {((pay-(base))/pay*100):.1f}%")
    else:
        st.error("利潤設定太高了！")

with tab2:
    st.subheader("🔍 帳單回測")
    cc1, cc2 = st.columns(2)
    with cc1:
        c_sp = st.number_input("售價 (Item Price)", 11.80, key="t2sp")
        c_pay = st.number_input("撥款 (Grand Total)", 7.76, key="t2pay")
    with cc2:
        c_twd = parse_expression(st.text_input("台幣成本 ", "150", key="t2c"))
        c_w = st.number_input("重量 (kg) ", 0.5, key="t2w")
        c_m = st.number_input("雜項 (SGD) ", 0.5, key="t2m")

    actual_base = (c_twd / ex_rate) + (c_w * ship_kg) + c_m
    prof = c_pay - actual_base
    p_m = (prof / c
