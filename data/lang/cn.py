labels = {'generate_prompt': '生成提示', 'save_txt': '保存为 TXT', 'translated_prompt': '准备好的提示（EN）:', 'weight_plus': '权重 (+)', 'weight_minus': '权重 (-)', 'adjust_weight': '调整所选文本的权重:', 'help': '帮助', 'main_subject': '主要主题（图像中的人物或物体）', 'style_genre': '风格或类型（赛博朋克、巴洛克、概念艺术）', 'medium_technique': '媒介和技术（油画、铅笔素描、3D 渲染、照片）', 'realism_quality': '写实度或质量级别（高度详细、超逼真、4K、清晰聚焦）', 'composition': '构图和取景（肖像、等距视图、鸟瞰图）', 'background': '背景和环境（雪林、海底、白色背景）', 'lighting_mood': '光线和氛围（柔光、电影感光、落日余晖、霓虹灯）', 'colors_palette': '颜色 / 调色板 / 强调色 / 主要细节'}
help_text = """📘 Prompter 2 – 用户指南
创建者 Damizon • 2025

🎯 什么是 Prompter2
Prompter 是一个用于为 Stable Diffusion 创建高质量英文 prompts 的工具。
该程序会自动将输入的短语从 70 多种语言翻译成英文。
填写所需字段后，程序会按照正确顺序构建 prompt 并翻译。
无需填写所有字段——只需使用您当前需要的字段。

📝 如何使用该程序：

在文本字段中填写描述：

主要主题、风格、技法、光照、背景等。
使用逗号分隔每个 prompt 元素，可帮助 AI 将它们视为独立特征或指令。
避免使用句号 (.) —— 不需要。
引号无特殊含义。

词语权重表示其在 prompt 中的重要性。
权重越高，AI 对该词的关注度越高。
使用方法：

选中文本，使用 [+] 或 [–] 按钮调整权重。

示例：(cyberpunk:1.6) 增加 “cyberpunk” 的重要性。

示例：(cyberpunk:0.6) 降低 “cyberpunk” 的重要性。
🔻 1.0 = 正常
🔺 2.0 = 非常重要
🔻 0.5 = 较不重要

点击“生成 Prompt”：

字段将组合成一个完整的 prompt。

文本将自动翻译成英文。

翻译后的 prompt 会复制到剪贴板。

可选： 将 prompt 保存为 TXT 文件。

💡 提示：
• 结合短句和长句（例如“人像”、“巴洛克风格”）。
• 利用色彩和光线营造氛围（例如“霓虹灯”、“日落”）。
• 多尝试并预览效果！

🔗 帮助与项目开发：
github.com/Damizon/Prompter
"""
about = "Prompter 2 • Damizon 2025"



