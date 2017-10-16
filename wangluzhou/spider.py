import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError

base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'CXID=B708B06249D4C35EE3AD4C7F4D36757D; SUV=0063509D65F492265999A2789D834114; UM_distinctid=15e26ab7b6cbd8-04a0ce3dd6b466-c313760-144000-15e26ab7b6dbf5; SMYUV=1503887326156898; teleplay_play_records=%C7%E0%B4%BA%C8%BC%C9%D5%B5%C4%CB%EA%D4%C2:9$%CE%D2%BA%CD%CB%FD%B5%C4%B4%AB%C6%E6%C7%E9%B3%F0:3; pgv_pvi=2890115072; ABTEST=0|1506666892|v1; weixinIndexVisited=1; ad=UKcK3yllll2BcnRWlllllVXkc5UlllllWsN99ZllllylllllRgDll5@@@@@@@@@@; SUID=E1E1F5654B238B0A58D5E0A50009CE14; SNUID=EE11A62852570A2DE5617E7952B81C94; ld=Lkllllllll2BcbhalllllVXPsw7lllllWsNlsZllll9lllllRklll5@@@@@@@@@@; LSTMV=244%2C82; LCLKINT=2723; JSESSIONID=aaaD11ngwLrY9gz11av8v; IPLOC=CN3100; sct=3; ppinf=5|1508155332|1509364932|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTglQjclODMlRTUlOTUlOEElRTglQjclODN8Y3J0OjEwOjE1MDgxNTUzMzJ8cmVmbmljazoyNzolRTglQjclODMlRTUlOTUlOEElRTglQjclODN8dXNlcmlkOjQ0Om85dDJsdUNRa0VDUGZkMjUzQ0tTOTBfNVUtdUVAd2VpeGluLnNvaHUuY29tfA; pprdig=PV_pAHIotu5LhTmhy0QHpxRbeBaSKBwOio1aFngzcJPqUPaKKmsmkyoiwyXKG2GdJagvlRR7TiSU-J5ox15qfi4XmoWII3b2kOtPWBZ-j7BRZV3hQn3pxZaMHqsvPyPVNJmrZ59YAPa0y_XzNsIhd1G30EKUBnL-OX9PBKYrgKY; sgid=08-31513519-AVnkn8RDqibgZqCc6UFPs9Xw; ppmdig=1508155333000000c0d4fd42096884ead625b2934b6e6476',
    'Host': 'weixin.sogou.com',
    'Referer': 'http://weixin.sogou.com/weixin?query=Python&_sug_type_=&s_from=input&_sug_=n&type=2&page=30&ie=utf8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


def get_html(url):
    try:
        response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # need proxy
            pass
    except ConnectionError:
        return get_html(url)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

if __name__ == '__main__':
    get_index('风景', 1)
