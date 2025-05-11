from common.Character import Character


class StrokeRenderer:
    def __init__(
        self,
        character: Character,
        old_stroke_color: str = "black",
        cur_stroke_color: str = "red",
        next_stroke_color: str = "grey",
    ):
        self.character = character
        self.old_stroke_color = old_stroke_color
        self.cur_stroke_color = cur_stroke_color
        self.next_stroke_color = next_stroke_color
        self.BASE_HEIGHT = 1000
        self.BASE_Y_SHIFT = 900

    @staticmethod
    def get_colorized_path(path, color) -> str:

        # 生成 <path> 标签
        svg_path = f'<path d="{path}" fill="{color}" stroke="none" />'
        return svg_path

    def get_colorized_paths(self, cur_idx: int = -1) -> str:
        # 生成多个 <path> 标签
        svg_paths = []
        paths = self.character.strokes
        stroke_count = len(paths)
        if cur_idx < 0 or cur_idx > stroke_count:
            cur_idx = stroke_count

        colors = [self.old_stroke_color] * stroke_count
        if cur_idx < stroke_count:
            colors[cur_idx] = self.cur_stroke_color
            if cur_idx + 1 < stroke_count:
                colors[cur_idx + 1 :] = [self.next_stroke_color] * (
                    stroke_count - cur_idx - 1
                )

        for path, color in zip(paths, colors):
            svg_path = StrokeRenderer.get_colorized_path(path, color)
            svg_paths.append(svg_path)
            
        # svg_paths = svg_paths[::-1]

        return "\n".join(svg_paths)

    def get_colorized_graph(self, cur_idx: int = -1, height=1000) -> str:
        colorized_paths = self.get_colorized_paths(cur_idx)
        scale = height / self.BASE_HEIGHT
        y_shift = self.BASE_Y_SHIFT * scale
        g_template = '<g transform="translate(0, {y_shift}) scale({scale_factor}, -{scale_factor})">\n    {colorized_paths}\n</g>'

        return g_template.format(
            y_shift=y_shift, scale_factor=scale, colorized_paths=colorized_paths
        )
