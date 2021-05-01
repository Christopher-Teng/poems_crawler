import re

from w3lib.html import remove_tags


def parse_content(value):
    """
    对诗词正文内容进行整理，去掉文本中的html标签以及多余的空格，并且在诗句末尾出现句号或问号或感叹号后面添加一个换行
    """
    value = remove_tags(value.strip())
    return re.sub(r'(。|！|？)', r'\1\n', value)


def get_times(value):
    """
    获取作者的年代
    """
    result = re.search(r'(?:年代:\s*)(.+?)(?:\s)', value)
    return result.group(1)


def get_author(value):
    """
    获取作者的名字
    """
    result = re.search(r'(?:作者:\s*)(.+)(?:\s*)', value)
    return result.group(1)


def modify_title(title, content):
    """
    将title的值修改为原title的值加上content中第一个诗句
    """
    first_line = re.match(r'(.+)(?=\n)', content).group()
    title = title+' —— '+first_line
    return title


def find_author_url(link, author):
    """
    查找指定作者名对应的诗歌列表页面的地址
    """
    if re.search(r'>\s*{}\s*<'.format(author), link) is not None:
        return re.search(r'(?:href\s*\=\s*")(.+?)(?:")', link).group(1)
    return None
