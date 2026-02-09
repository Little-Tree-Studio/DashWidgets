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


class WidgetTemplate:
    """组件模板基类"""
    def __init__(self, name, description, icon_name, size="medium"):
        self.name = name
        self.description = description
        self.icon_name = icon_name
        self.size = size


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

    def __init__(self, parent, template, x=100, y=100):
        self.template = template
        self.x = x
        self.y = y

        # 根据组件大小设置尺寸
        if template.size == "small":
            width, height = 150, 150
        elif template.size == "medium":
            width, height = 200, 200
        else:  # large
            width, height = 300, 300

        self.width = width
        self.height = height

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

        # 拖拽功能
        self._start_x = 0
        self._start_y = 0
        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)

        # 右键菜单
        self.context_menu = tk.Menu(self.window, tearoff=0)

        if self.template.name == "待办事项":
            self.context_menu.add_command(label="清空已完成", command=self._clear_completed_todos)
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
        # 时钟图标
        canvas.create_text(width//2, height//3, text=self.template.icon_name, font=("Segoe UI Emoji", 40))

        # 时间
        self.time_text = canvas.create_text(
            width//2, height//2 + 20,
            text=datetime.datetime.now().strftime("%H:%M:%S"),
            font=("Consolas", 24, "bold"),
            fill="#333333"
        )

        # 日期
        canvas.create_text(
            width//2, height - 30,
            text=datetime.datetime.now().strftime("%Y年%m月%d日"),
            font=("Arial", 10),
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
        # 天气图标
        canvas.create_text(width//2, height//3, text=self.template.icon_name, font=("Segoe UI Emoji", 50))

        # 温度
        canvas.create_text(
            width//2, height//2 + 10,
            text="25°C",
            font=("Arial", 28, "bold"),
            fill="#FF6B35"
        )

        # 天气描述
        canvas.create_text(
            width//2, height//2 + 40,
            text="晴朗",
            font=("Arial", 12),
            fill="#666666"
        )

        # 地点
        canvas.create_text(
            width//2, height - 20,
            text="📍 北京市",
            font=("Arial", 10),
            fill="#999999"
        )

    def _create_todo_widget(self, canvas, width, height):
        """创建待办事项组件"""
        # 标题
        canvas.create_text(
            width//2, 25,
            text="📝 待办事项",
            font=("Arial", 14, "bold"),
            fill="#333333"
        )

        # 分隔线
        canvas.create_line(20, 40, width-20, 40, fill="#E0E0E0", width=1)

        # 待办事项列表
        self._render_todo_list(canvas, width, height)

        # 添加按钮
        btn_y = height - 35
        canvas.create_rectangle(
            width//2 - 40, btn_y,
            width//2 + 40, btn_y + 20,
            fill="#007AFF",
            outline=""
        )
        add_btn_text = canvas.create_text(
            width//2, btn_y + 10,
            text="+ 添加",
            fill="white",
            font=("Arial", 10)
        )

        # 绑定按钮点击事件
        self.canvas.tag_bind(add_btn_text, "<Button-1>", self._add_todo)

    def _render_todo_list(self, canvas, width, height):
        """渲染待办事项列表"""
        canvas.delete("todo_item")

        y_pos = 60
        for i, (todo, completed) in enumerate(self.todos):
            # 待办事项文本
            text = f"☑ {todo}" if completed else f"☐ {todo}"
            color = "#999999" if completed else "#333333"

            todo_text = canvas.create_text(
                25, y_pos,
                text=text,
                font=("Arial", 11),
                fill=color,
                anchor="w",
                tags=("todo_item", f"todo_{i}")
            )

            # 绑定点击事件
            canvas.tag_bind(todo_text, "<Button-1>", lambda e, idx=i: self._toggle_todo(idx))

            y_pos += 25

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
        # 标题
        canvas.create_text(
            width//2, 25,
            text="📌 笔记",
            font=("Arial", 14, "bold"),
            fill="#333333"
        )

        # 分隔线
        canvas.create_line(20, 40, width-20, 40, fill="#E0E0E0", width=1)

        # 笔记内容（使用 Text widget 实现可编辑）
        self.note_text = tk.Text(
            self.window,
            width=25,
            height=8,
            font=("Arial", 10),
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
        self.note_text.place(x=20, y=50, width=width-40, height=height-70)

        # 保存按钮
        save_btn = tk.Button(
            self.window,
            text="💾 保存",
            bg="#007AFF",
            fg="white",
            borderwidth=0,
            font=("Arial", 9),
            command=self._save_note
        )
        save_btn.place(x=width//2 - 30, y=height-30, width=60, height=20)

    def _save_note(self):
        """保存笔记"""
        note_content = self.note_text.get("1.0", "end-1c")
        # TODO: 实现持久化保存到文件或数据库
        from tkinter import messagebox
        messagebox.showinfo("笔记已保存", "笔记内容已保存！", parent=self.window)

    def _create_system_monitor_widget(self, canvas, width, height):
        """创建系统监控组件"""
        # 标题
        canvas.create_text(
            width//2, 20,
            text="📊 系统监控",
            font=("Arial", 12, "bold"),
            fill="#333333"
        )

        # 初始化监控元素ID
        self.monitor_elements = {}

        # CPU 使用率
        cpu_percent = self._get_cpu_usage()
        self.monitor_elements['cpu_text'] = canvas.create_text(
            25, height//2 - 15,
            text=f"CPU: {cpu_percent}%",
            font=("Arial", 10),
            fill="#333333",
            anchor="w"
        )

        # CPU 进度条背景
        canvas.create_rectangle(
            25, height//2,
            125, height//2 + 10,
            outline="#E0E0E0",
            width=1,
            tags="monitor_bg"
        )

        # CPU 进度条
        self.monitor_elements['cpu_bar'] = canvas.create_rectangle(
            25, height//2,
            25 + (cpu_percent / 100) * 100, height//2 + 10,
            fill="#34C759",
            outline="",
            tags="monitor_fg"
        )

        # 内存使用
        mem_percent = self._get_memory_usage()
        self.monitor_elements['mem_text'] = canvas.create_text(
            25, height//2 + 30,
            text=f"内存: {mem_percent}%",
            font=("Arial", 10),
            fill="#333333",
            anchor="w"
        )

        # 内存进度条背景
        canvas.create_rectangle(
            25, height//2 + 45,
            125, height//2 + 55,
            outline="#E0E0E0",
            width=1,
            tags="monitor_bg"
        )

        # 内存进度条
        self.monitor_elements['mem_bar'] = canvas.create_rectangle(
            25, height//2 + 45,
            25 + (mem_percent / 100) * 100, height//2 + 55,
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

            # 更新CPU显示
            self.canvas.itemconfig(
                self.monitor_elements['cpu_text'],
                text=f"CPU: {cpu_percent}%"
            )

            # 更新CPU进度条
            self.canvas.coords(
                self.monitor_elements['cpu_bar'],
                25, self.height//2,
                25 + (cpu_percent / 100) * 100, self.height//2 + 10
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
            self.canvas.coords(
                self.monitor_elements['mem_bar'],
                25, self.height//2 + 45,
                25 + (mem_percent / 100) * 100, self.height//2 + 55
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
        # 图标
        canvas.create_text(width//2, 35, text=self.template.icon_name, font=("Segoe UI Emoji", 40))

        # 日期
        now = datetime.datetime.now()
        canvas.create_text(
            width//2, height//2 + 10,
            text=str(now.day),
            font=("Arial", 48, "bold"),
            fill="#333333"
        )

        # 年月
        canvas.create_text(
            width//2, height - 25,
            text=f"{now.year}年 {now.month}月",
            font=("Arial", 12),
            fill="#666666"
        )

    def _create_timer_widget(self, canvas, width, height):
        """创建计时器组件"""
        # 图标
        canvas.create_text(width//2, 30, text=self.template.icon_name, font=("Segoe UI Emoji", 30))

        # 计时器显示
        canvas.create_text(
            width//2, height//2 + 10,
            text="00:00",
            font=("Consolas", 28, "bold"),
            fill="#333333"
        )

        # 按钮
        canvas.create_oval(
            width//2 - 40, height - 40,
            width//2 + 40, height - 10,
            fill="#007AFF",
            outline=""
        )
        canvas.create_text(
            width//2, height - 25,
            text="▶",
            fill="white",
            font=("Arial", 12)
        )

    def _create_exchange_widget(self, canvas, width, height):
        """创建汇率组件"""
        # 标题
        canvas.create_text(
            width//2, 25,
            text="💱 汇率",
            font=("Arial", 12, "bold"),
            fill="#333333"
        )

        # 汇率信息
        canvas.create_text(
            width//2, height//2 - 10,
            text="1 USD = 7.24 CNY",
            font=("Arial", 16, "bold"),
            fill="#007AFF"
        )

        canvas.create_text(
            width//2, height//2 + 20,
            text="1 EUR = 7.85 CNY",
            font=("Arial", 12),
            fill="#333333"
        )

        canvas.create_text(
            width//2, height - 20,
            text="更新于 5分钟前",
            font=("Arial", 9),
            fill="#999999"
        )

    def _on_press(self, event):
        """鼠标按下事件"""
        self._start_x = event.x
        self._start_y = event.y

    def _on_drag(self, event):
        """鼠标拖拽事件"""
        x = self.window.winfo_x() + (event.x - self._start_x)
        y = self.window.winfo_y() + (event.y - self._start_y)
        self.window.geometry(f"+{x}+{y}")

    def _show_context_menu(self, event):
        """显示右键菜单"""
        self.context_menu.post(event.x_root, event.y_root)

    def _show_settings(self):
        """显示设置"""
        pass

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

        # 创建可拖拽的组件
        widget = DraggableWidget(self.root, template)

        # 在列表中添加记录
        self._add_widget_to_list(template, widget)

        self.active_widgets.append(widget)
        self._update_stats()

    def _add_widget_to_list(self, template, widget):
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
