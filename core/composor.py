from typing import List

from common import Character
from core.render.StrokeRenderer import StrokeRenderer
from core.render.BackgroundRenderer import BackgroundRenderer
from core.render.GridRenderer import GridRenderer
from core.render.SVGRenderer import SVGRenderer
from core.render.BorderRenderer import BorderRenderer


def get_character_svg_at_index(
    character: Character,
    cur_idx: int = -1,
    height: int = 1000,
    border_color: str = "black",
    border_width: int = 2,
    grid_colors: List[str] = ["grey"] * 4,
    grid_dasharray: List[str] = ["3 3"] * 4,
    grid_width: List[int] = [0.5] * 4,
) -> str:
    """
    获取指定字符在指定索引处的 SVG 图形
    :param character: 字符对象
    :param cur_idx: 当前索引
    :param height: SVG 高度
    :param border_color: 边框颜色
    :param border_width: 边框宽度
    :param grid_colors: 网格颜色列表
    :param grid_dasharray: 网格虚线样式列表
    :param grid_width: 网格宽度列表
    :return: SVG 图形字符串
    """
    strokeRenderer = StrokeRenderer(character)
    # backgroundRenderer = BackgroundRenderer(background_color)
    gridRenderer = GridRenderer(
        grid_colors=grid_colors, grid_dasharray=grid_dasharray, grid_width=grid_width
    )
    borderRenderer = BorderRenderer(
        border_color=border_color, border_width=border_width
    )
    svgRenderer = SVGRenderer(strokeRenderer, gridRenderer, borderRenderer, height)

    return svgRenderer.get_svg(cur_idx)


def get_character_svgs_in_range(
    character: Character,
    start_idx: int = 0,
    end_idx: int = 0,
    height: int = 1000,
    border_color: str = "black",
    border_width: int = 2,
    grid_colors: List[str] = ["grey"] * 4,
    grid_dasharray: List[str] = ["3 3"] * 4,
    grid_width: List[int] = [0.5] * 4,
) -> List[str]:
    svg_list = []
    strokeRenderer = StrokeRenderer(character)
    # backgroundRenderer = BackgroundRenderer(background_color)
    gridRenderer = GridRenderer(
        grid_colors=grid_colors, grid_dasharray=grid_dasharray, grid_width=grid_width
    )
    borderRenderer = BorderRenderer(
        border_color=border_color, border_width=border_width
    )
    svgRenderer = SVGRenderer(strokeRenderer, gridRenderer, borderRenderer, height)
    
    for cur_idx in range(start_idx, end_idx + 1):
        svg = svgRenderer.get_svg(cur_idx)
        svg_list.append(svg)
    
    return svg_list
