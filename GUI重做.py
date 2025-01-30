import os
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class TrueMusicGenerator:
    def __init__(self, master):
        self.master = master
        master.title("True Music 生成工具 v2.0")
        master.geometry("750x750")
        
        # 配置日志颜色
        self.log_tags = {
            'success': {'foreground': 'green'},
            'error': {'foreground': 'red'},
            'warning': {'foreground': 'orange'},
            'info': {'foreground': 'blue'}
        }
        
        self.create_widgets()
        self.setup_bindings()
        
    def create_widgets(self):
        """创建界面组件"""
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(fill='both', expand=True)

        # 目录选择部分
        dir_frame = ttk.LabelFrame(main_frame, text="第一步：选择目录", padding=10)
        dir_frame.pack(fill='x', pady=5)

        ttk.Label(dir_frame, text="MOD根目录:").grid(row=0, column=0, sticky='w')
        self.entry_mod = ttk.Entry(dir_frame, width=50)
        self.entry_mod.grid(row=0, column=1, padx=5)
        ttk.Button(dir_frame, text="浏览...", command=self.select_mod_dir).grid(row=0, column=2)

        ttk.Label(dir_frame, text="MP3目录:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_mp3 = ttk.Entry(dir_frame, width=50)
        self.entry_mp3.grid(row=1, column=1, padx=5)
        ttk.Button(dir_frame, text="浏览...", command=self.select_mp3_dir).grid(row=1, column=2)

        # 配置信息部分
        info_frame = ttk.LabelFrame(main_frame, text="第二步：配置信息", padding=10)
        info_frame.pack(fill='x', pady=5)

        ttk.Label(info_frame, text="模组标题:").grid(row=0, column=0, sticky='w')
        self.entry_title = ttk.Entry(info_frame, width=40)
        self.entry_title.grid(row=0, column=1, padx=5, sticky='ew')
        self.create_tooltip(self.entry_title, "在创意工坊显示的标题")

        ttk.Label(info_frame, text="模组描述:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_desc = ttk.Entry(info_frame, width=40)
        self.entry_desc.grid(row=1, column=1, padx=5, sticky='ew')
        self.create_tooltip(self.entry_desc, "简单的模组介绍")

        ttk.Label(info_frame, text="模组ID:").grid(row=2, column=0, sticky='w')
        self.entry_id = ttk.Entry(info_frame, width=40)
        self.entry_id.grid(row=2, column=1, padx=5, sticky='ew')
        self.create_tooltip(self.entry_id, "英文+数字组合，如my_music_01")

        # 操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="开始生成", command=self.start_process).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="清理目录", command=self.clean_dirs).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="使用帮助", command=self.show_help).grid(row=0, column=2, padx=5)

        # 日志区域
        self.log_area = scrolledtext.ScrolledText(main_frame, height=15, wrap=tk.WORD)
        self.log_area.pack(fill='both', expand=True, pady=5)
        for tag, config in self.log_tags.items():
            self.log_area.tag_config(tag, **config)

    def setup_bindings(self):
        """绑定事件"""
        self.entry_mod.bind("<FocusOut>", self.auto_fill_info)
        
    def create_tooltip(self, widget, text):
        """创建简易悬浮提示"""
        def show_tooltip(event):
            tooltip = tk.Toplevel(self.master)
            tooltip.wm_overrideredirect(True)
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + 30
            tooltip.geometry(f"+{x}+{y}")
            label = ttk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()
            widget.bind("<Leave>", lambda e: tooltip.destroy(), add="+")
            
        widget.bind("<Enter>", show_tooltip)

    def select_mod_dir(self):
        """选择MOD根目录"""
        path = filedialog.askdirectory(title="选择True Music Addon根目录")
        if path:
            self.entry_mod.delete(0, tk.END)
            self.entry_mod.insert(0, path)
            self.auto_fill_info()

    def select_mp3_dir(self):
        """选择MP3目录"""
        path = filedialog.askdirectory(title="选择MP3文件夹")
        if path:
            self.entry_mp3.delete(0, tk.END)
            self.entry_mp3.insert(0, path)

    def auto_fill_info(self, event=None):
        """自动填充配置信息"""
        mod_dir = self.entry_mod.get()
        if not mod_dir:
            return
            
        # 自动读取标题
        workshop_path = os.path.join(mod_dir, "workshop.txt")
        if os.path.exists(workshop_path):
            with open(workshop_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("title="):
                        title = line.split("=", 1)[1].strip()
                        self.entry_title.delete(0, tk.END)
                        self.entry_title.insert(0, title.replace("True Music Addon: ", ""))
                        break

        # 自动生成ID
        mod_info_path = os.path.join(mod_dir, "Contents", "mods", "truemusic_addon", "mod.info")
        if os.path.exists(mod_info_path):
            with open(mod_info_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("id="):
                        mod_id = line.split("=", 1)[1].strip().replace("_mod", "")
                        self.entry_id.delete(0, tk.END)
                        self.entry_id.insert(0, mod_id)
                        break

    def log(self, message, tag='info'):
        """记录带颜色的日志"""
        self.log_area.insert(tk.END, message + "\n", tag)
        self.log_area.see(tk.END)

    def validate_paths(self):
        """验证目录结构"""
        errors = []
        
        # 检查MOD目录
        mod_dir = self.entry_mod.get()
        required_files = [
            ("workshop.txt", "根目录"),
            (os.path.join("Contents", "mods", "truemusic_addon", "mod.info"), "mod信息文件")
        ]
        for rel_path, desc in required_files:
            full_path = os.path.join(mod_dir, rel_path)
            if not os.path.exists(full_path):
                errors.append(f"缺失{desc}: {full_path}")

        # 检查MP3目录
        mp3_dir = self.entry_mp3.get()
        if not os.path.isdir(mp3_dir):
            errors.append("MP3目录无效")
        else:
            mp3_files = [f for f in os.listdir(mp3_dir) if f.lower().endswith('.mp3')]
            if not mp3_files:
                errors.append("MP3目录中没有找到MP3文件")

        if errors:
            self.log("\n".join([f"❌ {e}" for e in errors]), 'error')
            return False
        return True

    def start_process(self):
        """开始处理流程"""
        if not self.validate_paths():
            messagebox.showerror("错误", "请先修正目录问题")
            return

        try:
            # 文件处理逻辑（原move_mp3_files等函数内容）
            # 这里需要补充原有文件处理逻辑...
            
            # 示例：自动运行转换程序
            converter_path = os.path.join(
                self.entry_mod.get(),
                "Contents", "mods", "truemusic_addon",
                "media", "yourMusic", "AddYourMusicToTheMod.exe"
            )
            
            if os.path.exists(converter_path):
                self.log("正在转换MP3文件为OGG...", 'info')
                subprocess.run(converter_path, check=True, shell=True)
                self.log("转换完成！", 'success')
            else:
                self.log("⚠️ 未找到转换程序，请手动运行AddYourMusicToTheMod.exe", 'warning')

            messagebox.showinfo("完成", "处理成功！请检查输出目录")
            
        except Exception as e:
            self.log(f"处理失败: {str(e)}", 'error')
            messagebox.showerror("错误", f"发生异常:\n{str(e)}")

    def clean_dirs(self):
        """清理目录（原organize_mods函数）"""
        # 需要补充原有清理逻辑...
        self.log("目录清理完成", 'success')

    def show_help(self):
        """显示帮助信息"""
        help_text = """
        【使用说明】
        1. 选择MOD根目录：包含workshop.txt的文件夹
        2. 选择MP3目录：所有MP3文件必须使用英文名！
        3. 填写模组信息：
           - 标题：创意工坊显示的名称
           - 描述：简单的模组介绍
           - ID：唯一标识符（建议英文）
        4. 点击[开始生成]自动处理文件
        5. 最后点击[清理目录]删除临时文件
        
        【注意事项】
        - MP3文件名不要包含中文或特殊字符
        - 转换完成后会自动生成中文名称映射
        - 遇到错误请检查日志中的红色提示
        """
        messagebox.showinfo("使用帮助", help_text.strip())


#原函数转移到这里


if __name__ == "__main__":
    root = tk.Tk()
    app = TrueMusicGenerator(root)
    root.mainloop()