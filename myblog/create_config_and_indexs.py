import os
import re
import sys
import functools

# markdown文件匹配规则
MATCH_FILE_RULE = re.compile(r"^(?!README).*\.md$")
# 文件夹匹配规则
MATCH_DIR_RULE = re.compile(r"[^._].*")
# 输入路径 python文件相对于docs的路径
INPUT_PATH = r"./docs"
# README.md
TABLE_FLAG = "  "

# 站点配置
# 博客名
BLOG_TITLE = "博客标题"
# 博客副标题
BLOG_SUBTITLE = "博客副标题"
# 博客描述
BLOG_DESCRIPTION = "博客"
# Github连接
GITHUB_LINK ="（例：https://github.com/formatjn2019/myblog）"

# 邮箱
MAIL = "Mailto:（邮箱）"
#备案相关
IPC="IPC号"
IPC_NUM="IPC号，纯数字"

BEIAN='备案号'
BEIAN_NUM='备案号，纯数字'

# 文件夹文件数量统计
def count_files(dir_path):
    if os.path.isfile(dir_path):
        return MATCH_FILE_RULE.match(dir_path) and 1 or 0
    result = 0
    for name in os.listdir(dir_path):
        path = dir_path + os.sep + name
        if os.path.isdir(path) and MATCH_DIR_RULE.match(name):
            result += count_files(path)
        if os.path.isfile(path):
            result += 1
    return result


# 根路径 首文件夹名称
def create_readme(root_path, head_name, web_path='/'):
    current_content = ""
    files = os.listdir(root_path)
    if (web_path == '/'):
        dir_files = {name: count_files(root_path + os.sep + name)
                     for name in os.listdir(root_path)}
        files.sort(key=functools.cmp_to_key(
            lambda c1, c2: dir_files[c1] - dir_files[c2]))
    else:
        files.sort()
    result_lines = []
    # 超链接格式模板
    modle = "+ " + "[{}]({})\n"
    head = modle.format(head_name, web_path)
    current_content += head
    result_lines.append(head)
    for file_name in files:
        # 文件路径
        file_path = root_path + os.sep + file_name
        # 符合扫描条件的文件夹
        if os.path.isdir(file_path) and MATCH_DIR_RULE.match(file_name):
            print("扫描到文件夹:" + file_path)
            # 将子目录的条目添加到当前目录
            sub_lines = create_readme(
                file_path, file_name, web_path=web_path + file_name + '/')
            for line in sub_lines:
                line = TABLE_FLAG + line
                current_content += line
                result_lines.append(line)
        # 符合扫描条件的文件,格式化内容
        elif os.path.isfile(file_path) and MATCH_FILE_RULE.match(file_name):
            print("扫描到文件" + file_path)
            url = web_path + file_name[:-3]
            line = TABLE_FLAG + modle.format(file_name[:-3], url)
            result_lines.append(line)
            current_content += line

    # 写入当前目录README.md
    with open(root_path + os.sep + "README.md", "w", encoding="utf-8") as file:
        file.write(current_content)
    return result_lines


# 侧边栏自动生成
def create_sidebar_arr(root_path, web_path='/'):
    result = []
    files = os.listdir(root_path)
    files.sort()
    for name in files:
        path = root_path + os.sep + name
        if os.path.isdir(path) and MATCH_DIR_RULE.match(name):
            item = {"title": name, "path": web_path + name + "/"}
            item["children"] = create_sidebar_arr(path, web_path + name + "/")
            result.append(item)
        if os.path.isfile(path) and MATCH_FILE_RULE.match(name):
            name = name[:-3]
            result.append({"title": name, "path": web_path + name})
    return result


'''
module.exports = {
    title: 'VuePress Blog Example', // Title for the site. This will be displayed in the navbar.
    theme: '@vuepress/theme-blog',
    plugins: [
        [
            '@vuepress/blog',
            {
                directories: [
                    {
                        // 当前分类的唯一 ID
                        id: 'post',
                        // 目标文件夹
                        dirname: '_posts',
                        // `entry page` (或者 `list page`) 的路径
                        path: '/',
                        // itemPermalink: '/post/:year/:month/:day/:slug',
                    },
                ],
            },
        ],
    ],
    themeConfig: {

        nav: [
            {
                text: 'Blog',
                link: '/',
            },
            {
                text: 'Tags',
                link: '/tag/',
            },
            {
                text: 'test',
                link: '/tag/',
            },
        ],
        footer: {
            contact: [
                {
                    type: 'github',
                    link: 'https://github.com/vuejs/vuepress',
                },
            ],
            copyright: [
                {
                    text: 'Privacy Policy',
                    link: 'https://policies.google.com/privacy?hl=en-US',
                },
                {
                    text: 'MIT Licensed | Copyright © 2018-present Vue.js',
                },
            ],
        },
    }
}
'''


# 博客配置创建
# .vuepress/comfig.js
# 根路径，博客名
def create_configs(root_path, blog_title, auto_sidebar=False):
    # key,dic
    config_dic = {}
    # 模块导出设置
    module_exports = {
        "title": blog_title,
        "theme": '@vuepress/theme-blog',
        "description": BLOG_DESCRIPTION,
        "head": [
            # # 收藏栏与新标签页图标
            # ['link', {"rel": 'icon', "type": "image/png", "href": '/logo.png'}],
            # ['link', {"rel": 'icon', "type": "image/png", "href": '/logo.png'}],
        ],
        "plugins": [
            [
                '@vuepress/blog',
            ],
        ],
        "base": '/',
        "themeConfig": {
            # 导航栏图标
            "logo": "/logo.png",
            "repo": GITHUB_LINK,
            "nav": [  # 导航栏配置
            ],
            "sitemap": {
                "hostname": "http://blog.zuixue.site"
            },
            "footer": {
                "contact": [
                    {
                        "type": 'github',
                        "link": GITHUB_LINK,
                    },
                    {
                        "type": 'mail',
                        "link": MAIL,
                    },
                ],
                "copyright": [
                    {
                        "text": IPC,
                        "link": LINK,
                    },
                    {
                        "text": BEIAN,
                        "link": "http://www.beian.gov.cn/portal/registerSystemInfo?recordcode={}".format(BEIAN_NUM),
                    },
                    {
                        "text": '欢迎转载，转载请注明出处',
                    },
                ],
            },
            "sidebar": 'auto',  # 侧边栏配置
            "sidebarDepth": 2,  # 侧边栏显示2级
        }
    }
    config_dic["module.exports"] = module_exports
    # if not auto_sidebar:
    #     config_dic["module.exports"]["themeConfig"]["sidebar"] = create_sidebar_arr(root_path)

    # 为导航栏添加内容
    contents = os.listdir(root_path)
    contents.sort()
    for name in contents:
        if os.path.isdir(root_path + os.sep + name) and MATCH_DIR_RULE.match(name):
            module_exports["themeConfig"]["nav"].append(
                {"text": name, "link": '/' + name + '/'})

    module_exports["themeConfig"]["nav"].append({"text": "联系我", "link": MAIL})

    # 生成js配置文件内容
    content = _create_js_style_content(config_dic)

    # 写入文件
    with open(root_path + "/.vuepress/config.js", "w", encoding='utf-8') as f:
        f.write(content)


def create_configs_old(root_path, blog_title, auto_sidebar=False):
    # key,dic
    config_dic = {}
    # 模块导出设置
    module_exports = {
        "title": blog_title,
        "description": BLOG_DESCRIPTION,
        "head": [
            # 收藏栏与新标签也图标
            ['link', {"rel": 'icon', "type": "image/png", "href": '/logo.png'}],
            ['link', {"rel": 'icon', "type": "image/png", "href": '/logo.png'}],
        ],
        "base": '/',
        "themeConfig": {
            # 导航栏图标
            "logo": "/logo.png",
            "repo": GITHUB_LINK,
            "nav": [  # 导航栏配置
            ],

            "sidebar": 'auto',  # 侧边栏配置
            "sidebarDepth": 2,  # 侧边栏显示2级
        }
    }
    config_dic["module.exports"] = module_exports
    if not auto_sidebar:
        config_dic["module.exports"]["themeConfig"]["sidebar"] = create_sidebar_arr(
            root_path)

    # 为导航栏添加内容
    contents = os.listdir(root_path)
    contents.sort()
    for name in contents:
        if os.path.isdir(root_path + os.sep + name) and MATCH_DIR_RULE.match(name):
            module_exports["themeConfig"]["nav"].append(
                {"text": name, "link": '/' + name + '/'})

    module_exports["themeConfig"]["nav"].append({"text": "联系我", "link": MAIL})

    # 生成js配置文件内容
    content = _create_js_style_content(config_dic)

    # 写入文件
    with open(root_path + "/.vuepress/config.js", "w", encoding='utf-8') as f:
        f.write(content)


# 将python字典转换为js格式
def _create_js_style_content(dict):
    template = "{} = {}\n"
    content = ""
    for k, v in dict.items():
        content += template.format(k, _create_content(v))

    return content


# 递归生成嵌套括号
def _create_content(data):
    # 字典
    if type(data).__name__ == 'dict':
        dict_temple = "\t{}: {}"
        items = []
        for ki, vi in data.items():
            items.append(dict_temple.format(ki, _create_content(vi)))
        return "{{ {} }}".format(", ".join(items))
    # 列表
    elif type(data).__name__ == 'list':
        items = []
        for item in data:
            items.append(_create_content(item))
        return "[\t{}]".format(",\t".join(items))
    # 数字
    elif type(data).__name__ == 'int':
        return data
    # 数字
    elif type(data).__name__ == 'bool':
        return data and 'true' or 'false'
    # 字符串
    else:
        return "'{}'".format(data)


if __name__ == '__main__':
    # 相对路径转绝对路径
    INPUT_PATH = os.path.abspath(os.path.join(
        os.path.dirname(sys.argv[0]), INPUT_PATH))
    create_readme(INPUT_PATH, BLOG_TITLE)
    create_configs(INPUT_PATH, BLOG_TITLE)
    # create_sidebar_arr(INPUT_PATH)
