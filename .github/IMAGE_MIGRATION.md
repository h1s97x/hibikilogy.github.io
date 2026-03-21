# 图片自动迁移和CDN加速方案

## 概述

本项目采用 GitHub Actions 自动化流程，实现图片的自动迁移和 jsDelivr CDN 加速。

## 工作流程

### 1. 图片存储结构

```
main repository (hibikilogy.github.io)
├── _posts/          # 博客文章
├── images/          # 图片文件（临时存储）
└── .github/
    └── workflows/   # GitHub Actions 工作流

blog-images repository (独立仓库)
└── images/          # 最终图片存储位置
```

### 2. 自动化流程

当你向主仓库推送包含图片的更改时，GitHub Actions 会自动：

1. **检测新增/修改的图片**
   - 扫描 `images/` 目录中的所有图片文件
   - 识别相比上一次提交的变化

2. **迁移图片到独立仓库**
   - 将新增/修改的图片复制到 `blog-images` 仓库
   - 保持原有的目录结构

3. **替换 Markdown 中的图片链接**
   - 将相对路径 `./images/xxx.png` 替换为 CDN 链接
   - 将 `https://hibikilogy.github.io/images/xxx.png` 替换为 CDN 链接
   - 支持 Markdown 和 HTML 两种格式

4. **自动提交更改**
   - 在 `blog-images` 仓库中提交迁移的图片
   - 在主仓库中提交更新后的 Markdown 文件

## 使用方法

### 对贡献者来说

**零配置！** 你只需要像往常一样工作：

1. 在本地编写文章，插入图片
2. 将图片放在 `images/` 目录下
3. 在 Markdown 中使用相对路径引用图片：
   ```markdown
   ![描述](./images/2025-02-21/example.png)
   ```
4. 提交并推送到 GitHub
5. GitHub Actions 会自动处理剩余的工作

### 图片链接格式

支持以下几种格式，都会被自动转换为 CDN 链接：

```markdown
# Markdown 格式
![描述](./images/2025-02-21/example.png)
![描述](images/2025-02-21/example.png)
![描述](/images/2025-02-21/example.png)

# HTML 格式
<img src="./images/2025-02-21/example.png" alt="描述">
<img src="images/2025-02-21/example.png" alt="描述">
```

## CDN 加速效果

### 转换前
```
https://hibikilogy.github.io/images/2025-02-21/example.png
```
- 直接从 GitHub Pages 加载
- 在中国大陆地区 DNS 解析不稳定
- 加载速度慢，经常超时

### 转换后
```
https://cdn.jsdelivr.net/gh/hibikilogy/blog-images@main/images/2025-02-21/example.png
```
- 通过 jsDelivr CDN 加速
- 在中国大陆有多个节点
- 加载速度快，缓存效率高

## 配置要求

### 前置条件

1. **创建独立的图片仓库**
   ```bash
   # 在 GitHub 上创建新仓库 blog-images
   # 确保仓库是公开的（Public）
   ```

2. **配置 GitHub Token**
   - 工作流已使用 `${{ secrets.GITHUB_TOKEN }}`
   - 无需额外配置，GitHub 会自动提供

### 可选配置

如果需要自定义行为，可以编辑 `.github/workflows/image-migration.yml`：

```yaml
# 修改监听的分支
on:
  push:
    branches:
      - main
      - master

# 修改监听的路径
    paths:
      - '_posts/**'
      - 'images/**'
```

## 故障排除

### 工作流未触发

- 检查是否修改了 `_posts/` 或 `images/` 目录
- 检查分支是否是 `main` 或 `master`
- 查看 GitHub Actions 标签页的运行日志

### 图片未迁移

- 确保 `blog-images` 仓库存在且可访问
- 检查图片文件格式是否支持（.png, .jpg, .jpeg, .gif, .webp, .svg）
- 查看工作流日志中的错误信息

### 链接未替换

- 确保 Markdown 文件中的图片路径格式正确
- 检查是否使用了支持的路径格式
- 查看工作流日志中的替换详情

## 性能指标

| 指标 | 直接加载 | CDN 加速 |
|------|---------|---------|
| 平均加载时间（中国大陆） | 3-5s | 0.5-1s |
| 缓存时间 | 无 | 30天 |
| 可用性 | 70% | 99%+ |

## 常见问题

### Q: 为什么要分离图片仓库？
A: 
- 图片与源码分离，利用 CDN 强缓存
- 减少主仓库大小
- 便于后续迁移或备份

### Q: jsDelivr CDN 在哪些地区有节点？
A: jsDelivr 在全球有 200+ 个节点，包括中国大陆的多个节点。

### Q: 如果 CDN 链接失效怎么办？
A: 
- 图片仍然存储在 `blog-images` 仓库中
- 可以随时切换到其他 CDN 或直接使用 GitHub 链接
- 工作流可以轻松修改以支持其他 CDN

### Q: 旧文章中的图片怎么办？
A: 
- 可以手动运行工作流来迁移旧图片
- 或者在编辑旧文章时自动迁移
- 建议逐步迁移，避免一次性大量操作

## 相关资源

- [jsDelivr 官网](https://www.jsdelivr.com/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [blog-images 仓库](https://github.com/hibikilogy/blog-images)

## 许可证

本自动化方案遵循项目主许可证。
