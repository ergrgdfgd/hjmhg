st.cache_data.clear()
# streamlit_battleship_bot.py
import streamlit as st
import numpy as np

FIELD_SIZE = 10
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']

# Инициализация сессии
if 'player_memory' not in st.session_state:
    st.session_state.player_memory = np.zeros((FIELD_SIZE, FIELD_SIZE), dtype=int)
    st.session_state.remaining_ships = SHIP_SIZES.copy()
    st.session_state.last_click = None

# Обработка выстрела
def update_player_shot(x, y, result):
    if result == 'miss':
        st.session_state.player_memory[x, y] = -1
    elif result == 'hit':
        st.session_state.player_memory[x, y] = 1
    elif result.startswith('sunk'):
        st.session_state.player_memory[x, y] = 1
        size = int(result.split('_')[1])
        if size in st.session_state.remaining_ships:
            st.session_state.remaining_ships.remove(size)

# Тепловая карта
@st.cache_data

def build_heatmap(memory, ships):
    heatmap = np.zeros_like(memory)
    for ship_len in ships:
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if j + ship_len <= FIELD_SIZE and all(memory[i, j+k] == 0 for k in range(ship_len)):
                    for k in range(ship_len):
                        heatmap[i, j+k] += 1
                if i + ship_len <= FIELD_SIZE and all(memory[i+k, j] == 0 for k in range(ship_len)):
                    for k in range(ship_len):
                        heatmap[i+k, j] += 1
    return heatmap

# Получить наилучшие цели
def suggest_next_target():
    heatmap = build_heatmap(st.session_state.player_memory, st.session_state.remaining_ships)
    max_val = np.max(heatmap)
    targets = np.argwhere(heatmap == max_val)
    return targets, heatmap

st.title("Морской Бой Бот")
st.write("Нажми на клетку, чтобы указать выстрел. Потом выбери результат.")

selected_cell = None
cols = st.columns(FIELD_SIZE + 1)
cols[0].markdown("**#**")
for j in range(FIELD_SIZE):
    cols[j+1].markdown(f"**{LETTERS[j]}**")

for i in range(FIELD_SIZE):
    row = st.columns(FIELD_SIZE + 1)
    row[0].markdown(f"**{i+1}**")
    for j in range(FIELD_SIZE):
        label = f"{i},{j}"
        cell = st.session_state.player_memory[i, j]
        btn_color = '⚪'
        if cell == -1:
            btn_color = '❌'
        elif cell == 1:
            btn_color = '🔥'
        if row[j+1].button(btn_color, key=label):
            st.session_state.last_click = (i, j)

if st.session_state.last_click:
    i, j = st.session_state.last_click
    st.markdown(f"**Выстрел в:** {i+1}{LETTERS[j]}")
    result = st.radio("Результат выстрела:", ["miss", "hit"] + [f"sunk_{n}" for n in set(SHIP_SIZES)])
    if st.button("Подтвердить выстрел"):
        update_player_shot(i, j, result)
        st.session_state.last_click = None

    st.divider()

# Показываем подсказку
targets, heatmap = suggest_next_target()
st.subheader("Лучшие врпанов для следующего выстрела:")
for x, y in targets:
    st.markdown(f"- {x+1}{LETTERS[y]}")

# Визуализация тепловой карты (по желанию)
st.subheader("Тепловая карта (чем выше цифра — тем вероятнее):")
heat_display = ""
for i in range(FIELD_SIZE):
    for j in range(FIELD_SIZE):
        if st.session_state.player_memory[i, j] != 0:
            heat_display += "⬛"
        else:
            heat_display += f"{int(heatmap[i,j]):2d} "
    heat_display += "\n"
st.code(heat_display, language="text")
