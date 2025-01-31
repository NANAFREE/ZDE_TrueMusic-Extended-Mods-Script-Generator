import os
import shutil
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
        self.create_tooltip(self.entry_title, "在创意工坊显示的名称")

        ttk.Label(info_frame, text="模组描述:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_desc = ttk.Entry(info_frame, width=40)
        self.entry_desc.grid(row=1, column=1, padx=5, sticky='ew')
        self.create_tooltip(self.entry_desc, "简单的模组介绍")

        ttk.Label(info_frame, text="模组ID:").grid(row=2, column=0, sticky='w')
        self.entry_id = ttk.Entry(info_frame, width=40)
        self.entry_id.grid(row=2, column=1, padx=5, sticky='ew')
        self.create_tooltip(self.entry_id, "英文+数字组合，如my_music_01")

        ttk.Label(info_frame, text="导出文件夹名称:").grid(row=3, column=0, sticky='w', pady=5)
        self.entry_export_name = ttk.Entry(info_frame, width=40)
        self.entry_export_name.grid(row=3, column=1, padx=5, sticky='ew')
        self.entry_export_name.insert(0, "TrueMusicaddon_")  # 默认名称
        self.create_tooltip(self.entry_export_name, "自定义导出文件夹的名称")

        # 操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        self.btn_start = ttk.Button(btn_frame, text="开始生成", command=self.start_process)
        self.btn_start.grid(row=0, column=0, padx=5)

        self.btn_clean = ttk.Button(btn_frame, text="清理目录", command=self.clean_dirs, state=tk.DISABLED)
        self.btn_clean.grid(row=0, column=1, padx=5)

        self.btn_export = ttk.Button(btn_frame, text="导出Mods", command=self.export_mods, state=tk.DISABLED)
        self.btn_export.grid(row=0, column=2, padx=5)

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
            # 移动MP3文件并获取映射内容
            mp3_directory = self.entry_mp3.get()
            operation_directory = self.entry_mod.get()
            title = self.entry_title.get()
            description = self.entry_desc.get()
            id_entry = self.entry_id.get()
            name_entry = self.entry_id.get()

            # 移动MP3文件并重命名
            mapping_content = self.move_mp3_files(mp3_directory, operation_directory, title, description, name_entry, id_entry)

            # 生成ItemName_CN.txt文件
            self.generate_item_file(mapping_content, operation_directory)

            # 更新workshop.txt文件
            self.update_workshop_file(operation_directory, title, description)

            # 更新mod.info文件
            self.update_mod_info_file(operation_directory, name_entry, id_entry)

            converter_path = os.path.join(
                operation_directory,
                "Contents", "mods", "truemusic_addon",
                "media", "yourMusic", "AddYourMusicToTheMod.exe"
            )

            if os.path.exists(converter_path):
                self.log("请手动运行转换程序 AddYourMusicToTheMod.exe 来转换MP3文件为OGG", 'info')
                messagebox.showinfo("提示", f"请手动运行转换程序: {converter_path}")
            else:
                self.log("⚠️ 未找到转换程序，请手动运行AddYourMusicToTheMod.exe", 'warning')
                messagebox.showwarning("警告", "未找到转换程序，请手动运行 AddYourMusicToTheMod.exe")

            # 启用清理目录按钮
            self.btn_clean.config(state=tk.NORMAL)

            messagebox.showinfo("完成", "处理成功！请检查输出目录")

        except Exception as e:
            self.log(f"处理失败: {str(e)}", 'error')
            messagebox.showerror("错误", f"发生异常:\n{str(e)}")

    def clean_dirs(self):
        """清理目录"""
        operation_directory = self.entry_mod.get()
        self.organize_mods(operation_directory)

        # 启用导出Mods按钮
        self.btn_export.config(state=tk.NORMAL)

    def export_mods(self):
        """导出处理后的mods目录"""
        operation_directory = self.entry_mod.get()
        mods_source_dir = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon')
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 获取用户输入的导出名称
        export_name = self.entry_export_name.get().strip()
        if not export_name:
            export_name = "TrueMusicaddon_"  # 默认名称

        # 构建目标目录路径
        mods_target_dir = os.path.join(script_dir, export_name)

        try:
            # 复制mods目录及其内容到脚本所在目录
            shutil.copytree(mods_source_dir, mods_target_dir)
            self.log(f"mods目录已导出到: {mods_target_dir}", 'success')
            messagebox.showinfo("完成", f"mods目录已导出到: {mods_target_dir}")
        except Exception as e:
            self.log(f"导出mods目录时出错: {str(e)}", 'error')
            messagebox.showerror("错误", f"导出mods目录时出错:\n{str(e)}")

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
        5. 点击[清理目录]删除临时文件
        6. 点击[导出Mods]导出处理后的mods目录
        
        【注意事项】
        - MP3文件名不要包含中文或特殊字符
        - 转换完成后会自动生成中文名称映射
        - 遇到错误请检查日志中的红色提示
        """
        messagebox.showinfo("使用帮助", help_text.strip())

    def generate_new_filenames(self, count):
        """生成新的文件名，使用字母组合"""
        def get_next_filename(current):
            if not current:
                return 'a'
            last_char = current[-1]
            if last_char == 'z':
                return self.get_next_filename(current[:-1]) + 'a'
            else:
                return current[:-1] + chr(ord(last_char) + 1)

        filenames = []
        current = ''
        for _ in range(count):
            current = get_next_filename(current)
            filenames.append(current)
        return filenames

    def move_mp3_files(self, source_dir, target_dir, title, description, name_entry, id_entry):
        # 移动MP3文件并重命名
        # 确保源目录存在
        if not os.path.exists(source_dir):
            self.log(f"MP3源目录 {source_dir} 不存在", 'error')
            return

        # 遍历源目录中的所有MP3文件并排序
        mp3_files = [filename for filename in os.listdir(source_dir) if filename.lower().endswith('.mp3')]
        mp3_files.sort()

        # 生成新的文件名
        new_filenames = self.generate_new_filenames(len(mp3_files))

        # 创建映射文件内容
        mapping_content = []
        for original_filename, new_filename in zip(mp3_files, new_filenames):
            mapping_content.append(f"{original_filename} -> {new_filename}")

        # 写入映射文件
        mapping_file_path = os.path.join(target_dir, 'Contents', 'mods', 'truemusic_addon', 'media', 'yourMusic', 'mapping.txt')
        with open(mapping_file_path, 'w', encoding='utf-8') as mapping_file:
            mapping_file.write('\n'.join(mapping_content))
        self.log(f"映射文件已生成: {mapping_file_path}", 'success')

        # 复制并重命名文件到目标目录1
        for original_filename, new_filename in zip(mp3_files, new_filenames):
            source_file_path = os.path.join(source_dir, original_filename)
            target_file_path1 = os.path.join(target_dir, 'Contents', 'mods', 'truemusic_addon', 'media', 'yourMusic', 'TCBoombox', new_filename + '.mp3')

            try:
                shutil.copy(source_file_path, target_file_path1)
                self.log(f"文件 {original_filename} 已复制并重命名为 {new_filename}.mp3 到 {target_dir}/TCBoombox\n", 'success')
            except Exception as e:
                self.log(f"复制文件 {original_filename} 到 {target_dir}/TCBoombox 时出错: {e}", 'error')

        # 复制并重命名文件到目标目录2
        for original_filename, new_filename in zip(mp3_files, new_filenames):
            source_file_path = os.path.join(source_dir, original_filename)
            target_file_path2 = os.path.join(target_dir, 'Contents', 'mods', 'truemusic_addon', 'media', 'yourMusic', 'TCVinylplayer', new_filename + '.mp3')

            try:
                shutil.copy(source_file_path, target_file_path2)
                self.log(f"文件 {original_filename} 已复制并重命名为 {new_filename}.mp3 到 {target_dir}/TCVinylplayer\n", 'success')
            except Exception as e:
                self.log(f"复制文件 {original_filename} 到 {target_dir}/TCVinylplayer 时出错: {e}", 'error')

        return mapping_content

    def generate_item_file(self, mapping_content, base_dir):
        """根据映射文件生成ItemName_CN.txt文件"""
        translate_cn_dir = os.path.join(base_dir, 'Contents', 'mods', 'truemusic_addon', 'media', 'lua', 'shared', 'Translate', 'CN')
        os.makedirs(translate_cn_dir, exist_ok=True)

        item_file_path = os.path.join(translate_cn_dir, 'ItemName_CN.txt')

        with open(item_file_path, 'w', encoding='utf-8') as item_file:
            item_file.write('ItemName_CN = {\n')
            for line in mapping_content:
                original_filename, new_filename = line.split(' -> ')
                new_filename = new_filename.replace('.mp3', '')
                item_file.write(f'    ItemName_Tsarcraft.Cassette{new_filename} = "磁带/{original_filename}",\n')
                item_file.write(f'    ItemName_Tsarcraft.Vinyl{new_filename} = "黑胶/{original_filename}",\n')
            item_file.write('}\n')
        self.log(f"ItemName_CN.txt 文件已生成: {item_file_path}", 'success')

    def update_workshop_file(self, operation_directory, title, description):
        """更新workshop.txt文件中的title和description"""
        workshop_file_path = os.path.join(operation_directory, 'workshop.txt')

        if not os.path.exists(workshop_file_path):
            self.log(f"文件 {workshop_file_path} 不存在", 'error')
            return

        # 读取workshop.txt文件内容
        with open(workshop_file_path, 'r', encoding='utf-8') as workshop_file:
            lines = workshop_file.readlines()

        # 更新title和description
        new_lines = []
        for line in lines:
            if line.startswith('title='):
                new_lines.append(f"title=True Music Addon: {title}\n")
            elif line.startswith('description='):
                new_lines.append(f"description={description}\n")
            else:
                new_lines.append(line)

        # 写回workshop.txt文件
        with open(workshop_file_path, 'w', encoding='utf-8') as workshop_file:
            workshop_file.writelines(new_lines)

        self.log(f"workshop.txt 文件已更新: {workshop_file_path}", 'success')

    def update_mod_info_file(self, operation_directory, name, id_entry):
        """更新mod.info文件中的name和id"""
        mod_info_file_path = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon', 'mod.info')

        if not os.path.exists(mod_info_file_path):
            self.log(f"文件 {mod_info_file_path} 不存在", 'error')
            return

        # 读取mod.info文件内容
        with open(mod_info_file_path, 'r', encoding='utf-8') as mod_info_file:
            lines = mod_info_file.readlines()

        # 更新name和id
        new_lines = []
        for line in lines:
            if line.startswith('name='):
                new_lines.append(f"name=True Music Addon: {name}\n")
            elif line.startswith('id='):
                new_lines.append(f"id={id_entry}_mod\n")
            else:
                new_lines.append(line)

        # 写回mod.info文件
        with open(mod_info_file_path, 'w', encoding='utf-8') as mod_info_file:
            mod_info_file.writelines(new_lines)

        self.log(f"mod.info 文件已更新: {mod_info_file_path}", 'success')

    def organize_mods(self, operation_directory):
        """规整化mods目录，删除除了TCBoombox和TCVinylplayer以外的所有文件"""
        your_music_dir = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon', 'media', 'yourMusic')

        if not os.path.exists(your_music_dir):
            self.log(f"目录 {your_music_dir} 不存在", 'error')
            return

        # 删除yourMusic目录中的所有文件和文件夹，除了TCBoombox和TCVinylplayer
        for item in os.listdir(your_music_dir):
            item_path = os.path.join(your_music_dir, item)

            if item not in ['TCBoombox', 'TCVinylplayer']:
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    self.log(f"已删除: {item_path}", 'success')
                except Exception as e:
                    self.log(f"删除 {item_path} 时出错: {e}", 'error')

        # 规整化TCBoombox和TCVinylplayer目录
        for directory in ['TCBoombox', 'TCVinylplayer']:
            target_dir = os.path.join(your_music_dir, directory)

            if os.path.exists(target_dir):
                for item in os.listdir(target_dir):
                    item_path = os.path.join(target_dir, item)

                    if not item.lower().endswith('.mp3'):
                        try:
                            if os.path.isfile(item_path):
                                os.remove(item_path)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                            self.log(f"已删除: {item_path}", 'success')
                        except Exception as e:
                            self.log(f"删除 {item_path} 时出错: {e}", 'error')
            else:
                self.log(f"目录 {target_dir} 不存在", 'error')

    def clean_dirs(self):
        """清理目录"""
        operation_directory = self.entry_mod.get()
        self.organize_mods(operation_directory)

        # 启用导出Mods按钮
        self.btn_export.config(state=tk.NORMAL)

    def export_mods(self):
        """导出处理后的mods目录"""
        operation_directory = self.entry_mod.get()
        mods_source_dir = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon')
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 获取用户输入的导出名称
        export_name = self.entry_export_name.get().strip()
        if not export_name:
            export_name = "TrueMusicaddon_"  # 默认名称

        # 构建目标目录路径
        mods_target_dir = os.path.join(script_dir, export_name)

        try:
            # 复制mods目录及其内容到脚本所在目录
            shutil.copytree(mods_source_dir, mods_target_dir)
            self.log(f"mods目录已导出到: {mods_target_dir}", 'success')
            messagebox.showinfo("完成", f"mods目录已导出到: {mods_target_dir}")
        except Exception as e:
            self.log(f"导出mods目录时出错: {str(e)}", 'error')
            messagebox.showerror("错误", f"导出mods目录时出错:\n{str(e)}")

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
           - 导出文件夹名称：自定义导出文件夹的名称
        4. 点击[开始生成]自动处理文件
        5. 点击[清理目录]删除临时文件
        6. 点击[导出Mods]导出处理后的mods目录
        
        【注意事项】
        - MP3文件名不要包含中文或特殊字符
        - 转换完成后会自动生成中文名称映射
        - 遇到错误请检查日志中的红色提示
        """
        messagebox.showinfo("使用帮助", help_text.strip())

    def generate_new_filenames(self, count):
        """生成新的文件名，使用字母组合"""
        def get_next_filename(current):
            if not current:
                return 'a'
            last_char = current[-1]
            if last_char == 'z':
                return self.get_next_filename(current[:-1]) + 'a'
            else:
                return current[:-1] + chr(ord(last_char) + 1)

        filenames = []
        current = ''
        for _ in range(count):
            current = get_next_filename(current)
            filenames.append(current)
        return filenames


if __name__ == "__main__":
    root = tk.Tk()
    app = TrueMusicGenerator(root)
    root.mainloop()
