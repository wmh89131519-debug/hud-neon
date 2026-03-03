"""
DesignPreview - HUD Neon 风格预览面板 (Neon Minimal 方向)
用于快速预览和对比不同UI组件的风格效果，支持主题切换
方向A: 简洁线条、干净对比、淡入淡出动画
"""

import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
    QCheckBox,
    QTextEdit,
    QFrame,
    QScrollArea,
    QComboBox,
    QTabWidget,
    QGridLayout,
    QGroupBox,
    QRadioButton,
    QLineEdit,
    QSpinBox,
    QDial,
    QProgressBar,
    QListWidget,
)
from PyQt6.QtCore import Qt, QTimer

# 导入设计系统
from gui.design_system import (
    STYLE_TOKENS,
    get_colors,
    get_fonts,
    set_theme,
    get_theme_name,
    get_all_theme_names,
    THEMES,
    NeonMinimalTheme,
    glow,
    glow_pulse,
    fade_in,
    fade_out,
    get_button_style,
    get_input_style,
    get_slider_style,
    get_checkbox_style,
    get_progressbar_style,
    get_scrollbar_style,
    get_combobox_style,
)


class ComponentShowcase(QFrame):
    """单个组件展示卡片"""

    def __init__(self, title: str, widget, parent=None):
        super().__init__(parent)
        self.setObjectName("componentCard")
        self._setup_ui(title, widget)

    def _setup_ui(self, title: str, widget):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        title_label = QLabel(title)
        colors = get_colors()
        title_label.setStyleSheet(
            f"color: {colors['neon']}; font-weight: bold; font-size: 11pt;"
        )

        layout.addWidget(title_label)
        layout.addWidget(widget)


class DesignPreviewWindow(QWidget):
    """HUD Neon 设计预览主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Design Preview - Neon Minimal Theme")
        self.resize(1000, 800)
        self._setup_ui()
        self._apply_theme("neon_minimal")

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)

        # 标题
        title = QLabel("Neon Minimal 设计系统预览")
        colors = get_colors()
        title.setStyleSheet(
            f"color: {colors['neon']}; font-size: 20pt; font-weight: bold;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # 副标题
        subtitle = QLabel("简洁线条 · 干净对比 · 淡入淡出动画")
        subtitle.setStyleSheet(f"color: {colors['fg_secondary']}; font-size: 11pt;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)

        # 主题选择器
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("选择主题:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(get_all_theme_names())
        # 默认选择 neon_minimal
        self.theme_combo.setCurrentText("neon_minimal")
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        theme_row.addWidget(self.theme_combo)
        theme_row.addStretch()
        main_layout.addLayout(theme_row)

        # Tab控件
        tabs = QTabWidget()

        # Tab 1: 基础组件
        tabs.addTab(self._create_basic_tab(), "基础组件")

        # Tab 2: 按钮
        tabs.addTab(self._create_buttons_tab(), "按钮")

        # Tab 3: 输入控件
        tabs.addTab(self._create_inputs_tab(), "输入控件")

        # Tab 4: 颜色方案
        tabs.addTab(self._create_colors_tab(), "颜色方案")

        # Tab 5: 动画效果
        tabs.addTab(self._create_animation_tab(), "动画效果")

        main_layout.addWidget(tabs)

        # 底部信息
        colors = get_colors()
        info = QLabel("点击组件查看效果变化 | 使用上方下拉框切换主题")
        info.setStyleSheet(f"color: {colors['neon_alt']}; font-size: 9pt;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(info)

    def _on_theme_changed(self, theme_name):
        """主题切换"""
        self._apply_theme(theme_name)

    def _apply_theme(self, theme_name):
        """应用主题"""
        set_theme(theme_name)
        colors = get_colors()
        fonts = get_fonts()

        # 更新窗口整体样式
        self.setStyleSheet(f"""
            QWidget {{
                background: {colors["bg"]};
                color: {colors["fg"]};
                font-family: {fonts["family"]};
                font-size: {fonts["size_pt"]}pt;
            }}
        """)

        # 刷新所有tab
        self._refresh_tabs()

    def _refresh_tabs(self):
        """刷新所有Tab内容 - 重建整个UI"""
        # 删除旧窗口内容重建
        self._setup_ui()

    def _create_basic_tab(self) -> QScrollArea:
        """创建基础组件Tab"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)

        colors = get_colors()

        # 标签
        layout.addWidget(QLabel("标签 (QLabel)"))
        label = QLabel("这是 HUD Neon 风格的标签文本")
        label.setStyleSheet(f"color: {colors['fg']}; font-size: 12pt;")
        layout.addWidget(label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"color: {colors['neon']};")
        layout.addWidget(line)

        # 复选框
        layout.addWidget(QLabel("复选框 (QCheckBox)"))
        for i, text in enumerate(["选项一", "选项二", "选项三"]):
            chk = QCheckBox(text)
            chk.setStyleSheet(get_checkbox_style())
            layout.addWidget(chk)

        # 单选框
        layout.addWidget(QLabel("单选框 (QRadioButton)"))
        for i, text in enumerate(["Radio A", "Radio B", "Radio C"]):
            radio = QRadioButton(text)
            radio.setStyleSheet(f"color: {colors['fg']};")
            layout.addWidget(radio)

        # 进度条
        layout.addWidget(QLabel("进度条 (QProgressBar)"))
        progress = QProgressBar()
        progress.setValue(65)
        progress.setStyleSheet(get_progressbar_style())
        layout.addWidget(progress)
        glow(progress, blur_radius=8)

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setStyleSheet(get_scrollbar_style())
        scroll.setWidgetResizable(True)
        return scroll

    def _create_buttons_tab(self) -> QScrollArea:
        """创建按钮Tab"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)

        # 普通按钮
        layout.addWidget(QLabel("普通按钮 (QPushButton)"))
        btn_normal = QPushButton("点击我")
        btn_normal.setStyleSheet(get_button_style("normal"))
        layout.addWidget(btn_normal)

        # 发光按钮
        btn_glow = QPushButton("发光按钮")
        btn_glow.setStyleSheet(get_button_style("glow"))
        layout.addWidget(btn_glow)
        glow(btn_glow, blur_radius=15)

        # 图标按钮
        btn_icon = QPushButton("🔔 图标按钮")
        btn_icon.setStyleSheet(get_button_style("icon"))
        layout.addWidget(btn_icon)

        # 切换按钮
        btn_toggle = QPushButton("切换按钮")
        btn_toggle.setCheckable(True)
        btn_toggle.setStyleSheet(get_button_style("glow"))
        layout.addWidget(btn_toggle)

        # 按钮组
        layout.addWidget(QLabel("按钮组"))
        btn_group = QGroupBox()
        btn_group_layout = QHBoxLayout()
        for i in range(3):
            btn = QPushButton(f"按钮 {i + 1}")
            btn.setStyleSheet(get_button_style("normal"))
            btn_group_layout.addWidget(btn)
        btn_group_layout.addStretch()
        btn_group.setLayout(btn_group_layout)
        layout.addWidget(btn_group)

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setStyleSheet(get_scrollbar_style())
        scroll.setWidgetResizable(True)
        return scroll

    def _create_inputs_tab(self) -> QScrollArea:
        """创建输入控件Tab"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)

        # 单行输入框
        layout.addWidget(QLabel("单行输入框 (QLineEdit)"))
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("请输入文本...")
        line_edit.setStyleSheet(get_input_style())
        layout.addWidget(line_edit)

        # 数字输入框
        layout.addWidget(QLabel("数字输入框 (QSpinBox)"))
        spin = QSpinBox()
        spin.setValue(50)
        spin.setStyleSheet(get_input_style())
        layout.addWidget(spin)

        # 滑块
        layout.addWidget(QLabel("滑块 (QSlider)"))
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(60)
        slider.setStyleSheet(get_slider_style())
        layout.addWidget(slider)

        # 旋钮
        layout.addWidget(QLabel("旋钮 (QDial)"))
        dial = QDial()
        dial.setValue(50)
        dial.setStyleSheet(f"""
            QDial {{
                background: {get_colors()["bg"]};
                border: 1px solid {get_colors()["border"]};
                border-radius: 40px;
            }}
        """)
        layout.addWidget(dial)

        # 下拉框
        layout.addWidget(QLabel("下拉框 (QComboBox)"))
        combo = QComboBox()
        combo.addItems(["选项 A", "选项 B", "选项 C"])
        combo.setStyleSheet(get_combobox_style())
        layout.addWidget(combo)

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setStyleSheet(get_scrollbar_style())
        scroll.setWidgetResizable(True)
        return scroll

    def _create_colors_tab(self) -> QScrollArea:
        """创建颜色方案Tab"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)

        colors = get_colors()
        fonts = get_fonts()
        theme_name = get_theme_name()

        # 主题信息
        theme_desc = {
            "neon_minimal": "Neon Minimal - 简洁线条、干净对比、淡入淡出动画",
            "neon_dark": "Neon Dark - 深色霓虹风格",
            "neon_light": "Neon Light - 浅色霓虹风格",
            "cyberpunk": "Cyberpunk - 赛博朋克风格",
        }
        layout.addWidget(QLabel(f"当前主题: {theme_desc.get(theme_name, theme_name)}"))
        layout.addWidget(QLabel(""))

        # 主色调展示
        layout.addWidget(QLabel("主色调"))
        main_colors_row = QHBoxLayout()
        for color_name in ["neon", "neon_alt", "bg"]:
            color_box = QFrame()
            color_box.setFixedSize(80, 50)
            color_box.setStyleSheet(
                f"background: {colors[color_name]}; border: 1px solid {colors['border']}; border-radius: 4px;"
            )
            main_colors_row.addWidget(color_box)
        main_colors_row.addStretch()
        layout.addLayout(main_colors_row)

        # 显示颜色令牌
        layout.addWidget(QLabel("颜色令牌 (Color Tokens)"))
        for name, color in colors.items():
            row = QHBoxLayout()
            color_box = QFrame()
            color_box.setFixedSize(60, 30)
            color_box.setStyleSheet(
                f"background: {color}; border: 1px solid {colors['border']}; border-radius: 2px;"
            )
            label = QLabel(f"{name}: {color}")
            label.setStyleSheet(f"color: {colors['fg']}; font-size: 9pt;")
            row.addWidget(color_box)
            row.addWidget(label)
            row.addStretch()
            layout.addLayout(row)

        # 字体信息
        layout.addWidget(QLabel("字体设置"))
        font_label = QLabel(
            f"字体: {fonts['family']}\n字号: {fonts['size_pt']}pt | 行高: {fonts.get('line_height', 'N/A')}"
        )
        font_label.setStyleSheet(f"color: {colors['fg']};")
        layout.addWidget(font_label)

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setStyleSheet(get_scrollbar_style())
        scroll.setWidgetResizable(True)
        return scroll

    def _create_animation_tab(self) -> QScrollArea:
        """创建动画效果Tab"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)

        colors = get_colors()

        # 脉冲发光按钮
        layout.addWidget(QLabel("脉冲发光按钮 (点击测试动画)"))
        pulse_btn = QPushButton("脉冲发光")
        pulse_btn.setStyleSheet(get_button_style("glow"))
        pulse_btn.clicked.connect(
            lambda: glow_pulse(pulse_btn, min_blur=10, max_blur=20, duration=2000)
        )
        layout.addWidget(pulse_btn)

        # 静态发光
        layout.addWidget(QLabel("静态发光"))
        static_glow = QPushButton("静态发光")
        static_glow.setStyleSheet(get_button_style("glow"))
        layout.addWidget(static_glow)
        glow(static_glow, blur_radius=20)

        # 进度条动画
        layout.addWidget(QLabel("进度条动画"))
        anim_progress = QProgressBar()
        anim_progress.setStyleSheet(get_progressbar_style())
        layout.addWidget(anim_progress)

        # 模拟进度动画
        self.anim_progress = anim_progress
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._update_progress)
        self.anim_progress_val = 0
        self.anim_timer.start(50)

        layout.addWidget(QLabel("提示: 点击脉冲发光按钮查看动画效果"))

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setStyleSheet(get_scrollbar_style())
        scroll.setWidgetResizable(True)
        return scroll

    def _update_progress(self):
        """更新进度条动画"""
        self.anim_progress_val = (self.anim_progress_val + 1) % 100
        self.anim_progress.setValue(self.anim_progress_val)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 创建预览窗口
    window = DesignPreviewWindow()
    window.show()

    print("=" * 50)
    print("Design Preview - HUD Neon Style (增强版)")
    print("  - 多种主题切换: neon_dark, neon_light, cyberpunk")
    print("  - 完整控件样式预览")
    print("  - 动画效果展示")
    print("=" * 50)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
