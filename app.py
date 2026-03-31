import streamlit as st

# 1. 網頁基本設定 (標題已更新)
st.set_page_config(page_title="Foodie Pricing Calculator", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# 數學公式解析函數
def parse_expression(expression):
    try:
        allowed_chars = "0123456789+-*/.() "
        if all(c in allowed_chars for c in str(expression)):
            return float(eval(str(expression)))
        return 0.0
    except:
        return 0.0

# --- 第一部分：側邊欄參數 ---
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

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 成本輸入")
        # 強化：支援公式輸入
        t1_c_raw = st.text_input("商品台幣成本 (支援公式如 180/3)", value="150.0", key="t1_c")
        t1_c_twd = parse_expression(t1_c_raw)
        st.caption(f"💡 計算結果：NT$ {t1_c_twd:.2f}")
        
        # 修正：移除重量限制 (min_value=None)
        t1_w = st.number_input("商品重量 (kg)", value=0.5, key="t1_w", min_value=None)
        t1_m = st.number_input("雜項/包材 (SGD)", value=0.5, key="t1_m")
        
        base_cost = (t1_c_twd / ex_rate) + (t1_w * ship_kg_rate) + t1_m
        
    with col2:
        st.subheader("💰 獲利目標")
        t1_target_p = st.slider("期望純利潤率 (%)", 5.0, 50.0, 13.0, key="t1_t") / 100.0

    st.divider()
    denom = 1.0 - f_rate - t1_target_p
    
    if denom > 0:
        sp = (base_cost + ship_gap_global) / denom
        payout = sp * (1.0 - f_rate) - ship_gap_global
        profit = payout - base_cost
        
        r1, r2, r3 = st.columns(3)
        r1.success(f"### 🎯 建議售價\n## {sp:.2f} SGD")
        r2.info(f"### 💵 預估撥款\n## {payout:.2f} SGD")
        
        pure_m = (profit / sp) * 100.0
        hand_m = (profit / payout) * 100.0 if payout > 0 else 0.0
        r3.warning(f"### 📈 利潤分析\n純利：**{pure_m:.1f}%**\n到手：**{hand_m:.1f}%**")
    else:
        st.error("⚠️ 設定過高，請降低利潤率。")

with tab2:
    st.subheader("🔍 帳單健康度驗收")
    c1, c2 = st.columns(2)
    with c1:
        st.write("📖 **帳單數據**")
        c_sp = st.number_input("帳單 Item Price (售價)", value=11.80, key="t2_sp")
        c_pay = st.number_input("帳單 Grand Total (撥款)", value=7.76, key="t2_pay")
    with c2:
        st.write("📦 **原始成本**")
        # 強化：支援公式輸入
        c_c_raw = st.text_input("商品台幣成本 (支援公式)", value="150.0", key="t2_ct")
        c_c_twd = parse_expression(c_c_raw)
        st.caption(f"💡 計算結果：NT$ {c_c_twd:.2f}")
        
        # 修正：移除重量限制 (min_value=None)
        c_w = st.number_input("商品重量 (kg)", value=0.5, key="t2_w", min_value=None)
        c_m = st.number_input("雜項成本 (SGD)", value=0.5, key="t2_m")

    actual_base_cost = (c_c_twd / ex_rate) + (c_w * ship_kg_rate) + c_m
    actual_profit = c_pay - actual_base_cost
    
    b_p_margin = (actual_profit / c_sp) * 100.0 if c_sp > 0 else 0.0
    b_pay_margin = (actual_profit / c_pay) * 100.0 if c_pay > 0 else 0.0
    
    st.divider()
    res_l, res_m, res_r = st.columns(3)
    with res_l:
        st.metric("實際純利金額", f"{actual_profit:.2f} SGD")
        st.write(f"### ✅ 純利潤率：**{b_p_margin:.1f}%**")
        if b_p_margin < 15.0: st.error("❌ 警告：利潤過低")
        elif 15.0 <= b_p_margin <= 25.0: st.success("✅ 健康")
        else: st.info("🔥 優秀")

    with res_m:
        act_f_rate = ((c_sp - c_pay - ship_gap_global) / c_sp) * 100.0 if c_sp > 0 else 0.0
        st.metric("反推實際抽成率", f"{act_f_rate:.2f}%")
        st.write(f"基礎總成本: {actual_base_cost:.2f}")
        st.caption(f"平台扣款: {(c_sp - c_pay - ship_gap_global):.2f}")

    with res_r:
        st.metric("到手利潤率", f"{b_pay_margin:.1f}%")
        if b_pay_margin < 18.0: st.error("❌ 壓抑")
        elif 18.0 <= b_pay_margin <= 30.0: st.success("✅ 正常")
        else: st.info("🔥 很舒服")
