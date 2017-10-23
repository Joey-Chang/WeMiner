# encoding: utf-8
# 获取指定公众号的最新发布的文章
from urllib.parse import urlencode
from lxml import etree
import requests
from sortedcollections import OrderedDict
_search_type_gzh = 1  # 公众号
_search_type_article = 2  # 文章


def get_lastest_article(wechat_id_or_name):
    # 通过搜狗微信搜索该公众号
    # 获取该搜索页面的地址
    search_url = gen_search_gzh_url(wechat_id_or_name, page=1)
    content = get_html(search_url)
    page = etree.HTML(content)
    lis = page.xpath('//ul[@class="news-list2"]/li')
    relist = []
    for li in lis:
        url = li.xpath('div/div[1]/a/@href')
        headimage = li.xpath('div/div[1]/a/img/@src')
        wechat_name = get_elem_text(li.xpath('div/div[2]/p[1]')[0])
        info = get_elem_text(li.xpath('div/div[2]/p[2]')[0])
        post_perm = 0
        qrcode = li.xpath('div/div[3]/span/img[1]/@src')
        introduction = get_elem_text(li.xpath('dl[1]/dd')[0])
        authentication = li.xpath('dl[2]/dd/text()')
        relist.append({
            'open_id': headimage[0].split('/')[-1],
            'profile_url': url[0],
            'headimage': headimage[0],
            'wechat_name': wechat_name.replace('red_beg', '').replace('red_end', ''),
            'wechat_id': info.replace('微信号：', ''),
            'post_perm': post_perm,
            'qrcode': qrcode[0] if qrcode else '',
            'introduction': introduction.replace('red_beg', '').replace('red_end', ''),
            'authentication': authentication[0] if authentication else ''
        })
    print(relist)


def gen_search_gzh_url(keyword, page=1):
    """拼接搜索 公众号 URL

    Parameters
    ----------
    keyword : str or unicode
        搜索文字
    page : int, optional
        页数 the default is 1

    Returns
    -------
    str
        search_gzh_url
    """
    assert isinstance(page, int) and page > 0

    qs_dict = OrderedDict()
    qs_dict['type'] = _search_type_gzh
    qs_dict['page'] = page
    qs_dict['ie'] = 'utf8'
    qs_dict['query'] = keyword
    return 'http://weixin.sogou.com/weixin?{}'.format(urlencode(qs_dict))


def get_html(url):
    try:
        response = requests.get(url, allow_redirects=False)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # need proxy
            print('302')
    except ConnectionError:
        return get_html(url)


def get_elem_text(elem):
    """抽取lxml.etree库中elem对象中文字

    Args:
        elem: lxml.etree库中elem对象

    Returns:
        elem中文字
    """
    return ''.join([node.strip() for node in elem.itertext()])

def get_encoding_from_reponse(r):
    """获取requests库get或post返回的对象编码

    Args:
        r: requests库get或post返回的对象

    Returns:
        对象编码
    """
    encoding = requests.utils.get_encodings_from_content(r.text)
    return encoding[0] if encoding else requests.utils.get_encoding_from_headers(r.headers)


def _replace_str_html(s):
    """替换html‘&quot;’等转义内容为正常内容

    Args:
        s: 文字内容

    Returns:
        s: 处理反转义后的文字
    """
    html_str_list = [
        ('&#39;', '\''),
        ('&quot;', '"'),
        ('&amp;', '&'),
        ('&yen;', '¥'),
        ('amp;', ''),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&nbsp;', ' '),
        ('\\', '')
    ]
    for i in html_str_list:
        s = s.replace(i[0], i[1])
    return s


def replace_html(data):
    if isinstance(data, dict):
        return dict([(replace_html(k), replace_html(v)) for k, v in data.items()])
    elif isinstance(data, list):
        return [replace_html(l) for l in data]
    elif isinstance(data, str) or isinstance(data, unicode):
        return _replace_str_html(data)
    else:
        return data


def str_to_dict(json_str):
    json_dict = ast.literal_eval(json_str)
    return replace_html(json_dict)


def replace_space(s):
    return s.replace(' ', '').replace('\r\n', '')


def get_url_param(url):
    result = url_parse.urlparse(url)
    return url_parse.parse_qs(result.query, True)

if __name__ == "__main__":
    get_lastest_article("债券小馆")

