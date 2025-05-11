class BorderRenderer:
    def __init__(self, border_color: str = "black", border_width=2):
        self.BASE_HEIGHT = 100
        self.border_color = border_color
        self.border_width = border_width

    def get_border_path(self) -> str:
        # 生成边框路径
        border_path = f"M 0 0 H {self.BASE_HEIGHT} V {self.BASE_HEIGHT} H 0 Z"
        border_path_template = '<path d="{path}" stroke="{color}" fill="none" stroke-width="{width}" />'

        # 生成 SVG 路径
        svg_path = border_path_template.format(
            path=border_path, color=self.border_color, width=self.border_width
        )

        return svg_path

    def get_border_graph(self, height: int = 1000) -> str:
        border_path = self.get_border_path()
        scale = height / self.BASE_HEIGHT
        g_template = '<g transform="scale({scale_factor}, {scale_factor})">\n    {border_path}\n</g>'

        return g_template.format(scale_factor=scale, border_path=border_path)
