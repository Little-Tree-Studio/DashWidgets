# =============================================================================
# Copyright (c) 2026 Little Tree Studio
#
# This program and all associated documentation and files are protected by
# the Eclipse Public License 2.0. You may obtain a complete copy of this
# license at:
#
#     https://www.eclipse.org/legal/epl-2.0/
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is provided on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""
File Description
==============================================================================
The main entry point for the DashWidgets application.

@author: Little Tree Studio
@contact: studio@zsxiaoshu.cn
@organization: https://zsxiaoshu.cn/
@project: DashWidgets
@repository: https://github.com/Little-Tree-Studio/DashWidgets
@license: Eclipse Public License 2.0 (EPL-2.0)
@copyright: Copyright (c) 2026 Little Tree Studio. All rights reserved.
"""

# SPDX-License-Identifier: EPL-2.0
# Identifier Note: SPDX (Software Package Data Exchange) license identifier
# for automated license identification tools

# =============================================================================
# Development Team Information
# =============================================================================
# Primary Developer  : Little Tree Studio
# Contact Email      : studio@zsxiaoshu.cn
# Official Website   : https://zsxiaoshu.cn/
# Project Homepage   : https://github.com/Little-Tree-Studio/DashWidgets
# Issue Tracker      : https://github.com/Little-Tree-Studio/DashWidgets/issues
# Documentation      : https://github.com/Little-Tree-Studio/DashWidgets/wiki
#
# Technical Support  : support@zsxiaoshu.cn
# Business Inquiries : business@zsxiaoshu.cn
# =============================================================================

# =============================================================================
# License Compliance Statement
# =============================================================================
# IMPORTANT NOTICE:
# 1. This file is open source software under the Eclipse Public License 2.0
# 2. You may freely use, modify, and distribute this software subject to EPL 2.0 terms
# 3. If you distribute this software as a standalone application, you must
#    release the source code under the same license
# 4. If you link this software as a library/module to your proprietary software,
#    this restriction does not apply
# 5. All modified files must retain this copyright notice and license information
# 6. Distribution must include a means to obtain the complete license text
#
# Full legal terms available at: https://www.eclipse.org/legal/epl-2.0/
# =============================================================================



import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkfont
from loguru import logger
from app.path import LOGO_PATH, FONTS_PATH
import datetime
import random
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import threading

__author__ = "Little Tree Studio"
__copyright__ = "Copyright (c) 2026 Little Tree Studio"
__license__ = "EPL-2.0"
__version__ = "1.0.0"
__maintainer__ = "Little Tree Studio"
__email__ = "studio@zsxiaoshu.cn"
__status__ = "Development"  # Development/Testing/Production
__project__ = "DashWidgets"
__repository__ = "https://github.com/Little-Tree-Studio/DashWidgets"
__website__ = "https://zsxiaoshu.cn/"

# 配置日志系统
log_dir = Path.home() / ".dashwidgets" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logger.add(
    log_dir / "dashwidgets_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="7 days",
    level="INFO",
    encoding="utf-8"
)


class ThemeColors:
    """主题颜色配置 - 现代圆润设计配色"""
    def __init__(self, light_mode=True):
        self.light_mode = light_mode
        self._update_colors()

    def set_light_mode(self, light_mode):
        self.light_mode = light_mode
        self._update_colors()

    def _update_colors(self):
        if self.light_mode:
            # 浅色主题 - 现代柔和配色
            self.bg_main = "#F8FAFC"           # 主背景 - 浅灰蓝
            self.bg_card = "#FFFFFF"          # 卡片背景 - 纯白
            self.bg_nav = "#FFFFFF"           # 导航栏背景 - 纯白
            self.bg_hint = "#F1F5F9"          # 提示框背景 - 浅灰
            self.bg_input = "#F8FAFC"         # 输入框背景
            self.bg_button = "#F1F5F9"        # 按钮背景
            self.text_primary = "#1E293B"     # 主要文字 - 深灰蓝
            self.text_secondary = "#64748B"    # 次要文字 - 灰色
            self.text_hint = "#94A3B8"         # 提示文字 - 浅灰
            self.border = "#E2E8F0"            # 边框颜色 - 浅灰
            self.accent = "#6366F1"            # 强调色 - 靛蓝
            self.hover = "#4F46E5"             # 悬停色 - 深靛蓝
            self.success = "#10B981"           # 成功色 - 绿色
            self.warning = "#F59E0B"           # 警告色 - 橙色
            self.error = "#EF4444"             # 错误色 - 红色
        else:
            # 深色主题 - 现代深色配色
            self.bg_main = "#0F172A"           # 主背景 - 深灰蓝
            self.bg_card = "#1E293B"           # 卡片背景 - 深灰
            self.bg_nav = "#1E293B"            # 导航栏背景 - 深灰
            self.bg_hint = "#334155"           # 提示框背景 - 中灰
            self.bg_input = "#334155"          # 输入框背景 - 中灰
            self.bg_button = "#334155"         # 按钮背景 - 中灰
            self.text_primary = "#F1F5F9"      # 主要文字 - 浅灰
            self.text_secondary = "#94A3B8"    # 次要文字 - 灰色
            self.text_hint = "#64748B"         # 提示文字 - 深灰
            self.border = "#475569"           # 边框颜色 - 中灰
            self.accent = "#818CF8"            # 强调色 - 浅靛蓝
            self.hover = "#6366F1"            # 悬停色 - 靛蓝
            self.success = "#34D399"           # 成功色 - 浅绿
            self.warning = "#FBBF24"           # 警告色 - 浅橙
            self.error = "#F87171"             # 错误色 - 浅红


def load_fonts():
    """加载自定义字体"""
    try:
        ctk.CTkFont("HarmonyOS Sans SC")
        logger.info("Font loaded: HarmonyOS Sans SC Regular")
    except Exception as e:
        logger.warning(f"Font not found, using default font: {e}")


# 全局字体设置
_current_font_family = None

def get_current_font_family():
    """获取当前字体"""
    return _current_font_family

def set_font_family(font_name):
    """设置全局字体"""
    global _current_font_family
    _current_font_family = font_name
    logger.info(f"字体已设置为: {font_name}")

def get_font(size, bold=False):
    """获取字体，支持自定义字体"""
    global _current_font_family

    # 可用字体列表
    font_names = [
        "HarmonyOS Sans SC",
        "HarmonyOS Sans",
        "Microsoft YaHei UI",
        "Microsoft YaHei",
        "SimHei",
        "PingFang SC",
        "STHeiti",
        "Arial"
    ]

    font_family = font_names[0]  # 默认使用华为鸿蒙字体

    # 如果设置了自定义字体，优先使用
    if _current_font_family and _current_font_family != "系统默认":
        font_family = _current_font_family
    else:
        # 尝试找到可用的字体
        available_fonts = tkfont.families()
        for font_name in font_names:
            if font_name in available_fonts:
                font_family = font_name
                break

    weight = "bold" if bold else "normal"
    return (font_family, size, weight)


class WidgetTemplate:
    """组件模板基类"""
    def __init__(self, name, description, icon_name, size="medium"):
        self.name = name
        self.description = description
        self.icon_name = icon_name
        self.size = size  # small, medium, large

    def get_size_dimensions(self):
        """获取组件尺寸"""
        return SIZE_MAP.get(self.size, (200, 200))


# 示例组件模板
WIDGET_TEMPLATES = [
    WidgetTemplate("时钟", "显示当前时间", "🕐", "medium"),
    WidgetTemplate("天气", "显示天气信息", "🌤", "medium"),
    WidgetTemplate("待办事项", "管理每日任务", "📝", "large"),
    WidgetTemplate("笔记", "快速记录想法", "📌", "medium"),
    WidgetTemplate("系统监控", "显示CPU、内存使用率", "📊", "small"),
    WidgetTemplate("日历", "显示当前日期", "📅", "medium"),
    WidgetTemplate("计时器", "倒计时功能", "⏱", "small"),
    WidgetTemplate("汇率", "汇率查询", "💱", "medium"),
]

# 尺寸映射常量
SIZE_MAP = {
    "small": (150, 150),
    "medium": (200, 200),
    "large": (300, 300)
}


# =============================================================================
# 工具函数
# =============================================================================

def hex_to_rgb(hex_color):
    """十六进制颜色转RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """RGB转十六进制颜色"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def lighten_color(hex_color, amount=20):
    """使颜色变亮"""
    rgb = hex_to_rgb(hex_color)
    new_rgb = tuple(min(255, c + amount) for c in rgb)
    return rgb_to_hex(new_rgb)

def darken_color(hex_color, amount=20):
    """使颜色变暗"""
    rgb = hex_to_rgb(hex_color)
    new_rgb = tuple(max(0, c - amount) for c in rgb)
    return rgb_to_hex(new_rgb)


# =============================================================================
# 动画过渡类 - 实现丝滑的动画效果
# =============================================================================

class AnimationManager:
    """动画管理器，处理所有UI动画效果"""

    @staticmethod
    def ease_out_cubic(t):
        """缓动函数：三次方缓出"""
        return 1 - pow(1 - t, 3)

    @staticmethod
    def ease_out_quart(t):
        """缓动函数：四次方缓出"""
        return 1 - pow(1 - t, 4)

    @staticmethod
    def ease_out_back(t):
        """缓动函数：带回弹效果"""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

    @staticmethod
    def animate_alpha(window, start_alpha, end_alpha, duration=300, callback=None):
        """透明度渐变动画"""
        frames = int(duration / 16)  # 60fps
        if frames == 0:
            window.attributes('-alpha', end_alpha)
            if callback:
                callback()
            return

        current_alpha = start_alpha

        def animate(frame):
            nonlocal current_alpha
            if frame >= frames:
                window.attributes('-alpha', end_alpha)
                if callback:
                    callback()
                return

            # 应用缓动效果
            progress = AnimationManager.ease_out_cubic(frame / frames)
            current_alpha = start_alpha + (end_alpha - start_alpha) * progress
            window.attributes('-alpha', current_alpha)
            window.after(16, lambda: animate(frame + 1))

        animate(0)

    @staticmethod
    def animate_color(widget, attribute, start_color, end_color, duration=300, callback=None):
        """颜色渐变动画"""
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        frames = int(duration / 16)

        def animate(frame):
            if frame >= frames:
                widget.config(**{attribute: end_color})
                if callback:
                    callback()
                return

            progress = AnimationManager.ease_out_cubic(frame / frames)
            current_rgb = tuple(
                start_rgb[i] + (end_rgb[i] - start_rgb[i]) * progress
                for i in range(3)
            )
            widget.config(**{attribute: rgb_to_hex(current_rgb)})
            widget.after(16, lambda: animate(frame + 1))

        animate(0)

    @staticmethod
    def animate_scale(widget, start_scale, end_scale, duration=300, callback=None):
        """缩放动画"""
        frames = int(duration / 16)
        current_scale = start_scale

        def animate(frame):
            nonlocal current_scale
            if frame >= frames:
                # 恢复原始大小
                widget.scale('all', widget.winfo_width() / 2, widget.winfo_height() / 2,
                            end_scale / current_scale, end_scale / current_scale)
                current_scale = end_scale
                if callback:
                    callback()
                return

            progress = AnimationManager.ease_out_back(frame / frames)
            new_scale = start_scale + (end_scale - start_scale) * progress
            scale_factor = new_scale / current_scale if current_scale > 0 else 1
            widget.scale('all', widget.winfo_width() / 2, widget.winfo_height() / 2,
                        scale_factor, scale_factor)
            current_scale = new_scale
            widget.after(16, lambda: animate(frame + 1))

        animate(0)

    @staticmethod
    def animate_slide(widget, start_x, end_x, start_y, end_y, duration=300, callback=None):
        """滑动动画"""
        frames = int(duration / 16)

        def animate(frame):
            if frame >= frames:
                widget.place(x=end_x, y=end_y)
                if callback:
                    callback()
                return

            progress = AnimationManager.ease_out_cubic(frame / frames)
            current_x = start_x + (end_x - start_x) * progress
            current_y = start_y + (end_y - start_y) * progress
            widget.place(x=current_x, y=current_y)
            widget.after(16, lambda: animate(frame + 1))

        animate(0)

    @staticmethod
    def create_glow_effect(canvas, x, y, radius, color):
        """创建发光效果"""
        # 在Canvas上绘制多层圆形模拟发光
        for i in range(radius, 0, -5):
            # 由于Canvas不支持alpha，这里简化处理
            canvas.create_oval(
                x - i, y - i, x + i, y + i,
                outline=color,
                width=1,
                tags="glow"
            )


class HoverEffect:
    """悬停效果管理"""

    def __init__(self, widget, bg_color, hover_bg_color, duration=150):
        self.widget = widget
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color
        self.duration = duration
        self.current_color = bg_color
        self.animating = False

        # 绑定事件
        self.widget.bind('<Enter>', self._on_enter)
        self.widget.bind('<Leave>', self._on_leave)

    def _on_enter(self, _=None):
        """鼠标进入时"""
        if not self.animating:
            self.animating = True
            AnimationManager.animate_color(
                self.widget, 'bg',
                self.current_color, self.hover_bg_color,
                self.duration,
                lambda: setattr(self, 'animating', False)
            )
            self.current_color = self.hover_bg_color

    def _on_leave(self, _=None):
        """鼠标离开时"""
        if not self.animating:
            self.animating = True
            AnimationManager.animate_color(
                self.widget, 'bg',
                self.current_color, self.bg_color,
                self.duration,
                lambda: setattr(self, 'animating', False)
            )
            self.current_color = self.bg_color


class DraggableWidget:
    """可拖拽的桌面小组件"""

    def __init__(self, parent, template, x=100, y=100, size="medium", light_mode=True, theme_colors=None):
        self.template = template
        self.x = x
        self.y = y
        self.size = size  # 自定义尺寸
        self.resizing = False
        self.resize_edge = None  # 'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'

        # 组件个性化设置
        self.widget_opacity = 88  # 默认透明度 88%
        self.widget_bg_color = "#FFFDE7"  # 默认背景色（浅黄色）
        self.widget_border_color = "#FFD54F"  # 默认边框色（金黄色）
        self.widget_corner_radius = 0  # 默认圆角（tkinter Canvas不支持圆角，仅作为设置选项）
        self.follow_theme = False  # 是否跟随主窗口主题

        # 接收主题信息
        self.light_mode = light_mode
        self.theme_colors = theme_colors or ThemeColors(light_mode=light_mode)

        # 加载组件配置
        self._load_widget_config()

        # 根据组件大小设置尺寸
        width, height = SIZE_MAP.get(size, template.get_size_dimensions())
        self.width = width
        self.height = height
        self.min_width = 100
        self.min_height = 100

        # 创建组件窗口（无边框、透明背景）
        self.window = tk.Toplevel(parent)
        self.window.title(template.name)
        self.window.geometry(f"{width}x{height}")
        self.window.overrideredirect(True)  # 无边框
        self.window.attributes('-topmost', True)  # 始终置顶
        self.window.attributes('-alpha', 0)  # 初始透明度为0，用于入场动画
        self.window.geometry(f"+{x}+{y}")
        self.window.resizable(False, False)

        # 应用主题颜色（如果跟随主题）
        if self.follow_theme:
            self._apply_theme_colors()

        # 待办事项数据
        if template.name == "待办事项":
            self.todos = self._load_todos() or [["完成项目设计", False], ["准备会议材料", False], ["回复邮件", False]]

        # 使用 Canvas 作为主容器，增加圆角阴影效果
        self.canvas = tk.Canvas(
            self.window,
            width=width,
            height=height,
            bg=self.widget_bg_color,
            highlightbackground=self.widget_border_color,
            highlightthickness=1,
            relief="flat"
        )
        self.canvas.pack(fill="both", expand=True)

        # 绘制圆角效果（通过多层矩形模拟）
        self._draw_rounded_corner_background(width, height)

        # 创建组件内容
        self._create_widget_content(self.canvas, width, height)

        # 入场动画
        AnimationManager.animate_alpha(
            self.window, 0, self.widget_opacity / 100, duration=400
        )

        # 拖拽和调整大小相关变量
        self._start_x = 0
        self._start_y = 0
        self._start_width = 0
        self._start_height = 0
        self._start_window_x = 0
        self._start_window_y = 0
        self._hover_state = False  # 悬停状态

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<Motion>", self._on_motion)
        self.canvas.bind("<Enter>", self._on_mouse_enter)
        self.canvas.bind("<Leave>", self._on_mouse_leave)

        # 创建调整大小的边框
        self.resize_margin = 8  # 边缘检测范围
        self._create_resize_handlers()

        # 右键菜单
        self.context_menu = tk.Menu(self.window, tearoff=0)

        if self.template.name == "待办事项":
            self.context_menu.add_command(label="清空已完成", command=self._clear_completed_todos)
            self.context_menu.add_separator()

        self.context_menu.add_command(label="重置大小", command=self._reset_size)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="设置", command=self._show_settings)
        self.context_menu.add_command(label="刷新", command=self._refresh)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="关闭", command=self._close_widget)

        self.window.bind("<Button-3>", self._show_context_menu)  # Windows
        self.window.bind("<Button-2>", self._show_context_menu)  # macOS

    def _draw_rounded_corner_background(self, width, height):
        """绘制圆角背景效果"""
        radius = 12  # 圆角半径
        # 使用多个小矩形模拟圆角效果
        # 四个角
        corner_size = radius
        # 左上角
        self.canvas.create_rectangle(
            0, 0, corner_size, corner_size,
            fill="", outline=self.widget_border_color, width=1, tags="rounded_bg"
        )
        # 右上角
        self.canvas.create_rectangle(
            width - corner_size, 0, width, corner_size,
            fill="", outline=self.widget_border_color, width=1, tags="rounded_bg"
        )
        # 左下角
        self.canvas.create_rectangle(
            0, height - corner_size, corner_size, height,
            fill="", outline=self.widget_border_color, width=1, tags="rounded_bg"
        )
        # 右下角
        self.canvas.create_rectangle(
            width - corner_size, height - corner_size, width, height,
            fill="", outline=self.widget_border_color, width=1, tags="rounded_bg"
        )

    def _on_mouse_enter(self, _=None):
        """鼠标进入组件时"""
        self._hover_state = True
        if self.window.winfo_exists():
            AnimationManager.animate_color(
                self.canvas, 'highlightbackground',
                self.widget_border_color,
                lighten_color(self.widget_border_color, 20),
                duration=150
            )

    def _on_mouse_leave(self, _=None):
        """鼠标离开组件时"""
        self._hover_state = False
        if self.window.winfo_exists():
            AnimationManager.animate_color(
                self.canvas, 'highlightbackground',
                self.canvas['highlightbackground'],
                self.widget_border_color,
                duration=150
            )

    def _close_widget(self):
        """关闭组件（带动画）"""
        def destroy_callback():
            if self.window.winfo_exists():
                self.window.destroy()

        AnimationManager.animate_alpha(
            self.window,
            self.window.attributes('-alpha'),
            0,
            duration=200,
            callback=destroy_callback
        )

    def _create_widget_content(self, canvas, width, height):
        """创建组件内容"""
        # 根据组件类型创建不同内容
        if self.template.name == "时钟":
            self._create_clock_widget(canvas, width, height)
        elif self.template.name == "天气":
            self._create_weather_widget(canvas, width, height)
        elif self.template.name == "待办事项":
            self._create_todo_widget(canvas, width, height)
        elif self.template.name == "笔记":
            self._create_note_widget(canvas, width, height)
        elif self.template.name == "系统监控":
            self._create_system_monitor_widget(canvas, width, height)
        elif self.template.name == "日历":
            self._create_calendar_widget(canvas, width, height)
        elif self.template.name == "计时器":
            self._create_timer_widget(canvas, width, height)
        elif self.template.name == "汇率":
            self._create_exchange_widget(canvas, width, height)

    def _create_clock_widget(self, canvas, width, height):
        """创建时钟组件 - 现代圆润设计"""
        # 根据组件大小计算字体大小
        icon_size = int(width * 0.22)
        time_size = int(width * 0.14)
        date_size = int(width * 0.055)

        # 现代设计颜色
        text_primary = "#1F2937"
        text_secondary = "#6B7280"

        # 绘制装饰性圆形背景（渐变效果模拟）
        glow_radius = min(width, height) * 0.25
        canvas.create_oval(
            width//2 - glow_radius, height//3 - glow_radius,
            width//2 + glow_radius, height//3 + glow_radius,
            fill="#F3F4F6",
            outline="#E5E7EB",
            width=2,
            tags="clock_bg"
        )

        # 时钟图标
        canvas.create_text(
            width//2, height//3,
            text=self.template.icon_name,
            font=("Segoe UI Emoji", icon_size),
            tags="clock_icon"
        )

        # 装饰性元素 - 小圆点
        for i in range(3):
            x = width//2 - 30 + i * 30
            canvas.create_oval(
                x, height//2 - 40, x + 6, height//2 - 34,
                fill="#E0E7FF", outline="", tags="decor"
            )

        # 时间
        self.time_text = canvas.create_text(
            width//2, height//2 + height//12,
            text=datetime.datetime.now().strftime("%H:%M:%S"),
            font=get_font(time_size, bold=True),
            fill=text_primary,
            tags="clock_time"
        )

        # 日期 - 添加圆角背景框
        date_bg_height = 28
        canvas.create_rectangle(
            width//2 - 70, height - height//6 - date_bg_height//2,
            width//2 + 70, height - height//6 + date_bg_height//2,
            fill="#F3F4F6",
            outline="#E5E7EB",
            width=1,
            tags="date_bg"
        )

        canvas.create_text(
            width//2, height - height//6,
            text=datetime.datetime.now().strftime("%Y年%m月%d日"),
            font=get_font(date_size),
            fill=text_secondary,
            tags="clock_date"
        )

        # 定时更新
        self._update_clock()

    def _update_clock(self):
        """更新时钟"""
        if not hasattr(self, 'window') or not self.window.winfo_exists():
            return

        if hasattr(self, 'time_text'):
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                self.canvas.itemconfig(self.time_text, text=current_time)
            except Exception:
                return

            self.window.after(1000, self._update_clock)

    def _create_weather_widget(self, canvas, width, height):
        """创建天气组件 - 现代圆润设计"""
        # 根据组件大小计算字体大小
        icon_size = int(width * 0.26)
        temp_size = int(width * 0.16)
        desc_size = int(width * 0.065)
        loc_size = int(width * 0.05)

        # 现代设计颜色
        text_secondary = "#6B7280"
        text_hint = "#9CA3AF"

        # 绘制温度渐变背景（模拟）
        temp_bg_height = 80
        canvas.create_rectangle(
            20, height//2 - 10, width - 20, height//2 + temp_bg_height - 10,
            fill="#EFF6FF",
            outline="#DBEAFE",
            width=1,
            tags="weather_bg"
        )

        # 天气图标
        canvas.create_text(
            width//2, height//3,
            text=self.template.icon_name,
            font=("Segoe UI Emoji", icon_size),
            tags="weather_icon"
        )

        # 温度
        canvas.create_text(
            width//2, height//2 + 15,
            text="25°C",
            font=get_font(temp_size, bold=True),
            fill="#3B82F6",
            tags="weather_temp"
        )

        # 天气描述
        canvas.create_text(
            width//2, height//2 + 45,
            text="晴朗",
            font=get_font(desc_size),
            fill=text_secondary,
            tags="weather_desc"
        )

        # 地点 - 圆角标签样式
        loc_bg_width = 100
        loc_bg_height = 26
        canvas.create_rectangle(
            width//2 - loc_bg_width//2, height - height//8 - loc_bg_height//2,
            width//2 + loc_bg_width//2, height - height//8 + loc_bg_height//2,
            fill="#F9FAFB",
            outline="#E5E7EB",
            width=1,
            tags="loc_bg"
        )

        canvas.create_text(
            width//2, height - height//8,
            text="📍 北京市",
            font=get_font(loc_size),
            fill=text_hint,
            tags="weather_loc"
        )

    def _create_todo_widget(self, canvas, width, height):
        """创建待办事项组件 - 液态玻璃效果"""
        # 根据组件大小计算字体和位置
        title_size = int(width * 0.07)
        title_y = int(height * 0.1)
        line_y = int(height * 0.15)
        btn_height = int(height * 0.08)
        btn_y = height - btn_height - int(height * 0.05)
        btn_text_size = int(width * 0.04)

        # 液态玻璃效果颜色
        text_primary = "#1A1A1A"
        border_color = "#BFDBFE"
        accent_color = "#3B82F6"

        # 标题
        canvas.create_text(
            width//2, title_y,
            text="📝 待办事项",
            font=get_font(title_size, bold=True),
            fill=text_primary
        )

        # 分隔线
        margin = int(width * 0.1)
        canvas.create_line(margin, line_y, width-margin, line_y, fill=border_color, width=1)

        # 待办事项列表
        self._render_todo_list(canvas, width, height)

        # 添加按钮
        btn_width = int(width * 0.4)
        canvas.create_rectangle(
            width//2 - btn_width//2, btn_y,
            width//2 + btn_width//2, btn_y + btn_height,
            fill=accent_color,
            outline=""
        )
        add_btn_text = canvas.create_text(
            width//2, btn_y + btn_height//2,
            text="+ 添加",
            fill="white",
            font=get_font(btn_text_size)
        )

        # 绑定按钮点击事件
        self.canvas.tag_bind(add_btn_text, "<Button-1>", self._add_todo)

    def _render_todo_list(self, canvas, width, height):
        """渲染待办事项列表"""
        canvas.delete("todo_item")

        margin = int(width * 0.1)
        line_height = int(height * 0.08)
        start_y = int(height * 0.2)
        font_size = int(width * 0.04)

        # 液态玻璃效果颜色
        text_primary = "#1A1A1A"
        text_completed = "#6B7280"

        y_pos = start_y
        for i, (todo, completed) in enumerate(self.todos):
            # 待办事项文本
            text = f"☑ {todo}" if completed else f"☐ {todo}"
            color = text_completed if completed else text_primary

            todo_text = canvas.create_text(
                margin, y_pos,
                text=text,
                font=get_font(font_size),
                fill=color,
                anchor="w",
                tags=("todo_item", f"todo_{i}")
            )

            # 绑定点击事件
            canvas.tag_bind(todo_text, "<Button-1>", lambda _, idx=i: self._toggle_todo(idx))

            y_pos += line_height

    def _add_todo(self, event=None):
        """添加新的待办事项"""
        _ = event  # 未使用，保留以兼容事件处理
        from tkinter import simpledialog

        new_todo = simpledialog.askstring(
            "添加待办事项",
            "请输入待办事项:",
            parent=self.window
        )

        if new_todo and new_todo.strip():
            todo_text = new_todo.strip()
            # 限制长度以避免UI显示问题
            if len(todo_text) > 100:
                todo_text = todo_text[:100] + "..."
                from tkinter import messagebox
                messagebox.showwarning("提示", "待办事项过长，已截断为100字符", parent=self.window)

            self.todos.append([todo_text, False])
            self._render_todo_list(self.canvas, self.width, self.height)
            self._save_todos()  # 持久化保存

    def _toggle_todo(self, index):
        """切换待办事项完成状态"""
        if 0 <= index < len(self.todos):
            self.todos[index][1] = not self.todos[index][1]
            self._render_todo_list(self.canvas, self.width, self.height)
            self._save_todos()

    def _delete_todo(self, index):
        """删除待办事项"""
        if 0 <= index < len(self.todos):
            self.todos.pop(index)
            self._render_todo_list(self.canvas, self.width, self.height)
            self._save_todos()

    def _save_todos(self):
        """保存待办事项到文件"""
        data_dir = Path.home() / ".dashwidgets"
        data_dir.mkdir(exist_ok=True)
        todo_file = data_dir / "todos.json"

        try:
            data = {'todos': self.todos}
            with open(todo_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存待办事项失败: {e}")

    def _load_todos(self):
        """加载保存的待办事项"""
        data_dir = Path.home() / ".dashwidgets"
        todo_file = data_dir / "todos.json"

        if todo_file.exists():
            try:
                with open(todo_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('todos', [])
            except Exception as e:
                logger.warning(f"加载待办事项失败: {e}")
        return None

    def _clear_completed_todos(self):
        """清空已完成的待办事项"""
        self.todos = [[todo, completed] for todo, completed in self.todos if not completed]
        self._render_todo_list(self.canvas, self.width, self.height)

    def _create_note_widget(self, canvas, width, height):
        """创建笔记组件"""
        # 根据组件大小计算字体和位置
        title_size = int(width * 0.07)
        title_y = int(height * 0.1)
        line_y = int(height * 0.15)
        margin = int(width * 0.1)
        font_size = int(width * 0.04)
        btn_height = int(height * 0.08)

        # 标题
        canvas.create_text(
            width//2, title_y,
            text="📌 笔记",
            font=get_font(title_size, bold=True),
            fill="#333333"
        )

        # 分隔线
        canvas.create_line(margin, line_y, width-margin, line_y, fill="#E0E0E0", width=1)

        # 笔记内容（使用 Text widget 实现可编辑）
        self.note_text = tk.Text(
            self.window,
            font=get_font(font_size),
            bg="#FFF9C4",
            borderwidth=0,
            highlightthickness=0,
            wrap="word"
        )

        default_note = """记得今天下午3点
参加产品评审会议

需要准备的材料:
1. 功能演示
2. 数据报告
3. 问题清单"""

        self.note_text.insert("1.0", default_note)
        self.note_text.place(x=margin, y=line_y + 10, width=width-2*margin, height=height-line_y-btn_height-20)

        # 保存按钮
        btn_width = int(width * 0.25)
        save_btn = tk.Button(
            self.window,
            text="💾 保存",
            bg="#007AFF",
            fg="white",
            borderwidth=0,
            font=get_font(int(font_size*0.8)),
            command=self._save_note
        )
        save_btn.place(x=width//2 - btn_width//2, y=height-btn_height-10, width=btn_width, height=btn_height)

    def _save_note(self):
        """保存笔记"""
        note_content = self.note_text.get("1.0", "end-1c")

        # 创建数据目录
        data_dir = Path.home() / ".dashwidgets"
        data_dir.mkdir(exist_ok=True)

        # 保存笔记到文件
        note_file = data_dir / "notes.json"
        try:
            data = {}
            if note_file.exists():
                with open(note_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            data['note'] = note_content
            with open(note_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            from tkinter import messagebox
            messagebox.showinfo("笔记已保存", "笔记内容已保存！", parent=self.window)
        except Exception as e:
            logger.error(f"保存笔记失败: {e}")

    def _create_system_monitor_widget(self, canvas, width, height):
        """创建系统监控组件"""
        # 根据组件大小计算字体和位置
        title_size = int(width * 0.06)
        title_y = int(height * 0.1)
        margin = int(width * 0.1)
        font_size = int(width * 0.04)
        bar_height = int(height * 0.05)
        bar_spacing = int(height * 0.03)
        start_y = int(height * 0.25)
        bar_width = int(width * 0.6)

        # 标题
        canvas.create_text(
            width//2, title_y,
            text="📊 系统监控",
            font=get_font(title_size, bold=True),
            fill="#333333"
        )

        # 初始化监控元素ID
        self.monitor_elements = {}
        self.monitor_config = {
            'bar_width': bar_width,
            'bar_height': bar_height,
            'margin': margin,
            'start_y': start_y,
            'bar_spacing': bar_spacing
        }

        # CPU 使用率
        cpu_percent = self._get_cpu_usage()
        cpu_y = start_y
        self.monitor_elements['cpu_text'] = canvas.create_text(
            margin, cpu_y - bar_height - 5,
            text=f"CPU: {cpu_percent}%",
            font=get_font(font_size),
            fill="#333333",
            anchor="w"
        )

        # CPU 进度条背景
        canvas.create_rectangle(
            margin, cpu_y,
            margin + bar_width, cpu_y + bar_height,
            outline="#E0E0E0",
            width=1,
            tags="monitor_bg"
        )

        # CPU 进度条
        self.monitor_elements['cpu_bar'] = canvas.create_rectangle(
            margin, cpu_y,
            margin + (cpu_percent / 100) * bar_width, cpu_y + bar_height,
            fill="#34C759",
            outline="",
            tags="monitor_fg"
        )

        # 内存使用
        mem_percent = self._get_memory_usage()
        mem_y = cpu_y + bar_height + bar_spacing * 2
        self.monitor_elements['mem_text'] = canvas.create_text(
            margin, mem_y - bar_height - 5,
            text=f"内存: {mem_percent}%",
            font=get_font(font_size),
            fill="#333333",
            anchor="w"
        )

        # 内存进度条背景
        canvas.create_rectangle(
            margin, mem_y,
            margin + bar_width, mem_y + bar_height,
            outline="#E0E0E0",
            width=1,
            tags="monitor_bg"
        )

        # 内存进度条
        self.monitor_elements['mem_bar'] = canvas.create_rectangle(
            margin, mem_y,
            margin + (mem_percent / 100) * bar_width, mem_y + bar_height,
            fill="#007AFF",
            outline="",
            tags="monitor_fg"
        )

        # 每2秒刷新一次
        self._update_system_monitor()

    def _get_cpu_usage(self):
        """获取CPU使用率（模拟）"""
        return random.randint(20, 80)

    def _get_memory_usage(self):
        """获取内存使用率（模拟）"""
        return random.randint(30, 70)

    def _update_system_monitor(self):
        """更新系统监控数据"""
        if not hasattr(self, 'monitor_elements') or not hasattr(self, 'window'):
            return

        try:
            # 获取新的数据
            cpu_percent = self._get_cpu_usage()
            mem_percent = self._get_memory_usage()

            # 获取配置
            config = getattr(self, 'monitor_config', {
                'bar_width': 100,
                'bar_height': 10,
                'margin': 25,
                'start_y': self.height // 2,
                'bar_spacing': 30
            })

            bar_width = config['bar_width']
            bar_height = config['bar_height']
            margin = config['margin']
            start_y = config['start_y']
            bar_spacing = config['bar_spacing']

            # 更新CPU显示
            self.canvas.itemconfig(
                self.monitor_elements['cpu_text'],
                text=f"CPU: {cpu_percent}%"
            )

            # 更新CPU进度条
            cpu_y = start_y
            self.canvas.coords(
                self.monitor_elements['cpu_bar'],
                margin, cpu_y,
                margin + (cpu_percent / 100) * bar_width, cpu_y + bar_height
            )

            # 根据使用率改变颜色
            cpu_color = "#34C759" if cpu_percent < 50 else "#FF9500" if cpu_percent < 80 else "#FF3B30"
            self.canvas.itemconfig(self.monitor_elements['cpu_bar'], fill=cpu_color)

            # 更新内存显示
            self.canvas.itemconfig(
                self.monitor_elements['mem_text'],
                text=f"内存: {mem_percent}%"
            )

            # 更新内存进度条
            mem_y = cpu_y + bar_height + bar_spacing * 2
            self.canvas.coords(
                self.monitor_elements['mem_bar'],
                margin, mem_y,
                margin + (mem_percent / 100) * bar_width, mem_y + bar_height
            )

            # 根据使用率改变颜色
            mem_color = "#34C759" if mem_percent < 50 else "#FF9500" if mem_percent < 80 else "#FF3B30"
            self.canvas.itemconfig(self.monitor_elements['mem_bar'], fill=mem_color)

            # 2秒后再次刷新
            self.window.after(2000, self._update_system_monitor)

        except Exception:
            pass

    def _create_calendar_widget(self, canvas, width, height):
        """创建日历组件"""
        # 根据组件大小计算字体和位置
        icon_size = int(width * 0.2)
        day_size = int(width * 0.24)
        year_size = int(width * 0.06)
        icon_y = int(height * 0.25)
        year_y = int(height * 0.85)

        # 图标
        canvas.create_text(width//2, icon_y, text=self.template.icon_name, font=("Segoe UI Emoji", icon_size))

        # 日期
        now = datetime.datetime.now()
        canvas.create_text(
            width//2, height//2 + height//20,
            text=str(now.day),
            font=get_font(day_size, bold=True),
            fill="#333333"
        )

        # 年月
        canvas.create_text(
            width//2, year_y,
            text=f"{now.year}年 {now.month}月",
            font=get_font(year_size),
            fill="#666666"
        )

    def _create_timer_widget(self, canvas, width, height):
        """创建计时器组件"""
        # 根据组件大小计算字体和位置
        icon_size = int(width * 0.15)
        time_size = int(width * 0.14)
        icon_y = int(height * 0.2)
        btn_radius = int(width * 0.13)
        btn_y = height - int(height * 0.15)
        btn_text_size = int(width * 0.06)

        # 图标
        canvas.create_text(width//2, icon_y, text=self.template.icon_name, font=("Segoe UI Emoji", icon_size))

        # 计时器显示
        canvas.create_text(
            width//2, height//2 + height//20,
            text="00:00",
            font=get_font(time_size, bold=True),
            fill="#333333"
        )

        # 按钮
        canvas.create_oval(
            width//2 - btn_radius, btn_y - btn_radius,
            width//2 + btn_radius, btn_y + btn_radius,
            fill="#007AFF",
            outline=""
        )
        canvas.create_text(
            width//2, btn_y,
            text="▶",
            fill="white",
            font=get_font(btn_text_size)
        )

    def _create_exchange_widget(self, canvas, width, height):
        """创建汇率组件"""
        # 根据组件大小计算字体和位置
        title_size = int(width * 0.06)
        title_y = int(height * 0.1)
        main_size = int(width * 0.08)
        sub_size = int(width * 0.05)
        time_size = int(width * 0.04)
        time_y = height - int(height * 0.1)

        # 标题
        canvas.create_text(
            width//2, title_y,
            text="💱 汇率",
            font=get_font(title_size, bold=True),
            fill="#333333"
        )

        # 汇率信息
        canvas.create_text(
            width//2, height//2 - height//15,
            text="1 USD = 7.24 CNY",
            font=get_font(main_size, bold=True),
            fill="#007AFF"
        )

        canvas.create_text(
            width//2, height//2 + height//10,
            text="1 EUR = 7.85 CNY",
            font=get_font(sub_size),
            fill="#333333"
        )

        canvas.create_text(
            width//2, time_y,
            text="更新于 5分钟前",
            font=get_font(time_size),
            fill="#999999"
        )

    def _create_resize_handlers(self):
        """创建调整大小的手柄（透明区域）"""
        self.resize_handlers = {}

        # 创建8个方向的调整区域（使用透明矩形）
        for edge in ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']:
            # 使用Frame作为调整手柄，可以设置透明背景
            handler = tk.Frame(
                self.window,
                cursor=self._get_cursor_for_edge(edge)
            )
            handler.bind("<Button-1>", lambda e, edge=edge: self._start_resize(e, edge))
            handler.bind("<B1-Motion>", lambda e: self._do_resize(e))
            handler.bind("<ButtonRelease-1>", lambda e: self._end_resize(e))
            self.resize_handlers[edge] = handler

        # 定位调整区域
        self._update_resize_handlers()

    def _get_cursor_for_edge(self, edge):
        """根据边缘返回光标样式"""
        cursor_map = {
            'n': 'sb_v_double_arrow',
            's': 'sb_v_double_arrow',
            'e': 'sb_h_double_arrow',
            'w': 'sb_h_double_arrow',
            'ne': 'top_right_corner',
            'nw': 'top_left_corner',
            'se': 'bottom_right_corner',
            'sw': 'bottom_left_corner'
        }
        return cursor_map.get(edge, 'fleur')

    def _update_resize_handlers(self):
        """更新调整区域的位置和大小"""
        w = self.width
        h = self.height
        m = self.resize_margin

        # 北边（上边缘）
        self.resize_handlers['n'].place(x=m, y=0, width=w-2*m, height=m)
        # 南边（下边缘）
        self.resize_handlers['s'].place(x=m, y=h-m, width=w-2*m, height=m)
        # 东边（右边缘）
        self.resize_handlers['e'].place(x=w-m, y=m, width=m, height=h-2*m)
        # 西边（左边缘）
        self.resize_handlers['w'].place(x=0, y=m, width=m, height=h-2*m)
        # 东北角
        self.resize_handlers['ne'].place(x=w-m, y=0, width=m, height=m)
        # 西北角
        self.resize_handlers['nw'].place(x=0, y=0, width=m, height=m)
        # 东南角
        self.resize_handlers['se'].place(x=w-m, y=h-m, width=m, height=m)
        # 西南角
        self.resize_handlers['sw'].place(x=0, y=h-m, width=m, height=m)

    def _start_resize(self, event, edge):
        """开始调整大小"""
        self.resizing = True
        self.resize_edge = edge
        self._start_x = event.x_root
        self._start_y = event.y_root
        self._start_width = self.width
        self._start_height = self.height
        self._start_window_x = self.window.winfo_x()
        self._start_window_y = self.window.winfo_y()

    def _do_resize(self, event):
        """执行调整大小"""
        if not self.resizing:
            return

        dx = event.x_root - self._start_x
        dy = event.y_root - self._start_y
        edge = self.resize_edge

        new_width = self._start_width
        new_height = self._start_height
        new_x = self._start_window_x
        new_y = self._start_window_y

        # 根据边缘调整尺寸和位置
        if 'e' in edge:  # 东边（右）
            new_width = max(self.min_width, self._start_width + dx)
        if 'w' in edge:  # 西边（左）
            new_width = max(self.min_width, self._start_width - dx)
            new_x = self._start_window_x + (self._start_width - new_width)
        if 's' in edge:  # 南边（下）
            new_height = max(self.min_height, self._start_height + dy)
        if 'n' in edge:  # 北边（上）
            new_height = max(self.min_height, self._start_height - dy)
            new_y = self._start_window_y + (self._start_height - new_height)

        # 应用新尺寸
        self.width = new_width
        self.height = new_height

        # 更新窗口
        self.window.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")

        # 更新Canvas
        self.canvas.config(width=new_width, height=new_height)

        # 更新调整区域
        self._update_resize_handlers()

    def _end_resize(self, event):
        """结束调整大小"""
        _ = event  # 未使用，保留以兼容事件处理
        if self.resizing:
            self.resizing = False
            self.resize_edge = None

            # 重新创建内容以适应新尺寸
            self.canvas.delete("all")
            self._create_widget_content(self.canvas, self.width, self.height)

    def _on_motion(self, event):
        """鼠标移动事件（用于更新光标）"""
        if self.resizing:
            return

        x, y = event.x, event.y
        w, h = self.width, self.height
        m = self.resize_margin

        # 先检测角落（优先级更高）
        edge = None
        if x < m and y < m:
            edge = 'nw'
        elif x > w - m and y < m:
            edge = 'ne'
        elif x < m and y > h - m:
            edge = 'sw'
        elif x > w - m and y > h - m:
            edge = 'se'
        # 然后检测边缘
        elif y < m:
            edge = 'n'
        elif y > h - m:
            edge = 's'
        elif x < m:
            edge = 'w'
        elif x > w - m:
            edge = 'e'

        # 更新光标
        if edge:
            self.canvas.config(cursor=self._get_cursor_for_edge(edge))
        else:
            self.canvas.config(cursor="fleur")

    def _on_press(self, event):
        """鼠标按下事件"""
        # 如果正在调整大小，不触发拖拽
        if self.resizing:
            return

        self._start_x = event.x
        self._start_y = event.y

    def _on_drag(self, event):
        """鼠标拖拽事件"""
        # 如果正在调整大小，不触发拖拽
        if self.resizing:
            return

        x = self.window.winfo_x() + (event.x - self._start_x)
        y = self.window.winfo_y() + (event.y - self._start_y)
        self.window.geometry(f"+{x}+{y}")

    def _show_context_menu(self, event):
        """显示右键菜单"""
        self.context_menu.post(event.x_root, event.y_root)

    def _show_settings(self):
        """显示组件设置对话框"""
        # 创建设置窗口
        settings_window = tk.Toplevel(self.window)
        settings_window.title(f"{self.template.name} - 设置")
        settings_window.geometry("400x320")
        settings_window.resizable(False, False)

        # 设置窗口在组件附近显示
        widget_x = self.window.winfo_x()
        widget_y = self.window.winfo_y()
        settings_window.geometry(f"+{widget_x + 50}+{widget_y + 50}")

        # 创建主容器
        main_frame = tk.Frame(settings_window, bg="#F5F5F5")
        main_frame.pack(fill="both", expand=True)

        # 标题
        title_frame = tk.Frame(main_frame, bg="#007AFF", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text=f"⚙️ {self.template.name} 设置",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg="#007AFF",
            fg="white"
        )
        title_label.pack(pady=15)

        # 内容区域
        content_frame = tk.Frame(main_frame, bg="#F5F5F5", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)

        # 透明度设置
        opacity_frame = tk.Frame(content_frame, bg="#F5F5F5")
        opacity_frame.pack(fill="x", pady=(0, 15))

        opacity_label = tk.Label(
            opacity_frame,
            text="透明度:",
            font=("Microsoft YaHei UI", 11),
            bg="#F5F5F5",
            fg="#333333",
            anchor="w"
        )
        opacity_label.pack(fill="x", pady=(0, 5))

        opacity_slider = tk.Scale(
            opacity_frame,
            from_=20,
            to=100,
            orient="horizontal",
            bg="#F5F5F5",
            fg="#333333",
            highlightthickness=0,
            command=self._on_opacity_change
        )
        opacity_slider.set(self.widget_opacity)
        opacity_slider.pack(fill="x")
        self.opacity_slider = opacity_slider

        opacity_value_label = tk.Label(
            opacity_frame,
            text=f"{self.widget_opacity}%",
            font=("Microsoft YaHei UI", 10),
            bg="#F5F5F5",
            fg="#666666"
        )
        opacity_value_label.pack(anchor="e")
        self.opacity_value_label = opacity_value_label

        # 跟随主题设置
        follow_theme_frame = tk.Frame(content_frame, bg="#F5F5F5")
        follow_theme_frame.pack(fill="x", pady=(0, 15))

        follow_theme_label = tk.Label(
            follow_theme_frame,
            text="🎨 统一主题:",
            font=("Microsoft YaHei UI", 11),
            bg="#F5F5F5",
            fg="#333333",
            anchor="w"
        )
        follow_theme_label.pack(fill="x", pady=(0, 5))

        follow_theme_var = tk.BooleanVar(value=self.follow_theme)
        follow_theme_check = tk.Checkbutton(
            follow_theme_frame,
            text="跟随主窗口主题（自动同步颜色）",
            variable=follow_theme_var,
            bg="#F5F5F5",
            fg="#333333",
            selectcolor="#007AFF",
            activebackground="#F5F5F5",
            activeforeground="#007AFF",
            font=("Microsoft YaHei UI", 10),
            command=self._on_follow_theme_change
        )
        follow_theme_check.pack(anchor="w")
        self.follow_theme_var = follow_theme_var

        # 背景颜色设置（当不跟随主题时可用）
        bg_color_frame = tk.Frame(content_frame, bg="#F5F5F5")
        bg_color_frame.pack(fill="x", pady=(0, 15))

        bg_color_label = tk.Label(
            bg_color_frame,
            text="背景颜色:",
            font=("Microsoft YaHei UI", 11),
            bg="#F5F5F5",
            fg="#333333",
            anchor="w"
        )
        bg_color_label.pack(fill="x", pady=(0, 5))

        # 预设颜色选项
        color_options_frame = tk.Frame(bg_color_frame, bg="#F5F5F5")
        color_options_frame.pack(fill="x")

        preset_colors = [
            ("浅黄", "#FFFDE7"),
            ("浅蓝", "#E3F2FD"),
            ("浅绿", "#E8F5E9"),
            ("浅粉", "#FCE4EC"),
            ("浅紫", "#F3E5F5"),
            ("白色", "#FFFFFF"),
            ("深蓝", "#263238"),
            ("深灰", "#37474F"),
        ]

        for color_name, color_value in preset_colors:
            color_btn = tk.Button(
                color_options_frame,
                bg=color_value,
                fg="white" if color_value in ["#263238", "#37474F"] else "#333333",
                text="✓" if self.widget_bg_color == color_value else "",
                width=6,
                height=2,
                command=lambda c=color_value: self._on_bg_color_change(c)
            )
            color_btn.pack(side="left", padx=2, pady=5)

        # 自定义颜色
        custom_color_frame = tk.Frame(bg_color_frame, bg="#F5F5F5")
        custom_color_frame.pack(fill="x", pady=(5, 0))

        tk.Label(
            custom_color_frame,
            text="自定义:",
            font=("Microsoft YaHei UI", 10),
            bg="#F5F5F5",
            fg="#666666"
        ).pack(side="left", padx=(0, 5))

        custom_color_btn = tk.Button(
            custom_color_frame,
            text="选择颜色",
            bg="#DDDDDD",
            fg="#333333",
            relief="flat",
            command=self._choose_custom_color
        )
        custom_color_btn.pack(side="left")

        # 边框颜色设置
        border_color_frame = tk.Frame(content_frame, bg="#F5F5F5")
        border_color_frame.pack(fill="x", pady=(0, 15))

        border_color_label = tk.Label(
            border_color_frame,
            text="边框颜色:",
            font=("Microsoft YaHei UI", 11),
            bg="#F5F5F5",
            fg="#333333",
            anchor="w"
        )
        border_color_label.pack(fill="x", pady=(0, 5))

        # 边框颜色选项
        border_options_frame = tk.Frame(border_color_frame, bg="#F5F5F5")
        border_options_frame.pack(fill="x")

        border_colors = [
            ("金黄", "#FFD54F"),
            ("蓝色", "#2196F3"),
            ("绿色", "#4CAF50"),
            ("红色", "#F44336"),
            ("无", "#F5F5F5"),
        ]

        for color_name, color_value in border_colors:
            if color_name == "无":
                border_btn = tk.Button(
                    border_options_frame,
                    bg=color_value,
                    fg="#333333",
                    text="无边框",
                    width=8,
                    height=2,
                    command=lambda: self._on_border_color_change(None, 0)
                )
            else:
                border_btn = tk.Button(
                    border_options_frame,
                    bg=color_value,
                    fg="white",
                    text="✓" if self.widget_border_color == color_value else "",
                    width=6,
                    height=2,
                    command=lambda c=color_value: self._on_border_color_change(c, 1)
                )
            border_btn.pack(side="left", padx=2, pady=5)

        # 说明文字
        note_label = tk.Label(
            content_frame,
            text="注意：圆角功能在Canvas组件中有限制",
            font=("Microsoft YaHei UI", 9),
            bg="#F5F5F5",
            fg="#999999",
            anchor="w"
        )
        note_label.pack(fill="x", pady=(5, 0))

        # 底部按钮
        button_frame = tk.Frame(main_frame, bg="#F5F5F5")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        # 保存按钮
        save_btn = tk.Button(
            button_frame,
            text="保存",
            bg="#007AFF",
            fg="white",
            font=("Microsoft YaHei UI", 11, "bold"),
            width=10,
            relief="flat",
            command=lambda: self._save_widget_settings(settings_window)
        )
        save_btn.pack(side="right", padx=5)

        # 取消按钮
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            bg="#DDDDDD",
            fg="#333333",
            font=("Microsoft YaHei UI", 11),
            width=10,
            relief="flat",
            command=settings_window.destroy
        )
        cancel_btn.pack(side="right", padx=5)

    def _on_opacity_change(self, value):
        """透明度滑块回调"""
        self.opacity_value_label.config(text=f"{int(value)}%")

    def _on_follow_theme_change(self):
        """跟随主题复选框回调"""
        self.follow_theme = self.follow_theme_var.get()

        # 如果跟随主题，禁用颜色选择器
        if self.follow_theme:
            self._disable_color_controls()
        else:
            self._enable_color_controls()

    def _on_bg_color_change(self, color):
        """背景颜色更改回调"""
        self.widget_bg_color = color

    def _on_border_color_change(self, color, thickness):
        """边框颜色更改回调"""
        self.widget_border_color = color if color else "#F5F5F5"
        self.canvas.config(highlightthickness=thickness)

    def _choose_custom_color(self):
        """选择自定义颜色"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(
            title="选择背景颜色",
            initialcolor=self.widget_bg_color,
            parent=self.window
        )
        if color[1]:
            self.widget_bg_color = color[1]

    def _save_widget_settings(self, settings_window):
        """保存组件设置"""
        # 应用透明度
        self.widget_opacity = int(self.opacity_slider.get())

        # 应用跟随主题设置
        self.follow_theme = self.follow_theme_var.get()

        # 如果跟随主题，应用主题颜色
        if self.follow_theme:
            self._apply_theme_colors()
        else:
            # 应用自定义背景和边框颜色
            self.canvas.config(
                bg=self.widget_bg_color,
                highlightbackground=self.widget_border_color
            )

        # 更新窗口透明度
        self.window.attributes('-alpha', self.widget_opacity / 100)

        # 保存到配置文件
        self._save_widget_config()

        from tkinter import messagebox
        messagebox.showinfo("成功", "组件设置已保存！", parent=self.window)
        settings_window.destroy()

    def _save_widget_config(self):
        """保存组件配置到文件"""
        data_dir = Path.home() / ".dashwidgets"
        data_dir.mkdir(exist_ok=True)

        config_file = data_dir / "widget_configs.json"

        try:
            # 加载现有配置
            configs = {}
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    configs = json.load(f)

            # 保存当前组件配置
            widget_key = f"{self.template.name}_{id(self)}"
            configs[widget_key] = {
                "opacity": self.widget_opacity,
                "bg_color": self.widget_bg_color,
                "border_color": self.widget_border_color,
                "corner_radius": self.widget_corner_radius,
                "follow_theme": self.follow_theme
            }

            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(configs, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"保存组件配置失败: {e}")

    def _load_widget_config(self):
        """加载组件配置"""
        data_dir = Path.home() / ".dashwidgets"
        config_file = data_dir / "widget_configs.json"

        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    configs = json.load(f)

                # 尝试查找匹配的配置
                for widget_key, config in configs.items():
                    if widget_key.startswith(self.template.name):
                        self.widget_opacity = config.get("opacity", 88)
                        self.widget_bg_color = config.get("bg_color", "#FFFDE7")
                        self.widget_border_color = config.get("border_color", "#FFD54F")
                        self.widget_corner_radius = config.get("corner_radius", 0)
                        self.follow_theme = config.get("follow_theme", False)
                        logger.info(f"加载组件配置: {widget_key}")
                        break
            except Exception as e:
                logger.warning(f"加载组件配置失败: {e}")

    def _apply_theme_colors(self):
        """应用主题颜色到组件"""
        if self.follow_theme and self.theme_colors:
            self.widget_bg_color = self.theme_colors.bg_card
            self.widget_border_color = self.theme_colors.border
            self.canvas.config(
                bg=self.widget_bg_color,
                highlightbackground=self.widget_border_color
            )

    def update_theme(self, light_mode, theme_colors):
        """更新组件主题（由主应用调用）"""
        self.light_mode = light_mode
        self.theme_colors = theme_colors

        # 如果跟随主题，立即应用
        if self.follow_theme:
            self._apply_theme_colors()

    def _reset_size(self):
        """重置组件大小到预设值（带动画）"""
        target_width, target_height = SIZE_MAP.get(self.size, (200, 200))

        # 获取当前窗口位置
        current_x = self.window.winfo_x()
        current_y = self.window.winfo_y()

        # 计算居中位置
        new_x = max(0, current_x + (self.width - target_width) // 2)
        new_y = max(0, current_y + (self.height - target_height) // 2)

        # 确保窗口不会超出屏幕
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        new_x = min(new_x, screen_width - target_width)
        new_y = min(new_y, screen_height - target_height)

        # 添加缩放动画效果
        self._animate_size_change(self.width, self.height, target_width, target_height, new_x, new_y)

    def _animate_size_change(self, start_w, start_h, end_w, end_h, new_x, new_y):
        """窗口大小变化动画"""
        duration = 300
        frames = int(duration / 16)

        def animate(frame):
            nonlocal start_w, start_h
            if frame >= frames:
                # 动画结束，应用最终尺寸
                self.width = end_w
                self.height = end_h
                self.window.geometry(f"{int(end_w)}x{int(end_h)}+{new_x}+{new_y}")
                self.canvas.config(width=int(end_w), height=int(end_h))
                self._update_resize_handlers()
                self.canvas.delete("all")
                self._create_widget_content(self.canvas, int(end_w), int(end_h))
                return

            progress = AnimationManager.ease_out_cubic(frame / frames)
            curr_w = start_w + (end_w - start_w) * progress
            curr_h = start_h + (end_h - start_h) * progress
            curr_x = self.window.winfo_x() + (new_x - self.window.winfo_x()) * progress
            curr_y = self.window.winfo_y() + (new_y - self.window.winfo_y()) * progress

            self.window.geometry(f"{int(curr_w)}x{int(curr_h)}+{int(curr_x)}+{int(curr_y)}")
            self.canvas.config(width=int(curr_w), height=int(curr_h))

            self.window.after(16, lambda: animate(frame + 1))

        animate(0)

    def _refresh(self):
        """刷新组件"""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self._create_widget_content(self.canvas, width, height)


class DashWidgetsApp:
    """主应用程序类"""

    def __init__(self):
        # 加载已保存的设置
        settings = self._load_settings()

        # 设置外观
        theme = settings.get('theme', '浅色')
        if theme == '深色':
            ctk.set_appearance_mode("dark")
            self.light_mode = False
        elif theme == '跟随系统':
            self._apply_system_theme()
        else:
            ctk.set_appearance_mode("light")
            self.light_mode = True

        ctk.set_default_color_theme("blue")

        # 创建主窗口（控制面板）
        self.root = ctk.CTk()
        self.root.title("DashWidgets 控制面板")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        self.root.minsize(900, 500)

        # 设置主窗口透明度
        opacity = settings.get('opacity', 95) / 100
        self.root.attributes('-alpha', opacity)

        try:
            self.root.iconbitmap(str(LOGO_PATH))
        except:
            pass

        self.active_widgets = []  # 已激活的组件列表
        self.light_mode = True  # 当前是否为浅色模式
        self.theme = ThemeColors(light_mode=self.light_mode)  # 主题颜色

        # 创建托盘图标
        self.tray_icon = None
        self.tray_thread = None

        self._create_ui()
        self._create_tray_icon()

    def _load_settings(self):
        """加载设置"""
        data_dir = Path.home() / ".dashwidgets"
        settings_file = data_dir / "settings.json"

        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载设置失败: {e}")
        return {}

    def _apply_system_theme(self):
        """应用系统主题"""
        import platform
        system = platform.system()
        if system == "Darwin":  # macOS
            try:
                import darkdetect
                mode = darkdetect.theme()
                is_dark = mode == "Dark"
                ctk.set_appearance_mode("dark" if is_dark else "light")
                self.light_mode = not is_dark
            except:
                ctk.set_appearance_mode("light")
                self.light_mode = True
        elif system == "Windows":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                is_light = bool(value)
                ctk.set_appearance_mode("dark" if not is_light else "light")
                self.light_mode = is_light
                winreg.CloseKey(key)
            except:
                ctk.set_appearance_mode("light")
                self.light_mode = True
        else:
            ctk.set_appearance_mode("light")
            self.light_mode = True

    def _create_ui(self):
        """创建用户界面 - 现代圆润设计"""
        # 主容器
        main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.theme.bg_main)
        main_container.pack(fill="both", expand=True)

        # 入场动画
        self.root.attributes('-alpha', 0)
        AnimationManager.animate_alpha(self.root, 0, 1, duration=500)

        # 顶部导航栏
        self._create_navbar(main_container)

        # 内容区域（左右分栏）
        content_frame = ctk.CTkFrame(main_container, corner_radius=0, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=24, pady=(16, 16))

        # 左侧：组件库
        self._create_widget_library(content_frame)

        # 右侧：已添加组件列表
        self._create_active_widgets_panel(content_frame)

    def _create_navbar(self, parent):
        """创建顶部导航栏 - 现代圆润设计"""
        nav_bar = ctk.CTkFrame(parent, height=64, corner_radius=0, fg_color=self.theme.bg_nav)
        nav_bar.pack(fill="x")

        # Logo 和标题
        title_container = ctk.CTkFrame(nav_bar, fg_color="transparent")
        title_container.pack(side="left", padx=24, pady=10)

        # Logo
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open(LOGO_PATH),
                dark_image=Image.open(LOGO_PATH),
                size=(40, 40)
            )
            logo_label = ctk.CTkLabel(
                title_container,
                image=logo_image,
                text="",
                width=40,
                height=40
            )
            logo_label.pack(side="left", padx=(0, 12))
        except Exception as e:
            logger.warning(f"加载 logo 失败，使用默认图标: {e}")
            # 如果加载失败，使用备用的 emoji logo
            logo_frame = ctk.CTkFrame(title_container, width=40, height=40, corner_radius=10, fg_color=self.theme.accent)
            logo_frame.pack(side="left", padx=(0, 12))
            logo_frame.pack_propagate(False)

            logo_label = ctk.CTkLabel(
                logo_frame,
                text="🚀",
                font=("Segoe UI Emoji", 22),
                text_color="white"
            )
            logo_label.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(
            title_container,
            text="DashWidgets",
            font=("Microsoft YaHei UI", 22, "bold"),
            text_color=self.theme.text_primary
        )
        title_label.pack(side="left")

        # 右侧功能按钮
        button_container = ctk.CTkFrame(nav_bar, fg_color="transparent")
        button_container.pack(side="right", padx=24, pady=12)

        # 最小化到托盘按钮
        minimize_btn = ctk.CTkButton(
            button_container,
            text="最小化到托盘",
            width=130,
            height=38,
            corner_radius=10,
            font=("Microsoft YaHei UI", 12),
            hover_color=self.theme.hover,
            fg_color=self.theme.bg_button,
            text_color=self.theme.text_primary,
            command=self.minimize_to_tray
        )
        minimize_btn.pack(side="left", padx=6)

        # 设置按钮
        settings_btn = ctk.CTkButton(
            button_container,
            text="⚙ 设置",
            width=110,
            height=38,
            corner_radius=10,
            font=("Microsoft YaHei UI", 12),
            hover_color=self.theme.hover,
            fg_color=self.theme.bg_button,
            text_color=self.theme.text_primary,
            command=self.show_settings_window
        )
        settings_btn.pack(side="left", padx=6)

        # 关于按钮
        about_btn = ctk.CTkButton(
            button_container,
            text="ℹ 关于",
            width=110,
            height=38,
            corner_radius=10,
            font=("Microsoft YaHei UI", 12),
            hover_color=self.theme.hover,
            fg_color=self.theme.bg_button,
            text_color=self.theme.text_primary,
            command=self.show_about_dialog
        )
        about_btn.pack(side="left", padx=6)

    def _create_widget_library(self, parent):
        """创建左侧组件库 - 现代圆润设计"""
        # 组件库框架
        library_frame = ctk.CTkFrame(parent, width=380, corner_radius=16, fg_color=self.theme.bg_card)
        library_frame.pack(side="left", fill="y", padx=(0, 16))
        library_frame.pack_propagate(False)

        # 标题区域
        header_frame = ctk.CTkFrame(library_frame, height=64, fg_color=self.theme.bg_hint, corner_radius=16)
        header_frame.pack(fill="x")

        header_label = ctk.CTkLabel(
            header_frame,
            text="🧩 组件库",
            font=("Microsoft YaHei UI", 17, "bold"),
            text_color=self.theme.text_primary
        )
        header_label.pack(pady=15)

        # 搜索框
        search_frame = ctk.CTkFrame(library_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(10, 5))

        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="搜索组件...",
            height=36,
            corner_radius=8
        )
        search_entry.pack(fill="x")

        # 组件列表（可滚动）
        scrollable_frame = ctk.CTkScrollableFrame(
            library_frame,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=self.theme.border,
            scrollbar_button_hover_color=self.theme.text_hint
        )
        scrollable_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # 添加组件模板
        for template in WIDGET_TEMPLATES:
            self._add_widget_template(scrollable_frame, template)

    def _add_widget_template(self, parent, template):
        """添加组件模板卡片 - 现代圆润设计"""
        card = ctk.CTkFrame(parent, height=100, corner_radius=14, fg_color=self.theme.bg_input, border_width=1, border_color=self.theme.border)
        card.pack(fill="x", pady=10)
        card.pack_propagate(False)

        # 组件图标 - 圆形背景
        icon_bg = ctk.CTkFrame(card, width=56, height=56, corner_radius=14, fg_color=self.theme.accent)
        icon_bg.pack(side="left", padx=16, pady=22)
        icon_bg.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            icon_bg,
            text=template.icon_name,
            font=("Segoe UI Emoji", 26),
            text_color="white"
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # 组件名称和描述
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=8, pady=18, fill="both", expand=True)

        name_label = ctk.CTkLabel(
            info_frame,
            text=template.name,
            font=("Microsoft YaHei UI", 15, "bold"),
            text_color=self.theme.text_primary,
            anchor="w"
        )
        name_label.pack(fill="x", pady=(6, 3))

        desc_label = ctk.CTkLabel(
            info_frame,
            text=template.description,
            font=("Microsoft YaHei UI", 11),
            text_color=self.theme.text_secondary,
            anchor="w"
        )
        desc_label.pack(fill="x", pady=(0, 6))

        # 添加按钮 - 圆形按钮
        add_btn = ctk.CTkButton(
            card,
            text="+",
            width=44,
            height=44,
            corner_radius=12,
            font=("Microsoft YaHei UI", 22, "bold"),
            fg_color=self.theme.accent,
            hover_color=self.theme.hover,
            text_color="white",
            command=lambda t=template: self.create_widget(t)
        )
        add_btn.pack(side="right", padx=16, pady=28)

    def _create_active_widgets_panel(self, parent):
        """创建右侧已添加组件面板 - 现代圆润设计"""
        panel_frame = ctk.CTkFrame(parent, corner_radius=16, fg_color=self.theme.bg_card)
        panel_frame.pack(side="right", fill="both", expand=True)

        # 标题区域
        header_frame = ctk.CTkFrame(panel_frame, height=64, fg_color=self.theme.bg_hint, corner_radius=16)
        header_frame.pack(fill="x")

        header_label = ctk.CTkLabel(
            header_frame,
            text="🖥 已添加组件",
            font=("Microsoft YaHei UI", 17, "bold"),
            text_color=self.theme.text_primary
        )
        header_label.pack(side="left", padx=20, pady=15)

        # 统计信息
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="0 个组件",
            font=("Arial", 12),
            text_color=self.theme.text_secondary
        )
        self.stats_label.pack(side="right", padx=20, pady=15)

        # 提示信息
        hint_frame = ctk.CTkFrame(panel_frame, corner_radius=12, fg_color=self.theme.bg_hint)
        hint_frame.pack(fill="x", padx=20, pady=20)

        hint_label = ctk.CTkLabel(
            hint_frame,
            text="💡 提示：点击左侧组件添加到桌面，添加后可以自由拖拽。右键点击组件可以设置、刷新或关闭。",
            font=("Arial", 11),
            text_color=self.theme.text_secondary,
            wraplength=600
        )
        hint_label.pack(padx=15, pady=10)

        # 组件列表（可滚动）
        self.widgets_list = ctk.CTkScrollableFrame(
            panel_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.widgets_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 欢迎提示
        self.welcome_label = ctk.CTkLabel(
            self.widgets_list,
            text="从左侧组件库添加组件到桌面",
            font=("Arial", 14),
            text_color=self.theme.text_hint
        )
        self.welcome_label.pack(pady=30)

    def create_widget(self, template):
        """创建桌面组件"""
        # 移除欢迎提示
        if hasattr(self, 'welcome_label') and self.welcome_label.winfo_exists():
            self.welcome_label.destroy()

        # 获取当前设置的默认尺寸
        if hasattr(self, 'size_menu'):
            size_map = {"小号": "small", "中号": "medium", "大号": "large"}
            size = size_map.get(self.size_menu.get(), "medium")
        else:
            size = template.size

        # 创建可拖拽的组件，传递主题信息
        widget = DraggableWidget(
            self.root,
            template,
            size=size,
            light_mode=self.light_mode,
            theme_colors=self.theme
        )

        # 在列表中添加记录
        self._add_widget_to_list(template, widget, size)

        self.active_widgets.append(widget)
        self._update_stats()

    def _add_widget_to_list(self, template, widget, size="medium"):
        """在列表中添加组件记录"""
        card = ctk.CTkFrame(self.widgets_list, height=60, corner_radius=8, fg_color=self.theme.bg_input)
        card.pack(fill="x", pady=6)
        card.pack_propagate(False)

        # 图标和名称
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=12, pady=15, fill="both", expand=True)

        icon_name_label = ctk.CTkLabel(
            info_frame,
            text=template.icon_name,
            font=("Segoe UI Emoji", 20)
        )
        icon_name_label.pack(side="left")

        name_label = ctk.CTkLabel(
            info_frame,
            text=template.name,
            font=("Arial", 13),
            text_color=self.theme.text_primary
        )
        name_label.pack(side="left", padx=8)

        # 尺寸标签
        size_map = {"small": "小", "medium": "中", "large": "大"}
        size_label = ctk.CTkLabel(
            info_frame,
            text=f"({size_map.get(size, '中')})",
            font=("Arial", 10),
            text_color=self.theme.text_hint
        )
        size_label.pack(side="left")

        # 操作按钮
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(side="right", padx=12, pady=15)

        # 显示/隐藏按钮
        visibility_btn = ctk.CTkButton(
            button_frame,
            text="👁",
            width=32,
            height=32,
            corner_radius=6,
            font=("Arial", 12),
            fg_color="transparent",
            text_color=self.theme.text_secondary,
            hover_color=self.theme.border
        )
        visibility_btn.pack(side="left", padx=2)

        # 关闭按钮
        close_btn = ctk.CTkButton(
            button_frame,
            text="✕",
            width=32,
            height=32,
            corner_radius=6,
            font=("Arial", 12),
            fg_color="transparent",
            text_color="#FF3B30",
            hover_color="#FFE5E5",
            command=lambda w=widget, c=card: self.remove_widget(w, c)
        )
        close_btn.pack(side="left", padx=2)

    def remove_widget(self, widget, card):
        """移除组件"""
        try:
            # 取消所有待处理的after回调（如果有）
            if hasattr(widget, '_after_ids'):
                for after_id in widget._after_ids:
                    try:
                        self.root.after_cancel(after_id)
                    except:
                        pass
        except:
            pass

        widget.window.destroy()
        card.destroy()
        self.active_widgets.remove(widget)
        self._update_stats()

        # 如果没有组件了，显示欢迎提示
        if len(self.active_widgets) == 0:
            self.welcome_label = ctk.CTkLabel(
                self.widgets_list,
                text="从左侧组件库添加组件到桌面",
                font=("Arial", 14),
                text_color="#999999"
            )
            self.welcome_label.pack(pady=30)

    def _update_stats(self):
        """更新统计信息"""
        self.stats_label.configure(text=f"{len(self.active_widgets)} 个组件")

    def minimize_to_tray(self):
        """最小化到托盘"""
        self.root.withdraw()
        # TODO: 实现系统托盘功能

    def show_settings_window(self):
        """显示设置窗口 - 现代圆润设计"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("580x650")
        settings_window.resizable(False, False)

        # 入场动画
        settings_window.attributes('-alpha', 0)

        container = ctk.CTkFrame(settings_window, corner_radius=0, fg_color=self.theme.bg_main)
        container.pack(fill="both", expand=True)

        # 标题栏
        header_frame = ctk.CTkFrame(container, height=64, fg_color=self.theme.bg_nav, corner_radius=0)
        header_frame.pack(fill="x")

        # Logo 和标题
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(side="left", padx=24, pady=10)

        header_label = ctk.CTkLabel(
            header_content,
            text="⚙ 设置",
            font=("Microsoft YaHei UI", 18, "bold"),
            text_color=self.theme.text_primary
        )
        header_label.pack(side="left")

        # 关闭按钮
        close_btn = ctk.CTkButton(
            header_frame,
            text="✕",
            width=38,
            height=38,
            corner_radius=10,
            font=("Microsoft YaHei UI", 14),
            fg_color="transparent",
            text_color=self.theme.text_secondary,
            hover_color=self.theme.bg_hint,
            command=lambda: self._close_with_animation(settings_window)
        )
        close_btn.pack(side="right", padx=24, pady=13)

        # 设置内容（可滚动）
        scrollable_content = ctk.CTkScrollableFrame(
            container,
            fg_color="transparent",
            corner_radius=0
        )
        scrollable_content.pack(fill="both", expand=True, padx=24, pady=20)

        # 通用设置
        general_frame = ctk.CTkFrame(scrollable_content, corner_radius=16, fg_color=self.theme.bg_card)
        general_frame.pack(fill="x", pady=(0, 16))

        general_label = ctk.CTkLabel(
            general_frame,
            text="🔧 通用设置",
            font=("Microsoft YaHei UI", 15, "bold"),
            text_color=self.theme.text_primary
        )
        general_label.pack(anchor="w", padx=20, pady=(18, 12))

        # 开机自启动
        self.auto_start_switch = ctk.CTkSwitch(
            general_frame,
            text="开机自动启动",
            font=("Microsoft YaHei UI", 12),
            command=self._toggle_auto_start
        )
        self.auto_start_switch.pack(anchor="w", padx=20, pady=6)
        self.auto_start_switch.select() if self._is_auto_start_enabled() else self.auto_start_switch.deselect()

        # 最小化到托盘
        self.tray_switch = ctk.CTkSwitch(
            general_frame,
            text="关闭时最小化到托盘",
            font=("Microsoft YaHei UI", 12)
        )
        self.tray_switch.pack(anchor="w", padx=20, pady=6)

        # 启动时显示主窗口
        startup_show_switch = ctk.CTkSwitch(
            general_frame,
            text="启动时显示主窗口",
            font=("Microsoft YaHei UI", 12)
        )
        startup_show_switch.pack(anchor="w", padx=20, pady=(6, 18))

        # 外观设置
        appearance_frame = ctk.CTkFrame(scrollable_content, corner_radius=16, fg_color=self.theme.bg_card)
        appearance_frame.pack(fill="x", pady=(0, 16))

        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="🎨 外观设置",
            font=("Microsoft YaHei UI", 15, "bold"),
            text_color=self.theme.text_primary
        )
        appearance_label.pack(anchor="w", padx=20, pady=(18, 12))

        # 主题选择
        theme_container = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        theme_container.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(theme_container, text="主题:", font=("Microsoft YaHei UI", 12), text_color=self.theme.text_secondary).pack(side="left")

        self.theme_menu = ctk.CTkOptionMenu(
            theme_container,
            values=["浅色", "深色", "跟随系统"],
            width=160,
            height=38,
            corner_radius=10,
            font=("Microsoft YaHei UI", 12),
            command=self._change_theme
        )
        self.theme_menu.pack(side="right")

        # 字体选择
        font_container = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        font_container.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(font_container, text="字体:", font=("Microsoft YaHei UI", 12), text_color=self.theme.text_secondary).pack(side="left")

        # 获取系统可用字体
        available_fonts = sorted(tkfont.families())

        # 筛选常用的中文字体
        font_options = [
            "系统默认",
            "HarmonyOS Sans SC",
            "HarmonyOS Sans",
            "Microsoft YaHei UI",
            "Microsoft YaHei",
            "SimHei",
            "PingFang SC",
            "STHeiti",
            "KaiTi",
            "FangSong"
        ]

        # 过滤出系统实际存在的字体
        available_font_options = ["系统默认"]
        for font_name in font_options[1:]:
            if font_name in available_fonts:
                available_font_options.append(font_name)

        self.font_menu = ctk.CTkOptionMenu(
            font_container,
            values=available_font_options,
            width=160,
            height=38,
            corner_radius=10,
            font=("Microsoft YaHei UI", 12),
            command=self._change_font
        )
        self.font_menu.pack(side="right")

        # 组件设置
        widget_frame = ctk.CTkFrame(scrollable_content, corner_radius=16, fg_color=self.theme.bg_card)
        widget_frame.pack(fill="x", pady=(0, 16))

        widget_label = ctk.CTkLabel(
            widget_frame,
            text="🧩 组件设置",
            font=("Microsoft YaHei UI", 15, "bold"),
            text_color=self.theme.text_primary
        )
        widget_label.pack(anchor="w", padx=20, pady=(18, 12))

        # 自动刷新间隔
        refresh_container = ctk.CTkFrame(widget_frame, fg_color="transparent")
        refresh_container.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(refresh_container, text="自动刷新间隔:", font=("Microsoft YaHei UI", 12), text_color=self.theme.text_secondary).pack(side="left")

        self.refresh_slider = ctk.CTkSlider(
            refresh_container,
            from_=1,
            to=10,
            number_of_steps=9,
            width=160,
            corner_radius=8
        )
        self.refresh_slider.set(2)
        self.refresh_slider.pack(side="right")

        self.refresh_label = ctk.CTkLabel(
            refresh_container,
            text="2 秒",
            font=("Microsoft YaHei UI", 11),
            text_color=self.theme.text_secondary
        )
        self.refresh_label.pack(side="right", padx=12)

        self.refresh_slider.configure(command=lambda v: self.refresh_label.configure(text=f"{int(v)} 秒"))

        # 组件透明度
        opacity_container = ctk.CTkFrame(widget_frame, fg_color="transparent")
        opacity_container.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(opacity_container, text="组件透明度:", font=("Microsoft YaHei UI", 12), text_color=self.theme.text_secondary).pack(side="left")

        self.opacity_slider = ctk.CTkSlider(
            opacity_container,
            from_=50,
            to=100,
            number_of_steps=10,
            width=160,
            corner_radius=8
        )
        self.opacity_slider.set(90)
        self.opacity_slider.pack(side="right")

        self.opacity_label = ctk.CTkLabel(
            opacity_container,
            text="90%",
            font=("Microsoft YaHei UI", 11),
            text_color=self.theme.text_secondary
        )
        self.opacity_label.pack(side="right", padx=12)

        self.opacity_slider.configure(command=lambda v: self.opacity_label.configure(text=f"{int(v)}%"))

        # 默认组件尺寸
        size_container = ctk.CTkFrame(widget_frame, fg_color="transparent")
        size_container.pack(fill="x", padx=20, pady=(6, 18))

        ctk.CTkLabel(size_container, text="默认组件尺寸:", font=("Microsoft YaHei UI", 12), text_color=self.theme.text_secondary).pack(side="left")

        self.size_menu = ctk.CTkOptionMenu(
            size_container,
            values=["小号", "中号", "大号"],
            width=160,
            height=38,
            corner_radius=10,
            font=("Microsoft YaHei UI", 12)
        )
        self.size_menu.set("中号")
        self.size_menu.pack(side="right")

        # 数据管理
        data_frame = ctk.CTkFrame(scrollable_content, corner_radius=16, fg_color=self.theme.bg_card)
        data_frame.pack(fill="x", pady=(0, 16))

        data_label = ctk.CTkLabel(
            data_frame,
            text="🗂 数据管理",
            font=("Microsoft YaHei UI", 15, "bold"),
            text_color=self.theme.text_primary
        )
        data_label.pack(anchor="w", padx=20, pady=(18, 12))

        # 清除所有组件
        clear_btn = ctk.CTkButton(
            data_frame,
            text="清除所有桌面组件",
            width=220,
            height=40,
            corner_radius=10,
            fg_color=self.theme.error,
            hover_color="#DC2626",
            font=("Microsoft YaHei UI", 12),
            command=self._clear_all_widgets
        )
        clear_btn.pack(anchor="w", padx=20, pady=(6, 18))

        # 关于设置
        about_frame = ctk.CTkFrame(scrollable_content, corner_radius=16, fg_color=self.theme.bg_card)
        about_frame.pack(fill="x", pady=(0, 8))

        about_label = ctk.CTkLabel(
            about_frame,
            text="ℹ 关于",
            font=("Microsoft YaHei UI", 15, "bold"),
            text_color=self.theme.text_primary
        )
        about_label.pack(anchor="w", padx=20, pady=(18, 12))

        version_label = ctk.CTkLabel(
            about_frame,
            text=f"版本: {__version__}",
            font=("Microsoft YaHei UI", 12),
            text_color=self.theme.text_secondary
        )
        version_label.pack(anchor="w", padx=20, pady=6)

        # GitHub 链接
        link_label = ctk.CTkLabel(
            about_frame,
            text="🔗 github.com/Little-Tree-Studio/DashWidgets",
            font=("Microsoft YaHei UI", 11),
            text_color=self.theme.accent,
            cursor="hand2"
        )
        link_label.pack(anchor="w", padx=20, pady=(6, 18))

        # 底部按钮
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x", padx=24, pady=(0, 24))

        # 取消按钮
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="取消",
            width=120,
            height=40,
            corner_radius=10,
            font=("Microsoft YaHei UI", 12),
            fg_color=self.theme.bg_button,
            hover_color=self.theme.border,
            text_color=self.theme.text_primary,
            command=lambda: self._close_with_animation(settings_window)
        )
        cancel_btn.pack(side="right", padx=8)

        # 保存按钮
        save_btn = ctk.CTkButton(
            button_frame,
            text="保存设置",
            width=120,
            height=40,
            corner_radius=10,
            font=("Microsoft YaHei UI", 12, "bold"),
            fg_color=self.theme.accent,
            hover_color=self.theme.hover,
            text_color="white",
            command=lambda: self._save_settings(settings_window)
        )
        save_btn.pack(side="right")

        # 入场动画
        AnimationManager.animate_alpha(settings_window, 0, 1, duration=300)

    def _close_with_animation(self, window):
        """带动画关闭窗口"""
        AnimationManager.animate_alpha(
            window,
            window.attributes('-alpha'),
            0,
            duration=200,
            callback=window.destroy
        )

    def _is_auto_start_enabled(self):
        """检查是否已设置开机自启动"""
        # TODO: 实现真正的开机自启动检查
        return False

    def _toggle_auto_start(self):
        """切换开机自启动状态"""
        is_enabled = self.auto_start_switch.get()
        from tkinter import messagebox

        if is_enabled:
            messagebox.showinfo("开机自启动", "开机自启动功能已启用（示例）")
        else:
            messagebox.showinfo("开机自启动", "开机自启动功能已禁用（示例）")

    def _change_theme(self, choice):
        """更改主题"""
        if choice == "浅色":
            ctk.set_appearance_mode("light")
            self.light_mode = True
            self._apply_theme()
        elif choice == "深色":
            ctk.set_appearance_mode("dark")
            self.light_mode = False
            self._apply_theme()
        else:
            # 跟随系统
            self._apply_system_theme()
            self._apply_theme()

    def _change_font(self, font_name):
        """更改字体"""
        # 设置字体
        if font_name == "系统默认":
            set_font_family("系统默认")
        else:
            set_font_family(font_name)

        logger.info(f"应用字体: {font_name}")

        # 刷新所有桌面组件以应用新字体
        for widget in self.active_widgets:
            try:
                # 保存位置
                x = widget.window.winfo_x()
                y = widget.window.winfo_y()

                # 清除所有内容
                widget.canvas.delete("all")

                # 重新创建组件内容
                widget._create_widget_content(widget.canvas, widget.width, widget.height)

                # 恢复位置
                widget.window.geometry(f"+{x}+{y}")

                # 如果是待办事项组件，需要重新渲染列表
                if widget.template.name == "待办事项":
                    widget._render_todo_list(widget.canvas, widget.width, widget.height)

            except Exception as e:
                logger.warning(f"刷新组件字体时出错: {e}")

        from tkinter import messagebox
        messagebox.showinfo("字体已更改", f"字体已更改为: {font_name}\n所有组件已更新！", parent=self.root)

    def _apply_theme(self):
        """应用主题到所有组件"""
        # 更新主题颜色
        self.theme.set_light_mode(self.light_mode)

        # 重新创建界面以应用新主题
        # 先保存窗口状态
        geometry = self.root.geometry()

        # 清空现有界面
        for widget in self.root.winfo_children():
            widget.destroy()

        # 重新创建UI
        self._create_ui()

        # 恢复窗口大小
        self.root.geometry(geometry)

        # 刷新所有桌面组件的主题
        for widget in self.active_widgets:
            # 通知组件更新主题
            widget.update_theme(self.light_mode, self.theme)

            # 更新组件内文字颜色
            self._update_widget_colors(widget)

    def _clear_all_widgets(self):
        """清除所有桌面组件"""
        from tkinter import messagebox

        if messagebox.askyesno("确认", "确定要清除所有桌面组件吗？", parent=self.root):
            for widget in self.active_widgets[:]:
                try:
                    widget.window.destroy()
                except Exception:
                    pass
            self.active_widgets.clear()
            self._update_stats()

            # 清空组件列表
            for child in self.widgets_list.winfo_children():
                if hasattr(child, 'winfo_class') and child.winfo_class() == 'CTkFrame':
                    child.destroy()

            # 显示欢迎提示
            if len(self.active_widgets) == 0:
                self.welcome_label = ctk.CTkLabel(
                    self.widgets_list,
                    text="从左侧组件库添加组件到桌面",
                    font=("Arial", 14),
                    text_color="#999999"
                )
                self.welcome_label.pack(pady=30)

            messagebox.showinfo("成功", "已清除所有桌面组件")

    def _save_settings(self, settings_window):
        """保存设置"""
        font_name = self.font_menu.get() if hasattr(self, 'font_menu') else "系统默认"

        settings = {
            "auto_start": self.auto_start_switch.get(),
            "theme": self.theme_menu.get(),
            "refresh_interval": int(self.refresh_slider.get()),
            "opacity": int(self.opacity_slider.get()),
            "font": font_name
        }

        # 创建数据目录
        data_dir = Path.home() / ".dashwidgets"
        data_dir.mkdir(exist_ok=True)

        # 保存设置到文件
        settings_file = data_dir / "settings.json"
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            logger.info(f"保存设置: {settings}")

            from tkinter import messagebox
            messagebox.showinfo("设置已保存", "设置已成功保存！", parent=settings_window)
        except Exception as e:
            logger.error(f"保存设置失败: {e}")
            from tkinter import messagebox
            messagebox.showerror("错误", f"保存设置失败: {e}", parent=settings_window)

        settings_window.destroy()

    def _update_widget_colors(self, widget):
        """更新桌面组件的颜色以匹配液态玻璃主题"""
        if not hasattr(widget, 'canvas'):
            return

        # 更新时钟组件
        if widget.template.name == "时钟":
            text_color = self.theme.text_primary if self.light_mode else "#F1F5F9"
            if hasattr(widget, 'time_text'):
                widget.canvas.itemconfig(widget.time_text, fill=text_color)

        # 更新待办事项组件
        elif widget.template.name == "待办事项":
            # 重新渲染待办列表
            widget._render_todo_list(widget.canvas, widget.width, widget.height)

    def show_about_dialog(self):
        """显示关于对话框 - 现代圆润设计"""
        about_window = ctk.CTkToplevel(self.root)
        about_window.title("关于 DashWidgets")
        about_window.geometry("450x500")
        about_window.resizable(False, False)

        # 入场动画
        about_window.attributes('-alpha', 0)

        container = ctk.CTkFrame(about_window, corner_radius=0, fg_color=self.theme.bg_main)
        container.pack(fill="both", expand=True)

        # Logo - 圆形背景
        logo_frame = ctk.CTkFrame(container, width=96, height=96, corner_radius=24, fg_color=self.theme.accent)
        logo_frame.pack(pady=(32, 24))
        logo_frame.pack_propagate(False)

        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open(LOGO_PATH),
                dark_image=Image.open(LOGO_PATH),
                size=(64, 64)
            )
            logo_label = ctk.CTkLabel(
                logo_frame,
                image=logo_image,
                text="",
                width=64,
                height=64
            )
            logo_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            # 备用 emoji
            logo_label = ctk.CTkLabel(
                logo_frame,
                text="📦",
                font=("Segoe UI Emoji", 48),
                text_color="white"
            )
            logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # 标题
        title_label = ctk.CTkLabel(
            container,
            text="DashWidgets",
            font=("Microsoft YaHei UI", 28, "bold"),
            text_color=self.theme.text_primary
        )
        title_label.pack(pady=(0, 6))

        # 版本
        version_label = ctk.CTkLabel(
            container,
            text=f"版本 {__version__}",
            font=("Microsoft YaHei UI", 13),
            text_color=self.theme.text_secondary
        )
        version_label.pack(pady=(0, 8))

        # 装饰性分隔线
        separator_frame = ctk.CTkFrame(container, height=1, fg_color=self.theme.border)
        separator_frame.pack(fill="x", padx=60, pady=(8, 24))

        # 描述
        desc_label = ctk.CTkLabel(
            container,
            text="一个类似 macOS Dashboard 的\n桌面小组件管理器",
            font=("Microsoft YaHei UI", 12),
            text_color=self.theme.text_primary,
            justify="center"
        )
        desc_label.pack(pady=(0, 24))

        # 信息卡片
        info_frame = ctk.CTkFrame(container, corner_radius=12, fg_color=self.theme.bg_card)
        info_frame.pack(fill="x", padx=40, pady=(0, 16))

        # 开发者信息
        dev_label = ctk.CTkLabel(
            info_frame,
            text=f"👨‍💻 开发: Little Tree Studio",
            font=("Microsoft YaHei UI", 11),
            text_color=self.theme.text_secondary
        )
        dev_label.pack(pady=(12, 6))

        # 官网信息
        web_label = ctk.CTkLabel(
            info_frame,
            text=f"🌐 官网: {__website__}",
            font=("Microsoft YaHei UI", 11),
            text_color=self.theme.text_secondary
        )
        web_label.pack(pady=6)

        # GitHub 链接
        github_label = ctk.CTkLabel(
            info_frame,
            text="🔗 GitHub: github.com/Little-Tree-Studio/DashWidgets",
            font=("Microsoft YaHei UI", 10),
            text_color=self.theme.accent,
            cursor="hand2"
        )
        github_label.pack(pady=(6, 12))

        # 版权信息
        copyright_label = ctk.CTkLabel(
            container,
            text=f"© 2025 Little Tree Studio.\nAll rights reserved.",
            font=("Microsoft YaHei UI", 10),
            text_color=self.theme.text_hint,
            justify="center"
        )
        copyright_label.pack(pady=(8, 24))

        # 关闭按钮
        close_btn = ctk.CTkButton(
            container,
            text="关闭",
            width=140,
            height=42,
            corner_radius=12,
            font=("Microsoft YaHei UI", 12, "bold"),
            fg_color=self.theme.accent,
            hover_color=self.theme.hover,
            text_color="white",
            command=lambda: self._close_with_animation(about_window)
        )
        close_btn.pack(pady=(0, 32))

        # 入场动画
        AnimationManager.animate_alpha(about_window, 0, 1, duration=300)

    def _create_tray_icon(self):
        """创建系统托盘图标"""
        try:
            # 创建简单的托盘图标
            from pystray import Icon, Menu, MenuItem

            # 创建图标图片
            icon_image = self._create_tray_image()

            # 定义菜单项
            def show_window(icon, item):
                _ = icon  # 未使用，保留以兼容接口
                _ = item  # 未使用，保留以兼容接口
                self.root.deiconify()
                self.root.lift()

            def hide_window(icon, item):
                _ = icon  # 未使用，保留以兼容接口
                _ = item  # 未使用，保留以兼容接口
                self.root.withdraw()

            def quit_app(icon, item):
                _ = item  # 未使用，保留以兼容接口
                self.root.quit()
                icon.stop()

            # 创建菜单
            menu = Menu(
                MenuItem('显示', show_window),
                MenuItem('隐藏', hide_window),
                Menu.SEPARATOR,
                MenuItem('退出', quit_app)
            )

            # 创建托盘图标
            self.tray_icon = Icon(
                'DashWidgets',
                icon_image,
                'DashWidgets',
                menu
            )

            # 在新线程中运行托盘图标
            self.tray_thread = threading.Thread(
                target=self.tray_icon.run,
                daemon=True
            )
            self.tray_thread.start()

            logger.info("系统托盘图标已创建")

        except Exception as e:
            logger.warning(f"创建托盘图标失败: {e}")

    def _create_tray_image(self):
        """创建托盘图标图片"""
        try:
            # 尝试使用logo图标
            if LOGO_PATH.exists():
                return Image.open(str(LOGO_PATH))
        except:
            pass

        # 如果没有logo，创建简单的图标
        image = Image.new('RGB', (64, 64), color='#007AFF')

        # 简单的"DW"文字
        draw = ImageDraw.Draw(image)

        # 绘制圆角矩形背景
        draw.rounded_rectangle([0, 0, 64, 64], radius=12, fill='#007AFF')

        # 绘制文字
        try:
            font_path = FONTS_PATH / "HarmonyOS_Sans_SC_Regular.ttf"
            if font_path.exists():
                font = ImageFont.truetype(str(font_path), 24)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        text = "DW"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (64 - text_width) // 2
        y = (64 - text_height) // 2

        draw.text((x, y), text, font=font, fill='white')

        return image

    def run(self):
        """运行应用"""
        try:
            self.root.mainloop()
        finally:
            # 清理托盘图标
            if self.tray_icon:
                try:
                    self.tray_icon.stop()
                except Exception as e:
                    logger.warning(f"停止托盘图标时出错: {e}")


def main_window():
    """创建并运行主窗口"""
    app = DashWidgetsApp()
    app.run()


if __name__ == "__main__":
    load_fonts()
    main_window()
