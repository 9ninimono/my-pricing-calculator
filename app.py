import streamlit as st

# 網頁基本設定
st.set_page_config(page_title="Foodie Pricing", layout="wide")
st.title("Foodie Pricing Calculator 🍽️")

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
    st.subheader("💰 其他成本與利潤")
    miscellaneous_sgd = st.number_input("雜項固定支出 (SGD)", min_value=0.0, value=1.0, step=0.1)
    platform_fixed_shipping = 2.3  # 你之前提到的固定平台運費
    target_margin = st.slider("期望獲利率 (%)", 5, 50, 20) / 100

# --- 第三部分：計算結果 ---
st.divider()

# 總成本 (SGD) = 商品成本 + 重量運費 + 雜項 + 平台固定運費
total_base_cost_sgd = cost_sgd + weight_shipping_sgd + miscellaneous_sgd + platform_fixed_shipping

# 公式：售價 = 總成本 / (1 - 抽成率 - 獲利率)
denominator = 1 - fee_rate - target_margin

if denominator > 0:
    final_price_sgd = total_base_cost_sgd / denominator
    final_profit_sgd = final_price_sgd * target_margin
    
    result_col1, result_col2 = st.columns(2)
    with result_col1:
        st.success(f"### 🎯 建議售價：{final_price_sgd:.2f} SGD")
        st.write(f"約合台幣：{final_price_sgd * exchange_rate:.0f} TWD")
    
    with result_col2:
        st.info(f"### 💵 每單純利：{final_profit_sgd:.2f} SGD")
        st.write(f"平台抽成金額：{final_price_sgd * fee_rate:.2f} SGD")
        
    # 成本結構圓餅圖 (選配功能，新手可先參考數據)
# 數據詳情展開
        st.expander("查看成本結構詳情").write({
            "商品成本 (SGD)": round(cost_sgd, 2),
            "國際重量運費 (SGD)": round(weight_shipping_sgd, 2),
            "平台固定運費 (SGD)": platform_fixed_shipping,
            "雜項支出 (SGD)": miscellaneous_sgd,
            "平台手續費 (SGD)": round(final_price_sgd * fee_rate, 2),
            "預期利潤 (SGD)": round(final_profit_sgd, 2)
        }) # <--- 這裡必須有括號關閉 write
    else:
        st.error("⚠️ 警告：抽成率與獲利率相加超過 100%，請重新調整參數。")
