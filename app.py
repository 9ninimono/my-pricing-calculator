import streamlit as st

st.set_page_config(page_title="Foodie Pricing Calculator 🍔", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# --- 側邊欄：固定參數 ---
st.sidebar.header("⚙️ 平台費率設定")
# 根據你的帳單 (1.74/11.8 = 14.75%)
fee_rate = st.sidebar.slider("平台總抽成率 (%)", 0.0, 30.0, 14.75, step=0.05) / 100
shipping_gap = st.sidebar.number_input("賣家負擔運費差額 (SGD)", value=2.30)
exchange_rate = st.sidebar.slider("匯率 (TWD/SGD)", 20.0, 26.0, 23.5)

# --- 主畫面：輸入區 ---
tab1, tab2 = st.tabs(["🚀 售價逆推 (我要標多少錢？)", "📝 帳單回測 (為什麼這單拿這麼少？)"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        cost_twd = st.number_input("商品台幣成本", value=150.0)
        weight_kg = st.number_input("商品重量 (kg)", value=0.5)
        shipping_per_kg = st.number_input("每公斤運費成本 (SGD)", value=8.0)
    with col2:
        misc = st.number_input("雜項/包材 (SGD)", value=0.5)
        target_margin = st.slider("期望純利潤率 (%)", 5, 50, 20) / 100

    # 公式計算
    total_c = (cost_twd / exchange_rate) + (weight_kg * shipping_per_kg) + misc + shipping_gap
    denom = 1 - fee_rate - target_margin
    
    if denom > 0:
        sp = total_c / denom
        st.success(f"### 建議標價：{sp:.2f} SGD")
        st.write(f"此價格下，撥款金額約為：**{sp * (1 - fee_rate) - shipping_gap:.2f} SGD**")
    else:
        st.error("設定的利潤與抽成過高，無法計算！")

with tab2:
    st.subheader("輸入你帳單上的金額，看看哪裡出問題")
    check_sp = st.number_input("帳單上的 Item Price (售價)", value=11.80)
    actual_payout = st.number_input("帳單最後的 Grand Total (撥款)", value=7.76)
    
    loss = check_sp - actual_payout
    st.warning(f"這筆單總共被扣走了：**{loss:.2f} SGD**")
    
    st.write("🔍 扣款拆解預估：")
    st.write(f"- 預估平台抽成 ({fee_rate*100:.2f}%): {check_sp * fee_rate:.2f} SGD")
    st.write(f"- 剩餘扣款 (可能是運費差額): {loss - (check_sp * fee_rate):.2f} SGD")
