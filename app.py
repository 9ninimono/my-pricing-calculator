import streamlit as st

# 網頁基本設定
st.set_page_config(page_title="Foodie Pricing Calculator 🍔", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# --- 第一部分：參數調節區 ---
st.sidebar.header("⚙️ 全域參數設定")
exchange_rate = st.sidebar.slider("即時匯率 (TWD/SGD)", 20.0, 26.0, 23.5, step=0.1)
shipping_rate_per_kg = st.sidebar.slider("每公斤成本 (SGD/kg)", 0.0, 20.0, 8.0, step=0.5)

st.sidebar.subheader("平台費用設定")
platform_type = st.sidebar.radio("選擇計算平台", ["Shopee", "Lazada"])
if platform_type == "Shopee":
    fee_rate = st.sidebar.slider("總抽成率 (%)", 0.0, 30.0, 14.7, step=0.1) / 100
else:
    fee_rate = st.sidebar.slider("總抽成率 (%)", 0.0, 30.0, 15.0, step=0.1) / 100

# 新增：運費差額設定 (即：物流收費 - 買家支付)
shipping_gap = st.sidebar.number_input("賣家負擔運費差額 (SGD)", value=2.30, step=0.1)

# --- 第二部分：數據輸入區 ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 商品成本")
    cost_twd = st.number_input("商品成本 (TWD)", min_value=0.0, value=150.0)
    weight_kg = st.number_input("商品重量 (kg)", min_value=0.0, value=0.5)
    cost_sgd = cost_twd / exchange_rate
    weight_shipping_sgd = weight_kg * shipping_rate_per_kg

with col2:
    st.subheader("💰 獲利目標")
    miscellaneous_sgd = st.number_input("雜項固定支出 (SGD)", min_value=0.0, value=0.5)
    target_margin = st.slider("期望純利潤率 (%)", 5, 50, 20) / 100

# --- 第三部分：修正後的計算邏輯 ---
st.divider()

# 總固定成本 (C) = 商品成本 + 重量運費 + 雜項 + 賣家負擔的運費差額
total_c_sgd = cost_sgd + weight_shipping_sgd + miscellaneous_sgd + shipping_gap

# 公式：售價 (SP) = 總固定成本 / (1 - 平台抽成率 - 期望利潤率)
denominator = 1 - fee_rate - target_margin

if denominator > 0:
    sp_sgd = total_c_sgd / denominator
    platform_fee_actual = sp_sgd * fee_rate
    profit_actual = sp_sgd * target_margin
    payout_actual = sp_sgd - platform_fee_actual - shipping_gap
    
    # 顯示結果
    res1, res2, res3 = st.columns(3)
    res1.success(f"### 🎯 建議售價 (SP)\n## {sp_sgd:.2f} SGD")
    res1.write(f"約合台幣：{sp_sgd * exchange_rate:.0f} TWD")
    
    res2.info(f"### 💵 實際撥款 (Payout)\n## {payout_actual:.2f} SGD")
    res2.caption(f"已扣除平台費及運費差額 ${shipping_gap}")

    res3.warning(f"### 📈 利潤分析")
    res3.write(f"純利潤率：**{(profit_actual/sp_sgd)*100:.1f}%**")
    res3.write(f"到手利潤率：**{((payout_actual - (cost_sgd + weight_shipping_sgd + miscellaneous_sgd))/payout_actual)*100:.1f}%**")
else:
    st.error("⚠️ 抽成與獲利設定過高，請調整參數！")
