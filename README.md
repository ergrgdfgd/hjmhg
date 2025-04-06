import random
import streamlit as st

# Данные по категориям кейса
case_cost = 5
probabilities = {
    "Шлак (<5₽)": 0.2286,
    "Средний дроп (5–50₽)": 0.3714,
    "Хороший дроп (50–200₽)": 0.2286,
    "Жирный дроп (200+₽)": 0.1714,
}

avg_prices = {
    "Шлак (<5₽)": 3,
    "Средний дроп (5–50₽)": 25,
    "Хороший дроп (50–200₽)": 100,
    "Жирный дроп (200+₽)": 500,
}

# Интерфейс Streamlit
st.title("🎯 Симулятор кейса Rags to Riches")

num_cases = st.slider("Сколько кейсов открыть?", 1, 500, 100)

if st.button("🔓 Открыть кейсы"):
    drops = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=num_cases)
    result = {cat: drops.count(cat) for cat in probabilities}
    total_earned = sum(avg_prices[cat] * count for cat, count in result.items())
    total_spent = case_cost * num_cases
    net = total_earned - total_spent

    st.subheader("📦 Результаты:")
    for cat, count in result.items():
        st.write(f"{cat}: {count} шт")

    st.markdown("---")
    st.write(f"💸 Потрачено: **{total_spent}₽**")
    st.write(f"💰 Получено дропа на: **{round(total_earned, 2)}₽**")
    st.write(f"📈 Чистая прибыль: **{round(net, 2)}₽**")

    st.markdown("---")
    if net > 0:
        st.success("Окупился! Но не забывай — это удача, а не гарантия!")
    else:
        st.error("Не повезло в этот раз. Может, повезёт в следующий!")
