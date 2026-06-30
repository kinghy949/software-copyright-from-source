# Config Schema

Use a JSON file. Keep chapter order aligned with the operation manual.

```json
{
  "software_name": "BotLink Platform 智能体即时通讯平台",
  "software_short": "BotLink Platform",
  "output_basename": "Botlink智能机器人即时通讯平台",
  "version": "V1.0",
  "completed_date": "2026 年 05 月 18 日",
  "writing_date": "2026 年 06 月 29 日",
  "source_line_total": "5129",
  "application_profile": {
    "development_hardware": "MacBook Pro、x86_64 或 ARM64 开发机，16GB RAM",
    "runtime_hardware": "x86_64 云服务器或内网服务器，8GB RAM",
    "development_os": "macOS、Windows 11、Linux",
    "development_tools": "VS Code、pnpm、Vite、TypeScript、Git",
    "runtime_platform": "Linux、Docker、Nginx、Web 浏览器",
    "support_software": "Vue、Node.js、PostgreSQL、Redis、Docker",
    "programming_languages": "TypeScript、Vue、SQL、CSS",
    "development_purpose": "提升企业智能体会话协同效率",
    "target_domain": "企业智能办公和人机协同领域",
    "main_feature": "本软件面向企业智能办公和人机协同沟通场景，提供账号登录、权限识别、智能体管理、会话协作、消息收发、问题反馈和新手引导等功能。用户可通过手机号验证码完成登录，进入工作台后查看会话列表、智能体状态和历史沟通信息。智能体管理模块支持创建、编辑、删除和查看在线状态，帮助管理员掌握智能体接入情况。会话模块支持按用户或智能体发起私聊、项目会话或协作会话，并在聊天窗口中完成文本、附件、表情和定时消息处理。系统可记录消息投递状态、最后回复时间、会话成员和业务反馈内容，便于后续查询和运营跟进。问题反馈模块支持填写问题说明、上传截图并提交处理，帮助运营人员收集使用过程中的异常和建议。新手指南模块提供登录、智能体创建、客户端配置、工作目录和移动端安装等说明，降低首次使用门槛。系统通过统一入口组织多角色协同过程，使用户与智能体之间的沟通记录可管理、操作流程可追踪、问题处理可闭环，适用于企业内部智能办公和自动化协作场景。管理人员可根据会话状态、智能体状态和反馈记录判断业务处理进度，及时定位未回复、未接入或提交异常的事项。平台还可沉淀常见操作入口和业务材料，减少重复沟通成本，提高团队协作效率，并为后续统计分析、流程优化和系统审计提供统一的数据基础。",
    "technical_feature": "100 字内说明架构、语言、存储、实时通信等技术特点。"
  },
  "manual_profile": {
    "overview": "按实际产品功能概述系统用途，不写源码路径。",
    "runtime_environment": "描述用户访问方式、浏览器、服务端和支撑软件。",
    "common_issues": "描述登录、列表、提交、查询等常见操作异常处理。"
  },
  "screenshots": [
    {
      "id": "S01",
      "file": "login.png",
      "title": "手机号验证码登录",
      "module": "登录与身份认证",
      "desc": "登录页提供手机号和验证码输入，验证通过后进入工作台。",
      "steps": ["输入手机号。", "填写验证码。", "点击登录。"],
      "page_break_before": false,
      "sources": [
        "web/src/views/LoginView.vue",
        "user-service/src/routes/auth.ts"
      ]
    }
  ],
  "code_sections": [
    {
      "title": "登录与身份认证",
      "screenshot": "S01",
      "blocks": [
        {"path": "web/src/views/LoginView.vue", "line_range": [1, 240]},
        {"path": "user-service/src/routes/auth.ts", "line_range": [1, 180]}
      ]
    }
  ]
}
```

## Fields

- `software_name`: Full software name printed on covers and headers.
- `software_short`: Short name for prose; optional.
- `output_basename`: Filename stem used in `out/`.
- `version`: Usually `V1.0`.
- `completed_date`: Development completion date for the application form.
- `writing_date`: Cover writing date for all three PDFs.
- `source_line_total`: Total source-program line count shown in the application form. Count real source files only; exclude dependencies, generated build output, screenshots, PDFs, archives, and existing copyright materials.
- `application_profile`: Application-form field values. Keep these within the online-entry limits listed below.
- `manual_profile`: Manual prose that is not tied to a single screenshot.
- `screenshots[].file`: Must exist in `--screenshots-dir`.
- `screenshots[].desc`: Must describe what the screenshot visibly shows.
- `screenshots[].steps`: User-facing operation steps; do not include code paths.
- `screenshots[].page_break_before`: Optional boolean. Set to `true` when a screenshot/section must start on a new page to keep the figure under the correct chapter.
- `screenshots[].sources`: Matching source paths. This is used for planning and consistency; the manual must not expose these paths.
- `code_sections[].blocks[].path`: Path relative to `--source-root`.
- `code_sections[].blocks[].line_range`: Optional inclusive line range. Omit or set `null` to include the whole file.

## Application Field Limits

The generator validates these fields by default when producing the application form:

| Field | Limit |
| --- | --- |
| `development_hardware` | 50 characters or fewer |
| `runtime_hardware` | 50 characters or fewer |
| `development_os` | 50 characters or fewer |
| `development_tools` | 50 characters or fewer |
| `runtime_platform` | 50 characters or fewer |
| `support_software` | 50 characters or fewer |
| `programming_languages` | 120 characters or fewer |
| `development_purpose` | 50 characters or fewer |
| `target_domain` | 50 characters or fewer |
| `main_feature` | 500-1300 characters |
| `technical_feature` | 100 characters or fewer |

Use `--skip-application-validation` only when reproducing an old artifact that intentionally does not follow the current form rules.

## Code Document Size

Keep code documents between 60 and 80 pages unless the user gives a different requirement. Use high-relevance excerpts that correspond to the manual chapters:

- Frontend pages and components shown in screenshots.
- API clients, stores, routes, controllers, services, and database access that implement those operations.
- Shared validation, permission, upload, WebSocket, scheduling, or export logic only when it is directly used by the documented function.

Avoid generated files, dependency folders, bundled assets, build output, repeated style blocks, and unrelated utilities.

## BotLink Mapping Used Successfully

The BotLink bundle used these operation chapters:

1. 登录与身份认证
2. 智能体管理
3. 智能体创建
4. 会话协同
5. 消息收发工作台
6. 反馈与运营处理
7. 新手指南

The code document grouped related source excerpts under the same functional order.
