import streamlit as st

# 1. 網頁基本設定
st.set_page_config(page_title="Foodie Pricing Calculator", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# --- 新增：數學公式解析工具 ---
def parse_expression(expression):
    try:
        # 只允許數字與算術符號，確保 eval 安全
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
# 這是你帳單中的 4.29 - 1.99 = 2.3
ship_gap_global = st.sidebar.number_input("賣家負擔運費差額 (SGD)", value=2.30, step=0.1)

st.sidebar.divider()
p_type = st.sidebar.radio("選擇計算平台", ["Shopee", "Lazada"])
f_rate_raw = st.sidebar.slider(f"{p_type} 抽成率 (%)", 0.0, 30.0, 14.75, step=0.01)
f_rate = f_rate_raw / 100

# --- 第二部分：功能頁籤 ---
tab1, tab2 = st.tabs(["🚀 售價逆推", "📝 帳單回測"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 成本輸入")
        # --- 強化處：改為支援公式輸入 ---
        t1_c_raw = st.text_input("商品台幣成本 (支援公式如 180/3)", value="150.0", key="t1_c")
        t1_c_twd = parse_expression(t1_c_raw)
        st.caption(f"💡 計算結果：NT$ {t1_c_twd:.2f}")
        
        t1_w = st.number_input("商品重量 (kg)", value=0.5, key="t1_w")
        t1_m = st.number_input("雜項/包材 (SGD)", value=0.5, key="t1_m")
        
        # 這是你的「口袋支出」成本
        base_cost = (t1_c_twd / ex_rate) + (t1_w * ship_kg_rate) + t1_m
        
    with col2:
        st.subheader("💰 獲利目標")
        # 這裡的純利潤率定義：利潤 / 售價
        t1_target_p = st.slider("期望純利潤率 (%)", 5.0, 50.0, 13.0, key="t1_t") / 100

    st.divider()
    # 【對齊公式】SP = (基礎成本 + 運費差額) / (1 - 抽成率 - 純利率)
    denom = 1 - f_rate - t1_target_p
    
    if denom > 0:
        sp = (base_cost
