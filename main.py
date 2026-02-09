# =============================================================================
# Copyright (c) 2025 Little Tree Studio
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
@copyright: Copyright (c) 2025 Little Tree Studio. All rights reserved.
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



__author__ = "Little Tree Studio"
__copyright__ = "Copyright (c) 2025 Little Tree Studio"
__license__ = "EPL-2.0"
__version__ = "1.0.0"
__maintainer__ = "Little Tree Studio"
__email__ = "studio@zsxiaoshu.cn"
__status__ = "Development"  # Development/Testing/Production
__project__ = "DashWidgets"
__repository__ = "https://github.com/Little-Tree-Studio/DashWidgets"
__website__ = "https://zsxiaoshu.cn/"


import customtkinter as ctk
import tkinter as tk
from loguru import logger
from app.path import LOGO_PATH, ICONS_PATH
import datetime
import random
from PIL import Image
import threading


class ThemeColors:
    """主题颜色配置"""
    def __init__(self, light_mode=True):
        self.light_mode = light_mode
        self._update_colors()

    def set_light_mode(self, light_mode):
        self.light_mode = light_mode
        self._update_colors()

    def _update_colors(self):
        if self.light_mode:
            # 浅色主题
            self.bg_main = "#F5F5F7"           # 主背景
            self.bg_card = "#FFFFFF"            # 卡片背景
            self.bg_nav = "#FFFFFF"             # 导航栏背景
            self.bg_hint = "#F0F0F0"           # 提示框背景
            self.bg_input = "#F8F9FA"          # 输入框背景
            self.text_primary = "#333333"          # 主要文字
            self.text_secondary = "#666666"       # 次要文字
            self.text_hint = "#999999"            # 提示文字
            self.border = "#E0E0E0"             # 边框颜色
            self.accent = "#007AFF"              # 强调色
        else:
            # 深色主题
            self.bg_main = "#1C1C1E"           # 主背景
            self.bg_card = "#2C2C2E"           # 卡片背景
            self.bg_nav = "#2C2C2E"            # 导航栏背景
            self.bg_hint = "#3A3A3C"           # 提示框背景
            self.bg_input = "#3A3A3C"          # 输入框背景
            self.text_primary = "#FFFFFF"          # 主要文字
            self.text_secondary = "#A1A1A6"      # 次要文字
            self.text_hint = "#8E8E93"           # 提示文字
            self.border = "#38383A"             # 边框颜色
            self.accent = "#0A84FF"              # 强调色


def load_fonts():
    """加载自定义字体"""
    try:
        ctk.CTkFont("HarmonyOS Sans SC")
        logger.info("Font loaded: HarmonyOS Sans SC Regular")
    except:
        logger.warning("Font not found, using default font")


# 全局字体设置
current_font_family = None

def get_font(size, bold=False):
    """获取字体，支持自定义字体"""
    global current_font_family

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
    if current_font_family:
        font_family = current_font_family
    else:
        # 尝试找到可用的字体
        import tkinter as tk
        available_fonts = tk.font.families()
        for font_name in font_names:
            if font_name in available_fonts:
                font_family = font_name
                break

    weight = "bold" if bold else "normal"
    return (font_family, size, weight)

def set_font_family(font_name):
    """设置全局字体"""
    global current_font_family
    current_font_family = font_name


class WidgetTemplate:
    """组件模板基类"""
    def __init__(self, name, description, icon_name, size="medium"):
        self.name = name
        self.description = description
        self.icon_name = icon_name
        self.size = size  # small, medium, large

    def get_size_dimensions(self):
        """获取组件尺寸"""
        size_map = {
            "small": (150, 150),
            "medium": (200, 200),
            "large": (300, 300)
        }
        return size_map.get(self.size, (200, 200))


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


class DraggableWidget:
    """可拖拽的桌面小组件"""

    def __init__(self, parent, template, x=100, y=100, size="medium"):
        self.template = template
        self.x = x
        self.y = y
        self.size = size  # 自定义尺寸
        self.resizing = False
        self.resize_edge = None  # 'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'

        # 根据组件大小设置尺寸
        if size == "small":
            width, height = 150, 150
        elif size == "medium":
            width, height = 200, 200
        elif size == "large":
            width, height = 300, 300
        else:  # 使用模板默认尺寸
            width, height = template.get_size_dimensions()

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
        self.window.geometry(f"+{x}+{y}")
        self.window.resizable(False, False)

        # 待办事项数据
        if template.name == "待办事项":
            self.todos = [["完成项目设计", False], ["准备会议材料", False], ["回复邮件", False]]

        # 使用 Canvas 作为主容器
        self.canvas = tk.Canvas(
            self.window,
            width=width,
            height=height,
            bg="#FFFFFF",
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        self.canvas.pack(fill="both", expand=True)

        # 创建组件内容
        self._create_widget_content(self.canvas, width, height)

        # 拖拽和调整大小相关变量
        self._start_x = 0
        self._start_y = 0
        self._start_width = 0
        self._start_height = 0
        self._start_window_x = 0
        self._start_window_y = 0

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<Motion>", self._on_motion)

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
        self.context_menu.add_command(label="关闭", command=self.window.destroy)

        self.window.bind("<Button-3>", self._show_context_menu)  # Windows
        self.window.bind("<Button-2>", self._show_context_menu)  # macOS

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
        """创建时钟组件"""
        # 根据组件大小计算字体大小
        icon_size = int(width * 0.2)
        time_size = int(width * 0.12)
        date_size = int(width * 0.05)

        # 时钟图标
        canvas.create_text(width//2, height//3, text=self.template.icon_name, font=("Segoe UI Emoji", icon_size))

        # 时间
        self.time_text = canvas.create_text(
            width//2, height//2 + height//10,
            text=datetime.datetime.now().strftime("%H:%M:%S"),
            font=get_font(time_size, bold=True),
            fill="#333333"
        )

        # 日期
        canvas.create_text(
            width//2, height - height//7,
            text=datetime.datetime.now().strftime("%Y年%m月%d日"),
            font=get_font(date_size),
            fill="#666666"
        )

        # 定时更新
        self._update_clock()

    def _update_clock(self):
        """更新时钟"""
        if hasattr(self, 'time_text'):
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                self.canvas.itemconfig(self.time_text, text=current_time)
            except:
                pass
            self.window.after(1000, self._update_clock)

    def _create_weather_widget(self, canvas, width, height):
        """创建天气组件"""
        # 根据组件大小计算字体大小
        icon_size = int(width * 0.25)
        temp_size = int(width * 0.14)
        desc_size = int(width * 0.06)
        loc_size = int(width * 0.05)

        # 天气图标
        canvas.create_text(width//2, height//3, text=self.template.icon_name, font=("Segoe UI Emoji", icon_size))

        # 温度
        canvas.create_text(
            width//2, height//2 + height//15,
            text="25°C",
            font=get_font(temp_size, bold=True),
            fill="#FF6B35"
        )

        # 天气描述
        canvas.create_text(
            width//2, height//2 + height//6,
            text="晴朗",
            font=get_font(desc_size),
            fill="#666666"
        )

        # 地点
        canvas.create_text(
            width//2, height - height//10,
            text="📍 北京市",
            font=get_font(loc_size),
            fill="#999999"
        )

    def _create_todo_widget(self, canvas, width, height):
        """创建待办事项组件"""
        # 根据组件大小计算字体和位置
        title_size = int(width * 0.07)
        title_y = int(height * 0.1)
        line_y = int(height * 0.15)
        btn_height = int(height * 0.08)
        btn_y = height - btn_height - int(height * 0.05)
        btn_text_size = int(width * 0.04)

        # 标题
        canvas.create_text(
            width//2, title_y,
            text="📝 待办事项",
            font=get_font(title_size, bold=True),
            fill="#333333"
        )

        # 分隔线
        margin = int(width * 0.1)
        canvas.create_line(margin, line_y, width-margin, line_y, fill="#E0E0E0", width=1)

        # 待办事项列表
        self._render_todo_list(canvas, width, height)

        # 添加按钮
        btn_width = int(width * 0.4)
        canvas.create_rectangle(
            width//2 - btn_width//2, btn_y,
            width//2 + btn_width//2, btn_y + btn_height,
            fill="#007AFF",
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

        y_pos = start_y
        for i, (todo, completed) in enumerate(self.todos):
            # 待办事项文本
            text = f"☑ {todo}" if completed else f"☐ {todo}"
            color = "#999999" if completed else "#333333"

            todo_text = canvas.create_text(
                margin, y_pos,
                text=text,
                font=get_font(font_size),
                fill=color,
                anchor="w",
                tags=("todo_item", f"todo_{i}")
            )

            # 绑定点击事件
            canvas.tag_bind(todo_text, "<Button-1>", lambda e, idx=i: self._toggle_todo(idx))

            y_pos += line_height

    def _add_todo(self, event=None):
        """添加新的待办事项"""
        from tkinter import simpledialog

        new_todo = simpledialog.askstring(
            "添加待办事项",
            "请输入待办事项:",
            parent=self.window
        )

        if new_todo and new_todo.strip():
            self.todos.append([new_todo.strip(), False])
            self._render_todo_list(self.canvas, self.width, self.height)

    def _toggle_todo(self, index):
        """切换待办事项完成状态"""
        if 0 <= index < len(self.todos):
            self.todos[index][1] = not self.todos[index][1]
            self._render_todo_list(self.canvas, self.width, self.height)

    def _delete_todo(self, index):
        """删除待办事项"""
        if 0 <= index < len(self.todos):
            self.todos.pop(index)
            self._render_todo_list(self.canvas, self.width, self.height)

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
        # TODO: 实现持久化保存到文件或数据库
        from tkinter import messagebox
        messagebox.showinfo("笔记已保存", "笔记内容已保存！", parent=self.window)

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
        # TODO: 使用 psutil 获取真实数据
        return random.randint(20, 80)

    def _get_memory_usage(self):
        """获取内存使用率（模拟）"""
        # TODO: 使用 psutil 获取真实数据
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

        except:
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

        # 检测鼠标在哪个边缘
        edge = None
        if y < m:
            edge = 'n' if x < m else 's' if x > h - m else 'n'
        elif y > h - m:
            edge = 's' if x < m else 's' if x > w - m else 's'
        elif x < m:
            edge = 'w'
        elif x > w - m:
            edge = 'e'

        # 检测角落
        if x < m and y < m:
            edge = 'nw'
        elif x > w - m and y < m:
            edge = 'ne'
        elif x < m and y > h - m:
            edge = 'sw'
        elif x > w - m and y > h - m:
            edge = 'se'

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
        """显示设置"""
        pass

    def _reset_size(self):
        """重置组件大小到预设值"""
        size_map = {
            "small": (150, 150),
            "medium": (200, 200),
            "large": (300, 300)
        }

        target_width, target_height = size_map.get(self.size, (200, 200))

        # 获取当前窗口位置
        current_x = self.window.winfo_x()
        current_y = self.window.winfo_y()

        # 计算居中位置
        new_x = current_x + (self.width - target_width) // 2
        new_y = current_y + (self.height - target_height) // 2

        # 更新尺寸
        self.width = target_width
        self.height = target_height

        # 更新窗口
        self.window.geometry(f"{target_width}x{target_height}+{new_x}+{new_y}")
        self.canvas.config(width=target_width, height=target_height)

        # 更新调整区域
        self._update_resize_handlers()

        # 重新创建内容
        self.canvas.delete("all")
        self._create_widget_content(self.canvas, target_width, target_height)

    def _refresh(self):
        """刷新组件"""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self._create_widget_content(self.canvas, width, height)


class DashWidgetsApp:
    """主应用程序类"""

    def __init__(self):
        # 设置外观
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # 创建主窗口（控制面板）
        self.root = ctk.CTk()
        self.root.title("DashWidgets 控制面板")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        self.root.minsize(900, 500)

        try:
            self.root.iconbitmap(str(LOGO_PATH))
        except:
            pass

        self.active_widgets = []  # 已激活的组件列表
        self.light_mode = True  # 当前是否为浅色模式
        self.theme = ThemeColors(light_mode=True)  # 主题颜色

        # 创建托盘图标
        self.tray_icon = None
        self.tray_thread = None

        self._create_ui()
        self._create_tray_icon()

    def _create_ui(self):
        """创建用户界面"""
        # 主容器
        main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.theme.bg_main)
        main_container.pack(fill="both", expand=True)

        # 顶部导航栏
        self._create_navbar(main_container)

        # 内容区域（左右分栏）
        content_frame = ctk.CTkFrame(main_container, corner_radius=0, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        # 左侧：组件库
        self._create_widget_library(content_frame)

        # 右侧：已添加组件列表
        self._create_active_widgets_panel(content_frame)

    def _create_navbar(self, parent):
        """创建顶部导航栏"""
        nav_bar = ctk.CTkFrame(parent, height=56, corner_radius=0, fg_color=self.theme.bg_nav)
        nav_bar.pack(fill="x")

        # Logo 和标题
        title_container = ctk.CTkFrame(nav_bar, fg_color="transparent")
        title_container.pack(side="left", padx=20, pady=8)

        title_label = ctk.CTkLabel(
            title_container,
            text="DashWidgets",
            font=("Arial", 20, "bold"),
            text_color=self.theme.accent
        )
        title_label.pack(side="left")

        # 右侧功能按钮
        button_container = ctk.CTkFrame(nav_bar, fg_color="transparent")
        button_container.pack(side="right", padx=20, pady=8)

        # 最小化到托盘按钮
        minimize_btn = ctk.CTkButton(
            button_container,
            text="最小化到托盘",
            width=120,
            height=36,
            corner_radius=8,
            command=self.minimize_to_tray
        )
        minimize_btn.pack(side="left", padx=5)

        # 设置按钮
        settings_btn = ctk.CTkButton(
            button_container,
            text="设置",
            width=100,
            height=36,
            corner_radius=8,
            command=self.show_settings_window
        )
        settings_btn.pack(side="left", padx=5)

        # 关于按钮
        about_btn = ctk.CTkButton(
            button_container,
            text="关于",
            width=100,
            height=36,
            corner_radius=8,
            command=self.show_about_dialog
        )
        about_btn.pack(side="left", padx=5)

    def _create_widget_library(self, parent):
        """创建左侧组件库"""
        # 组件库框架
        library_frame = ctk.CTkFrame(parent, width=350, corner_radius=12, fg_color=self.theme.bg_card)
        library_frame.pack(side="left", fill="y", padx=(0, 10))
        library_frame.pack_propagate(False)

        # 标题
        header_frame = ctk.CTkFrame(library_frame, height=56, fg_color=self.theme.bg_hint, corner_radius=0)
        header_frame.pack(fill="x")

        header_label = ctk.CTkLabel(
            header_frame,
            text="🧩 组件库",
            font=("Arial", 16, "bold"),
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
        """添加组件模板卡片"""
        card = ctk.CTkFrame(parent, height=90, corner_radius=10, fg_color=self.theme.bg_input)
        card.pack(fill="x", pady=8)
        card.pack_propagate(False)

        # 组件图标
        icon_label = ctk.CTkLabel(
            card,
            text=template.icon_name,
            font=("Segoe UI Emoji", 28),
            width=50
        )
        icon_label.pack(side="left", padx=12, pady=20)

        # 组件名称和描述
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=5, pady=15, fill="both", expand=True)

        name_label = ctk.CTkLabel(
            info_frame,
            text=template.name,
            font=("Arial", 14, "bold"),
            text_color=self.theme.text_primary,
            anchor="w"
        )
        name_label.pack(fill="x", pady=(5, 2))

        desc_label = ctk.CTkLabel(
            info_frame,
            text=template.description,
            font=("Arial", 11),
            text_color=self.theme.text_secondary,
            anchor="w"
        )
        desc_label.pack(fill="x", pady=(0, 5))

        # 添加按钮
        add_btn = ctk.CTkButton(
            card,
            text="+",
            width=36,
            height=36,
            corner_radius=8,
            font=("Arial", 18, "bold"),
            command=lambda t=template: self.create_widget(t)
        )
        add_btn.pack(side="right", padx=12, pady=27)

    def _create_active_widgets_panel(self, parent):
        """创建右侧已添加组件面板"""
        panel_frame = ctk.CTkFrame(parent, corner_radius=12, fg_color=self.theme.bg_card)
        panel_frame.pack(side="right", fill="both", expand=True)

        # 标题栏
        header_frame = ctk.CTkFrame(panel_frame, height=56, fg_color=self.theme.bg_hint, corner_radius=0)
        header_frame.pack(fill="x")

        header_label = ctk.CTkLabel(
            header_frame,
            text="🖥 已添加组件",
            font=("Arial", 16, "bold"),
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

        # 创建可拖拽的组件，使用自定义尺寸
        widget = DraggableWidget(self.root, template, size=size)

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
        """显示设置窗口"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("550x600")
        settings_window.resizable(False, False)

        container = ctk.CTkFrame(settings_window, corner_radius=0, fg_color=self.theme.bg_main)
        container.pack(fill="both", expand=True)

        # 标题
        header_frame = ctk.CTkFrame(container, height=56, fg_color=self.theme.bg_nav, corner_radius=0)
        header_frame.pack(fill="x")

        header_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ 设置",
            font=("Arial", 18, "bold"),
            text_color=self.theme.text_primary
        )
        header_label.pack(pady=15)

        # 设置内容（可滚动）
        scrollable_content = ctk.CTkScrollableFrame(
            container,
            fg_color="transparent",
            corner_radius=0
        )
        scrollable_content.pack(fill="both", expand=True, padx=20, pady=20)

        # 通用设置
        general_frame = ctk.CTkFrame(scrollable_content, corner_radius=12, fg_color=self.theme.bg_card)
        general_frame.pack(fill="x", pady=(0, 15))

        general_label = ctk.CTkLabel(
            general_frame,
            text="通用设置",
            font=("Arial", 14, "bold"),
            text_color=self.theme.text_primary
        )
        general_label.pack(anchor="w", padx=15, pady=(15, 10))

        # 开机自启动
        self.auto_start_switch = ctk.CTkSwitch(
            general_frame,
            text="开机自动启动",
            font=("Arial", 12),
            command=self._toggle_auto_start
        )
        self.auto_start_switch.pack(anchor="w", padx=15, pady=5)
        self.auto_start_switch.select() if self._is_auto_start_enabled() else self.auto_start_switch.deselect()

        # 最小化到托盘
        self.tray_switch = ctk.CTkSwitch(
            general_frame,
            text="关闭时最小化到托盘",
            font=("Arial", 12)
        )
        self.tray_switch.pack(anchor="w", padx=15, pady=5)

        # 启动时显示主窗口
        startup_show_switch = ctk.CTkSwitch(
            general_frame,
            text="启动时显示主窗口",
            font=("Arial", 12)
        )
        startup_show_switch.pack(anchor="w", padx=15, pady=5)

        # 外观设置
        appearance_frame = ctk.CTkFrame(scrollable_content, corner_radius=12, fg_color=self.theme.bg_card)
        appearance_frame.pack(fill="x", pady=(0, 15))

        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="外观设置",
            font=("Arial", 14, "bold"),
            text_color=self.theme.text_primary
        )
        appearance_label.pack(anchor="w", padx=15, pady=(15, 10))

        # 主题选择
        theme_container = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        theme_container.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(theme_container, text="主题:", font=("Arial", 12)).pack(side="left")

        self.theme_menu = ctk.CTkOptionMenu(
            theme_container,
            values=["浅色", "深色", "跟随系统"],
            width=150,
            height=32,
            corner_radius=6,
            command=self._change_theme
        )
        self.theme_menu.pack(side="right")

        # 字体选择
        font_container = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        font_container.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(font_container, text="字体:", font=("Arial", 12)).pack(side="left")

        # 获取系统可用字体
        import tkinter as tk
        available_fonts = sorted(tk.font.families())

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
            width=150,
            height=32,
            corner_radius=6,
            command=self._change_font
        )
        self.font_menu.pack(side="right")

        # 组件设置
        widget_frame = ctk.CTkFrame(scrollable_content, corner_radius=12, fg_color=self.theme.bg_card)
        widget_frame.pack(fill="x", pady=(0, 15))

        widget_label = ctk.CTkLabel(
            widget_frame,
            text="组件设置",
            font=("Arial", 14, "bold"),
            text_color=self.theme.text_primary
        )
        widget_label.pack(anchor="w", padx=15, pady=(15, 10))

        # 自动刷新间隔
        refresh_container = ctk.CTkFrame(widget_frame, fg_color="transparent")
        refresh_container.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(refresh_container, text="自动刷新间隔:", font=("Arial", 12)).pack(side="left")

        self.refresh_slider = ctk.CTkSlider(
            refresh_container,
            from_=1,
            to=10,
            number_of_steps=9,
            width=150
        )
        self.refresh_slider.set(2)
        self.refresh_slider.pack(side="right")

        self.refresh_label = ctk.CTkLabel(
            refresh_container,
            text="2 秒",
            font=("Arial", 11),
            text_color=self.theme.text_secondary
        )
        self.refresh_label.pack(side="right", padx=10)

        self.refresh_slider.configure(command=lambda v: self.refresh_label.configure(text=f"{int(v)} 秒"))

        # 组件透明度
        opacity_container = ctk.CTkFrame(widget_frame, fg_color="transparent")
        opacity_container.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(opacity_container, text="组件透明度:", font=("Arial", 12)).pack(side="left")

        self.opacity_slider = ctk.CTkSlider(
            opacity_container,
            from_=50,
            to=100,
            number_of_steps=10,
            width=150
        )
        self.opacity_slider.set(90)
        self.opacity_slider.pack(side="right")

        self.opacity_label = ctk.CTkLabel(
            opacity_container,
            text="90%",
            font=("Arial", 11),
            text_color=self.theme.text_secondary
        )
        self.opacity_label.pack(side="right", padx=10)

        self.opacity_slider.configure(command=lambda v: self.opacity_label.configure(text=f"{int(v)}%"))

        # 默认组件尺寸
        size_container = ctk.CTkFrame(widget_frame, fg_color="transparent")
        size_container.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(size_container, text="默认组件尺寸:", font=("Arial", 12)).pack(side="left")

        self.size_menu = ctk.CTkOptionMenu(
            size_container,
            values=["小号", "中号", "大号"],
            width=150,
            height=32,
            corner_radius=6
        )
        self.size_menu.set("中号")
        self.size_menu.pack(side="right")

        # 数据管理
        data_frame = ctk.CTkFrame(scrollable_content, corner_radius=12, fg_color=self.theme.bg_card)
        data_frame.pack(fill="x", pady=(0, 15))

        data_label = ctk.CTkLabel(
            data_frame,
            text="数据管理",
            font=("Arial", 14, "bold"),
            text_color=self.theme.text_primary
        )
        data_label.pack(anchor="w", padx=15, pady=(15, 10))

        # 清除所有组件
        clear_btn = ctk.CTkButton(
            data_frame,
            text="清除所有桌面组件",
            width=200,
            height=36,
            corner_radius=8,
            fg_color="#FF3B30",
            hover_color="#C8302A",
            command=self._clear_all_widgets
        )
        clear_btn.pack(anchor="w", padx=15, pady=5)

        # 关于设置
        about_frame = ctk.CTkFrame(scrollable_content, corner_radius=12, fg_color=self.theme.bg_card)
        about_frame.pack(fill="x")

        about_label = ctk.CTkLabel(
            about_frame,
            text="关于",
            font=("Arial", 14, "bold"),
            text_color=self.theme.text_primary
        )
        about_label.pack(anchor="w", padx=15, pady=(15, 10))

        version_label = ctk.CTkLabel(
            about_frame,
            text=f"版本: {__version__}",
            font=("Arial", 12),
            text_color=self.theme.text_secondary
        )
        version_label.pack(anchor="w", padx=15, pady=5)

        # GitHub 链接
        link_label = ctk.CTkLabel(
            about_frame,
            text="🔗 GitHub: github.com/Little-Tree-Studio/DashWidgets",
            font=("Arial", 10),
            text_color=self.theme.accent,
            cursor="hand2"
        )
        link_label.pack(anchor="w", padx=15, pady=5)

        # 保存按钮
        save_btn = ctk.CTkButton(
            container,
            text="保存设置",
            width=120,
            height=36,
            corner_radius=8,
            command=lambda: self._save_settings(settings_window)
        )
        save_btn.pack(side="bottom", pady=20)

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
            import platform
            system = platform.system()
            if system == "Darwin":  # macOS
                try:
                    import darkdetect
                    mode = darkdetect.theme()
                    is_dark = mode == "Dark"
                    ctk.set_appearance_mode("dark" if is_dark else "light")
                    self.light_mode = not is_dark
                    self._apply_theme()
                except:
                    ctk.set_appearance_mode("light")
                    self.light_mode = True
                    self._apply_theme()
            elif system == "Windows":
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                    value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                    is_light = bool(value)
                    ctk.set_appearance_mode("dark" if not is_light else "light")
                    self.light_mode = is_light
                    self._apply_theme()
                    winreg.CloseKey(key)
                except:
                    ctk.set_appearance_mode("light")
                    self.light_mode = True
                    self._apply_theme()
            else:
                ctk.set_appearance_mode("light")
                self.light_mode = True
                self._apply_theme()

    def _change_font(self, font_name):
        """更改字体"""
        global current_font_family

        if font_name == "系统默认":
            set_font_family(None)
        else:
            set_font_family(font_name)

        # 重新创建所有桌面组件以应用新字体
        for widget in self.active_widgets:
            try:
                # 保存当前窗口位置和大小
                x = widget.window.winfo_x()
                y = widget.window.winfo_y()
                width = widget.width
                height = widget.height

                # 销毁旧组件
                widget.window.destroy()

                # 重新创建组件
                new_widget = DraggableWidget(self.root, widget.template, x, y, widget.size)
                new_widget.width = width
                new_widget.height = height
                new_widget.window.geometry(f"{width}x{height}+{x}+{y}")
                new_widget.canvas.config(width=width, height=height)

                # 更新引用
                widget_list_index = self.active_widgets.index(widget)
                self.active_widgets[widget_list_index] = new_widget

                # 更新列表中的引用（需要找到对应的卡片并更新）
                # 这里简化处理，用户可以手动关闭并重新添加组件
            except Exception as e:
                logger.warning(f"重新创建组件时出错: {e}")
                ctk.set_appearance_mode("light")
                self.light_mode = True
                self._apply_theme()
            else:
                    ctk.set_appearance_mode("light")
                    self.light_mode = True
                    self._apply_theme()

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

        # 刷新所有桌面组件的背景
        for widget in self.active_widgets:
            if hasattr(widget, 'canvas'):
                bg_color = self.theme.bg_card if self.light_mode else "#2C2C2E"
                widget.canvas.configure(bg=bg_color)
                # 更新组件内文字颜色
                self._update_widget_colors(widget)

    def _clear_all_widgets(self):
        """清除所有桌面组件"""
        from tkinter import messagebox

        if messagebox.askyesno("确认", "确定要清除所有桌面组件吗？", parent=self.root):
            for widget in self.active_widgets[:]:
                try:
                    widget.window.destroy()
                except:
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

            from tkinter import messagebox
            messagebox.showinfo("成功", "已清除所有桌面组件")

    def _save_settings(self, settings_window):
        """保存设置"""
        # TODO: 实现设置持久化保存到配置文件
        settings = {
            "auto_start": self.auto_start_switch.get(),
            "theme": self.theme_menu.get(),
            "refresh_interval": int(self.refresh_slider.get()),
            "opacity": int(self.opacity_slider.get())
        }

        logger.info(f"保存设置: {settings}")

        from tkinter import messagebox
        messagebox.showinfo("设置已保存", "设置已成功保存！", parent=settings_window)
        settings_window.destroy()

    def _update_widget_colors(self, widget):
        """更新桌面组件的颜色以匹配主题"""
        if not hasattr(widget, 'canvas'):
            return

        text_color = self.theme.text_primary if self.light_mode else "#FFFFFF"
        secondary_color = self.theme.text_secondary if self.light_mode else "#A1A1A6"

        # 更新时钟组件
        if widget.template.name == "时钟":
            if hasattr(widget, 'time_text'):
                widget.canvas.itemconfig(widget.time_text, fill=text_color)

        # 更新待办事项组件
        elif widget.template.name == "待办事项":
            # 重新渲染待办列表
            widget._render_todo_list(widget.canvas, widget.width, widget.height)

        # 系统监控组件会在下次刷新时自动更新颜色

    def show_about_dialog(self):
        """显示关于对话框"""
        about_window = ctk.CTkToplevel(self.root)
        about_window.title("关于 DashWidgets")
        about_window.geometry("400x350")
        about_window.resizable(False, False)

        container = ctk.CTkFrame(about_window, corner_radius=0, fg_color=self.theme.bg_main)
        container.pack(fill="both", expand=True)

        # Logo
        logo_label = ctk.CTkLabel(
            container,
            text="📦",
            font=("Segoe UI Emoji", 56)
        )
        logo_label.pack(pady=20)

        # 标题
        title_label = ctk.CTkLabel(
            container,
            text="DashWidgets",
            font=("Arial", 24, "bold"),
            text_color=self.theme.accent
        )
        title_label.pack(pady=(0, 5))

        # 版本
        version_label = ctk.CTkLabel(
            container,
            text=f"版本 {__version__}",
            font=("Arial", 12),
            text_color=self.theme.text_secondary
        )
        version_label.pack(pady=(0, 20))

        # 描述
        desc_label = ctk.CTkLabel(
            container,
            text="一个类似 macOS Dashboard 的\n桌面小组件管理器",
            font=("Arial", 11),
            text_color=self.theme.text_primary
        )
        desc_label.pack(pady=(0, 20))

        # 版权信息
        copyright_label = ctk.CTkLabel(
            container,
            text=f"© 2025 Little Tree Studio\n{__website__}",
            font=("Arial", 10),
            text_color=self.theme.text_hint
        )
        copyright_label.pack(pady=10)

        # 关闭按钮
        close_btn = ctk.CTkButton(
            container,
            text="关闭",
            width=100,
            height=36,
            corner_radius=8,
            command=about_window.destroy
        )
        close_btn.pack(pady=20)

    def _create_tray_icon(self):
        """创建系统托盘图标"""
        try:
            # 创建简单的托盘图标
            from pystray import Icon, Menu, MenuItem

            # 创建图标图片
            icon_image = self._create_tray_image()

            # 定义菜单项
            def show_window(icon, item):
                self.root.deiconify()
                self.root.lift()

            def hide_window(icon, item):
                self.root.withdraw()

            def quit_app(icon, item):
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
        from PIL import ImageDraw, ImageFont

        draw = ImageDraw.Draw(image)

        # 绘制圆角矩形背景
        draw.rounded_rectangle([0, 0, 64, 64], radius=12, fill='#007AFF')

        # 绘制文字
        try:
            font = ImageFont.truetype(str(LOGO_PATH.parent / "fonts" / "HarmonyOS_Sans_SC_Regular.ttf"), 24)
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
                self.tray_icon.stop()


def main_window():
    """创建并运行主窗口"""
    app = DashWidgetsApp()
    app.run()


if __name__ == "__main__":
    load_fonts()
    main_window()
