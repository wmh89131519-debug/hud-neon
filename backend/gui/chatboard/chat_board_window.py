"""
ChatBoard 主窗口：无边框、顶部标题栏 + 三栏布局 + 底部控制栏。
"""

import os

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtWidgets import QStyle
from PyQt6.QtCore import Qt, QPoint, QRect, QSize, QTimer
from PyQt6.QtGui import QColor
from enum import Enum

from .widgets import SidebarSettings, ParticipantsPanel, ConversationView, ControlBar
from .design_system import apply_neon_theme, glow
from .input import InputBar


# 底板边缘拖动调整窗口大小时的热区宽度（像素）
EDGE_RESIZE_WIDTH = 8


class EdgeKind(Enum):
    LEFT = "left"
    RIGHT = "right"
    BOTTOM = "bottom"


class EdgeResizeStrip(QWidget):
    """
    底板左/右/底边缘条带：悬停显示调整光标，拖动时调整窗口大小。
    父控件为 mainContainer，几何在 ChatBoardWindow.resizeEvent 中更新。
    """

    def __init__(self, edge_kind: EdgeKind, parent: QWidget):
        super().__init__(parent)
        self._edge_kind = edge_kind
        self._resize_start_geometry: QRect | None = None
        self._resize_start_global: QPoint | None = None
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setCursor(self._cursor_for_edge())

    def _cursor_for_edge(self):
        if self._edge_kind == EdgeKind.BOTTOM:
            return Qt.CursorShape.SizeVerCursor
        return Qt.CursorShape.SizeHorCursor

    def enterEvent(self, event):
        self.setCursor(self._cursor_for_edge())
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._resize_start_global is None:
            self.unsetCursor()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            return
        win = self.window()
        if not win or win.isMaximized():
            super().mousePressEvent(event)
            return
        self._resize_start_geometry = win.frameGeometry()
        self._resize_start_global = event.globalPosition().toPoint()
        self.grabMouse()

    def mouseMoveEvent(self, event):
        if self._resize_start_geometry is None or self._resize_start_global is None:
            super().mouseMoveEvent(event)
            return
        win = self.window()
        if not win:
            super().mouseMoveEvent(event)
            return
        g = event.globalPosition().toPoint()
        r = self._resize_start_geometry
        min_w, min_h = win.minimumWidth(), win.minimumHeight()
        if self._edge_kind == EdgeKind.LEFT:
            dx = g.x() - self._resize_start_global.x()
            new_w = r.width() - dx
            new_w = max(min_w, new_w)
            new_left = r.right() - new_w
            win.setGeometry(new_left, r.top(), new_w, r.height())
        elif self._edge_kind == EdgeKind.RIGHT:
            dx = g.x() - self._resize_start_global.x()
            new_w = max(min_w, r.width() + dx)
            win.setGeometry(r.left(), r.top(), new_w, r.height())
        elif self._edge_kind == EdgeKind.BOTTOM:
            dy = g.y() - self._resize_start_global.y()
            new_h = max(min_h, r.height() + dy)
            win.setGeometry(r.left(), r.top(), r.width(), new_h)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._resize_start_geometry = None
            self._resize_start_global = None
            self.releaseMouse()
        super().mouseReleaseEvent(event)


class TitleBar(QFrame):
    """顶部栏：左侧品牌 + 语言徽标，右侧窗口控制。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start = None
        self.setFixedHeight(32)
        self.setObjectName("titleBar")
        self.setAutoFillBackground(True)

        # 创建主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建标题功能块容器
        self._title_block = QFrame()
        self._title_block.setObjectName("titleBlock")  # 设置对象名称以应用样式
        self._title_block.setAutoFillBackground(True)

        # 功能块内部布局
        layout = QHBoxLayout(self._title_block)
        layout.setContentsMargins(12, 0, 8, 0)
        layout.setSpacing(8)

        # 左侧：LOGO（动态地球）+ 品牌名 VOXSWAP
        self._globe = QLabel("🌐")
        self._globe.setObjectName("logoGlobe")
        self._title = QLabel(" VOXSWAP")
        # LOGO 文字颜色改为与右上角窗口控制按钮一致的绿色 #00e58e
        self._title.setStyleSheet("color: #00e58e; font-size: 12pt; font-weight: bold;")
        self._title.setCursor(Qt.CursorShape.SizeAllCursor)
        layout.addWidget(self._globe)
        layout.addWidget(self._title)

        # 语言徽标已移除，保持界面简洁，后续可用设计系统徽标替代

        layout.addStretch()

        # 中间：显示模式切换（完整 <-> 精简） – 图标化按钮
        self._btn_compact = QPushButton()
        self._btn_compact.setObjectName("compactToggle")
        self._btn_compact.setCheckable(True)
        self._btn_compact.setChecked(False)
        self._btn_compact.setToolTip(
            "切换显示模式：精简模式将隐藏左侧栏与成员栏，并调整为竖屏比例。"
        )
        self._btn_compact.setText("")  # 不显示文本
        self._btn_compact.setIcon(
            self._btn_compact.style().standardIcon(
                QStyle.StandardPixmap.SP_TitleBarMenuButton
            )
        )
        self._btn_compact.toggled.connect(self._on_compact_toggled)
        layout.addWidget(self._btn_compact)

        layout.addStretch()

        # 右侧：窗口控制 顶置、最小化、最大化、关闭
        self._btn_pin = QPushButton("📌")
        self._btn_pin.setCheckable(True)
        self._btn_pin.setToolTip("顶置窗口")
        self._btn_pin.setFixedSize(28, 24)
        layout.addWidget(self._btn_pin)

        self._btn_min = QPushButton("−")
        self._btn_min.setToolTip("最小化")
        self._btn_min.setFixedSize(28, 24)
        self._btn_min.clicked.connect(self._on_minimize)
        layout.addWidget(self._btn_min)

        self._btn_max = QPushButton("□")
        self._btn_max.setCheckable(True)
        self._btn_max.setToolTip("最大化/还原")
        self._btn_max.setFixedSize(28, 24)
        self._btn_max.clicked.connect(self._on_toggle_max)
        layout.addWidget(self._btn_max)

        self._btn_close = QPushButton("×")
        self._btn_close.setToolTip("关闭")
        self._btn_close.setFixedSize(28, 24)
        self._btn_close.clicked.connect(self._on_close)
        layout.addWidget(self._btn_close)

        # 将功能块添加到主布局
        main_layout.addWidget(self._title_block)

        # 图钉初始为"未顶置"（倾斜），并启动 LOGO 旋转动画
        self._update_pin_icon(False)
        self._init_globe_animation()

    # ------- 公共接口 -------
    def set_language(self, text: str):
        # 语言徽标已移除，保持接口不抛错，未来可通过设计系统实现语言切换指示
        pass

    def set_pinned(self, on: bool):
        self._btn_pin.setChecked(on)
        self._update_pin_icon(on)

    # ------- 内部事件 -------
    def _on_minimize(self):
        w = self.window()
        if w:
            w.showMinimized()

    def _on_toggle_max(self):
        w = self.window()
        if not w:
            return
        if w.isMaximized():
            w.showNormal()
            self._btn_max.setChecked(False)
        else:
            w.showMaximized()
            self._btn_max.setChecked(True)

    def _on_close(self):
        w = self.window()
        if w:
            w.close()

    def _on_compact_toggled(self, on: bool):
        # 更新按钮文案
        self._btn_compact.setText("完整模式" if on else "精简模式")
        w = self.window()
        if w and hasattr(w, "set_compact_mode"):
            w.set_compact_mode(on)

    # ------- 辅助方法 -------
    def _update_pin_icon(self, pinned: bool):
        """根据是否顶置更新图钉形态：未顶置=倾斜📌，顶置=竖直📍。"""
        self._btn_pin.setText("📍" if pinned else "📌")

    def _init_globe_animation(self):
        """使用定时器在几种地球符号之间切换，营造旋转感。"""
        self._globe_frames = ["🌍", "🌎", "🌏", "🌍"]
        self._globe_index = 0
        self._globe_timer = QTimer(self)
        self._globe_timer.timeout.connect(self._tick_globe)
        self._globe_timer.start(500)

    def _tick_globe(self):
        if not hasattr(self, "_globe_frames"):
            return
        self._globe_index = (self._globe_index + 1) % len(self._globe_frames)
        self._globe.setText(self._globe_frames[self._globe_index])

    def _is_on_button(self, pos: QPoint) -> bool:
        child = self.childAt(pos)
        while child:
            if isinstance(child, QPushButton):
                # 检查按钮是否包含点击位置
                button_pos = child.mapFrom(self, pos)
                if child.rect().contains(button_pos):
                    return True
            child = child.parentWidget()
        return False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self._is_on_button(
            event.pos()
        ):
            # 记录拖动起点，用于移动窗口
            self._drag_start = (
                event.globalPosition().toPoint()
                - self.window().frameGeometry().topLeft()
            )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_start is not None:
            self.window().move(event.globalPosition().toPoint() - self._drag_start)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = None
        super().mouseReleaseEvent(event)


class ChatBoardWindow(QWidget):
    """会话板块主窗口：可拖动、半透明、可顶置"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("会话板块")
        self.setMinimumSize(640, 560)  # 最小宽度约比原 800 缩减 20%
        self.resize(1000, 640)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.WindowMinMaxButtonsHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # 精简模式状态与还原用快照
        self._compact_mode = False
        self._compact_restore_geometry: QRect | None = None
        self._compact_restore_min_size: QSize | None = None
        self._compact_restore_max_size: QSize | None = None
        self._compact_restore_splitter_sizes: list[int] | None = None
        self._compact_restore_handle_width: int | None = None

        self._setup_ui()
        # 背景不透明度百分比，仅作用于各个容器背景，不影响文字和图标
        self._opacity_percent = 100
        self._title_bar.set_language("EN")

    def _setup_ui(self):
        # 1. 顶层透明壳 (不可见)
        #    - 使用QWidget作为根容器
        #    - 无边框、无背景色
        #    - 透明背景，用于接收鼠标事件

        # 2. 根布局 (QVBoxLayout) - [Margins: 0, Spacing: 0]
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)  # 无边距
        root_layout.setSpacing(0)  # 无间距

        # 3. 实体底板 (MainContainer - QFrame)
        #    - 作为所有内容的容器
        #    - 设置样式：背景色、圆角、边框、拦截鼠标
        #    - 用于控制整个界面的视觉效果和交互
        self._main_container = QFrame(self)
        self._main_container.setObjectName("mainContainer")

        # 4. 内容布局 (content_layout - QVBoxLayout) - [Margins: 4, Spacing: 8]
        content_layout = QVBoxLayout(self._main_container)
        content_layout.setContentsMargins(0, 0, 0, 0)  # 移除内部边距
        content_layout.setSpacing(0)  # 移除内部间距

        # 5. 创建大容器来包含所有板块
        self._main_content_container = QFrame(self._main_container)
        self._main_content_container.setObjectName("mainContentContainer")

        # 5.1 大容器内部布局
        main_content_layout = QVBoxLayout(self._main_content_container)
        # 容器内部各板块之间统一 2 像素间距
        main_content_layout.setContentsMargins(2, 2, 2, 2)
        main_content_layout.setSpacing(2)

        # 6. 顶部标题栏 (TitleBar)
        self._title_bar = TitleBar(self._main_content_container)
        self._title_bar.setFixedHeight(32)
        main_content_layout.addWidget(self._title_bar)

        # 应用 HUD 风格设计系统
        try:
            apply_neon_theme(self)
            # 给关键元素加一点发光，增强科技感
            glow(self._title_bar._title_block, radius=8)
            glow(self._title_bar._globe, radius=4)
            glow(self._title_bar._title, radius=4)
        except Exception:
            pass

        # 7. 核心内容区域：左侧固定侧边栏 + 中间/右侧分割器
        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        # 左侧侧边栏与中间对话区之间的间距为 0 像素，
        # 由各自内部 2 像素的 contentsMargins 来保证容器与容器之间的视觉间距为 2
        content_row.setSpacing(0)

        # 7.1 左侧工具栏 (Sidebar - Card Frame)，直接放在横向布局中，不参与分割拖动
        sidebar_card = QFrame(self._main_content_container)
        self._sidebar_card = sidebar_card
        sidebar_card.setObjectName("sidebarCard")
        sidebar_layout = QVBoxLayout(sidebar_card)
        sidebar_layout.setContentsMargins(2, 2, 2, 2)
        sidebar_layout.setSpacing(0)

        self._sidebar = SidebarSettings(sidebar_card)
        # SidebarSettings 自身内部固定宽度为 50 像素，这里不再二次覆盖
        sidebar_layout.addWidget(self._sidebar)

        # 7.2 中间与右侧使用分割器：聊天区域 + 成员栏
        content_splitter = QSplitter(
            Qt.Orientation.Horizontal, self._main_content_container
        )
        content_splitter.setObjectName("contentSplitter")
        # 左右拖拽条宽度统一为 2 像素（细分隔线）
        content_splitter.setHandleWidth(2)
        # 记录分割器与右侧成员栏宽度限制，用于拖动时约束成员栏最大宽度
        self._content_splitter = content_splitter
        self._participants_min_width = 160
        self._participants_max_width = 360

        # 7.2 聊天区域 (ChatArea - Widget)
        chat_area = QWidget(content_splitter)
        chat_area.setObjectName("chatArea")
        chat_layout = QVBoxLayout(chat_area)
        # 让中间栏容器与左右两侧容器在上下方向对齐：统一 2 像素边距和间距
        chat_layout.setContentsMargins(2, 2, 2, 2)
        chat_layout.setSpacing(2)

        # 创建聊天区域功能块容器（作为对话区整体卡片）
        self._chat_block = QFrame(chat_area)
        self._chat_block.setObjectName("chatBlock")  # 设置对象名称以应用样式
        self._chat_block.setAutoFillBackground(True)

        # 功能块内部布局：使用垂直分割器，让对话区与输入栏可以上下拖动调整比例
        chat_block_layout = QVBoxLayout(self._chat_block)
        chat_block_layout.setContentsMargins(2, 2, 2, 2)
        chat_block_layout.setSpacing(2)

        convo_splitter = QSplitter(Qt.Orientation.Vertical, self._chat_block)
        convo_splitter.setObjectName("convoSplitter")
        convo_splitter.setHandleWidth(4)

        # 7.2.1 消息列表 (ConversationView)
        self._conversation = ConversationView(self._chat_block)
        # 7.2.2 输入栏 (InputBar)
        self._input_bar = InputBar(self._chat_block)
        # 使用最小高度约束，而不是固定高度，方便通过分割条调整
        self._input_bar.setMinimumHeight(100)

        convo_splitter.addWidget(self._conversation)
        convo_splitter.addWidget(self._input_bar)
        convo_splitter.setSizes([400, 140])
        convo_splitter.setCollapsible(0, False)
        convo_splitter.setCollapsible(1, False)

        chat_block_layout.addWidget(convo_splitter)

        # 将功能块添加到聊天区域布局
        chat_layout.addWidget(self._chat_block)

        # 7.3 右侧成员栏 (Participants - Card Frame)
        participants_card = QFrame(content_splitter)
        self._participants_card = participants_card
        participants_card.setObjectName("participantsCard")
        participants_layout = QVBoxLayout(participants_card)
        participants_layout.setContentsMargins(2, 2, 2, 2)
        participants_layout.setSpacing(0)

        self._participants = ParticipantsPanel(participants_card)
        # 成员栏宽度范围由 ParticipantsPanel 的 min/max 控制；
        # 分隔条拖动时通过移动左边界来调节宽度，右侧与外层边框的间距保持不变
        participants_layout.addWidget(self._participants)

        # 将聊天区域和成员栏添加到分割器
        content_splitter.addWidget(chat_area)
        content_splitter.addWidget(participants_card)
        content_splitter.setSizes([700, 180])
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 0)
        content_splitter.setCollapsible(0, False)
        content_splitter.setCollapsible(1, False)
        # 拖动分隔条时，限制右侧成员栏宽度在预设范围内
        content_splitter.splitterMoved.connect(self._on_splitter_moved)

        # 将左侧侧边栏和中/右分割器添加到横向布局
        content_row.addWidget(sidebar_card)
        content_row.addWidget(content_splitter)

        main_content_layout.addLayout(content_row)
        main_content_layout.setStretchFactor(content_row, 1)

        # 8. 底部控制栏 (ControlBar)
        self._control_bar = ControlBar(self._main_content_container)
        self._control_bar.setFixedHeight(60)
        main_content_layout.addWidget(self._control_bar)

        # 顶置联动
        self._title_bar._btn_pin.toggled.connect(self._on_title_pin_toggled)

        # 将大容器添加到主内容布局
        content_layout.addWidget(self._main_content_container)

        # 将实体底板添加到根布局
        root_layout.addWidget(self._main_container)

        # 加载样式
        qss_path = os.path.join(os.path.dirname(__file__), "styles", "chatboard.qss")
        if os.path.isfile(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self._main_container.setStyleSheet(f.read())

        # 9. 底板左/右/底边缘条带：悬停显示调整光标，拖动调整窗口大小
        self._resize_left = EdgeResizeStrip(EdgeKind.LEFT, self._main_container)
        self._resize_right = EdgeResizeStrip(EdgeKind.RIGHT, self._main_container)
        self._resize_bottom = EdgeResizeStrip(EdgeKind.BOTTOM, self._main_container)
        self._resize_left.raise_()
        self._resize_right.raise_()
        self._resize_bottom.raise_()
        self._update_resize_strip_geometry()

    def set_compact_mode(self, on: bool):
        """切换精简模式：隐藏左侧栏与成员栏，并在进入时自动调整竖屏比例。"""
        on = bool(on)
        if on == getattr(self, "_compact_mode", False):
            return

        splitter = getattr(self, "_content_splitter", None)
        sidebar_card = getattr(self, "_sidebar_card", None)
        participants_card = getattr(self, "_participants_card", None)
        if splitter is None or sidebar_card is None or participants_card is None:
            self._compact_mode = on
            return

        if on:
            # 保存快照，供退出精简模式恢复
            self._compact_restore_geometry = self.frameGeometry()
            self._compact_restore_min_size = self.minimumSize()
            self._compact_restore_max_size = self.maximumSize()
            self._compact_restore_splitter_sizes = splitter.sizes()
            self._compact_restore_handle_width = splitter.handleWidth()

            sidebar_card.setVisible(False)
            participants_card.setVisible(False)
            splitter.setHandleWidth(0)
            splitter.setSizes([1, 0])

            # 进入精简模式时，自动调整为更窄的竖屏比例（只做一次）
            # 宽度相对原窗口再缩小约 30%
            target_w, target_h = 300, 780
            screen = self.screen()
            if screen:
                avail = screen.availableGeometry()
                # 预留少量边距，避免贴边
                max_w = max(300, avail.width() - 40)
                max_h = max(400, avail.height() - 40)
                target_w = min(target_w, max_w)
                target_h = min(target_h, max_h)

            # 临时下调最小宽度，便于更窄竖屏
            self.setMinimumSize(target_w, max(self.minimumHeight(), 560))
            self.resize(target_w, target_h)
        else:
            sidebar_card.setVisible(True)
            participants_card.setVisible(True)

            if self._compact_restore_handle_width is not None:
                splitter.setHandleWidth(self._compact_restore_handle_width)
            if self._compact_restore_splitter_sizes:
                splitter.setSizes(self._compact_restore_splitter_sizes)

            if self._compact_restore_min_size is not None:
                self.setMinimumSize(self._compact_restore_min_size)
            if self._compact_restore_max_size is not None:
                self.setMaximumSize(self._compact_restore_max_size)
            if self._compact_restore_geometry is not None:
                self.setGeometry(self._compact_restore_geometry)

        self._compact_mode = on

    def _update_resize_strip_geometry(self):
        """根据底板尺寸更新三条边缘条带在底板内的几何。"""
        w = self._main_container.width()
        h = self._main_container.height()
        ew = EDGE_RESIZE_WIDTH
        self._resize_left.setGeometry(0, 0, ew, h)
        self._resize_right.setGeometry(w - ew, 0, ew, h)
        self._resize_bottom.setGeometry(0, h - ew, w, ew)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_resize_strip_geometry()

    def _setup_drag_region(self):
        """拖拽逻辑完全由 TitleBar 处理，这里留空即可。"""
        pass

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def set_always_on_top(self, on: bool):
        flags = self.windowFlags()
        if on:
            self.setWindowFlags(flags | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()
        self._title_bar.set_pinned(on)

    def _on_title_pin_toggled(self, on: bool):
        self.set_always_on_top(on)

    def set_background_opacity(self, percent: int):
        """
        调整整体窗口的不透明度（恢复为原来的全局效果）。
        """
        self._opacity_percent = max(30, min(100, percent))
        self.setWindowOpacity(self._opacity_percent / 100.0)

    def _on_splitter_moved(self, pos: int, index: int):
        """
        限制右侧成员栏宽度：当拖动分隔条使成员栏达到最大/最小宽度时，
        进一步拖动不再继续改变成员栏宽度，从而实现“拖不动”的效果。
        """
        splitter = getattr(self, "_content_splitter", None)
        if splitter is None:
            return
        sizes = splitter.sizes()
        # 现在分割器只包含 [聊天区域, 成员栏] 两个部分
        if len(sizes) != 2:
            return
        total = sum(sizes)
        min_w = getattr(self, "_participants_min_width", 160)
        max_w = getattr(self, "_participants_max_width", 360)
        right = sizes[1]
        changed = False
        if right < min_w:
            delta = min_w - right
            right = min_w
            sizes[1] = right
            sizes[0] = max(0, sizes[0] - delta)
            changed = True
        elif right > max_w:
            delta = right - max_w
            right = max_w
            sizes[1] = right
            sizes[0] = max(0, sizes[0] + delta)
            changed = True
        if changed:
            # 重新设置尺寸，防止成员栏宽度继续超出限制
            # 保持总宽度不变
            factor = total / max(1, sum(sizes))
            sizes = [int(s * factor) for s in sizes]
            splitter.setSizes(sizes)

    @property
    def sidebar(self):
        return self._sidebar

    @property
    def participants_panel(self):
        return self._participants

    @property
    def conversation_view(self):
        return self._conversation

    @property
    def control_bar(self):
        return self._control_bar
