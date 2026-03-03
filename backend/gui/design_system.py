"""设计系统 - HUD Neon 风格（初版）
集中管理颜色、字体、发光效果等风格 token，方便后续统一应用到前端 UI。
"""

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


# 颜色与字体令牌（初版，后续可扩展为更多主题）
NEON_COLORS = {
    # 背景/界面主色调，偏向深色 HUD 风格
    "bg": "#0A0F1A",
    "panel": "#12252A",
    # 文字/前景
    "fg": "#E6F0FF",
    # 霓虹强调色
    "neon": "#00e5ff",
    "neon_alt": "#00e58e",
}

FONTS = {
    "family": '"Microsoft YaHei", "Segoe UI", Roboto, Arial, sans-serif',
    "size_pt": 10,
}


def glow(
    widget,
    color: str | None = None,
    radius: int = 14,
    offset_x: int = 0,
    offset_y: int = 0,
):
    """为控件添加发光效果，便于打造 HUD 的光辉边缘。"""
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(radius)
    eff.setColor(QColor(color or NEON_COLORS["neon"]))
    eff.setOffset(offset_x, offset_y)
    widget.setGraphicsEffect(eff)


def apply_neon_theme(widget):
    """应用基础 Neon HUD 风格到给定的控件/窗口。"""
    base_style = f"""
    QWidget {{
        background: {NEON_COLORS["bg"]};
        color: {NEON_COLORS["fg"]};
        font-family: {FONTS["family"]};
        font-size: {FONTS["size_pt"]}pt;
    }}
    QFrame#mainContainer {{
        background: rgba(18, 40, 50, 0.6);
        border: 1px solid {NEON_COLORS["neon"]};
        border-radius: 8px;
    }}
    TitleBar {{
        background: transparent;
    }}
    TitleBar #titleBlock {{
        background: linear-gradient(to bottom, #1A2C32, #12252A);
        border: 1px solid {NEON_COLORS["neon"]};
        border-radius: 6px;
        padding: 2px;
    }}
    TitleBar QPushButton {{
        color: {NEON_COLORS["neon"]};
        border: 1px solid {NEON_COLORS["neon"]};
        border-radius: 6px;
        padding: 4px 8px;
    }}
    TitleBar QPushButton:hover {{
        background: rgba(0, 200, 216, 0.15);
    }}
    """
    widget.setStyleSheet(base_style)
