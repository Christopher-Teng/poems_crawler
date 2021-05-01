# 中华诗词 Scrapy 爬虫项目

## 项目介绍

本项目将从[中华诗词网](https://www.zhsc.net)爬取指定作者的诗词，项目详情在我的[Github Page](https://christopher-teng.github.io)上。

## 安装与使用

推荐使用 Docker 进行部署运行，以下步骤假定已在本地运行环境中安装并启动 Docker。

1. 克隆项目仓库到本地
2. 打开终端进入项目目录，执行以下命令：

   ```shell
   sudo chmod u+x ./start.sh
   ```

3. 启动爬虫：

   ```shell
   ./start.sh author=作者
   ```

   爬虫启动后，将使用 docker 在后台开启 redis、mongo、mongo-express 服务，访问 localhost:8081 可以进入 mongo-express 管理页面。

   爬取获得的数据将分别存放于：

   1. ./zhsc_crawler/poems/poems.jsonl，采用 JSON Lines 格式存储，方便以后使用时逐行读取数据
   2. 使用 MongoDB 存储数据，挂载与./mongo_data 目录。使用数据库 zhsc_crawler，集合 poems，使用管理员账户 root/123456 连接。
   3. ./redis_data 目录用于 redis 数据持久化，其中存储的是已爬取的 url，由爬虫中使用的基于 Redis 的布隆过滤器生成。

   后台运行的 redis 和 mongo 服务使用 docker 的 network=host 网络方式以及默认的 6379 和 27017 端口，因此你可以将自己的其他应用通过本地主机地址进行连接来读取数据。

   **_tips_**:由于目标网站中收录的古诗词非常多，涵盖了从先秦两汉时期到近现代时期大量文人的作品，如果一次性全部爬取，耗时长而且意义不大，对于古诗词我们关注的重点多集中于历史上的著名文人，因此需要在启动爬虫时指定要爬取的作者，格式为：`author=作者`
