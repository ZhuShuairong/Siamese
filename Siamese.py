# prompt_manager.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pystray
from pystray import MenuItem as item, Menu
from PIL import Image as PILImage, ImageDraw
import pyperclip
import json
import os
import threading
import queue
import time
import sys
import winreg
from ctypes import windll, byref, sizeof, c_int

# Configuration file paths
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts.json")
ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
ICON_ICO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")

class Localization:
    """Localization manager for multi-language support"""
    def __init__(self, language='en'):
        self.language = language
        self.translations = {
            'zh': {
                'settings': '设置', 'app_title': '提示词管理器', 'tray_title': '提示词管理器',
                'copied_notify': '已复制到剪贴板', 'copy_failed': '复制失败',
                'clear_clipboard': '剪贴板已自动清除', 'edit': '编辑', 'delete': '删除',
                'refresh': '刷新', 'add_new': '添加新提示词',
                'manage_prompts': '管理提示词', 'exit': '退出', 'title': '标题',
                'content_preview': '内容预览', 'edit_prompt': '编辑提示词',
                'add_prompt': '添加新提示词', 'title_label': '标题:', 'content_label': '内容:',
                'save': '保存', 'cancel': '取消', 'input_incomplete': '输入不完整',
                'empty_fields': '标题和内容都不能为空', 'no_selection': '未选择',
                'select_edit': '请先选择一个提示词进行编辑', 'select_delete': '请先选择一个提示词进行删除',
                'confirm_delete': '确认删除', 'delete_confirm_msg': '确定要删除这个提示词吗？',
                'save_failed': '保存失败', 'save_failed_msg': '无法保存配置文件',
                'language_switch': '切换语言', 'theme_switch': '切换主题',
                'switch_to_english': 'English', 'switch_to_chinese': '中文',
                'switch_to_dark': '深色模式', 'switch_to_light': '浅色模式',
                'language': '语言', 'theme': '主题', 'search': '搜索',
                'search_placeholder': '输入关键词搜索...', 'pin': '置顶', 'unpin': '取消置顶',
                'pinned': '已置顶', 'pin_limit_title': '置顶限制',
                'pin_limit_message': '您最多只能置顶5个提示词。请选择要替换的：',
                'replace': '替换', 'pin_limit_select': '请选择一个提示词进行替换',
                'import_prompts': '导入提示词', 'export_prompts': '导出提示词',
                'import_success': '导入成功', 'import_failed': '导入失败',
                'export_success': '导出成功', 'export_failed': '导出失败',
                'invalid_format': '格式错误', 'file_too_large': '文件过大',
                'auto_start': '开机自启动', 'auto_start_enabled': '已启用开机自启动',
                'auto_start_disabled': '已禁用开机自启动'
            },
            'en': {
                'settings': 'Settings', 'app_title': 'Prompt Manager', 'tray_title': 'Prompt Manager',
                'copied_notify': 'Copied to clipboard', 'copy_failed': 'Copy failed',
                'clear_clipboard': 'Clipboard cleared automatically', 'edit': 'Edit', 'delete': 'Delete',
                'refresh': 'Refresh', 'add_new': 'Add New Prompt',
                'manage_prompts': 'Manage Prompts', 'exit': 'Exit', 'title': 'Title',
                'content_preview': 'Content Preview', 'edit_prompt': 'Edit Prompt',
                'add_prompt': 'Add New Prompt', 'title_label': 'Title:', 'content_label': 'Content:',
                'save': 'Save', 'cancel': 'Cancel', 'input_incomplete': 'Incomplete Input',
                'empty_fields': 'Title and content cannot be empty', 'no_selection': 'No Selection',
                'select_edit': 'Please select a prompt to edit', 'select_delete': 'Please select a prompt to delete',
                'confirm_delete': 'Confirm Delete', 'delete_confirm_msg': 'Are you sure you want to delete this prompt?',
                'save_failed': 'Save Failed', 'save_failed_msg': 'Failed to save configuration file',
                'language_switch': 'Switch Language', 'theme_switch': 'Switch Theme',
                'switch_to_english': 'English', 'switch_to_chinese': '中文',
                'switch_to_dark': 'Dark Mode', 'switch_to_light': 'Light Mode',
                'language': 'Language', 'theme': 'Theme', 'search': 'Search',
                'search_placeholder': 'Search prompts...', 'pin': 'Pin', 'unpin': 'Unpin',
                'pinned': 'Pinned', 'pin_limit_title': 'Pin Limit Reached',
                'pin_limit_message': 'You can only pin 5 prompts. Select one to replace:',
                'replace': 'Replace', 'pin_limit_select': 'Please select a prompt to replace',
                'import_prompts': 'Import Prompts', 'export_prompts': 'Export Prompts',
                'import_success': 'Import Successful', 'import_failed': 'Import Failed',
                'export_success': 'Export Successful', 'export_failed': 'Export Failed',
                'invalid_format': 'Invalid Format', 'file_too_large': 'File Too Large',
                'auto_start': 'Auto Start with Windows', 'auto_start_enabled': 'Auto-start enabled',
                'auto_start_disabled': 'Auto-start disabled'
            }
        }
    
    def get(self, key):
        return self.translations.get(self.language, {}).get(key, key)

class ThemeManager:
    """Theme manager for dark/light mode with improved color schemes"""
    def __init__(self, theme='dark'):
        self.theme = theme
        self.colors = {
            'light': {
                'bg': '#FFEAC5',           # Light cream background
                'fg': '#4A3820',           # Dark brown text (darker for readability)
                'button_bg': '#E6C896',    # Slightly darker tan for buttons
                'button_fg': '#3D2F1A',    # Very dark brown for button text
                'button_hover': '#D4B884', # Even darker on hover
                'entry_bg': '#FFF5E1',     # Very light cream for input
                'entry_fg': '#3D2F1A',     # Dark text in inputs
                'tree_bg': '#FFEAC5',      # Match main bg
                'tree_fg': '#4A3820',      # Dark text
                'select_bg': '#6C4E31',    # Brown selection
                'select_fg': '#FFEAC5',    # Light text on selection
                'menu_bg': '#D4B884',      # Darker menu bar
                'menu_fg': '#3D2F1A',      # Dark menu text
                'titlebar': 0xC5EAFF      # Light titlebar (BGR format)
            },
            'dark': {
                'bg': '#222831',           # Dark gray background
                'fg': '#EEEEEE',           # Very light gray text (brighter)
                'button_bg': '#31363F',    # Lighter gray for buttons
                'button_fg': '#EEEEEE',    # Bright text on buttons
                'button_hover': '#3E4451', # Even lighter on hover
                'entry_bg': '#2D323A',     # Slightly lighter than bg for inputs
                'entry_fg': '#EEEEEE',     # Bright input text
                'tree_bg': '#1A1E25',      # Darker for tree
                'tree_fg': '#E0E0E0',      # Light gray text
                'select_bg': '#76ABAE',    # Teal selection
                'select_fg': '#1A1E25',    # Dark text on selection
                'menu_bg': '#2D323A',      # Slightly lighter menu
                'menu_fg': '#EEEEEE',      # Bright menu text
                'titlebar': 0x312822      # Dark titlebar (BGR format)
            }
        }
    
    def get(self, element):
        return self.colors.get(self.theme, {}).get(element, '#ffffff')

def set_window_titlebar_color(window, color_value):
    """Set Windows 11 title bar color using DWM API"""
    try:
        hwnd = windll.user32.GetParent(window.winfo_id())
        DWMWA_CAPTION_COLOR = 35
        
        # Set caption color
        windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 
            DWMWA_CAPTION_COLOR,
            byref(c_int(color_value)),
            sizeof(c_int)
        )
    except Exception as e:
        print(f"Could not set title bar color: {e}")

def set_window_icon(window, icon_path):
    """Set window icon if icon file exists"""
    try:
        ico_path = icon_path.replace('.png', '.ico')
        if os.path.exists(ico_path):
            window.iconbitmap(ico_path)
        elif os.path.exists(icon_path) and icon_path.endswith('.ico'):
            window.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not set window icon: {e}")


def set_dpi_awareness():
    """Enable DPI awareness for sharper text on high-DPI displays"""
    try:
        # Try Windows 8.1 and later
        windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except:
        try:
            # Fall back to Windows Vista and later
            windll.user32.SetProcessDPIAware()
        except:
            pass

class AutoStartManager:
    """Manages Windows startup registry entries"""
    
    @staticmethod
    def get_registry_key():
        return r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    @staticmethod
    def get_app_name():
        return "PromptManager"
    
    @staticmethod
    def get_app_path():
        if getattr(sys, 'frozen', False):
            return sys.executable
        else:
            return f'"{sys.executable}" "{os.path.abspath(__file__)}"'
    
    @classmethod
    def is_enabled(cls):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.get_registry_key(), 0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, cls.get_app_name())
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    
    @classmethod
    def enable(cls):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.get_registry_key(), 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, cls.get_app_name(), 0, winreg.REG_SZ, cls.get_app_path())
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Failed to enable auto-start: {e}")
            return False
    
    @classmethod
    def disable(cls):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.get_registry_key(), 0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, cls.get_app_name())
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Failed to disable auto-start: {e}")
            return False
    
    @classmethod
    def toggle(cls):
        if cls.is_enabled():
            return cls.disable()
        else:
            return cls.enable()

class ConfigManager:
    """Configuration manager for prompts and settings"""
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit
    
    def __init__(self):
        self.config_path = CONFIG_PATH
        self.settings = {'language': 'en', 'theme': 'dark'}
        self.prompts = []
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.settings = data.get('settings', self.settings)
                    self.prompts = []
                    for p in data.get('prompts', []):
                        if isinstance(p, dict):
                            p['pinned'] = p.get('pinned', False)
                            self.prompts.append(p)
            except Exception as e:
                print(f"Config load error: {e}")
    
    def save_config(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump({'settings': self.settings, 'prompts': self.prompts}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise e
    
    def import_prompts(self, file_path):
        """Import prompts from JSON file with validation"""
        try:
            file_size = os.path.getsize(file_path)
            if file_size > self.MAX_FILE_SIZE:
                raise ValueError("file_too_large")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, dict):
                raise ValueError("invalid_format")
            
            if 'prompts' not in data or not isinstance(data['prompts'], list):
                raise ValueError("invalid_format")
            
            for prompt in data['prompts']:
                if not isinstance(prompt, dict):
                    raise ValueError("invalid_format")
                if 'title' not in prompt or 'content' not in prompt:
                    raise ValueError("invalid_format")
                if not isinstance(prompt['title'], str) or not isinstance(prompt['content'], str):
                    raise ValueError("invalid_format")
            
            for prompt in data['prompts']:
                prompt['pinned'] = prompt.get('pinned', False)
                self.prompts.append(prompt)
            
            self.save_config()
            return True, "import_success"
        except ValueError as e:
            return False, str(e)
        except json.JSONDecodeError:
            return False, "invalid_format"
        except Exception as e:
            print(f"Import error: {e}")
            return False, "import_failed"
    
    def export_prompts(self, file_path):
        """Export prompts to JSON file"""
        try:
            export_data = {
                'settings': self.settings,
                'prompts': self.prompts
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            return True, "export_success"
        except Exception as e:
            print(f"Export error: {e}")
            return False, "export_failed"
    
    def add_prompt(self, title, content, pinned=False):
        self.prompts.append({'title': title, 'content': content, 'pinned': pinned})
        self.save_config()
    
    def update_prompt(self, index, title, content, pinned=None):
        if 0 <= index < len(self.prompts):
            self.prompts[index]['title'] = title
            self.prompts[index]['content'] = content
            if pinned is not None:
                self.prompts[index]['pinned'] = pinned
            self.save_config()
    
    def delete_prompt(self, index):
        if 0 <= index < len(self.prompts):
            del self.prompts[index]
            self.save_config()
    
    def get_prompt(self, index):
        if 0 <= index < len(self.prompts):
            return self.prompts[index]
        return None
    
    def toggle_pin(self, index):
        if 0 <= index < len(self.prompts):
            self.prompts[index]['pinned'] = not self.prompts[index].get('pinned', False)
            self.save_config()
            return self.prompts[index]['pinned']
        return False
    
    def switch_language(self):
        self.settings['language'] = 'en' if self.settings['language'] == 'zh' else 'zh'
        self.save_config()
    
    def switch_theme(self):
        self.settings['theme'] = 'dark' if self.settings['theme'] == 'light' else 'light'
        self.save_config()

class PromptManagerWindow:
    """Unified window for managing prompts"""
    def __init__(self, app):
        self.app = app
        self.loc = app.loc
        self.window = tk.Toplevel(app.gui_root)
        self.window.title(self.loc.get('app_title'))
        self.window.geometry('900x650')  # Increased resolution for better clarity
        
        # Set window icon
        set_window_icon(self.window, ICON_PATH)
        
        # Apply theme and titlebar color
        app.apply_theme_to_window(self.window)
        self.window.update()
        set_window_titlebar_color(self.window, app.theme.get('titlebar'))
        
        # Main container
        main_frame = ttk.Frame(self.window, padding='15')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Search bar
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        ttk.Label(search_frame, text=self.loc.get('search'), font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.refresh_prompts())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Segoe UI', 10))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Treeview with larger font
        columns = (self.loc.get('title'), self.loc.get('content_preview'), self.loc.get('pinned'))
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=18)
        self.tree.heading(self.loc.get('title'), text=self.loc.get('title'))
        self.tree.heading(self.loc.get('content_preview'), text=self.loc.get('content_preview'))
        self.tree.heading(self.loc.get('pinned'), text=self.loc.get('pinned'))
        self.tree.column(self.loc.get('title'), width=200)
        self.tree.column(self.loc.get('content_preview'), width=550)
        self.tree.column(self.loc.get('pinned'), width=80, anchor=tk.CENTER)
        
        # Apply custom font to treeview
        style = ttk.Style()
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=28)
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'))
        
        self.app.apply_theme_to_treeview(self.tree)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Button frame with better spacing (Close button removed)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Create buttons with consistent font
        ttk.Button(btn_frame, text=self.loc.get('add_new'), command=self.add_prompt).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text=self.loc.get('edit'), command=self.edit_selected).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text=self.loc.get('delete'), command=self.delete_selected).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text=self.loc.get('pin'), command=self.toggle_pin_selected).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text=self.loc.get('import_prompts'), command=self.import_prompts).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text=self.loc.get('export_prompts'), command=self.export_prompts).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text=self.loc.get('settings'), command=self.open_settings).pack(side=tk.LEFT, padx=6)
        
        self.refresh_prompts()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def import_prompts(self):
        file_path = filedialog.askopenfilename(
            parent=self.window,
            title=self.loc.get('import_prompts'),
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            success, message_key = self.app.config.import_prompts(file_path)
            if success:
                messagebox.showinfo(self.loc.get('import_success'), 
                                  f"{self.loc.get('import_success')}! Imported from {os.path.basename(file_path)}")
                self.refresh_prompts()
                self.app.update_tray_menu()
            else:
                error_msg = self.loc.get(message_key)
                if message_key == "file_too_large":
                    error_msg += f" (Max: {ConfigManager.MAX_FILE_SIZE // (1024*1024)} MB)"
                messagebox.showerror(self.loc.get('import_failed'), error_msg)
    
    def export_prompts(self):
        file_path = filedialog.asksaveasfilename(
            parent=self.window,
            title=self.loc.get('export_prompts'),
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            success, message_key = self.app.config.export_prompts(file_path)
            if success:
                messagebox.showinfo(self.loc.get('export_success'), 
                                  f"{self.loc.get('export_success')}! Saved to {os.path.basename(file_path)}")
            else:
                messagebox.showerror(self.loc.get('export_failed'), self.loc.get(message_key))
    
    def show_pin_limit_dialog(self):
        dialog = tk.Toplevel(self.window)
        dialog.title(self.loc.get('pin_limit_title'))
        dialog.geometry('600x400')
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Set window icon
        set_window_icon(dialog, ICON_PATH)
        
        self.app.apply_theme_to_window(dialog)
        dialog.update()
        set_window_titlebar_color(dialog, self.app.theme.get('titlebar'))
        
        ttk.Label(dialog, text=self.loc.get('pin_limit_message'), wraplength=560, 
                 font=('Segoe UI', 10)).pack(pady=15, padx=15)
        
        pinned_prompts = [(i, p) for i, p in enumerate(self.app.config.prompts) if p.get('pinned', False)]
        selected_idx = tk.StringVar(value="-1")
        
        for idx, prompt in pinned_prompts:
            rb = ttk.Radiobutton(dialog, text=prompt['title'], variable=selected_idx, value=str(idx))
            rb.pack(anchor=tk.W, padx=25, pady=3)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=25)
        result = None
        
        def handle_replace():
            nonlocal result
            sel = selected_idx.get()
            if sel == "-1":
                messagebox.showwarning(self.loc.get('input_incomplete'), self.loc.get('pin_limit_select'))
                return
            result = int(sel)
            dialog.destroy()
        
        def handle_cancel():
            nonlocal result
            result = None
            dialog.destroy()
        
        ttk.Button(btn_frame, text=self.loc.get('replace'), command=handle_replace).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_frame, text=self.loc.get('cancel'), command=handle_cancel).pack(side=tk.LEFT, padx=8)
        
        dialog.wait_window()
        return result
    
    def refresh_prompts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.app.config.load_config()
        query = self.search_var.get().lower()
        for idx, prompt in enumerate(self.app.config.prompts):
            if query and query not in prompt['title'].lower() and query not in prompt['content'].lower():
                continue
            preview = prompt['content'][:70] + '...' if len(prompt['content']) > 70 else prompt['content']
            pinned_status = "✓" if prompt.get('pinned', False) else ""
            self.tree.insert('', tk.END, values=(prompt['title'], preview, pinned_status), iid=str(idx))
    
    def add_prompt(self):
        self.create_edit_dialog()
    
    def edit_selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(self.loc.get('no_selection'), self.loc.get('select_edit'))
            return
        idx = int(selection[0])
        prompt = self.app.config.prompts[idx]
        self.create_edit_dialog(idx, prompt['title'], prompt['content'])
    
    def delete_selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(self.loc.get('no_selection'), self.loc.get('select_delete'))
            return
        if messagebox.askyesno(self.loc.get('confirm_delete'), self.loc.get('delete_confirm_msg')):
            idx = int(selection[0])
            self.app.config.delete_prompt(idx)
            self.refresh_prompts()
            self.app.update_tray_menu()
    
    def toggle_pin_selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(self.loc.get('no_selection'), "Please select a prompt to pin/unpin")
            return
        idx = int(selection[0])
        prompt = self.app.config.prompts[idx]
        
        if prompt.get('pinned', False):
            self.app.config.toggle_pin(idx)
            self.refresh_prompts()
            self.app.update_tray_menu()
            return
        
        pinned_count = sum(1 for p in self.app.config.prompts if p.get('pinned', False))
        if pinned_count >= 5:
            replace_idx = self.show_pin_limit_dialog()
            if replace_idx is not None:
                self.app.config.toggle_pin(replace_idx)
                self.app.config.toggle_pin(idx)
                self.refresh_prompts()
                self.app.update_tray_menu()
        else:
            self.app.config.toggle_pin(idx)
            self.refresh_prompts()
            self.app.update_tray_menu()
    
    def open_settings(self):
        dialog = tk.Toplevel(self.window)
        dialog.title(self.loc.get('settings'))
        dialog.geometry('400x250')
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Set window icon
        set_window_icon(dialog, ICON_PATH)
        
        self.app.apply_theme_to_window(dialog)
        dialog.update()
        set_window_titlebar_color(dialog, self.app.theme.get('titlebar'))
        
        def on_language_change():
            self.app.switch_language()
            dialog.destroy()
            if self.app.manager_window:
                self.app.manager_window.window.destroy()
                self.app.manager_window = None
            self.app.show_manager()
        
        def on_theme_change():
            self.app.switch_theme()
            self.app.apply_theme_to_window(self.window)
            self.app.apply_theme_to_treeview(self.tree)
            set_window_titlebar_color(self.window, self.app.theme.get('titlebar'))
            dialog.destroy()
        
        def on_auto_start_toggle():
            success = AutoStartManager.toggle()
            if success:
                is_enabled = AutoStartManager.is_enabled()
                msg = self.loc.get('auto_start_enabled') if is_enabled else self.loc.get('auto_start_disabled')
                messagebox.showinfo(self.loc.get('settings'), msg)
                update_auto_start_btn()
            else:
                messagebox.showerror(self.loc.get('settings'), "Failed to modify auto-start setting")
        
        lang_btn = ttk.Button(dialog, text=self.loc.get('switch_to_chinese') if self.app.config.settings['language'] == 'en' else self.loc.get('switch_to_english'),
                            command=on_language_change)
        lang_btn.pack(pady=12, padx=25, fill=tk.X)
        
        theme_btn = ttk.Button(dialog, text=self.loc.get('switch_to_light') if self.app.config.settings['theme'] == 'dark' else self.loc.get('switch_to_dark'),
                             command=on_theme_change)
        theme_btn.pack(pady=12, padx=25, fill=tk.X)
        
        auto_start_btn = ttk.Button(dialog, text="", command=on_auto_start_toggle)
        auto_start_btn.pack(pady=12, padx=25, fill=tk.X)
        
        def update_auto_start_btn():
            is_enabled = AutoStartManager.is_enabled()
            status = "✓" if is_enabled else "✗"
            auto_start_btn.config(text=f"{self.loc.get('auto_start')} [{status}]")
        
        update_auto_start_btn()
    
    def create_edit_dialog(self, index=None, default_title='', default_content=''):
        dialog = tk.Toplevel(self.window)
        dialog.title(self.loc.get('edit_prompt') if index is not None else self.loc.get('add_prompt'))
        dialog.geometry('650x450')
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Set window icon
        set_window_icon(dialog, ICON_PATH)
        
        self.app.apply_theme_to_window(dialog)
        dialog.update()
        set_window_titlebar_color(dialog, self.app.theme.get('titlebar'))
        
        ttk.Label(dialog, text=self.loc.get('title_label'), font=('Segoe UI', 10)).pack(pady=(15, 0), padx=15, anchor=tk.W)
        title_entry = ttk.Entry(dialog, width=50, font=('Segoe UI', 10))
        title_entry.insert(0, default_title)
        title_entry.pack(pady=8, padx=15, fill=tk.X)
        
        ttk.Label(dialog, text=self.loc.get('content_label'), font=('Segoe UI', 10)).pack(pady=(15, 0), padx=15, anchor=tk.W)
        content_text = tk.Text(dialog, height=12, font=('Segoe UI', 10))
        content_text.insert('1.0', default_content)
        content_text.pack(pady=8, padx=15, fill=tk.BOTH, expand=True)
        self.app.apply_theme_to_text(content_text)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=15)
        
        def save():
            new_title = title_entry.get().strip()
            new_content = content_text.get('1.0', tk.END).strip()
            if not new_title or not new_content:
                messagebox.showwarning(self.loc.get('input_incomplete'), self.loc.get('empty_fields'))
                return
            if index is not None:
                self.app.config.update_prompt(index, new_title, new_content)
            else:
                self.app.config.add_prompt(new_title, new_content)
            self.app.update_tray_menu()
            self.refresh_prompts()
            dialog.destroy()
        
        ttk.Button(btn_frame, text=self.loc.get('save'), command=save).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_frame, text=self.loc.get('cancel'), command=dialog.destroy).pack(side=tk.LEFT, padx=8)
    
    def on_close(self):
        self.window.destroy()
        self.app.manager_window = None

class SystemTrayApp:
    def __init__(self):
        self.config = ConfigManager()
        self.loc = Localization(self.config.settings['language'])
        self.theme = ThemeManager(self.config.settings['theme'])
        
        self.gui_root = tk.Tk()
        self.gui_root.withdraw()
        self.gui_queue = queue.Queue()
        self.gui_root.after(100, self.process_gui_queue)
        
        self.manager_window = None
        self.clipboard_timer = None
        
        self.load_icon()
        self.setup_tray()
        
        self.tray_thread = threading.Thread(target=self.run_tray, daemon=True)
        self.tray_thread.start()
        
        self.gui_root.mainloop()
    
    def process_gui_queue(self):
        try:
            while True:
                func, args, kwargs = self.gui_queue.get_nowait()
                func(*args, **kwargs)
        except queue.Empty:
            pass
        self.gui_root.after(100, self.process_gui_queue)
    
    def load_icon(self):
        try:
            if os.path.exists(ICON_PATH):
                self.app_icon = PILImage.open(ICON_PATH)
            else:
                image = PILImage.new('RGB', (64, 64), color='#0078d4')
                draw = ImageDraw.Draw(image)
                draw.rectangle([16, 16, 48, 48], fill='white')
                self.app_icon = image
        except:
            image = PILImage.new('RGB', (64, 64), color='#0078d4')
            draw = ImageDraw.Draw(image)
            draw.rectangle([16, 16, 48, 48], fill='white')
            self.app_icon = image
    
    def create_menu(self):
        menu_items = []
        
        # Show pinned prompts
        pinned_count = 0
        
        def make_copy_handler(index):
            def handler(icon, item):
                self.copy_to_clipboard(index)
            return handler
        
        for idx, prompt in enumerate(self.config.prompts):
            if prompt.get('pinned', False) and pinned_count < 5:
                title = prompt['title'][:30] + '...' if len(prompt['title']) > 30 else prompt['title']
                menu_items.append(item(title, make_copy_handler(idx)))
                pinned_count += 1
        
        if pinned_count > 0:
            menu_items.append(Menu.SEPARATOR)
        
        # THIS IS THE KEY: default=True makes it respond to left-click
        menu_items.append(item(
            self.loc.get('manage_prompts'), 
            lambda icon, item: self.show_manager(),
            default=True
        ))
        menu_items.append(item(self.loc.get('exit'), lambda icon, item: self.exit_app()))
        
        return Menu(*menu_items)
    
    def setup_tray(self):
        self.icon = pystray.Icon(
            'PromptManager', 
            self.app_icon, 
            self.loc.get('tray_title'),
            menu=self.create_menu()
        )

    
    def run_tray(self):
        self.icon.run()
    
    def show_manager(self):
        self.gui_queue.put((self._show_manager, (), {}))
    
    def _show_manager(self):
        if self.manager_window and self.manager_window.window.winfo_exists():
            self.manager_window.window.lift()
            return
        self.manager_window = PromptManagerWindow(self)
    
    def copy_to_clipboard(self, index):
        prompt = self.config.get_prompt(index)
        if prompt:
            try:
                pyperclip.copy(prompt['content'])
                self.icon.notify(f"{self.loc.get('copied_notify')}: {prompt['title']}", self.loc.get('app_title'))
                
                if self.clipboard_timer and self.clipboard_timer.is_alive():
                    self.clipboard_timer.cancel()
                self.clipboard_timer = threading.Timer(30.0, self.clear_clipboard)
                self.clipboard_timer.start()
            except Exception as e:
                self.icon.notify(f"{self.loc.get('copy_failed')}: {e}", self.loc.get('app_title'))
    
    def clear_clipboard(self):
        try:
            pyperclip.copy('')
            self.icon.notify(self.loc.get('clear_clipboard'), self.loc.get('app_title'))
        except:
            pass
    
    def switch_language(self):
        self.config.switch_language()
        self.loc = Localization(self.config.settings['language'])
        self.update_tray_menu()
        lang_text = self.loc.get('switch_to_english') if self.config.settings['language'] == 'en' else self.loc.get('switch_to_chinese')
        self.icon.notify(f"{self.loc.get('language_switch')}: {lang_text}", self.loc.get('app_title'))
    
    def switch_theme(self):
        self.config.switch_theme()
        self.theme = ThemeManager(self.config.settings['theme'])
        theme_text = self.loc.get('switch_to_light') if self.config.settings['theme'] == 'light' else self.loc.get('switch_to_dark')
        self.icon.notify(f"{self.loc.get('theme_switch')}: {theme_text}", self.loc.get('app_title'))
    
    def apply_theme_to_window(self, window):
        colors = self.theme.colors[self.theme.theme]
        window.configure(bg=colors['bg'])
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=colors['bg'])
        style.configure('TButton', background=colors['button_bg'], foreground=colors['button_fg'],
                       borderwidth=1, focuscolor='none', relief='flat', font=('Segoe UI', 9))
        style.map('TButton', background=[('active', colors['button_hover'])])
        style.configure('TLabel', background=colors['bg'], foreground=colors['fg'])
        style.configure('TEntry', fieldbackground=colors['entry_bg'], foreground=colors['entry_fg'],
                       borderwidth=1, relief='flat')
        style.configure('TRadiobutton', background=colors['bg'], foreground=colors['fg'], font=('Segoe UI', 9))
        style.map('TRadiobutton', background=[('active', colors['bg'])])
    
    def apply_theme_to_treeview(self, tree):
        colors = self.theme.colors[self.theme.theme]
        style = ttk.Style()
        style.configure('Treeview', background=colors['tree_bg'], foreground=colors['tree_fg'], 
                       fieldbackground=colors['tree_bg'], borderwidth=0)
        style.configure('Treeview.Heading', background=colors['button_bg'], foreground=colors['button_fg'],
                       relief='flat')
        style.map('Treeview', background=[('selected', colors['select_bg'])], 
                 foreground=[('selected', colors['select_fg'])])
    
    def apply_theme_to_text(self, text_widget):
        colors = self.theme.colors[self.theme.theme]
        text_widget.configure(bg=colors['entry_bg'], fg=colors['entry_fg'], 
                             insertbackground=colors['fg'], relief='flat', borderwidth=2)
    
    def update_tray_menu(self):
        if self.icon:
            self.icon.menu = self.create_menu()
            try:
                self.icon.update_menu()
            except:
                pass
    
    def exit_app(self, icon=None):
        if self.clipboard_timer and self.clipboard_timer.is_alive():
            self.clipboard_timer.cancel()
        self.icon.stop()
        self.gui_root.quit()

def main():
    # Enable DPI awareness for sharper text
    set_dpi_awareness()
    
    # Optional: Hide console window when running as .exe
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    app = SystemTrayApp()

if __name__ == '__main__':
    main()
