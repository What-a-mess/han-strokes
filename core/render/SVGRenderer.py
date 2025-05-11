from typing import List

from .StrokeRenderer import StrokeRenderer
from .BackgroundRenderer import BackgroundRenderer
from .BorderRenderer import BorderRenderer


class SVGRenderer:
    def __init__(
        self,
        strokeRenderer: StrokeRenderer,
        backgroundRenderer: BackgroundRenderer,
        borderRenderer: BorderRenderer,
        height: int = 1000,
    ):
        self.strokeRenderer = strokeRenderer
        self.backgroundRenderer = backgroundRenderer
        self.borderRenderer = borderRenderer
        self.height = height

    def get_svg(self, cur_idx: int = -1) -> str:
        # 生成 SVG 图形
        svg_template = """<svg xmlns="http://www.w3.org/2000/svg" width="{height}" height="{height}">
            {background}
            {strokes}
            {border}
        </svg>"""

        background_graph = self.backgroundRenderer.get_background_graph(self.height)
        stroke_graph = self.strokeRenderer.get_colorized_graph(cur_idx, self.height)
        border_graph = self.borderRenderer.get_border_graph(self.height)

        return svg_template.format(
            height=self.height,
            background=background_graph,
            strokes=stroke_graph,
            border=border_graph,
        )

    def get_svgs(self) -> List[str]:
        res = []
        for i in range(len(self.strokeRenderer.character.strokes)):
            res.append(self.get_svg(i))
        return res
