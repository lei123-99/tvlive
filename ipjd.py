import time
import os
import requests
import concurrent.futures
import re
import threading
import eventlet

urls = [
"http://1.192.248.1:9901",
"http://36.44.157.1:9901",
"http://58.53.152.1:9901",
"http://106.118.70.1:9901",
"http://112.6.165.1:9901",
"http://112.194.128.1:9901",
"http://112.234.21.1:9901",
"http://113.220.235.1:9999",
"http://118.81.242.1:9999",
"http://119.125.104.1:9901",
"http://119.125.134.1:9901",
"http://119.163.56.1:9901",
"http://119.163.57.1:9901",
"http://119.163.61.1:9901",
"http://120.197.43.1:9901",
"http://122.246.75.1:9901",
"http://123.7.110.1:9901",
"http://123.161.37.1:9901",
"http://124.228.160.1:9901",
"http://125.43.244.1:9901",
"http://125.114.241.1:9901",
"http://144.52.160.1:9901",
"http://171.117.15.1:9999",
"http://183.131.246.1:9901",
"http://219.145.59.1:8888",
"http://219.154.240.1:9901",
"http://219.154.242.1:9901",
"http://221.226.4.1:9901",
"http://221.13.235.1:9901",
"http://221.193.168.1:9901"
    ]

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls

def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None

results = []

x_urls = []
for url in urls:  # 对urls进行处理，ip第四位修改为1，并去重
    url = url.strip()
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    ip_dot_start = url.find(".") + 1
    ip_dot_second = url.find(".", ip_dot_start) + 1
    ip_dot_three = url.find(".", ip_dot_second) + 1
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_dot_three]
    port = url[ip_end_index:]
    ip_end = "1"
    modified_ip = f"{ip_address}{ip_end}"
    x_url = f"{base_url}{modified_ip}{port}"
    x_urls.append(x_url)

urls = set(x_urls)  # 去重得到唯一的URL列表

valid_urls = []
#   多线程获取可用url
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for url in urls:
        url = url.strip()
        modified_urls = modify_urls(url)
        for modified_url in modified_urls:
            futures.append(executor.submit(is_url_accessible, modified_url))

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            valid_urls.append(result)

for url in valid_urls:
    print(url)
# 遍历网址列表，获取JSON文件并解析
for url in valid_urls:
    try:
        # 发送GET请求获取JSON文件，设置超时时间为0.5秒
        ip_start_index = url.find("//") + 2
        ip_dot_start = url.find(".") + 1
        ip_index_second = url.find("/", ip_dot_start)
        base_url = url[:ip_start_index]  # http:// or https://
        ip_address = url[ip_start_index:ip_index_second]
        url_x = f"{base_url}{ip_address}"

        json_url = f"{url}"
        response = requests.get(json_url, timeout=0.5)
        json_data = response.json()

        try:
            # 解析JSON文件，获取name和url字段
            for item in json_data['data']:
                if isinstance(item, dict):
                    name = item.get('name')
                    urlx = item.get('url')
                    if ',' in urlx:
                        urlx=f"aaaaaaaa"
                    #if 'http' in urlx or 'udp' in urlx or 'rtp' in urlx:
                    if 'http' in urlx:
                        urld = f"{urlx}"
                    else:
                        urld = f"{url_x}{urlx}"

                    if name and urlx:
                        # 删除特定文字
                        name = name.replace("cctv", "CCTV")
                        name = name.replace("中央", "CCTV")
                        name = name.replace("央视", "")
                        name = name.replace("高清", "")
                        name = name.replace("HD", "")
                        name = name.replace("标清", "")
                        name = name.replace("频道", "")
                        name = name.replace("-", "")
                        name = name.replace(" ", "")
                        name = name.replace("PLUS", "+")
                        name = name.replace("＋", "+")
                        name = name.replace("(", "")
                        name = name.replace(")", "")
                        name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                        name = name.replace("CCTV1综合", "CCTV1")
                        name = name.replace("CCTV2财经", "CCTV2")
                        name = name.replace("CCTV3综艺", "CCTV3")
                        name = name.replace("CCTV4国际", "CCTV4")
                        name = name.replace("CCTV4中文国际", "CCTV4")
                        name = name.replace("CCTV5体育", "CCTV5")
                        name = name.replace("CCTV6电影", "CCTV6")
                        name = name.replace("CCTV7军事", "CCTV7")
                        name = name.replace("CCTV7军农", "CCTV7")
                        name = name.replace("CCTV7农业", "CCTV7")
                        name = name.replace("CCTV7国防军事", "CCTV7")
                        name = name.replace("CCTV8电视剧", "CCTV8")
                        name = name.replace("CCTV9记录", "CCTV9")
                        name = name.replace("CCTV9纪录", "CCTV9")
                        name = name.replace("CCTV10科教", "CCTV10")
                        name = name.replace("CCTV11戏曲", "CCTV11")
                        name = name.replace("CCTV12社会与法", "CCTV12")
                        name = name.replace("CCTV13新闻", "CCTV13")
                        name = name.replace("CCTV新闻", "CCTV13")
                        name = name.replace("CCTV14少儿", "CCTV14")
                        name = name.replace("CCTV少儿", "CCTV14")
                        name = name.replace("CCTV15音乐", "CCTV15")
                        name = name.replace("CCTV16奥林匹克", "CCTV16")
                        name = name.replace("CCTV17农业农村", "CCTV17")
                        name = name.replace("CCTV17农业", "CCTV17")
                        name = name.replace("CCTV5+体育赛视", "CCTV5+")
                        name = name.replace("CCTV5+体育赛事", "CCTV5+")
                        name = name.replace("CCTV5+体育", "CCTV5+")
                        if "txiptv" in urld:
                            results.append(f"{name},{urld}")
        except:
            continue
    except:
        continue

def natural_key(string):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', string)]

results.sort(key=natural_key)

with open("iptv.txt", 'w', encoding='utf-8') as file:
    file.write('央视频道,#genre#\nCCTV1,\nCCTV2,\nCCTV3,\nCCTV4,\nCCTV5,\nCCTV5+,\nCCTV6,\nCCTV7,\nCCTV8,\nCCTV9,\nCCTV10,\nCCTV11,\nCCTV12,\nCCTV13,\nCCTV14,\nCCTV15,\nCCTV16,\nCCTV17,\nCHC家庭影院,\nCHC影迷电影,\nCHC动作电影,\nCCTV兵器科技,\nCCTV怀旧剧场,\nCCTV世界地理,\nCCTV文化精品,\nCCTV台球,\nCCTV高尔夫网球,\nCCTV风云剧场,\nCCTV风云音乐,\nCCTV第一剧场,\nCCTV女性时尚,\nCCTV风云足球,\nCCTV电视指南,\n')
    for result in results:
        channel_name, channel_url = result.split(',')
        if 'CCTV' in channel_name or 'CHC' in channel_name or '地理' in channel_name or '风云' in channel_name:
            file.write(f"{channel_name},{channel_url}\n")
    file.write('卫视频道,#genre#\n黑龙江卫视,\n吉林卫视,\n辽宁卫视,\n内蒙古卫视,\n北京卫视,\n天津卫视,\n河北卫视,\n河南卫视,\n山东卫视,\n山西卫视,\n东方卫视,\n浙江卫视,\n江苏卫视,\n江西卫视,\n东南卫视,\n广东卫视,\n广西卫视,\n安徽卫视,\n湖北卫视,\n湖南卫视,\n新疆卫视,\n青海卫视,\n甘肃卫视,\n宁夏卫视,\n陕西卫视,\n西藏卫视,\n四川卫视,\n重庆卫视,\n贵州卫视,\n云南卫视,\n海南卫视,\n深圳卫视,\n兵团卫视,\n凤凰资讯,\n凤凰中文,\n')
    for result in results:
        channel_name, channel_url = result.split(',')
        if '卫视' in channel_name or '凤凰' in channel_name:
            file.write(f"{channel_name},{channel_url}\n")
    file.write('其他频道,#genre#\n乐游频道,\n重庆汽摩,\n车迷频道,\n')
    for result in results:
        channel_name, channel_url = result.split(',')
        if '乐游' in channel_name or '都市' in channel_name or '车迷' in channel_name or '汽摩' in channel_name or '旅游' in channel_name:
            file.write(f"{channel_name},{channel_url}\n")

with open(f'df.txt', 'r', encoding='utf-8') as in_file,open(f'iptv.txt', 'a') as file:
    data = in_file.read()
    file.write(data)
