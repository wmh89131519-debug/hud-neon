# PR Draft: Neon Minimal Theme

## Title
Neon Minimal Theme: Tokens, NeonMinimalTheme and Initial DesignPreview Integration

---

## Summary
- 引入风格令牌 STYLE_TOKENS
- 新增 NeonMinimalTheme，作为 Neon 系列的默认简洁主题
- 简化并统一样式生成器，使按钮/输入/滑块/下拉等控件呈现更加干净、易读
- 改善淡入淡出和发光动画的可用性，提供 fade_in、fade_out、glow、glow_pulse
- DesignPreview 增加 Neon Minimal 演示用例，便于对比
- 更新文档 docs/design_system_neon.md，新增 Neon Minimal 区段

---

## Changes

### design_system.py
- 新增 STYLE_TOKENS（颜色、字体、圆角、动画等风格令牌）
- 新增 NeonMinimalTheme，并在 THEMES 中注册 neon_minimal
- 调整/扩展 glow、glow_pulse、fade_in、fade_out 等动画工具
- 统一并简化按钮、输入、滑块、下拉、复选框、进度条、滚动条等控件的样式生成逻辑
- 导出增强：NeonMinimalTheme、STYLE_TOKENS 等符号

### design_preview.py
- 适配 Neon Minimal，新增演示用例
- 修复主题切换时 refresh 的兼容性问题

### chat_board_window.py
- glow 调用改为使用 blur_radius 参数名

### docs/design_system_neon.md
- 新增 Neon Minimal 区段，包含风格令牌、颜色/字体规范、使用示例

---

## How to Test
1. 运行 DesignPreview：
   ```bash
   cd backend
   ../.venv/Scripts/python.exe -m gui.design_preview
   ```
2. 在主题选择器中选择 "neon_minimal"
3. 验证核心控件样式：
   - 按钮 (QPushButton)
   - 输入框 (QLineEdit)
   - 滑块 (QSlider)
   - 下拉框 (QComboBox)
   - 复选框 (QCheckBox)
   - 进度条 (QProgressBar)
   - 滚动条 (QScrollBar)
4. 测试动画效果：点击"脉冲发光"按钮查看 glow_pulse 动画

---

## Notes
- Neon Minimal 定位：简洁线条、干净对比、淡入淡出动画、强调可读性
- 适合长时间使用的工作场景
- 未来可扩展：对比度切换、统一字体排版、图标风格规范
