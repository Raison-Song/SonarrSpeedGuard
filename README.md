# SonarrSpeedGuard

[English](#english-version) | [中文](#中文版本)

## 

SonarrSpeedGuard is a lightweight tool designed to enhance the [Sonarr](https://github.com/Sonarr/Sonarr) experience by automatically monitoring and managing slow torrents. It identifies and removes problematic torrents that may cause queue stagnation, ensuring smooth download operations.

### Features

- **Automatically detect and remove slow torrents**: Set rules to identify torrents with speeds below a threshold and remove them from the queue, preventing disruptions in the overall download process.

- **Configurable rules and thresholds**: Customize the download speed threshold to determine which torrents should be removed, based on your needs.

### Installation and Configuration

1. **Run on a machine with a Python environment or install using Docker.**

     ```docker pull raisonsong/sonarr-speed-guard```

2. **Configure SonarrSpeedGuard**

   - Visit `http://127.0.0.1:5000/` to open the SonarrSpeedGuard configuration interface.
   - Fill in the relevant information such as Sonarr's URL and API Key on the webpage to complete the configuration.

3. **Modify Configuration File**

   - If you need to manually modify the configuration file, ensure you restart SonarrSpeedGuard after changes for the settings to take effect.

### FAQ

1. **Do I need to restart SonarrSpeedGuard for configuration changes to take effect?**

   - If changes are made via the web interface, SonarrSpeedGuard will automatically reload the configuration. If you modify the configuration file directly, a restart is required.

### Contribution

Contributions are welcome through issues and pull requests. If you have any questions or suggestions, feel free to reach out.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 

SonarrSpeedGuard 是一款轻量级工具，旨在通过自动监控和管理下载速度较慢的种子，提升 [Sonarr](https://github.com/Sonarr/Sonarr) 使用体验。通过识别并移除可能导致队列停滞的问题种子，确保下载任务顺利进行。

### 功能特点

- **自动检测并移除下载速度慢的种子**：通过设定规则，自动识别下载速度低于阈值的种子并从队列中移除，避免影响整体下载进程。

- **可配置规则和阈值**：用户可以根据自己的需求自定义下载速度阈值，决定哪些种子需要被移除。

### 安装与配置

1. **在有 Python 环境的机器上运行或者使用 Docker 安装。**

      ```docker pull raisonsong/sonarr-speed-guard```

2. **配置 SonarrSpeedGuard**

   - 访问 `http://127.0.0.1:5000/` 打开 SonarrSpeedGuard 配置界面。
   - 在网页上填写 Sonarr 的 URL 和 API Key 等相关信息，完成配置。

3. **修改配置文件**

   - 如果需要手动修改配置文件，确保修改完成后重启 SonarrSpeedGuard，以使设置生效。

### 常见问题

1. **需要重新启动 SonarrSpeedGuard 启动配置生效吗？**

   - 如果通过网页更改配置，SonarrSpeedGuard 会自动重新加载配置并生效。如果直接修改配置文件，则需要重启 SonarrSpeedGuard。

### 贡献

欢迎提交问题和 pull 请求。如果你有任何问题或建议，请随时反馈。

### 授权协议

该项目采用 MIT 许可证，详细内容请见 LICENSE 文件。
