import requests
from bs4 import BeautifulSoup

# 目标网页的URL
url = "https://www.tennis123.net/member/92575"

# 发送HTTP GET请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析HTML内容
    soup = BeautifulSoup(response.content, "html.parser")

    # 打印整个HTML内容（可选）
    print(soup.prettify())

    # 假设要爬取某个特定的元素，例如会员的信息
    # 你需要根据实际的HTML结构调整下面的代码
    # 例如：
    member_info = soup.find('div', class_='member-info')
    
    if member_info:
        print(member_info.text)
    else:
        print("未找到会员信息")

else:
    print(f"请求失败，状态码: {response.status_code}")
