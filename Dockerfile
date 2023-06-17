FROM node:lts-slim

# 创建工作目录
RUN mkdir /myblog 

# 设置运行位置
WORKDIR /myblog

# npm国内源
RUN npm config set registry https://registry.npm.taobao.org
RUN npm install -D vuepress
RUN npm install npm vuepress @vuepress/theme-blog
# 运行命令
CMD npm run docs:dev
