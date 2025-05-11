from core.utils import load_strokes

class Character:
    def __init__(self, character: str):
        self.character = character
        self.strokes = load_strokes(character)
        
    def get_stroke_count(self) -> int:
        return len(self.strokes)