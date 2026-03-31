import streamlit as st

# 1. 網頁基本設定
st.set_page_config(page_title="Foodie Pricing Calculator", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# 數學公式與數值解析函數 (全介面共用)
def parse_val(expression):
    try:
        # 清理字串，只允許數字、算術符號與括號
        allowed_chars = "0123456789+-*/.() "
        clean_expr = "".join(c for c in str(expression) if c in allowed_chars)
        return float(eval(clean_expr)) if clean_expr else 0.0
    except:
        return 0.0

# --- 第一部分：側邊欄參數 ---
st.sidebar.header("⚙️ 核心參數設定")
ex_rate = st.sidebar.slider("即時匯率 (TWD/SGD)", 20.0, 26.0, 23.5, step=0.1)
ship_kg_rate = st.sidebar.slider("重量運費成本 (SGD/kg)", 0.0, 20.0, 8.0, step=0.5)

# 停用記憶：側邊欄數值輸入
ship_gap_raw = st.sidebar.text_input("賣家負擔運費差額 (SGD)", value="2.30", autocomplete="new-password")
ship_gap_global = parse_val(ship_gap_raw)

st.sidebar.divider()
p_type = st.sidebar.radio("選擇計算平台", ["Shopee", "Lazada"])
f_rate_raw = st.sidebar.slider(f"{p_type} 抽成率 (%)", 0.0, 30.0, 14.75, step=0.01)
f_rate = f_rate_raw / 100.0

# --- 第二部分：功能頁籤 ---
tab1, tab2 = st.tabs(["🚀 售價逆推", "📝 帳單回測"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 成本輸入")
        # 成本支援公式
        t1_c_raw = st.text_input("商品台幣成本 (支援公式)", value="150.0", key="t1_c", autocomplete="new-password")
        t1_c_twd = parse_val(t1_c_raw)
        
        # 強化：重量也支援公式 (例如 0.3+0.2)
        t1_w_raw = st.text_input("商品重量 (kg) (支援公式)", value="0.5", key="t1_w", autocomplete="new-password")
        t1_w = parse_val(t1_w_raw)
        
        t1_m_raw = st.text_input("雜項/包材 (SGD)", value="0.5", key="t1_m", autocomplete="new-password")
        t1_m = parse_val(t1_m_raw)
        
        st.caption(f"💡 解析結果：成本 NT$ {t1_c_twd:.2f} / 重量 {t1_w:.3f} kg")
        
        # 成本拆解
        t1_item_only_cost = (t1_c_twd / ex_rate) + (t1_w * ship_kg_rate)
        base_cost = t1_item_only_cost + t1_m
        
    with col2:
        st.subheader("💰 獲利目標")
        t1_target_p = st.sidebar.slider("期望純利潤率 (%)", 5.0, 50.0, 13.0, key="t1_t_slider") / 100.0 if "t1_t_slider" in st.session_state else 0.13
        # 這裡為了維持版面美觀，保留 slider 在原位
        t1_target_p = st.slider("期望純利潤率 (%)", 5.0, 50.0, 13.0, key="t1_t") / 100.0

    st.divider()
    denom = 1.0 - f_rate - t1_target_p
    if denom > 0:
        sp = (base_cost + ship_gap_global) / denom
        payout = sp * (1 - f_rate) - ship_gap_global
        profit = payout - base_cost
        est_gross_margin = (payout - t1_item_only_cost) / sp * 100.0 if sp > 0 else 0.0

        # 毛利率顯示區 (售價逆推)
        g_col1, g_col2 = st.columns([1, 2])
        with g_col1:
            st.metric("📊 預估毛利率", f"{est_gross_margin:.1f}%")
        with g_col2:
            if est_gross_margin < 15.0: st.error("❌ 毛利偏低")
            elif 15.0 <= est_gross_margin < 20.0: st.warning("⚠️ 15%–20%：勉強可做 (食品基準)")
            elif 20.0 <= est_gross_margin < 30.0: st.success("✅ 20%–30%：健康")
            else: st.info("🔥 30% 以上：很好")

        st.divider()
        r1, r2, r3 = st.columns(3)
        r1.success(f"### 🎯 建議售價\n## {sp:.2f} SGD")
        r2.info(f"### 💵 預估撥款\n## {payout:.2f} SGD")
        
        pure_m, hand_m = (profit / sp) * 100.0, (profit / payout) * 100.0 if payout > 0 else 0.0
        r3.warning(f"### 📈 利潤分析\n純利：**{pure_m:.1f}%**\n到手：**{hand_m:.1f}%**")
    else:
        st.error("⚠️ 設定過高，無法計算。")

with tab2:
    st.subheader("🔍 帳單健康度驗收")
    c1, c2 = st.columns(2)
    with c1:
        st.write("📖 **帳單數據**")
        c_sp_raw = st.text_input("帳單售價 (Item Price)", value="11.80", key="t2_sp", autocomplete="new-password")
        c_pay_raw = st.text_input("帳單撥款 (Grand Total)", value="7.76", key="t2_pay", autocomplete="new-password")
        c_sp, c_pay = parse_val(c_sp_raw), parse_val(c_pay_raw)
    with c2:
        st.write("📦 **原始成本**")
        c_c_raw = st.text_input("商品台幣成本 (支援公式)", value="150.0", key="t2_ct", autocomplete="new-password")
        c_c_twd = parse_val(c_c_raw)
        
        # 強化：回測重量也支援公式
        c_w_raw = st.text_input("商品重量 (kg) (支援公式)", value="0.5", key="t2_w", autocomplete="new-password")
        c_w = parse_val(c_w_raw)
        
        c_m_raw = st.text_input("雜項成本 (SGD)", value="0.5", key="t2_m", autocomplete="new-password")
        c_m = parse_val(c_m_raw)

    # 運算邏輯
    item_only_cost = (c_c_twd / ex_rate) + (c_w * ship_kg_rate)
    actual_base_cost = item_only_cost + c_m
    actual_profit = c_pay - actual_base_cost
    gross_margin = (c_pay - item_only_cost) / c_sp * 100.0 if c_sp > 0 else 0.0
    b_p_margin = (actual_profit / c_sp) * 100.0 if c_sp > 0 else 0.0
    b_pay_margin = (actual_profit / c_pay) * 100.0 if c_pay > 0 else 0.0
    total_deduction = c_sp - c_pay

    st.divider()
    # 毛利率顯示區 (帳單回測)
    g_col1, g_col2 = st.columns([1, 2])
    with g_col1:
        st.metric("📊 實際毛利率", f"{gross_margin:.1f}%")
    with g_col2:
        if gross_margin < 15.0: st.error("❌ 毛利偏低")
        elif 15.0 <= gross_margin < 20.0: st.warning("⚠️ 15%–20%：勉強可做")
        elif 20.0 <= gross_margin < 30.0: st.success("✅ 20%–30%：健康")
        else: st.info("🔥 30% 以上：很好")

    st.divider()
    res_l, res_m, res_r = st.columns(3)
    with res_l:
        st.metric("實際純利金額", f"{actual_profit:.2f} SGD")
        st.write(f"純利潤率：**{b_p_margin:.1f}%**")
    with res_m:
        st.metric("此單總扣款 (含運)", f"{total_deduction:.2f} SGD")
        act_f_rate = ((total_deduction - ship_gap_global) / c_sp) * 100.0 if c_sp > 0 else 0.0
        st.write(f"反推實際抽成率: **{act_f_rate:.2f}%**")
    with res_r:
        st.metric("到手利潤率", f"{b_pay_margin:.1f}%")
        if b_pay_margin < 18.0: st.error("❌ 壓抑")
        elif 18.0 <= b_pay_margin <= 30.0: st.success("✅ 正常")
        else: st.info("🔥 很舒服")
