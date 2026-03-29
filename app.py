import streamlit as st

# 1. 網頁基本設定
st.set_page_config(page_title="Foodie Pricing Calculator 🍔", layout="wide")
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

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 成本輸入")
        t1_cost_twd = st.number_input("商品台幣成本", value=150.0, key="t1_c")
        t1_weight = st.number_input("商品重量 (kg)", value=0.5, key="t1_w")
        t1_cost_sgd = t1_cost_twd / exchange_rate
        t1_ship_sgd = t1_weight * shipping_rate_per_kg
    with col2:
        st.subheader("💰 目標設定")
        t1_misc = st.number_input("雜項/包材 (SGD)", value=0.5, key="t1_m")
        t1_target = st.slider("期望純利潤率 (%)", 5, 50, 20, key="t1_target") / 100

    st.divider()
    # 逆推公式
    t1_total_c = t1_cost_sgd + t1_ship_sgd + t1_misc + shipping_gap_global
    t1_denom = 1 - fee_rate - t1_target
    
    if t1_denom > 0:
        t1_sp = t1_total_c / t1_denom
        t1_fee = t1_sp * fee_rate
        t1_payout = t1_sp - t1_fee - shipping_gap_global
        t1_profit = t1_sp * t1_target
        
        # 顯示結果
        r1, r2, r3 = st.columns(3)
        r1.success(f"### 🎯 建議售價\n## {t1_sp:.2f} SGD")
        r2.info(f"### 💵 預估撥款\n## {t1_payout:.2f} SGD")
        
        # 兩種利潤率
        t1_p_rate = t1_target * 100
        t1_payout_rate = ((t1_payout - (t1_cost_sgd + t1_ship_sgd + t1_misc)) / t1_payout * 100) if t1_payout > 0 else 0
        r3.warning(f"### 📈 利潤分析\n純利潤率：**{t1_p_rate:.1f}%**\n\n到手利潤率：**{t1_payout_rate:.1f}%**")
    else:
        st.error("設定過高，無法計算。")

with tab2:
    st.subheader("依據實際帳單拆解利潤")
    c1, c2 = st.columns(2)
    with c1:
        check_sp = st.number_input("帳單上的 Item Price (售價)", value=11.80)
        check_payout = st.number_input("帳單最後的 Grand Total (撥款)", value=7.76)
    with c2:
        check_cost_twd = st.number_input("該商品台幣原成本", value=150.0)
        check_weight = st.number_input("該商品重量 (kg)", value=0.5)

    # 帳單分析邏輯
    check_cost_sgd = check_cost_twd / exchange_rate
    check_ship_sgd = check_weight * shipping_rate_per_kg
    check_total_base_cost = check_cost_sgd + check_ship_sgd + 0.5 # 假設雜項 0.5
    
    # 實際賺的錢 = 撥款 - (成本 + 運費成本 + 雜項)
    actual_profit_val = check_payout - check_total_base_cost
    
    # 兩種利潤率回測
    # 1. 純利潤率 = 實際利潤 / 售價
    back_profit_rate = (actual_profit_val / check_sp) * 100
    # 2. 到手利潤率 = (撥款 - 成本) / 撥款
    back_payout_rate = ((check_payout - check_total_base_cost) / check_payout) * 100 if check_payout > 0 else 0
    
    st.divider()
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.metric("實際純利金額", f"{actual_profit_val:.2f} SGD")
        st.write(f"此單平台總扣款：**{check_sp - check_payout:.2f} SGD**")

    with res_col2:
        st.subheader("📈 帳單利潤率回測")
        st.write(f"1. 純利潤率 (利潤/售價)： **{back_profit_rate:.1f}%**")
        st.write(f"2. 到手利潤率 (利潤/撥款)： **{back_payout_rate:.1f}%**")
        
    if back_profit_rate < 0:
        st.error("⚠️ 注意：這一單是虧損的！請檢查成本或運費差額。")
