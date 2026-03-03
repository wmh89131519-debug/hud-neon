"""
Design System - HUD Neon 风格 (Neon Minimal 方向)
方向A: 简洁线条、干净对比、淡入淡出动画，强调信息密度与可读性
"""

from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer


# ==================== 风格令牌 (Style Tokens) ====================

STYLE_TOKENS = {
    "colors": {
        "primary": "#00C8D8",
        "secondary": "#00E58E",
        "accent": "#B54EFF",
    },
    "typography": {
        "font_family": '"Inter", "Microsoft YaHei", "Segoe UI", sans-serif',
        "size_base": 10,
        "size_small": 8,
        "size_large": 14,
        "size_title": 18,
    },
    "shapes": {
        "radius_small": 4,
        "radius_medium": 6,
        "radius_large": 8,
    },
    "animation": {
        "duration_fast": 150,
        "duration_normal": 250,
        "duration_slow": 400,
    },
}


# ==================== 主题定义 ====================


class Theme:
    """主题基类"""

    COLORS = {}
    FONTS = {}
    ANIMATION = {}

    @classmethod
    def get_colors(cls):
        return cls.COLORS

    @classmethod
    def get_fonts(cls):
        return cls.FONTS

    @classmethod
    def get_animation(cls):
        return cls.ANIMATION


class NeonMinimalTheme(Theme):
    """Neon Minimal 主题 - 简洁线条、干净对比、淡入淡出动画

    特点:
    - 简洁线条设计
    - 高对比度确保可读性
    - 柔和的淡入淡出动画
    - 适合长时间使用的舒适感
    """

    COLORS = {
        "bg": "#0E141C",
        "panel": "#151D26",
        "fg": "#E8EDF2",
        "fg_secondary": "#8A9BAC",
        "neon": "#00C8D8",
        "neon_alt": "#00E58E",
        "neon_subtle": "#1A3A42",
        "border": "#2A3A46",
        "border_focus": "#00C8D8",
        "hover": "rgba(0, 200, 216, 0.12)",
        "active": "rgba(0, 200, 216, 0.2)",
        "disabled": "#3A4A56",
        "error": "#FF5252",
        "success": "#00E58E",
        "warning": "#FFB74D",
    }
    FONTS = {
        "family": '"Inter", "Microsoft YaHei", "Segoe UI", sans-serif',
        "size_pt": 10,
        "size_small": 8,
        "size_large": 14,
        "size_title": 18,
        "line_height": 1.5,
    }
    ANIMATION = {
        "duration_fast": 150,
        "duration_normal": 250,
        "duration_slow": 400,
        "easing": QEasingCurve.Type.InOutQuad,
    }


class NeonDarkTheme(Theme):
    """深色霓虹主题"""

    COLORS = {
        "bg": "#0A0F1A",
        "panel": "#12252A",
        "fg": "#E6F0FF",
        "fg_secondary": "#8A9BAC",
        "neon": "#00e5ff",
        "neon_alt": "#00e58e",
        "neon_subtle": "#1A3A42",
        "border": "#1A3A4A",
        "border_focus": "#00e5ff",
        "hover": "rgba(0, 229, 255, 0.15)",
        "active": "rgba(0, 229, 255, 0.25)",
        "disabled": "#3A4A5A",
        "error": "#ff5252",
        "success": "#69f0ae",
    }
    FONTS = {
        "family": '"Microsoft YaHei", "Segoe UI", Roboto, Arial, sans-serif',
        "size_pt": 10,
        "size_small": 8,
        "size_large": 14,
        "size_title": 18,
    }
    ANIMATION = {
        "duration_fast": 150,
        "duration_normal": 250,
        "duration_slow": 400,
        "easing": QEasingCurve.Type.InOutSine,
    }


class NeonLightTheme(Theme):
    """浅色霓虹主题"""

    COLORS = {
        "bg": "#F5F8FA",
        "panel": "#FFFFFF",
        "fg": "#1A2A3A",
        "fg_secondary": "#5A6A7A",
        "neon": "#0097A7",
        "neon_alt": "#00897B",
        "neon_subtle": "#E0F2F3",
        "border": "#B0BEC5",
        "border_focus": "#0097A7",
        "hover": "rgba(0, 151, 167, 0.12)",
        "active": "rgba(0, 151, 167, 0.2)",
        "disabled": "#CFD8DC",
        "error": "#D32F2F",
        "success": "#388E3C",
    }
    FONTS = {
        "family": '"Microsoft YaHei", "Segoe UI", Roboto, Arial, sans-serif',
        "size_pt": 10,
        "size_small": 8,
        "size_large": 14,
        "size_title": 18,
    }
    ANIMATION = {
        "duration_fast": 150,
        "duration_normal": 250,
        "duration_slow": 400,
        "easing": QEasingCurve.Type.InOutQuad,
    }


class CyberpunkTheme(Theme):
    """赛博朋克主题"""

    COLORS = {
        "bg": "#0D0221",
        "panel": "#1A0533",
        "fg": "#00FFF5",
        "fg_secondary": "#A0E0DC",
        "neon": "#FF00FF",
        "neon_alt": "#00FFF5",
        "neon_subtle": "#2A1040",
        "border": "#3D1A5C",
        "border_focus": "#FF00FF",
        "hover": "rgba(255, 0, 255, 0.2)",
        "active": "rgba(255, 0, 255, 0.35)",
        "disabled": "#2A1A3D",
        "error": "#FF1744",
        "success": "#00E676",
    }
    FONTS = {
        "family": '"Consolas", "Courier New", monospace',
        "size_pt": 10,
        "size_small": 8,
        "size_large": 14,
        "size_title": 18,
    }
    ANIMATION = {
        "duration_fast": 100,
        "duration_normal": 200,
        "duration_slow": 350,
        "easing": QEasingCurve.Type.InOutExpo,
    }


# 主题注册表
THEMES = {
    "neon_minimal": NeonMinimalTheme,  # 方向A: 默认主题
    "neon_dark": NeonDarkTheme,
    "neon_light": NeonLightTheme,
    "cyberpunk": CyberpunkTheme,
}

# 当前主题 (默认使用 Neon Minimal)
_current_theme = "neon_minimal"


# ==================== 颜色/字体访问器 ====================


def get_colors():
    """获取当前主题颜色"""
    return THEMES[_current_theme].COLORS


def get_fonts():
    """获取当前主题字体"""
    return THEMES[_current_theme].FONTS


def set_theme(theme_name: str):
    """设置主题"""
    global _current_theme
    if theme_name in THEMES:
        _current_theme = theme_name


def get_theme_name():
    """获取当前主题名"""
    return _current_theme


def get_all_theme_names():
    """获取所有主题名"""
    return list(THEMES.keys())


# 兼容旧版
NEON_COLORS = property(lambda self: get_colors())
FONTS = property(lambda self: get_fonts())


# ==================== Glow 效果 ====================


def glow(widget, color=None, blur_radius=14, offset_x=0, offset_y=0):
    """为控件添加发光效果

    Args:
        widget: 目标控件
        color: 发光颜色 (默认使用主题色)
        blur_radius: 模糊半径
        offset_x: X偏移
        offset_y: Y偏移
    """
    colors = get_colors()
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(blur_radius)
    eff.setColor(QColor(color or colors["neon"]))
    eff.setOffset(offset_x, offset_y)
    widget.setGraphicsEffect(eff)
    return eff


def glow_pulse(widget, color=None, min_blur=8, max_blur=20, duration=1500):
    """创建脉冲发光动画

    Args:
        widget: 目标控件
        color: 发光颜色
        min_blur: 最小模糊半径
        max_blur: 最大模糊半径
        duration: 动画周期 (毫秒)
    """
    colors = get_colors()
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(min_blur)
    eff.setColor(QColor(color or colors["neon"]))
    widget.setGraphicsEffect(eff)

    anim = QPropertyAnimation(eff, b"blurRadius")
    anim.setDuration(duration)
    anim.setStartValue(min_blur)
    anim.setEndValue(max_blur)
    anim.setEasingCurve(QEasingCurve.Type.InOutSine)
    anim.setLoopCount(-1)
    anim.setDirection(QPropertyAnimation.Direction.Forward)
    anim.start()
    return anim


# ==================== Fade 动画 ====================


def fade_in(widget, duration=250):
    """淡入动画

    Args:
        widget: 目标控件
        duration: 动画时长 (毫秒)
    """
    widget.setWindowOpacity(0)
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setDuration(duration)
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
    anim.start()
    return anim


def fade_out(widget, duration=250, hide_after=True):
    """淡出动画

    Args:
        widget: 目标控件
        duration: 动画时长 (毫秒)
        hide_after: 动画结束后是否隐藏控件
    """
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setDuration(duration)
    anim.setStartValue(1)
    anim.setEndValue(0)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
    if hide_after:
        anim.finished.connect(widget.hide)
    anim.start()
    return anim


# ==================== 样式生成器 ====================


def apply_neon_theme(widget, theme_name=None):
    """应用基础 Neon 主题到控件"""
    global _current_theme
    old_theme = _current_theme
    if theme_name:
        set_theme(theme_name)

    colors = get_colors()
    fonts = get_fonts()

    base_style = f"""
    QWidget {{
        background: {colors["bg"]};
        color: {colors["fg"]};
        font-family: {fonts["family"]};
        font-size: {fonts["size_pt"]}pt;
    }}
    QFrame#mainContainer {{
        background: rgba(18, 40, 50, 0.6);
        border: 1px solid {colors["neon"]};
        border-radius: 8px;
    }}
    TitleBar {{
        background: transparent;
    }}
    TitleBar #titleBlock {{
        background: linear-gradient(to bottom, #1A2C32, #12252A);
        border: 1px solid {colors["neon"]};
        border-radius: 6px;
        padding: 2px;
        margin: 2px;
    }}
    TitleBar QPushButton {{
        color: {colors["neon"]};
        border: 1px solid {colors["neon"]};
        border-radius: 6px;
        padding: 4px 8px;
    }}
    TitleBar QPushButton:hover {{
        background: {colors["hover"]};
    }}
    """
    widget.setStyleSheet(base_style)

    # 恢复原主题
    if theme_name:
        set_theme(old_theme)


def get_button_style(btn_type="normal", theme_name=None):
    """获取按钮样式 - Neon Minimal 简洁风格"""
    if theme_name:
        set_theme(theme_name)
    colors = get_colors()
    fonts = get_fonts()

    base = f"""
        QPushButton {{
            background: {colors["panel"]};
            color: {colors["fg"]};
            border: 1px solid {colors["border"]};
            border-radius: {STYLE_TOKENS["shapes"]["radius_medium"]}px;
            padding: 8px 16px;
            font-family: {fonts["family"]};
            font-size: {fonts["size_pt"]}pt;
            min-width: 60px;
            outline: none;
        }}
        QPushButton:hover {{
            background: {colors["hover"]};
            border-color: {colors["neon"]};
            color: {colors["neon"]};
        }}
        QPushButton:pressed {{
            background: {colors["active"]};
        }}
        QPushButton:disabled {{
            background: {colors["disabled"]};
            color: {colors["fg_secondary"]};
            border-color: {colors["disabled"]};
        }}
        QPushButton:focus {{
            border-color: {colors["neon"]};
        }}
    """

    if btn_type == "glow":
        base += f"""
        QPushButton:checked {{
            background: {colors["neon"]};
            color: {colors["bg"]};
            border-color: {colors["neon"]};
        }}
        """
    elif btn_type == "icon":
        base += f"""
        QPushButton {{
            font-size: {fonts["size_large"]}pt;
            padding: 6px 10px;
            min-width: 36px;
        }}
        """

    return base


def get_input_style(theme_name=None):
    """获取输入框样式 - Neon Minimal 简洁风格"""
    if theme_name:
        set_theme(theme_name)
    colors = get_colors()
    fonts = get_fonts()

    return f"""
    QLineEdit, QTextEdit, QSpinBox {{
        background: {colors["bg"]};
        color: {colors["fg"]};
        border: 1px solid {colors["border"]};
        border-radius: {STYLE_TOKENS["shapes"]["radius_small"]}px;
        padding: 8px 10px;
        font-family: {fonts["family"]};
        font-size: {fonts["size_pt"]}pt;
        outline: none;
    }}
    QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {{
        border: 2px solid {colors["border_focus"]};
    }}
    QLineEdit:hover, QTextEdit:hover, QSpinBox:hover {{
        border-color: {colors["neon"]};
    }}
    QLineEdit:disabled, QTextEdit:disabled, QSpinBox:disabled {{
        background: {colors["disabled"]};
        color: {colors["fg_secondary"]};
        border-color: {colors["disabled"]};
    }}
    QLineEdit::placeholder, QTextEdit::placeholder {{
        color: {colors["fg_secondary"]};
    }}
    """


def get_slider_style(theme_name=None):
    """获取滑块样式 - Neon Minimal 简洁风格"""
    if theme_name:
        set_theme(theme_name)
    colors = get_colors()

    return f"""
    QSlider::groove:horizontal {{
        background: {colors["border"]};
        height: 4px;
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        background: {colors["neon"]};
        width: 14px;
        height: 14px;
        margin: -5px 0;
        border-radius: 7px;
        border: 2px solid {colors["bg"]};
    }}
    QSlider::handle:horizontal:hover {{
        background: {colors["neon_alt"]};
    }}
    QSlider::sub-page:horizontal {{
        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
            stop:0 {colors["neon"]},
            stop:1 {colors["neon_alt"]});
        border-radius: 2px;
    }}
    QSlider::groove:vertical, QSlider::handle:vertical {{
        analogous to horizontal
    }}
    """


def get_checkbox_style(theme_name=None):
    """获取复选框样式 - Neon Minimal 简洁风格"""
    if theme_name:
        set_theme(theme_name)
    colors = get_colors()

    return f"""
    QCheckBox {{
        color: {colors["fg"]};
        spacing: 10px;
        font-size: {STYLE_TOKENS["typography"]["size_base"]}pt;
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 1px solid {colors["border"]};
        border-radius: {STYLE_TOKENS["shapes"]["radius_small"]}px;
        background: transparent;
    }}
    QCheckBox::indicator:checked {{
        background: {colors["neon"]};
        border-color: {colors["neon"]};
    }}
    QCheckBox::indicator:hover {{
        border-color: {colors["neon"]};
    }}
    QCheckBox:disabled {{
        color: {colors["fg_secondary"]};
    }}
    QCheckBox:disabled::indicator {{
        background: {colors["disabled"]};
        border-color: {colors["disabled"]};
    }}
    """


def get_progressbar_style(theme_name=None):
    """获取进度条样式 - Neon Minimal 简洁风格"""
    if theme_name:
        set_theme(theme_name)
    colors = get_colors()

    return f"""
    QProgressBar {{
        border: 1px solid {colors["border"]};
        border-radius: {STYLE_TOKENS["shapes"]["radius_small"]}px;
        background: {colors["bg"]};
        text-align: center;
        color: {colors["fg"]};
        font-size: {STYLE_TOKENS["typography"]["size_small"]}pt;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
            stop:0 {colors["neon"]},
            stop:1 {colors["neon_alt"]});
        border-radius: {STYLE_TOKENS["shapes"]["radius_small"]}px;
    }}
    """


def get_scrollbar_style(theme_name=None):
    """获取滚动条样式 - Neon Minimal 简洁风格"""
    if theme_name:
        set_theme(theme_name)
    colors = get_colors()

    return f"""
    QScrollBar:vertical {{
        width: 8px;
        background: transparent;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {colors["border"]};
        border-radius: 4px;
        min-height: 40px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {colors["neon"]};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}
    QScrollBar:horizontal {{
        height: 8px;
        background: transparent;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal {{
        background: {colors["border"]};
        border-radius: 4px;
        min-width: 40px;
        margin: 2px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {colors["neon"]};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}
    """


def get_combobox_style(theme_name=None):
    """获取下拉框样式 - Neon Minimal 简洁风格"""
    if theme_name:
        set_theme(theme_name)
    colors = get_colors()
    fonts = get_fonts()

    return f"""
    QComboBox {{
        background: {colors["bg"]};
        color: {colors["fg"]};
        border: 1px solid {colors["border"]};
        border-radius: {STYLE_TOKENS["shapes"]["radius_small"]}px;
        padding: 6px 10px;
        font-family: {fonts["family"]};
        font-size: {fonts["size_pt"]}pt;
    }}
    QComboBox:hover {{
        border-color: {colors["neon"]};
    }}
    QComboBox:focus {{
        border-color: {colors["border_focus"]};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 6px solid {colors["fg_secondary"]};
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background: {colors["panel"]};
        color: {colors["fg"]};
        selection-background: {colors["neon"]};
        selection-color: {colors["bg"]};
        border: 1px solid {colors["border"]};
        border-radius: {STYLE_TOKENS["shapes"]["radius_small"]}px;
        padding: 4px;
    }}
    QComboBox QAbstractItemView::item {{
        padding: 6px 8px;
        border-radius: 2px;
    }}
    QComboBox QAbstractItemView::item:hover {{
        background: {colors["hover"]};
    }}
    """


# ==================== 导出 ====================

__all__ = [
    "STYLE_TOKENS",
    "NEON_COLORS",
    "FONTS",
    "get_colors",
    "get_fonts",
    "set_theme",
    "get_theme_name",
    "get_all_theme_names",
    "THEMES",
    "NeonMinimalTheme",
    "NeonDarkTheme",
    "NeonLightTheme",
    "CyberpunkTheme",
    "glow",
    "glow_pulse",
    "fade_in",
    "fade_out",
    "apply_neon_theme",
    "get_button_style",
    "get_input_style",
    "get_slider_style",
    "get_checkbox_style",
    "get_progressbar_style",
    "get_scrollbar_style",
    "get_combobox_style",
]
