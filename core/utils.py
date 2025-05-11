import json


def flip_y(path, height=1000):
    # 将路径拆分为命令和坐标
    tokens = path.split()
    flipped_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.isalpha():  # 处理指令（如 M, Q, C, Z 等）
            flipped_tokens.append(token)
            i += 1
        else:  # 处理坐标（x y）
            # 提取连续的两个数值作为 x 和 y
            x = float(tokens[i])
            y = float(tokens[i + 1])
            flipped_y = height - y  # 反转 y 坐标
            flipped_tokens.extend([str(x), str(flipped_y)])
            i += 2
    return " ".join(flipped_tokens)


def load_strokes(character):
    # Placeholder for loading stroke data
    # In a real implementation, this would load the stroke data from a file or database
    with open(f"resource/stroke_data/{character}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get("strokes", [])
