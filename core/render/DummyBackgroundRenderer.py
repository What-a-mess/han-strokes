class DummyBackgroundRenderer:

    def __init__(self):
        self.BASE_HEIGHT = 100

    def get_background_graph(self, height: int = 1000) -> str:
        scale = height / self.BASE_HEIGHT
        g_template = '<g transform="scale({scale_factor}, {scale_factor})">\n</g>'

        return g_template.format(scale_factor=scale)
