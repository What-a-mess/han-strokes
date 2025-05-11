class BackgroundRenderer:

    def __init__(self, bg_color: str = "grey"):
        self.BASE_HEIGHT = 100
        self.bg_color = bg_color
        self.square_path = f"M 0 0 H {self.BASE_HEIGHT} V {self.BASE_HEIGHT} H 0 Z"
        self.vertical_path = f"M 50 0 V {self.BASE_HEIGHT}"
        self.horizontal_path = f"M 0 50 H {self.BASE_HEIGHT}"
        self.diagonal_path1 = f"M 0 0 L {self.BASE_HEIGHT} {self.BASE_HEIGHT}"
        self.diagonal_path2 = f"M {self.BASE_HEIGHT} 0 L 0 {self.BASE_HEIGHT}"

    def get_background_path(self) -> str:
        background_path_template = '<path d="{path}" stroke="{color}" fill="none" stroke-width="{width}" stroke-dasharray="{dasharray}" />'
        paths = [
            self.vertical_path,
            self.horizontal_path,
            self.diagonal_path1,
            self.diagonal_path2,
        ]

        colors = [self.bg_color] * len(paths)
        stroke_dasharray = ["3 3"] * len(paths)
        stroke_widths = [0.5] * len(paths)

        background_paths = []

        for idx, path in enumerate(paths):
            svg_path = background_path_template.format(
                path=path,
                color=colors[idx],
                width=stroke_widths[idx],
                dasharray=stroke_dasharray[idx],
            )
            background_paths.append(svg_path)

        background_paths.append(
            f'<path d="{self.square_path}" stroke="black" fill="none" stroke-width="{2}" />'
        )

        return "\n".join(background_paths)

    def get_background_graph(self, height: int = 1000) -> str:
        background_path = self.get_background_path()
        scale = height / self.BASE_HEIGHT
        g_template = '<g transform="scale({scale_factor}, {scale_factor})">\n    {background_path}\n</g>'

        return g_template.format(scale_factor=scale, background_path=background_path)
