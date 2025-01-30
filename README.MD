# True Music 生成工具 v2.0 🎵

✨ **为《僵尸毁灭工程》的 True Music Mod 快速生成扩展音乐 Mod 的工具** ✨

![GitHub Stars](https://img.shields.io/github/stars/yourusername/your-repo?style=social)  
![GitHub Forks](https://img.shields.io/github/forks/yourusername/your-repo?style=social)  
![GitHub Issues](https://img.shields.io/github/issues/yourusername/your-repo?color=red)  
![License](https://img.shields.io/badge/license-MIT-blue)  
![Python Version](https://img.shields.io/badge/python-3.x-green)  

---

## 简介 🌟

True Music 生成工具是一个为《僵尸毁灭工程》（Project Zomboid）的 **True Music Addon Mod** 设计的扩展生成工具。通过这个工具，你可以轻松地将自己喜欢的音乐添加到游戏中，并在游戏内通过 **磁带** 和 **唱片** 播放这些音乐。🎶

> **“让音乐在末日中回荡吧！”** 🎧

---

## 功能特性 🛠️

- **🎯 快速生成扩展 Mod**：只需几步操作，即可将 MP3 文件转换为游戏内可播放的磁带和唱片。
- **📝 自动重命名与映射**：自动将 MP3 文件重命名为符合游戏规范的格式，并生成中文名称映射文件。
- **⚙️ 自动更新配置文件**：自动更新 `workshop.txt` 和 `mod.info` 文件，确保 Mod 信息正确。
- **📜 日志记录**：提供详细的日志记录功能，帮助用户跟踪操作过程中的每一步。
- **🧹 清理功能**：提供清理功能，删除临时文件，保持 Mod 目录的整洁。

---

## 使用说明 📚

### 1. 准备工作 🛠️

- 确保你已经安装了《僵尸毁灭工程》并拥有 **True Music Addon Mod**。
- 准备好你想要添加到游戏中的 MP3 文件，确保文件名不包含中文或特殊字符。

### 2. 使用步骤 🚀

1. **选择 MOD 根目录**：
   - 点击“浏览...”按钮，选择包含 `workshop.txt` 文件的 True Music Addon 根目录。

2. **选择 MP3 目录**：
   - 点击“浏览...”按钮，选择包含你想要添加的 MP3 文件的文件夹。

3. **填写模组信息**：
   - **模组标题**：在创意工坊显示的 Mod 名称。
   - **模组描述**：简单的 Mod 介绍。
   - **模组 ID**：唯一标识符，建议使用英文和数字组合（如 `my_music_01`）。

4. **开始生成**：
   - 点击“开始生成”按钮，工具将自动处理 MP3 文件并生成扩展 Mod。

5. **清理目录**：
   - 生成完成后，点击“清理目录”按钮，删除临时文件，保持 Mod 目录整洁。

---

### 3. 注意事项 ⚠️

- **MP3 文件名**：确保 MP3 文件名不包含中文或特殊字符，否则可能导致生成失败。
- **转换程序**：如果工具未找到 `AddYourMusicToTheMod.exe` 转换程序，请手动运行该程序以完成 MP3 到 OGG 的转换。
- **日志检查**：如果遇到错误，请检查日志中的红色提示，根据提示修正问题。

---

## 安装与运行 🖥️

1. **下载脚本**：
   - 从 GitHub 仓库下载 `TrueMusicGenerator.py` 脚本文件。

2. **运行脚本**：
   - 确保你的系统已安装 Python 3.x 和 Tkinter 库。
   - 在命令行中运行以下命令启动脚本：
     ```bash
     python TrueMusicGenerator.py
     ```

3. **使用工具**：
   - 按照界面提示操作，生成你的扩展 Mod。

---

## 贡献与反馈 💬

如果你在使用过程中遇到任何问题，或有任何改进建议，欢迎在 GitHub 上提交 Issue 或 Pull Request。

![GitHub Issues](https://img.shields.io/github/issues/yourusername/your-repo?color=red)  
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/yourusername/your-repo?color=green)  

---

## 许可证 📜

本项目采用 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。

![License](https://img.shields.io/badge/license-MIT-blue)  

---
