import streamlit as st

# 1. 網頁基本設定
st.set_page_config(page_title="Foodie Pricing", layout="wide")
st.title("Foodie Pricing Calculator 🍔")

# --- 第一部分：參數調節區 (側邊欄) ---
st.sidebar.header("⚙️ 全域參數設定")
exchange_rate = st.sidebar.slider("即時匯率 (TWD/SGD)", 20.0, 26.0, 23.5, step=0.1)
shipping_rate_per_kg = st.sidebar.slider("每公斤運費成本 (SGD/kg)", 0.0, 20.0, 8.0, step=0.5)

st.sidebar.subheader("平台抽成比例 (%)")
platform_type = st.sidebar.radio("選擇計算平台", ["Shopee", "Lazada"])
if platform_type == "Shopee":
    fee_rate = st.sidebar.slider("Shopee 總抽成率 (%)", 0.0, 30.0, 17.3, step=0.1) / 100
else:
    fee_rate = st.sidebar.slider("Lazada 總抽成率 (%)", 0.0, 30.0, 15.0, step=0.1) / 100

# --- 第二部分：數據輸入區 ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 商品基本資料")
    cost_twd = st.number_input("商品成本 (TWD)", min_value=0.0, value=500.0)
    weight_kg = st.number_input("商品重量 (kg)", min_value=0.0, value=0.5)
    cost_sgd = cost_twd / exchange_rate
    weight_shipping_sgd = weight_kg * shipping_rate_per_kg
    st.write(f"➡️ 商品成本：{cost_sgd:.2f} SGD")
    st.write(f"➡️ 重量運費：{weight_shipping_sgd:.2f} SGD")

with col2:
    st.subheader("💰 其他成本與利潤設定")
    miscellaneous_sgd = st.number_input("雜項固定支出 (SGD)", min_value=0.0, value=1.0)
    platform_fixed_shipping = 2.3
    target_margin = st.slider("預設獲利率 (%)", 5, 50, 20) / 100

# --- 第三部分：計算邏輯 ---
st.divider()
total_c_sgd = cost_sgd + weight_shipping_sgd + miscellaneous_sgd + platform_fixed_shipping
denominator = 1 - fee_rate - target_margin

if denominator > 0:
    sp_sgd = total_c_sgd / denominator
    platform_fee_sgd = sp_sgd * fee_rate
    profit_sgd = sp_sgd * target_margin
    payout_sgd = sp_sgd - platform_fee_sgd
    
    # 計算利潤率
    profit_rate = (profit_sgd / sp_sgd) * 100
    payout_profit_rate = ((payout_sgd - total_c_sgd) / payout_sgd) * 100

    # 顯示結果 (注意這裡的垂直對齊)
    res1, res2, res3 = st.columns(3)
    res1.success(f"### 🎯 建議售價 (SP)\n## {sp_sgd:.2f} SGD")
    res1.write(f"約合台幣：{sp_sgd * exchange_rate:.0f} TWD")
    
    res2.info(f"### 💵 到手金額 (Payout)\n## {payout_sgd:.2f} SGD")
    res2.caption("已扣除平台抽成")

    res3.warning(f"### 📈 利潤率分析")
    res3.write(f"純利潤率：**{profit_rate:.1f}%**")
    res3.write(f"到手利潤率：**{payout_profit_rate:.1f}%**")

    with st.expander("查看詳細成本結構"):
        st.write({
            "建議售價 (SP)": round(sp_sgd, 2),
            "平台抽成 (Fee)": round(platform_fee_sgd, 2),
            "到手金額 (Payout)": round(payout_sgd, 2),
            "總成本 (C)": round(total_c_sgd, 2),
            "最終純利": round(profit_sgd, 2)
        })
else:
    st.error("⚠️ 警告：抽成率與獲利率相加超過 100%！")