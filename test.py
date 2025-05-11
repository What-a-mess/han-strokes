from core.render.BackgroundRenderer import BackgroundRenderer
from core.render.StrokeRenderer import StrokeRenderer
from common.Character import Character
from core.render.SVGRenderer import SVGRenderer
from core.render.DummyBackgroundRenderer import DummyBackgroundRenderer
from core.render.BorderRenderer import BorderRenderer

from core.composor import get_character_svg_at_index

character = Character("汉")
# strokeRenderer = StrokeRenderer(character)
# backgroundRenderer = BackgroundRenderer("#DDDDDD")
# # backgroundRenderer = DummyBackgroundRenderer()
# borderRenderer = BorderRenderer()
# svgRenderer = SVGRenderer(strokeRenderer, backgroundRenderer, borderRenderer, height=1000)

# svg = svgRenderer.get_svg(1)

svg = get_character_svg_at_index(
    character,
    cur_idx=3,
    height=1000,
    border_color="#000000",
    border_width=2,
    grid_colors=["#DDDDDD", "#DDDDDD", "#DDDDDD", "#DDDDDD"],
    grid_dasharray=["3 3", "3 3", "3 3", "3 3"],
    grid_width=[0.5, 0.5, 0.5, 0.5],
)

print(svg)

with open(f"output.svg", "w") as file:
    file.write(svg)

