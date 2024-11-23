# SonarrSpeedGuard

SonarrSpeedGuard 是一款轻量级工具，旨在通过自动监控和管理下载速度较慢的种子，提升 Sonarr(https://github.com/Sonarr/Sonarr) 使用体验。通过识别并移除可能导致队列停滞的问题种子，确保下载任务顺利进行。

## 功能特点

- **自动检测并移除下载速度慢的种子**：通过设定规则，自动识别下载速度低于阈值的种子并从队列中移除，避免影响整体下载进程。
- **可配置规则和阈值**：用户可以根据自己的需求自定义下载速度阈值，决定哪些种子需要被移除。

## 安装与配置

1. **配置 SonarrSpeedGuard**
   - 访问 `http://127.0.0.1:5000/` 打开 SonarrSpeedGuard 配置界面。
   - 在网页上填写 Sonarr 的 URL 和 API Key 等相关信息，完成配置。

2. **修改配置文件**
   - 如果需要手动修改配置文件，确保修改完成后重启 SonarrSpeedGuard，以使设置生效。

## 常见问题

1. **需要重新启动 SonarrSpeedGuard 启动配置生效吗？**
   - 如果通过网页更改配置，SonarrSpeedGuard 会自动重新加载配置并生效。如果直接修改配置文件，则需要重启 SonarrSpeedGuard。

## 贡献

欢迎提交问题和 pull 请求。如果你有任何问题或建议，请随时反馈。

## 授权协议

该项目采用 MIT 许可证，详细内容请见 LICENSE 文件。
