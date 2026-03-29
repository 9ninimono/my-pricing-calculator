import streamlit as st

# 網頁基本設定
st.set_page_config(page_title="Foodie Pricing", layout="wide")
st.title("🇸🇬 Foodie Pricing")

# --- 第一部分：參數調節區 (左側邊欄) ---
st.sidebar.header("⚙️ 全域參數設定")

# 1. 匯率調節
exchange_rate = st.sidebar.slider("即時匯率 (TWD/SGD)", 20.0, 26.0, 23.5, step=0.1)
st.sidebar.caption(f"目前設定：1 SGD = {exchange_rate} TWD")

# 2. 重量成本調節 (SGD/kg)
shipping_rate_per_kg = st.sidebar.slider("每公斤運費成本 (SGD/kg)", 0.0, 20.0, 8.0, step=0.5)

# 3. 平台抽成設定
st.sidebar.subheader("平台抽成比例 (%)")
platform_type = st.sidebar.radio("選擇計算平台", ["Shopee", "Lazada"])

if platform_type == "Shopee":
    fee_rate = st.sidebar.slider("Shopee 總抽成率 (%)", 0.0, 30.0, 17.3, step=0.1) / 100
else:
    fee_rate = st.sidebar.slider("Lazada 總抽成率 (%)", 0.0, 30.0, 15.0, step=0.1) / 100

# --- 第二部分：商品數據輸入區 (主介面) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 商品基本資料")
    cost_twd = st.number_input("商品成本 (TWD)", min_value=0.0, value=500.0, step=10.0)
    weight_kg = st.number_input("商品重量 (kg)", min_value=0.0, value=0.5, step=0.01)
    
    # 自動換算
    cost_sgd = cost_twd / exchange_rate
    weight_shipping_sgd = weight_kg * shipping_rate_per_kg
    
    st.write(f"➡️ 折合商品成本：**{cost_sgd:.2f} SGD**")
    st.write(f"➡️ 重量運費成本：**{weight_shipping_sgd:.2f} SGD**")

with col2:
    st.subheader("💰 其他成本與利潤設定")
    miscellaneous_sgd = st.number_input("雜項固定支出 (SGD)", min_value=0.0, value=1.0, step=0.1)
    platform_fixed_shipping = 2.3  # 固定平台運費
    target_margin = st.slider("預設獲利率 (%)", 5, 50, 20) / 100

# --- 第三部分：計算結果 ---
st.divider()

# 總基本成本 (C) = 商品成本 + 重量運費 + 雜項 + 平台固定運費
total_c_sgd = cost_sgd + weight_shipping_sgd + miscellaneous_sgd + platform_fixed_shipping

# 公式推導：售價 (SP) = C / (1 - 抽成率 - 獲利率)
denominator = 1 - fee_rate - target_margin

if denominator > 0:
    sp_sgd = total_c_sgd / denominator # 最終售價 (SP)
    platform_fee_sgd = sp_sgd * fee_rate # 平台抽成金額
    profit_sgd = sp_sgd * target_margin # 純利潤金額
    
    # 你的需求：到手金額與利潤率
    payout_sgd = sp_sgd - platform_fee_sgd # 到手金額 (SP - 平台費)
    profit_rate = (profit_sgd / sp_sgd) * 100 # 利潤率 (利潤 / SP)
    payout_profit_rate = ((payout_sgd - total_c_sgd) / payout_sgd) * 100 # 到手利潤率
    
    # 顯示主要數據
    res1, res2, res3 = st.columns(3)
    with res1:
# 顯示主要數據 (修正後的區塊)
    res1, res2, res3 = st.columns(3)
    with res1:
        st.success(f"### 🎯 建議售價 (SP)\n## {sp_sgd:.2f} SGD")
        st.write(f"約合台幣：{sp_sgd * exchange_rate:.0f} TWD")
    
    with res2:
        st.info(f"### 💵 到手金額 (Payout)\n## {payout_sgd:.2f} SGD")
        st.caption("已扣除平台抽成")

    with res3:
        st.warning(f"### 📈 利潤率分析")
        st.write(f"純利潤率：**{profit_rate:.1f}%**")
        st.write(f"到手利潤率：**{payout_profit_rate:.1f}%**")
