# Design System: HUD Neon

## 概述

**方向A: Neon Minimal** - 简洁线条、干净对比、淡入淡出动画，强调信息密度与可读性，适合实际工作场景的长期使用。

---

## 核心原则

1. **简洁线条** - 减少不必要的装饰元素
2. **干净对比** - 高对比度确保可读性
3. **柔和动画** - 淡入淡出，不过度刺激眼睛
4. **信息密度** - 适合长时间使用的舒适感

---

## 风格令牌 (Style Tokens)

```python
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
```

---

## 主题: Neon Minimal (默认)

Neon Minimal 是默认主题，专为长时间使用的工作场景设计。

### 颜色规范

| 键名 | 值 | 用途 |
|------|-----|------|
| `bg` | `#0E141C` | 窗口/背景 |
| `panel` | `#151D26` | 面板/卡片 |
| `fg` | `#E8EDF2` | 主文本 |
| `fg_secondary` | `#8A9BAC` | 次要文本 |
| `neon` | `#00C8D8` | 主强调色 (青色) |
| `neon_alt` | `#00E58E` | 次强调色 (绿色) |
| `neon_subtle` | `#1A3A42` | 柔和发光 |
| `border` | `#2A3A46` | 边框 |
| `border_focus` | `#00C8D8` | 聚焦边框 |
| `hover` | `rgba(0, 200, 216, 0.12)` | 悬停背景 |
| `active` | `rgba(0, 200, 216, 0.2)` | 激活背景 |
| `disabled` | `#3A4A56` | 禁用状态 |
| `error` | `#FF5252` | 错误 |
| `success` | `#00E58E` | 成功 |
| `warning` | `#FFB74D` | 警告 |

### 字体规范

```python
FONTS = {
    "family": '"Inter", "Microsoft YaHei", "Segoe UI", sans-serif',
    "size_pt": 10,
    "size_small": 8,
    "size_large": 14,
    "size_title": 18,
    "line_height": 1.5,
}
```

---

## 可用主题

| 主题名 | 描述 |
|--------|------|
| `neon_minimal` | **默认** - 简洁线条、干净对比 |
| `neon_dark` | 深色霓虹 |
| `neon_light` | 浅色霓虹 |
| `cyberpunk` | 赛博朋克风格 |

---

## 组件样式

### 按钮 (QPushButton)

```python
get_button_style("normal")   # 普通按钮
get_button_style("glow")     # 发光按钮
get_button_style("icon")     # 图标按钮
```

特点：
- 简洁边框设计
- 悬停时边框和文字变为强调色
- 支持三种类型

### 输入框 (QLineEdit, QSpinBox, QTextEdit)

```python
get_input_style()
```

特点：
- 简洁边框
- 聚焦时边框变为主强调色
- 悬停时边框微微发光

### 滑块 (QSlider)

```python
get_slider_style()
```

特点：
- 简洁轨道设计
- 渐变填充进度部分
- 圆形把手

### 复选框/单选框

```python
get_checkbox_style()
```

特点：
- 简洁方形指示器
- 选中状态填充强调色

### 滚动条 (QScrollBar)

```python
get_scrollbar_style()
```

特点：
- 细窄设计
- 悬停时高亮
- 不干扰内容阅读

### 下拉框 (QComboBox)

```python
get_combobox_style()
```

特点：
- 简洁下拉箭头
- 下拉列表带圆角和悬停效果

### 进度条 (QProgressBar)

```python
get_progressbar_style()
```

特点：
- 渐变填充
- 简洁边框

---

## 动画效果

### 静态发光

```python
from gui.design_system import glow

glow(widget, blur_radius=14)
```

### 脉冲发光

```python
from gui.design_system import glow_pulse

glow_pulse(widget, min_blur=8, max_blur=20, duration=1500)
```

### 淡入

```python
from gui.design_system import fade_in

fade_in(widget, duration=250)
```

### 淡出

```python
from gui.design_system import fade_out

fade_out(widget, duration=250)
```

---

## 使用方法

### 应用主题

```python
from gui.design_system import set_theme, apply_neon_theme

# 切换到 Neon Minimal
set_theme("neon_minimal")

# 应用到控件
apply_neon_theme(window)
```

### 应用组件样式

```python
from gui.design_system import (
    get_button_style,
    get_input_style,
    get_slider_style,
    get_checkbox_style,
    get_progressbar_style,
    get_scrollbar_style,
    get_combobox_style,
)

button.setStyleSheet(get_button_style("normal"))
input.setStyleSheet(get_input_style())
slider.setStyleSheet(get_slider_style())
```

### 主题预览

```bash
cd backend
../.venv/Scripts/python.exe -m gui.design_preview
```

---

## 设计对比

### Neon Minimal vs 其他主题

| 特性 | Neon Minimal | Neon Dark | Neon Light | Cyberpunk |
|------|--------------|-----------|------------|-----------|
| 对比度 | 高 | 中 | 高 | 中 |
| 边框 | 简洁 | 明显 | 简洁 | 明显 |
| 发光 | 柔和 | 强烈 | 柔和 | 强烈 |
| 动画 | 淡入淡出 | 脉冲 | 淡入淡出 | 脉冲 |
| 适用场景 | 长时间工作 | 夜间使用 | 白天使用 | 展示/娱乐 |

---

## 可访问性建议

1. **对比度** - Neon Minimal 使用高对比度配色，确保文本可读性
2. **字体大小** - 基础字号 10pt，建议不要小于 8pt
3. **动画控制** - 动画时长默认 250ms，避免过慢
4. **禁用状态** - 使用明显的禁用样式（降低对比度）

---

## 扩展建议

1. **图标规范** - 统一线宽、风格
2. **间距令牌** - 添加 spacing/margin tokens
3. **动画预设** - 预定义常用动画组合
4. **高对比模式** - 为视力障碍用户提供更高对比度选项

---

## 测试清单

- [ ] 主题切换到 neon_minimal
- [ ] 按钮样式正确渲染
- [ ] 输入框聚焦/悬停效果
- [ ] 滑块渐变填充
- [ ] 复选框选中状态
- [ ] 下拉框下拉列表
- [ ] 滚动条悬停效果
- [ ] 进度条渐变
- [ ] glow 动画
- [ ] glow_pulse 动画
- [ ] fade_in/fade_out 动画

---

## 更新日志

### 2026-03-03
- 新增 Neon Minimal 主题
- 引入 STYLE_TOKENS
- 添加 fade_in/fade_out 动画
- 简化组件样式生成器
