# 个人主页维护

GitHub 会把公开同名仓库 `Herz1/Herz1` 的 `README.md` 展示在个人主页。

- 文字、链接、展示顺序：编辑 `README.md`。
- 蓝紫横幅和打字效果：编辑 `assets/header.svg`、`assets/typing.svg`；均支持减少动态效果的系统设置。
- 技术图标：`assets/stack.svg`，源自 <https://github.com/tandpfun/skill-icons>。当前展示公开项目中使用的技术。
- 贪吃蛇：<https://github.com/Platane/snk>。
- 吃豆人、打砖块：<https://github.com/abozanona/pacman-contribution-graph>。
- 3D 城市：<https://github.com/yoshi389111/github-profile-3d-contrib>。
- 统计卡：`scripts/refresh_snapshot.py`，只读取公开仓库元数据；语言比例按非 fork 公开仓库的主要语言数量计算，不表示精确代码行数或个人熟练度。

## 自动刷新

`.github/workflows/profile.yml` 每天计划于新加坡时间 04:17 运行。GitHub 定时任务可能延迟。公开仓库长时间无活动时，GitHub 可能暂停定时工作流，可到 Actions 重新启用。

手动刷新：Actions → Refresh profile artwork → Run workflow。

不需要额外的付费 API Key 或个人访问令牌；工作流使用 GitHub 自动提供的仓库令牌，权限为本仓库内容写入，用于提交生成的图片。第三方 Action 固定到具体提交，更新时需要同步调整 SHA。

所有贡献游戏都是根据贡献数据生成的动画图片，不会改变真实贡献记录，也不支持在 README 内直接操控。吃豆人、打砖块和 3D 图默认折叠；点击标题展开。

## 停止自动刷新

在 Actions 中停用 `Refresh profile artwork` 工作流；已生成的图片仍会正常显示。
