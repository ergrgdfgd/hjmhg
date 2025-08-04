import numpy as np

# === Настройки ===
FIELD_SIZE = 10
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

# === Начальное состояние ===
player_memory = np.zeros((FIELD_SIZE, FIELD_SIZE), dtype=int)
remaining_ships = SHIP_SIZES.copy()

def update_player_shot(x, y, result):
    global player_memory, remaining_ships
    if result == 'miss':
        player_memory[x, y] = -1
    elif result == 'hit':
        player_memory[x, y] = 1
    elif result.startswith('sunk'):
        player_memory[x, y] = 1
        ship_size = int(result.split('_')[1])
        if ship_size in remaining_ships:
            remaining_ships.remove(ship_size)

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
    heatmap = build_heatmap(player_memory, remaining_ships)
    max_val = np.max(heatmap)
    if max_val == 0:
        return "Нет доступных клеток", heatmap
    targets = np.argwhere(heatmap == max_val)
    return targets.tolist(), heatmap

def print_board(board):
    print("    " + " ".join(str(i) for i in range(FIELD_SIZE)))
    for i in range(FIELD_SIZE):
        row = [f"{board[i, j]:2d}" for j in range(FIELD_SIZE)]
        print(f"{i:2d} | {' '.join(row)}")

# === Основной цикл ===
if __name__ == "__main__":
    print("=== Морской бой — помощник по стрельбе ===")
    print("Формат ввода: X Y результат (пример: 3 4 hit или 5 6 sunk_2 или 1 1 miss)")
    print("Команда 'exit' — выйти\n")

    while True:
        try:
            user_input = input("Введите выстрел и результат: ").strip().lower()
            if user_input == 'exit':
                break
            parts = user_input.split()
            if len(parts) != 3:
                print("❌ Неверный формат. Пример: 3 4 hit")
                continue

            x, y = int(parts[0]), int(parts[1])
            if not (0 <= x < FIELD_SIZE and 0 <= y < FIELD_SIZE):
                print("❌ Координаты вне поля.")
                continue

            result = parts[2]
            if result not in ['miss', 'hit'] and not result.startswith('sunk_'):
                print("❌ Неверный результат. Используй miss, hit или sunk_N (например, sunk_3)")
                continue

            update_player_shot(x, y, result)
            next_targets, heatmap = suggest_next_target()

            print("\n🎯 Лучшие клетки для следующего выстрела:")
            for t in next_targets:
                print(f" -> {tuple(t)}")

            print("\n📊 Тепловая карта вероятностей:")
            print_board(heatmap)
            print("\n")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
