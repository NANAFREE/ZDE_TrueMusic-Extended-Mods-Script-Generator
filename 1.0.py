import os
import shutil
from tkinter import Tk, filedialog, Button, Text, END, Label, Frame, Entry

def generate_new_filenames(count):
    """生成新的文件名，使用字母组合"""
    def get_next_filename(current):
        if not current:
            return 'a'
        last_char = current[-1]
        if last_char == 'z':
            return get_next_filename(current[:-1]) + 'a'
        else:
            return current[:-1] + chr(ord(last_char) + 1)

    filenames = []
    current = ''
    for _ in range(count):
        current = get_next_filename(current)
        filenames.append(current)
    return filenames

def move_mp3_files(source_dir, target_dir1, target_dir2, log_text):
    """移动MP3文件并重命名"""
    # 确保源目录存在
    if not os.path.exists(source_dir):
        log_text.insert(END, f"MP3源目录 {source_dir} 不存在\n")
        return

    # 遍历源目录中的所有MP3文件并排序
    mp3_files = [filename for filename in os.listdir(source_dir) if filename.endswith('.mp3')]
    mp3_files.sort()

    # 生成新的文件名
    new_filenames = generate_new_filenames(len(mp3_files))

    # 创建映射文件内容
    mapping_content = []
    for original_filename, new_filename in zip(mp3_files, new_filenames):
        mapping_content.append(f"{original_filename} -> {new_filename}")

    # 写入映射文件
    mapping_file_path = os.path.join(target_dir1, 'mapping.txt')
    with open(mapping_file_path, 'w', encoding='utf-8') as mapping_file:
        mapping_file.write('\n'.join(mapping_content))
    log_text.insert(END, f"映射文件已生成: {mapping_file_path}\n")

    # 复制并重命名文件到目标目录1
    for original_filename, new_filename in zip(mp3_files, new_filenames):
        source_file_path = os.path.join(source_dir, original_filename)
        target_file_path1 = os.path.join(target_dir1, new_filename + '.mp3')

        try:
            shutil.copy(source_file_path, target_file_path1)
            log_text.insert(END, f"文件 {original_filename} 已复制并重命名为 {new_filename}.mp3 到 {target_dir1}\n")
        except Exception as e:
            log_text.insert(END, f"复制文件 {original_filename} 到 {target_dir1} 时出错: {e}\n")

    # 复制并重命名文件到目标目录2
    for original_filename, new_filename in zip(mp3_files, new_filenames):
        source_file_path = os.path.join(source_dir, original_filename)
        target_file_path2 = os.path.join(target_dir2, new_filename + '.mp3')

        try:
            shutil.copy(source_file_path, target_file_path2)
            log_text.insert(END, f"文件 {original_filename} 已复制并重命名为 {new_filename}.mp3 到 {target_dir2}\n")
        except Exception as e:
            log_text.insert(END, f"复制文件 {original_filename} 到 {target_dir2} 时出错: {e}\n")

    return mapping_content

def generate_item_file(mapping_content, base_dir, log_text):
    """根据映射文件生成ItemName_CN.txt文件"""
    translate_cn_dir = os.path.join(base_dir, 'lua', 'shared', 'Translate', 'CN')
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
    log_text.insert(END, f"ItemName_CN.txt 文件已生成: {item_file_path}\n")

def update_workshop_file(operation_directory, title, description, log_text):
    """更新workshop.txt文件中的title和description"""
    workshop_file_path = os.path.join(operation_directory, 'workshop.txt')
    
    if not os.path.exists(workshop_file_path):
        log_text.insert(END, f"文件 {workshop_file_path} 不存在\n")
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
    
    log_text.insert(END, f"workshop.txt 文件已更新: {workshop_file_path}\n")

def update_mod_info_file(operation_directory, name, id, log_text):
    """更新mod.info文件中的name和id"""
    mod_info_file_path = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon', 'mod.info')
    
    if not os.path.exists(mod_info_file_path):
        log_text.insert(END, f"文件 {mod_info_file_path} 不存在\n")
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
            new_lines.append(f"id={id}_mod\n")
        else:
            new_lines.append(line)

    # 写回mod.info文件
    with open(mod_info_file_path, 'w', encoding='utf-8') as mod_info_file:
        mod_info_file.writelines(new_lines)
    
    log_text.insert(END, f"mod.info 文件已更新: {mod_info_file_path}\n")

def organize_mods(operation_directory, log_text):
    """规整化mods目录，删除除了TCBoombox和TCVinylplayer以外的所有文件"""
    your_music_dir = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon', 'media', 'yourMusic')
    
    if not os.path.exists(your_music_dir):
        log_text.insert(END, f"目录 {your_music_dir} 不存在\n")
        return

    # 遍历yourMusic目录中的所有文件和文件夹
    for item in os.listdir(your_music_dir):
        item_path = os.path.join(your_music_dir, item)
        
        if item not in ['TCBoombox', 'TCVinylplayer']:
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                log_text.insert(END, f"已删除: {item_path}\n")
            except Exception as e:
                log_text.insert(END, f"删除 {item_path} 时出错: {e}\n")

    # 规整化TCBoombox和TCVinylplayer目录
    for directory in ['TCBoombox', 'TCVinylplayer']:
        target_dir = os.path.join(your_music_dir, directory)
        
        if os.path.exists(target_dir):
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
                
                if not item.endswith('.ogg'):
                    try:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        log_text.insert(END, f"已删除: {item_path}\n")
                    except Exception as e:
                        log_text.insert(END, f"删除 {item_path} 时出错: {e}\n")
        else:
            log_text.insert(END, f"目录 {target_dir} 不存在\n")

def process_files(operation_directory, mp3_directory, title, description, name, mod_id, log_text):
    # 定义目标目录，基于用户选择的目录
    target_directory1 = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon', 'media', 'yourMusic', 'TCBoombox')
    target_directory2 = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon', 'media', 'yourMusic', 'TCVinylplayer')

    # 检查目标目录是否存在
    if not os.path.exists(target_directory1):
        log_text.insert(END, f"目标目录 {target_directory1} 不存在，请检查目录结构\n")
        return

    if not os.path.exists(target_directory2):
        log_text.insert(END, f"目标目录 {target_directory2} 不存在，请检查目录结构\n")
        return

    # 移动MP3文件并获取映射内容
    mapping_content = move_mp3_files(mp3_directory, target_directory1, target_directory2, log_text)

    # 生成ItemName_CN.txt文件
    base_dir = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon', 'media')
    generate_item_file(mapping_content, base_dir, log_text)

    # 更新workshop.txt文件
    update_workshop_file(operation_directory, title, description, log_text)

    # 更新mod.info文件
    update_mod_info_file(operation_directory, name, mod_id, log_text)

def select_operation_directory(operation_entry, log_text):
    # 获取用户选择的操作目录
    operation_directory = filedialog.askdirectory(title="请选择要操作的目录")
    if operation_directory:
        operation_entry.delete(0, END)
        operation_entry.insert(END, operation_directory)
    else:
        log_text.insert(END, "未选择操作目录\n")

def select_mp3_directory(mp3_entry, log_text):
    # 获取用户选择的MP3目录
    mp3_directory = filedialog.askdirectory(title="请选择包含MP3文件的目录")
    if mp3_directory:
        mp3_entry.delete(0, END)
        mp3_entry.insert(END, mp3_directory)
    else:
        log_text.insert(END, "未选择MP3目录\n")

def export_mods(operation_directory, log_text):
    """导出mods目录到脚本的根目录"""
    source_mods_dir = os.path.join(operation_directory, 'Contents', 'mods', 'truemusic_addon')
    target_mods_dir = os.path.join(os.path.dirname(__file__), 'truemusic_addon')

    if not os.path.exists(source_mods_dir):
        log_text.insert(END, f"源mods目录 {source_mods_dir} 不存在\n")
        return

    # 确保目标目录不存在，如果存在则删除
    if os.path.exists(target_mods_dir):
        try:
            shutil.rmtree(target_mods_dir)
            log_text.insert(END, f"已删除旧的目标mods目录: {target_mods_dir}\n")
        except Exception as e:
            log_text.insert(END, f"删除旧的目标mods目录时出错: {e}\n")
            return

    try:
        # 复制源mods目录到目标目录
        shutil.copytree(source_mods_dir, target_mods_dir)
        log_text.insert(END, f"mods目录已成功导出到: {target_mods_dir}\n")
    except Exception as e:
        log_text.insert(END, f"导出mods目录时出错: {e}\n")

def main():
    # 创建主窗口
    root = Tk()
    root.title("True Music Addon 音乐快速生成工具")
    root.geometry("650x800")

    # 创建框架以组织按钮和标签
    frame = Frame(root)
    frame.pack(pady=20)

    # 创建按钮和标签以选择操作目录
    Label(frame, text="选择要操作的目录:").grid(row=0, column=0, padx=10, pady=10)
    operation_entry = Entry(frame, width=50)
    operation_entry.grid(row=0, column=1, padx=10, pady=10)
    Button(frame, text="选择目录", command=lambda: select_operation_directory(operation_entry, log_text)).grid(row=0, column=2, padx=10, pady=10)

    # 创建按钮和标签以选择MP3目录
    Label(frame, text="选择MP3文件所在的目录:").grid(row=1, column=0, padx=10, pady=10)
    mp3_entry = Entry(frame, width=50)
    mp3_entry.grid(row=1, column=1, padx=10, pady=10)
    Button(frame, text="选择目录", command=lambda: select_mp3_directory(mp3_entry, log_text)).grid(row=1, column=2, padx=10, pady=10)

    # 创建输入框以输入title和description
    Label(frame, text="输入Title:").grid(row=2, column=0, padx=10, pady=10)
    title_entry = Entry(frame, width=50)
    title_entry.grid(row=2, column=1, padx=10, pady=10)

    Label(frame, text="输入Description:").grid(row=3, column=0, padx=10, pady=10)
    description_entry = Entry(frame, width=50)
    description_entry.grid(row=3, column=1, padx=10, pady=10)

    # 创建输入框以输入name和id
    Label(frame, text="输入Name:").grid(row=4, column=0, padx=10, pady=10)
    name_entry = Entry(frame, width=50)
    name_entry.grid(row=4, column=1, padx=10, pady=10)

    Label(frame, text="输入ID:").grid(row=5, column=0, padx=10, pady=10)
    id_entry = Entry(frame, width=50)
    id_entry.grid(row=5, column=1, padx=10, pady=10)

    # 创建“开始”按钮
    Button(frame, text="开始", command=lambda: process_files(operation_entry.get(), mp3_entry.get(), title_entry.get(), description_entry.get(), name_entry.get(), id_entry.get(), log_text)).grid(row=6, column=0, columnspan=3, padx=10, pady=10)
    #提示注释
    
    # 创建“规整化mods”按钮
    Button(frame, text="规整化mods", command=lambda: organize_mods(operation_entry.get(), log_text)).grid(row=7, column=0, columnspan=3, padx=10, pady=10)
    # 提示注释
    Label(frame, text="点击开始后需要先规整化mods目录来确保格式的统一").grid(row=8, column=0, columnspan=3, padx=10, pady=10)

    # 创建“导出mods”按钮
    Button(frame, text="导出mods", command=lambda: export_mods(operation_entry.get(), log_text)).grid(row=9, column=0, columnspan=3, padx=10, pady=10)
    # 提示注释
    Label(frame, text="点击导出mods按钮将操作目录中的mods文件夹导出到脚本的根目录下").grid(row=10, column=0, columnspan=3, padx=10, pady=10)

    # 创建日志文本框
    log_text = Text(root, height=20, width=60)
    log_text.pack(pady=20)

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()
