import streamlit as st
import numpy as np
import pandas as pd

FIELD_SIZE = 10
INITIAL_SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

# === Session State ===
if "player_memory" not in st.session_state:
    st.session_state.player_memory = np.zeros((FIELD_SIZE, FIELD_SIZE), dtype=int)
    st.session_state.remaining_ships = INITIAL_SHIP_SIZES.copy()

def update_player_shot(x, y, result):
    if result == 'miss':
        st.session_state.player_memory[x, y] = -1
    elif result == 'hit':
        st.session_state.player_memory[x, y] = 1
    elif result.startswith('sunk'):
        st.session_state.player_memory[x, y] = 1
        ship_size = int(result.split('_')[1])
        if ship_size in st.session_state.remaining_ships:
            st.session_state.remaining_ships.remove(ship_size)

def build_heatmap(memory, remaining_ship_sizes):
    heatmap = np.zeros_like(memory)
    for ship_len in remaining_ship_sizes:
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                # Горизонтально
                if j + ship_len <= FIELD_SIZE and all(memory[i, j+k] == 0 for k in range(ship_len)):
                    for k in range(ship_len):
                        heatmap[i, j + k] += 1
                # Вертикально
                if i + ship_len <= FIELD_SIZE and all(memory[i+k, j] == 0 for k in range(ship_len)):
                    for k in range(ship_len):
                        heatmap[i + k, j] += 1
    return heatmap

def suggest_next_target():
    heatmap = build_heatmap(st.session_state.player_memory, st.session_state.remaining_ships)
    max_val = np.max(heatmap)
    if max_val == 0:
        return "Нет доступных клеток", heatmap
    targets = np.argwhere(heatmap == max_val)
    return targets.tolist(), heatmap

# === Streamlit Interface ===

st.title("🎯 Морской бой — AI-помощник")
st.markdown("Вводи координаты и результат выстрела. Бот подскажет лучшие клетки для следующего выстрела.")

col1, col2, col3 = st.columns(3)
with col1:
    x = st.number_input("Координата X", min_value=0, max_value=FIELD_SIZE - 1, step=1)
with col2:
    y = st.number_input("Координата Y", min_value=0, max_value=FIELD_SIZE - 1, step=1)
with col3:
    result = st.selectbox("Результат", ["miss", "hit"] + [f"sunk_{s}" for s in set(INITIAL_SHIP_SIZES)])

if st.button("➕ Добавить выстрел"):
    update_player_shot(int(x), int(y), result)

st.markdown("### 📌 Память игрока")
st.dataframe(pd.DataFrame(st.session_state.player_memory))

next_targets, heatmap = suggest_next_target()

st.markdown("### 🔥 Рекомендованные клетки для следующего выстрела:")
if isinstance(next_targets, str):
    st.warning(next_targets)
else:
    for t in next_targets:
        st.write(f"👉 Клетка: ({t[0]}, {t[1]})")

st.markdown("### 🌡️ Тепловая карта вероятностей")
st.dataframe(pd.DataFrame(heatmap.astype(int)))

if st.button("🔄 Сбросить всё"):
    st.session_state.player_memory = np.zeros((FIELD_SIZE, FIELD_SIZE), dtype=int)
    st.session_state.remaining_ships = INITIAL_SHIP_SIZES.copy()
    st.success("Состояние сброшено!")
