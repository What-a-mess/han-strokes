from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import QByteArray, Qt

def get_qt_svg_item(svg_content: str) -> QGraphicsSvgItem:
    """
    Create a QGraphicsSvgItem from SVG content.
    """
    # 使用 QSvgRenderer 加载 SVG 字符串
    svg_data = QByteArray(svg_content.encode('utf-8'))
    
    # 创建SVG渲染器
    renderer = QSvgRenderer(svg_data)
    
    if renderer.isValid():
        # 创建SVG图形项
        svg_item = QGraphicsSvgItem()
        svg_item.setSharedRenderer(renderer)
        return svg_item
    else:
        print("Invalid SVG data")
        return None
    
def render_svg_to_view(svg_item: QGraphicsSvgItem, view: QGraphicsView):
    """
    Render SVG content to a QGraphicsView.
    """
    scene = view.scene()
    
    if scene is None:
        return
        # scene = QGraphicsScene()
        # view.setScene(scene)
    
    # 清空场景
    scene.clear()
    
    # 添加SVG图形项到场景
    scene.addItem(svg_item)
    
    # 调整视图以适应SVG图形项
    view.fitInView(svg_item, Qt.AspectRatioMode.KeepAspectRatio)

def render_svg_to_view_from_str(svg_content: str, view: QGraphicsView):

    scene = view.scene()
    # 使用 QSvgRenderer 加载 SVG 字符串
    svg_data = QByteArray(svg_content.encode('utf-8'))
    
    # 创建SVG渲染器
    renderer = QSvgRenderer(svg_data)
    
    if renderer.isValid():
        # 创建SVG图形项
        svg_item = QGraphicsSvgItem()
        svg_item.setSharedRenderer(renderer)
        scene.addItem(svg_item)
        view.fitInView(svg_item, Qt.AspectRatioMode.KeepAspectRatio)
    else:
        print("Invalid SVG data")