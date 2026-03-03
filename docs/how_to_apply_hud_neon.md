快速应用 HUD Neon 设计系统
- 现有组件：顶栏、主区域、控件、滚动条等
- 入口：backend/gui/design_system.py 提供 apply_neon_theme 和 glow
- 现有接入：backend/gui/chatboard/chat_board_window.py 调用 apply_neon_theme
- 步骤：1) 引入设计系统；2) 在窗口初始化阶段应用 neon 主题；3) 逐步对控件替换为 tokens 驱动的样式。
