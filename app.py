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
# 預設抽成率：Shopee 14.75%, Lazada 12%
f_rate_input = st.sidebar.slider(f"{p_type} 預期抽成率 (%)", 0.0, 30.0, 14.75 if p_type=="Shopee" else 12.0, step=0.05)
f_rate = f_rate_input / 100

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
    # 核心公式計算
    t1_total_c = t1_c_sgd + t1_s_sgd + t1_m + ship_gap
    t1_denom = 1 - f_rate - t1_target
    
    if t1_denom > 0:
        t1_sp = t1_total_c / t1_denom
        # 修正後的第 40 行：確保括號完全閉合
        t1_pay = t1_sp * (1 - f_rate) - ship_gap
        
        r1, r2, r3 = st.columns(3)
        r1.success(f"### 🎯 建議售價\n## {t1_sp:.2f} SGD")
        r2.info(f"### 💵 預估撥款\n## {t1_pay:.2f} SGD")
        
        t1_payout_rate = ((t1_pay - (t1_c_sgd + t1_s_sgd + t1_m)) / t1_pay * 100) if t1_pay > 0 else 0
        r3.warning(f"### 📈 利潤分析\n純利：**{t1_target*100:.1f}%**\n到手：**{t1_payout_rate:.1f}%**")
    else:
        st.error("設定過高，無法計算。")

# === Tab 2: 帳單回測 ===
with tab2:
    st.subheader("🔍 實際帳單與產品健康度檢測")
    c1, c2 = st.columns(2)
    with c1:
        st.write("📖 **帳單數據**")
        c_sp = st.number_input("帳單 Item Price (售價)", value=11.80, key="t2_sp")
        c_pay = st.number_input("帳單 Grand Total (撥款)", value=7.76, key="t2_pay")
    with c2:
        st.write("📦 **原始成本**")
        c_c_twd = st.number_input("商品台幣原成本", value=150.0, key="t2_ct")
        c_w = st.number_input("商品重量 (kg)", value=0.5, key="t2_w")

    # 運算邏輯
    c_c_sgd = c_c_twd / ex_rate
    c_s_sgd = c_w * ship_kg
    c_base = c_c_sgd + c_s_sgd + 0.5 # 基礎雜項成本預設 0.5
    act_profit = c_pay - c_base
    
    # 反推平台抽成邏輯
    actual_fee_amt = c_sp - c_pay - ship_gap
    actual_fee_rate = (actual_fee_amt / c_sp) * 100 if c_sp > 0 else 0
    
    b_p_rate = (act_profit / c_sp) * 100 if c_sp > 0 else 0
    b_pay_rate = ((c_pay - c_base) / c_pay) * 100 if c_pay > 0 else 0
    
    st.divider()
    res_l, res_m, res_r = st.columns(3)
    
    with res_l:
        st.metric("實際純利金額", f"{act_profit:.2f} SGD")
        st.write(f"### ✅ 純利潤率：**{b_p_rate:.1f}%**")
        if b_p_rate < 10: st.error("❌ 很危險（容易虧）")
        elif 10 <= b_p_rate < 15: st.warning("⚠️ 勉強（不能出問題）")
        elif 15 <= b_p_rate <= 25: st.success("✅ 健康（可長期做）")
        else: st.info("🔥 很優秀（但不常見）")

    with res_m:
        st.metric("反推實際抽成率", f"{actual_fee_rate:.2f} %")
        st.write(f"### 💸 平台扣款拆解")
        st.write(f"平台抽成金額：**{actual_fee_amt:.2f} SGD**")
        st.write(f"設定運費差額：**{ship_gap:.2f} SGD**")
        st.caption("註：若抽成率異常，請檢查 Service Fee。")

    with res_r:
        st.write(f"此單總扣款(含運)：**{c_sp - c_pay:.2f} SGD**")
        st.write(f"### ✅ 到手利潤率：**{b_pay_rate:.1f}%**")
        if b_pay_rate < 15: st.error("❌ 很壓（會覺得沒賺錢）")
        elif 15 <= b_pay_rate < 18: st.warning("⚠️ 偏低")
        elif 18 <= b_pay_rate <= 25: st.success("✅ 正常")
        elif 25 < b_pay_rate <= 30: st.info("👍 很舒服")
        else: st.info("🔥 很強（通常高毛利品）")
