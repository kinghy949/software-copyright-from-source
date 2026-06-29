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
  "screenshots": [
    {
      "id": "S01",
      "file": "login.png",
      "title": "手机号验证码登录",
      "module": "登录与身份认证",
      "desc": "登录页提供手机号和验证码输入，验证通过后进入工作台。",
      "steps": ["输入手机号。", "填写验证码。", "点击登录。"],
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
- `source_line_total`: Total source-program line count shown in the application form.
- `screenshots[].file`: Must exist in `--screenshots-dir`.
- `screenshots[].desc`: Must describe what the screenshot visibly shows.
- `screenshots[].steps`: User-facing operation steps; do not include code paths.
- `screenshots[].sources`: Matching source paths. This is used for planning and consistency; the manual must not expose these paths.
- `code_sections[].blocks[].path`: Path relative to `--source-root`.
- `code_sections[].blocks[].line_range`: Optional inclusive line range. Omit or set `null` to include the whole file.

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
