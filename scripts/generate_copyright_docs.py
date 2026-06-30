#!/usr/bin/env python3
from __future__ import annotations

import html
import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path.cwd()
SOURCE_ROOT = ROOT / "source"
SHOT_DIR = ROOT / "截图"
BUILD_DIR = ROOT / "manual_build"
MD_DIR = BUILD_DIR / "markdown"
PREVIEW_DIR = BUILD_DIR / "preview"
OUT_DIR = ROOT / "out"

SOFTWARE_NAME = "BotLink Platform 智能体即时通讯平台"
SOFTWARE_SHORT = "BotLink Platform"
VERSION = "V1.0"
COMPLETED_DATE = "2026 年 05 月 18 日"
WRITING_DATE = "2026 年 06 月 29 日"
OUTPUT_BASENAME = "Botlink智能机器人即时通讯平台"
SOURCE_LINE_TOTAL = "5129"
APPLICATION_PROFILE = {
    "software_category": "应用软件",
    "software_description": "原创",
    "development_mode": "单独开发",
    "publication_status": "未发表",
    "development_hardware": "MacBook Pro、x86_64 或 ARM64 标准开发机，16GB RAM 以上",
    "runtime_hardware": "x86_64 云服务器或企业内网服务器，8GB RAM 以上",
    "development_os": "macOS、Windows 11、Linux",
    "development_tools": "VS Code、pnpm、Vite、TypeScript、Git、Docker",
    "runtime_platform": "Linux、Docker、Nginx、Node.js 服务端、Web 浏览器",
    "support_software": "Vue、Hono、PostgreSQL、Redis、WebSocket、Docker",
    "programming_languages": "TypeScript、Vue、SQL、CSS",
    "development_purpose": "提升企业智能体会话协同和消息处理效率",
    "target_domain": "企业智能办公、人机协同和智能体运营领域",
    "main_feature": (
        "本软件面向企业智能办公和人机协同沟通场景，围绕用户、智能体和本地 Agent Bridge 的消息协作构建即时通讯入口。"
        "用户可通过手机号验证码完成登录，首次登录自动创建账号并进入聊天工作台。智能体管理模块展示用户名下的智能体列表，"
        "呈现在线状态、最后回复时间和最后心跳信息，并提供发送消息、编辑和删除入口；创建智能体时可填写名称、描述和访问模式，"
        "提交后生成智能体记录和接入凭据。会话模块支持私聊、项目会话和多智能体协作会话，用户可在智能体或用户页签中选择参与者并创建会话。"
        "消息工作台展示会话列表、聊天对象、消息输入框、附件和表情入口，通过 WebSocket 实现实时投递，并提供搜索和定时任务入口。"
        "问题反馈模块支持填写问题、上传或粘贴截图并提交，便于运营人员跟踪处理。新手指南以侧栏形式展示登录、智能体创建、本地桥接配置、"
        "工作目录和移动端安装步骤，帮助新用户完成平台初始化和日常协同。系统能够统一管理智能体接入、会话成员、消息记录和反馈材料，"
        "使用户与智能体之间的协作过程可见、可追踪、可持续运营。同时，平台通过统一入口、状态记录、筛选查询和权限控制，帮助管理人员"
        "掌握业务流转情况，减少线下沟通和重复维护成本，形成从智能体接入、会话发起、消息处理到问题反馈的闭环管理能力。"
    ),
    "technical_feature": "采用Vue前端、Hono微服务、WebSocket网关、PostgreSQL和Redis，实现实时消息、会话协同和反馈处理。",
}
MANUAL_PROFILE = {
    "overview": (
        "BotLink Platform 用于连接用户、智能体和本地 Agent Bridge，提供基于会话的智能协同沟通能力。"
        "本手册按照实际截图顺序描述登录、智能体管理、创建智能体、新建会话、消息收发、问题反馈和新手指南功能。"
        "用户可按照章节步骤完成账号登录、智能体配置、会话创建和日常消息协同。"
    ),
    "runtime_environment": "用户通过浏览器访问 Web 客户端；服务端由 user、bot、conversation、message、operation 等微服务提供接口；网关负责 WebSocket 连接和实时消息投递。",
    "common_issues": "登录失败时检查手机号格式、验证码有效期和网络状态；智能体不在线时检查接入端 token、心跳和网关连接；消息未送达时查看会话参与者、WebSocket 状态和消息服务日志；反馈提交失败时检查截图数量、文件大小和用户登录状态。",
}
APPLICATION_LIMITS = {
    "development_hardware": (0, 50, "开发硬件环境"),
    "runtime_hardware": (0, 50, "运行硬件环境"),
    "development_os": (0, 50, "开发操作系统"),
    "development_tools": (0, 50, "开发工具"),
    "runtime_platform": (0, 50, "运行平台"),
    "support_software": (0, 50, "支撑软件"),
    "programming_languages": (0, 120, "编程语言"),
    "development_purpose": (0, 50, "开发目的"),
    "target_domain": (0, 50, "面向领域"),
    "main_feature": (500, 1300, "主要功能"),
    "technical_feature": (0, 100, "技术特点"),
}


SCREENSHOTS = [
    {
        "id": "S01",
        "file": "Snipaste_2026-06-25_18-10-18.png",
        "title": "手机号验证码登录",
        "module": "登录与身份认证",
        "desc": "登录页提供手机号和验证码输入，首次登录自动创建账号，验证通过后进入聊天工作台。",
        "steps": ["输入 11 位手机号。", "获取并填写 6 位验证码。", "点击登录，系统完成身份校验和自动注册。"],
        "sources": [
            "botlink-web/src/views/LoginView.vue",
            "botlink-web/src/api/auth.api.ts",
            "botlink-web/src/stores/auth.ts",
            "botlink-user-service/src/routes/auth.ts",
        ],
    },
    {
        "id": "S02",
        "file": "Snipaste_2026-06-25_18-08-47.png",
        "title": "智能体管理列表",
        "module": "智能体管理",
        "desc": "智能体管理页展示我的智能体，显示在线状态、最后回复、最后心跳，并提供发送消息、编辑和删除入口。",
        "steps": ["进入左侧智能体入口。", "在我的智能体页查看智能体卡片。", "根据状态选择发送消息、编辑或删除。"],
        "sources": [
            "botlink-web/src/views/BotListView.vue",
            "botlink-web/src/api/bot.api.ts",
            "botlink-bot-service/src/routes/bots.ts",
        ],
    },
    {
        "id": "S03",
        "file": "Snipaste_2026-06-25_18-09-00.png",
        "title": "创建新智能体",
        "module": "智能体创建",
        "desc": "创建弹窗收集智能体名称、描述和访问模式，提交后生成智能体记录和接入凭据。",
        "steps": ["点击新建智能体。", "填写智能体名称和描述。", "保持访问模式为私有或按需调整后提交。"],
        "sources": [
            "botlink-web/src/views/BotListView.vue",
            "botlink-web/src/views/botCreateDialogState.ts",
            "botlink-web/src/api/bot.api.ts",
            "botlink-bot-service/src/routes/bots.ts",
        ],
    },
    {
        "id": "S04",
        "file": "Snipaste_2026-06-25_18-09-33.png",
        "title": "新建会话并选择参与者",
        "module": "会话协同",
        "desc": "新建会话弹窗支持私聊、项目和多智能体协作类型，用户可在智能体或用户页签中选择参与者。",
        "steps": ["在聊天工作台点击新增会话。", "选择会话类型。", "切换智能体或用户页签，勾选参与者并创建会话。"],
        "sources": [
            "botlink-web/src/views/ChatView.vue",
            "botlink-web/src/api/conversation.api.ts",
            "botlink-conversation-service/src/routes/conversations.ts",
        ],
    },
    {
        "id": "S05",
        "file": "Snipaste_2026-06-25_18-08-20.png",
        "title": "用户聊天工作台",
        "module": "消息收发工作台",
        "desc": "聊天页展示会话列表、聊天对象、消息输入框、附件和表情入口，并提供搜索与定时任务入口。",
        "steps": ["选择左侧私聊或群聊会话。", "在底部输入框输入消息。", "点击发送后通过 WebSocket 和消息服务完成投递。"],
        "sources": [
            "botlink-web/src/views/ChatView.vue",
            "botlink-web/src/composables/useChat.ts",
            "botlink-web/src/stores/websocket.ts",
            "botlink-web/src/api/message.api.ts",
            "botlink-message-service/src/routes/internal.ts",
        ],
    },
    {
        "id": "S06",
        "file": "Snipaste_2026-06-25_18-09-18.png",
        "title": "问题反馈提交",
        "module": "反馈与运营处理",
        "desc": "反馈弹窗允许用户描述问题、添加截图并提交，后台服务保存反馈记录和截图文件，运营后台可继续处理状态。",
        "steps": ["点击侧栏问题反馈入口。", "填写问题描述。", "上传或粘贴截图后提交反馈。"],
        "sources": [
            "botlink-web/src/components/IssueFeedbackDialog.vue",
            "botlink-web/src/api/feedback.api.ts",
            "botlink-operation-service/src/routes/feedback.ts",
            "botlink-operation-service/src/feedback/storage.ts",
        ],
    },
    {
        "id": "S07",
        "file": "Snipaste_2026-06-25_18-09-49.png",
        "title": "新手指南侧栏",
        "module": "新手指南",
        "desc": "新手指南从右侧抽屉展示登录、创建智能体、配置 agent-bridge、Codex 工作目录和移动端安装步骤。",
        "steps": ["点击左侧指南入口。", "在右侧抽屉阅读 Bot-Link 新手指南。", "按章节完成账号、智能体和本地桥接配置。"],
        "sources": [
            "botlink-web/src/components/BeginnerGuideDrawer.vue",
            "botlink-web/src/assets/beginnerGuideContent.ts",
        ],
    },
]


CODE_SECTIONS = [
    {
        "title": "登录与身份认证",
        "screenshot": "S01",
        "blocks": [
            ("botlink-web/src/views/LoginView.vue", None),
            ("botlink-web/src/api/auth.api.ts", None),
            ("botlink-web/src/stores/auth.ts", None),
            ("botlink-user-service/src/routes/auth.ts", (1, 180)),
        ],
    },
    {
        "title": "智能体管理与创建",
        "screenshot": "S02、S03",
        "blocks": [
            ("botlink-web/src/views/BotListView.vue", (1, 230)),
            ("botlink-web/src/views/BotListView.vue", (260, 420)),
            ("botlink-web/src/views/botCreateDialogState.ts", None),
            ("botlink-web/src/api/bot.api.ts", None),
            ("botlink-bot-service/src/routes/bots.ts", (1, 260)),
            ("botlink-bot-service/src/routes/bots.ts", (396, 552)),
        ],
    },
    {
        "title": "会话创建与参与者选择",
        "screenshot": "S04",
        "blocks": [
            ("botlink-web/src/views/ChatView.vue", (1839, 2120)),
            ("botlink-web/src/api/conversation.api.ts", (1, 210)),
            ("botlink-conversation-service/src/routes/conversations.ts", (1, 180)),
            ("botlink-conversation-service/src/routes/conversations.ts", (1361, 1508)),
        ],
    },
    {
        "title": "聊天工作台与消息收发",
        "screenshot": "S05",
        "blocks": [
            ("botlink-web/src/views/ChatView.vue", (1, 140)),
            ("botlink-web/src/views/ChatView.vue", (1280, 1360)),
            ("botlink-web/src/views/ChatView.vue", (5815, 5915)),
            ("botlink-web/src/composables/useChat.ts", None),
            ("botlink-web/src/stores/websocket.ts", (1, 260)),
            ("botlink-web/src/api/message.api.ts", None),
            ("botlink-message-service/src/routes/internal.ts", (1, 230)),
            ("botlink-message-service/src/routes/internal.ts", (381, 557)),
        ],
    },
    {
        "title": "问题反馈与运营处理",
        "screenshot": "S06",
        "blocks": [
            ("botlink-web/src/components/IssueFeedbackDialog.vue", None),
            ("botlink-web/src/api/feedback.api.ts", None),
            ("botlink-operation-service/src/routes/feedback.ts", None),
            ("botlink-operation-service/src/feedback/storage.ts", (1, 220)),
            ("botlink-operation-service/src/feedback/storage.ts", (319, 399)),
        ],
    },
    {
        "title": "新手指南内容展示",
        "screenshot": "S07",
        "blocks": [
            ("botlink-web/src/components/BeginnerGuideDrawer.vue", None),
            ("botlink-web/src/assets/beginnerGuideContent.ts", None),
        ],
    },
]


def rel_source(path: str) -> Path:
    return SOURCE_ROOT / path


def check_inputs(only: set[str]) -> None:
    missing = []
    invalid_ranges = []
    if "manual" in only:
        for shot in SCREENSHOTS:
            path = SHOT_DIR / shot["file"]
            if not path.exists():
                missing.append(str(path))
    if "code" in only:
        for section in CODE_SECTIONS:
            for path, _ in section["blocks"]:
                source_path = rel_source(path)
                if not source_path.exists():
                    missing.append(str(source_path))
        for section in CODE_SECTIONS:
            for path, line_range in section["blocks"]:
                if not line_range:
                    continue
                source_path = rel_source(path)
                if not source_path.exists():
                    continue
                line_count = len(source_path.read_text(encoding="utf-8", errors="ignore").splitlines())
                start, end = line_range
                if start < 1 or end < start or end > line_count:
                    invalid_ranges.append(f"{path}: requested {start}-{end}, file has {line_count} lines")
    if missing:
        raise FileNotFoundError("缺少输入文件:\n" + "\n".join(missing))
    if invalid_ranges:
        raise ValueError("代码摘录行号越界:\n" + "\n".join(invalid_ranges))


def clean_build() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    MD_DIR.mkdir(parents=True)
    PREVIEW_DIR.mkdir(parents=True)


def copy_assets() -> None:
    asset_dir = BUILD_DIR / "assets"
    asset_dir.mkdir()
    for shot in SCREENSHOTS:
        shutil.copy2(SHOT_DIR / shot["file"], asset_dir / shot["file"])


def md_escape(text: str) -> str:
    return str(text).replace("|", "\\|")


def image_md(shot: dict, fig_no: int) -> str:
    path = str((BUILD_DIR / "assets" / shot["file"]).resolve())
    return f"![{shot['title']}]({path}){{width=92%}}\n"


def read_source(path: str, line_range: tuple[int, int] | None = None) -> tuple[str, int, int]:
    full = rel_source(path)
    lines = full.read_text(encoding="utf-8", errors="ignore").splitlines()
    if line_range:
        start, end = line_range
        selected = lines[start - 1 : end]
    else:
        start, end = 1, len(lines)
        selected = lines
    return "\n".join(selected), start, end


def code_fence_lang(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".vue":
        return "vue"
    if suffix == ".ts":
        return "typescript"
    if suffix == ".js":
        return "javascript"
    if suffix == ".css":
        return "css"
    return ""


def yaml_header(title: str, title_page: bool = True, running_header: str | None = None) -> str:
    metadata_title = title if title_page else ""
    header_text = running_header if running_header is not None else f"{SOFTWARE_NAME} {VERSION}"
    return f"""---
title: "{metadata_title}"
title-meta: "{title}"
author: ""
date: ""
documentclass: article
papersize: a4
fontsize: 10pt
geometry: "left=2.35cm,right=2.35cm,top=2.2cm,bottom=2.2cm"
mainfont: "Times New Roman"
CJKmainfont: "Songti SC"
monofont: "Menlo"
colorlinks: false
toc: false
header-includes:
  - \\usepackage{{xeCJK}}
  - \\setCJKmainfont{{Songti SC}}
  - \\usepackage{{fancyhdr}}
  - \\usepackage{{graphicx}}
  - \\usepackage{{float}}
  - \\usepackage{{longtable}}
  - \\usepackage{{booktabs}}
  - \\usepackage{{array}}
  - \\usepackage{{listings}}
  - \\lstset{{breaklines=true,breakatwhitespace=false,basicstyle=\\ttfamily\\scriptsize,columns=fullflexible,keepspaces=true,showstringspaces=false,frame=single}}
  - \\renewcommand{{\\figurename}}{{图}}
  - \\floatplacement{{figure}}{{H}}
  - \\pagestyle{{fancy}}
  - \\fancyhf{{}}
  - \\fancyhead[L]{{{header_text}}}
  - \\fancyfoot[C]{{\\thepage}}
  - \\setlength{{\\headheight}}{{15pt}}
  - \\setlength{{\\parindent}}{{2em}}
---

"""


def cover_page(doc_type: str) -> str:
    return f"""\\thispagestyle{{empty}}
\\begin{{center}}
\\vspace*{{0.30\\textheight}}
{{\\Huge\\bfseries {SOFTWARE_NAME}\\par}}
\\vspace{{1.8cm}}
{{\\LARGE {doc_type} {VERSION}\\par}}
\\vfill
{{\\Large 版本：{VERSION}\\par}}
\\vspace{{1.0cm}}
{{\\Large 编写日期：{WRITING_DATE}\\par}}
\\vspace*{{0.16\\textheight}}
\\end{{center}}
\\newpage

"""


def application_cover_page() -> str:
    return f"""\\thispagestyle{{empty}}
\\begin{{center}}
\\vspace*{{0.30\\textheight}}
{{\\Huge\\bfseries {SOFTWARE_NAME}\\par}}
\\vspace{{1.8cm}}
{{\\LARGE 软件著作权申请表 {VERSION}\\par}}
\\vfill
{{\\Large 版本：{VERSION}\\par}}
\\vspace{{1.0cm}}
{{\\Large 编写日期：{WRITING_DATE}\\par}}
\\vspace*{{0.16\\textheight}}
\\end{{center}}
\\newpage
\\setcounter{{page}}{{1}}

"""


def tex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in str(value))


def section_title(title: str) -> str:
    return f"\\begin{{center}}\\LARGE\\bfseries {tex_escape(title)}\\end{{center}}\n\n"


def bordered_table(rows: list[tuple[str, str]], col1: str = "3.2cm", col2: str = "11.6cm") -> str:
    lines = [
        "\\renewcommand{\\arraystretch}{1.25}\n",
        f"\\noindent\\begin{{longtable}}{{|p{{{col1}}}|p{{{col2}}}|}}\n",
        "\\hline\n",
        "\\textbf{项目} & \\textbf{内容} \\\\\n",
        "\\hline\n",
    ]
    for key, value in rows:
        lines.append(f"\\textbf{{{tex_escape(key)}}} & {tex_escape(value)} \\\\\n")
        lines.append("\\hline\n")
    lines.append("\\end{longtable}\n\n")
    return "".join(lines)


def validate_application_profile() -> None:
    errors = []
    for key, (min_len, max_len, label) in APPLICATION_LIMITS.items():
        value = str(APPLICATION_PROFILE.get(key, ""))
        length = len(value)
        if length < min_len or length > max_len:
            errors.append(f"{label}({key}) 长度 {length}，要求 {min_len}-{max_len} 字")
    if errors:
        raise ValueError("申请表字段不符合当前填报规则:\n" + "\n".join(errors))


def toc_page() -> str:
    return """\\thispagestyle{empty}
\\renewcommand{\\contentsname}{目录}
\\setcounter{tocdepth}{3}
\\tableofcontents
\\newpage

"""


def make_application() -> str:
    content = [yaml_header(f"{SOFTWARE_NAME} {VERSION} 申请表", title_page=False, running_header=f"{SOFTWARE_NAME} {VERSION} 申请表")]
    content.append(application_cover_page())

    basic_rows = [
        ("权利取得方式", "原始取得"),
        ("软件全称", SOFTWARE_NAME),
        ("软件版本", VERSION),
        ("权利范围", "全部权利"),
    ]
    content.append(section_title("软件基本信息"))
    content.append(bordered_table(basic_rows))

    property_rows = [
        ("软件分类", APPLICATION_PROFILE["software_category"]),
        ("软件说明", APPLICATION_PROFILE["software_description"]),
        ("开发方式", APPLICATION_PROFILE["development_mode"]),
        ("开发完成日期", COMPLETED_DATE),
        ("发表状态", APPLICATION_PROFILE["publication_status"]),
    ]
    content.append(section_title("软件属性"))
    content.append(bordered_table(property_rows))

    tech_rows = [
        ("开发硬件环境", APPLICATION_PROFILE["development_hardware"]),
        ("运行硬件环境", APPLICATION_PROFILE["runtime_hardware"]),
        ("开发操作系统", APPLICATION_PROFILE["development_os"]),
        ("开发工具", APPLICATION_PROFILE["development_tools"]),
        ("运行平台", APPLICATION_PROFILE["runtime_platform"]),
        ("支撑软件", APPLICATION_PROFILE["support_software"]),
        ("编程语言", APPLICATION_PROFILE["programming_languages"]),
        ("源程序总行数", SOURCE_LINE_TOTAL),
        ("开发目的", APPLICATION_PROFILE["development_purpose"]),
        ("面向领域", APPLICATION_PROFILE["target_domain"]),
    ]
    content.append(section_title("技术与功能"))
    content.append(bordered_table(tech_rows))

    main_feature = APPLICATION_PROFILE["main_feature"]
    tech_feature = APPLICATION_PROFILE["technical_feature"]
    content.append("\\newpage\n")
    content.append(bordered_table([
        ("主要功能", main_feature),
        ("技术特点", tech_feature),
    ]))
    return "".join(content)


def make_manual() -> str:
    content = [yaml_header(f"{SOFTWARE_NAME} {VERSION} 操作手册", title_page=False, running_header="")]
    content.append(cover_page("操作手册"))
    content.append(toc_page())
    content.append("## 1 软件概述\n")
    content.append(f"{MANUAL_PROFILE['overview']}\n\n")
    content.append("## 2 运行环境\n")
    content.append(f"{MANUAL_PROFILE['runtime_environment']}\n\n")
    content.append("## 3 功能操作说明\n")
    fig_no = 1
    for idx, shot in enumerate(SCREENSHOTS, 1):
        if shot.get("page_break_before"):
            content.append("\\newpage\n\n")
        content.append(f"### 3.{idx} {shot['module']}\n")
        content.append(f"{shot['desc']}\n\n")
        content.append("操作步骤：\n\n")
        for step_no, step in enumerate(shot["steps"], 1):
            content.append(f"{step_no}. {step}\n")
        content.append("\n")
        content.append(image_md(shot, fig_no))
        fig_no += 1
        content.append("\n")
    content.append("## 4 常见问题处理\n")
    content.append(f"{MANUAL_PROFILE['common_issues']}\n")
    return "".join(content)


def make_code_doc() -> str:
    content = [yaml_header(f"{SOFTWARE_NAME} {VERSION} 代码文档", title_page=False, running_header="")]
    content.append(cover_page("代码文档"))
    total = 0
    for idx, section in enumerate(CODE_SECTIONS, 1):
        content.append(f"## {idx} {section['title']}\n")
        content.append(f"对应截图：{section['screenshot']}。本章代码实现操作手册中“{section['title']}”相关功能。\n\n")
        for block_idx, (path, line_range) in enumerate(section["blocks"], 1):
            code, start, end = read_source(path, line_range)
            total += len(code.splitlines())
            content.append(f"### {idx}.{block_idx} {path}（第 {start}-{end} 行）\n\n")
            content.append(f"```{code_fence_lang(path)}\n{code}\n```\n\n")
    content.append(f"\n## 源程序摘录统计\n\n本代码文档共摘录有效源程序 {total} 行，并按功能章节组织。\n")
    return "".join(content)


def write_markdown(only: set[str]) -> dict[str, Path]:
    docs = {
        "application": (f"{SOFTWARE_NAME}_{VERSION}_申请表.md", make_application),
        "manual": (f"{SOFTWARE_NAME}_{VERSION}_操作手册.md", make_manual),
        "code": (f"{SOFTWARE_NAME}_{VERSION}_代码文档.md", make_code_doc),
    }
    result = {}
    for key, (name, make_content) in docs.items():
        if key not in only:
            continue
        path = MD_DIR / name
        path.write_text(make_content(), encoding="utf-8")
        result[key] = path
    return result


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=str(cwd or ROOT), check=True)


def render_pdf(md_paths: dict[str, Path]) -> dict[str, Path]:
    pdf_paths = {}
    for key, md_path in md_paths.items():
        pdf_path = BUILD_DIR / md_path.name.replace(".md", ".pdf")
        run([
            "pandoc",
            str(md_path),
            "--pdf-engine=xelatex",
            "--listings",
            "--toc" if key != "application" else "--metadata=toc:false",
            "-o",
            str(pdf_path),
        ])
        pdf_paths[key] = pdf_path
    return pdf_paths


def copy_to_out(pdf_paths: dict[str, Path]) -> dict[str, Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    names = {
        "application": f"{OUTPUT_BASENAME}_申请表.pdf",
        "manual": f"{OUTPUT_BASENAME}_操作手册.pdf",
        "code": f"{OUTPUT_BASENAME}_代码文档.pdf",
    }
    out_paths = {}
    for key in pdf_paths:
        name = names[key]
        out_path = OUT_DIR / name
        shutil.copy2(pdf_paths[key], out_path)
        out_paths[key] = out_path
    return out_paths


def pdf_pages(path: Path) -> int:
    result = subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True, text=True)
    match = re.search(r"^Pages:\s+(\d+)$", result.stdout, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"无法读取 PDF 页数: {path}")
    return int(match.group(1))


def validate_rendered_pdfs(pdf_paths: dict[str, Path], args: argparse.Namespace) -> None:
    if "code" in pdf_paths and (args.code_page_min or args.code_page_max):
        pages = pdf_pages(pdf_paths["code"])
        if args.code_page_min and pages < args.code_page_min:
            raise ValueError(f"代码文档页数 {pages} 小于下限 {args.code_page_min}")
        if args.code_page_max and pages > args.code_page_max:
            raise ValueError(f"代码文档页数 {pages} 大于上限 {args.code_page_max}")


def preview_pdfs(pdf_paths: dict[str, Path]) -> None:
    preview_targets = {
        "application": (1, 3),
        "manual": (1, 14),
        "code": (1, 6),
    }
    for key, (first, last) in preview_targets.items():
        if key not in pdf_paths:
            continue
        out_prefix = PREVIEW_DIR / key / "page"
        out_prefix.parent.mkdir(parents=True, exist_ok=True)
        run([
            "pdftoppm",
            "-png",
            "-f",
            str(first),
            "-l",
            str(last),
            "-r",
            "120",
            str(pdf_paths[key]),
            str(out_prefix),
        ])


def normalize_code_sections(items: list[dict]) -> list[dict]:
    normalized = []
    for section in items:
        blocks = []
        for block in section["blocks"]:
            if isinstance(block, dict):
                line_range = block.get("line_range")
                blocks.append((block["path"], tuple(line_range) if line_range else None))
            else:
                path = block[0]
                line_range = block[1] if len(block) > 1 else None
                blocks.append((path, tuple(line_range) if line_range else None))
        normalized.append({
            "title": section["title"],
            "screenshot": section["screenshot"],
            "blocks": blocks,
        })
    return normalized


def apply_config(config: dict) -> None:
    global SOFTWARE_NAME, SOFTWARE_SHORT, VERSION, COMPLETED_DATE, WRITING_DATE
    global OUTPUT_BASENAME, SOURCE_LINE_TOTAL, SCREENSHOTS, CODE_SECTIONS
    global APPLICATION_PROFILE, MANUAL_PROFILE

    SOFTWARE_NAME = config.get("software_name", SOFTWARE_NAME)
    SOFTWARE_SHORT = config.get("software_short", SOFTWARE_SHORT)
    VERSION = config.get("version", VERSION)
    COMPLETED_DATE = config.get("completed_date", COMPLETED_DATE)
    WRITING_DATE = config.get("writing_date", WRITING_DATE)
    OUTPUT_BASENAME = config.get("output_basename", OUTPUT_BASENAME)
    SOURCE_LINE_TOTAL = str(config.get("source_line_total", SOURCE_LINE_TOTAL))
    if "application_profile" in config:
        APPLICATION_PROFILE = {**APPLICATION_PROFILE, **config["application_profile"]}
    if "manual_profile" in config:
        MANUAL_PROFILE = {**MANUAL_PROFILE, **config["manual_profile"]}
    if "screenshots" in config:
        SCREENSHOTS = config["screenshots"]
    if "code_sections" in config:
        CODE_SECTIONS = normalize_code_sections(config["code_sections"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate software copyright application, operation manual, and code document PDFs from source code and screenshots."
    )
    parser.add_argument("--root", type=Path, default=ROOT, help="Working/output root. Defaults to current directory.")
    parser.add_argument("--source-root", type=Path, default=None, help="Project source code root.")
    parser.add_argument("--screenshots-dir", type=Path, default=None, help="Directory containing real product screenshots.")
    parser.add_argument("--build-dir", type=Path, default=None, help="Intermediate build directory.")
    parser.add_argument("--out-dir", type=Path, default=None, help="Final PDF output directory.")
    parser.add_argument("--config", type=Path, default=None, help="JSON config for software metadata, screenshot map, and source sections.")
    parser.add_argument("--only", choices=["all", "application", "manual", "code"], default="all", help="Generate all documents or a single document type.")
    parser.add_argument("--skip-preview", action="store_true", help="Do not render PDF preview PNGs.")
    parser.add_argument("--skip-application-validation", action="store_true", help="Skip application-form field length validation.")
    parser.add_argument("--code-page-min", type=int, default=None, help="Fail if generated code document has fewer pages.")
    parser.add_argument("--code-page-max", type=int, default=None, help="Fail if generated code document has more pages.")
    return parser.parse_args()


def configure_paths(args: argparse.Namespace) -> None:
    global ROOT, SOURCE_ROOT, SHOT_DIR, BUILD_DIR, MD_DIR, PREVIEW_DIR, OUT_DIR

    ROOT = args.root.resolve()
    SOURCE_ROOT = (args.source_root.resolve() if args.source_root else (ROOT / "source")).resolve()
    SHOT_DIR = (args.screenshots_dir or (ROOT / "截图")).resolve()
    BUILD_DIR = (args.build_dir or (ROOT / "manual_build")).resolve()
    MD_DIR = BUILD_DIR / "markdown"
    PREVIEW_DIR = BUILD_DIR / "preview"
    OUT_DIR = (args.out_dir or (ROOT / "out")).resolve()


def main() -> None:
    args = parse_args()
    configure_paths(args)
    if args.config:
        apply_config(json.loads(args.config.read_text(encoding="utf-8")))
    only = {"application", "manual", "code"} if args.only == "all" else {args.only}
    if "application" in only and not args.skip_application_validation:
        validate_application_profile()
    check_inputs(only)
    clean_build()
    if "manual" in only:
        copy_assets()
    md_paths = write_markdown(only)
    pdf_paths = render_pdf(md_paths)
    validate_rendered_pdfs(pdf_paths, args)
    if not args.skip_preview:
        preview_pdfs(pdf_paths)
    out_paths = copy_to_out(pdf_paths)
    for key, path in pdf_paths.items():
        print(f"{key}: {path}")
    for key, path in out_paths.items():
        print(f"out_{key}: {path}")


if __name__ == "__main__":
    main()
