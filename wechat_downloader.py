import requests
from bs4 import BeautifulSoup
import os
import time
import re
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

# 配置参数
WECHAT_ARTICLE_URL = "https://mp.weixin.qq.com/s/8IJyeA3gP4f1W7UDuPvJ3Q"  # 微信文章URL
OUTPUT_DIR = "wechat_images"  # 图片保存目录
MIN_WIDTH = 600  # 最小宽度像素
MIN_HEIGHT = 900  # 最小高度像素


def download_wechat_images(url, output_dir='wechat_images', min_width=600, min_height=900):
    """
    下载微信公众号文章中的所有图片，并根据像素大小进行筛选

    参数:
        url (str): 微信文章的URL
        output_dir (str): 图片保存的目录
        min_width (int): 最小宽度像素
        min_height (int): 最小高度像素
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建目录: {output_dir}")

    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    try:
        # 获取网页内容
        print(f"正在获取文章: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 如果请求失败则抛出异常

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取文章标题作为子目录名称
        title_tag = soup.find('h1', class_='rich_media_title')
        if title_tag:
            article_title = title_tag.get_text().strip()
            # 处理标题，移除不合法的文件名字符
            article_title = re.sub(r'[\\/*?:"<>|]', '', article_title)
            # 使用标题作为子目录
            article_dir = os.path.join(output_dir, article_title)
            if not os.path.exists(article_dir):
                os.makedirs(article_dir)
                print(f"创建文章目录: {article_dir}")
        else:
            article_dir = output_dir
            article_title = "未知文章"

        # 查找所有图片标签
        img_tags = soup.find_all('img')
        print(f"找到 {len(img_tags)} 个图片标签")

        # 用于存储已下载的图片URL，避免重复下载
        downloaded_urls = set()

        # 计数器
        downloaded_count = 0

        # 遍历并下载图片
        for index, img in enumerate(img_tags):
            # 查找图片链接，微信图片可能在src或data-src属性中
            img_url = img.get('data-src') or img.get('src')

            # 跳过没有URL的图片和已下载的图片
            if not img_url or img_url in downloaded_urls:
                continue

            # 跳过SVG图标等非内容图片
            if 'svg' in img_url or img_url.startswith('data:'):
                continue

            # 微信图片通常包含这些域名
            if not ('mmbiz.qpic.cn' in img_url or 'mmsns.qpic.cn' in img_url):
                continue

            # 提取文件扩展名，如果没有则默认为jpg
            parsed_url = urlparse(img_url)
            path = parsed_url.path
            extension = os.path.splitext(path)[1]
            if not extension:
                extension = '.jpg'

            # 构建保存路径
            filename = f"image_{index + 1}{extension}"
            save_path = os.path.join(article_dir, filename)

            try:
                # 下载图片
                print(f"正在获取图片 {index + 1}: {img_url}")
                img_response = requests.get(img_url, headers=headers, timeout=10)
                img_response.raise_for_status()

                # 检查图片尺寸
                try:
                    img_data = BytesIO(img_response.content)
                    with Image.open(img_data) as img:
                        width, height = img.size
                        print(f"图片尺寸: {width}x{height} 像素")

                        # 仅保存符合尺寸要求的图片
                        if width >= min_width and height >= min_height:
                            # 保存图片
                            with open(save_path, 'wb') as f:
                                f.write(img_response.content)

                            # 添加到已下载集合
                            downloaded_urls.add(img_url)
                            downloaded_count += 1
                            print(f"✓ 符合尺寸要求，已保存")
                        else:
                            print(f"✗ 图片尺寸低于要求 ({min_width}x{min_height})，已跳过")
                except Exception as img_error:
                    print(f"无法获取图片尺寸: {str(img_error)}，直接保存")
                    # 如果无法获取尺寸，直接保存
                    with open(save_path, 'wb') as f:
                        f.write(img_response.content)

                    downloaded_urls.add(img_url)
                    downloaded_count += 1

                # 每次下载后短暂暂停，避免被封IP
                time.sleep(0.5)

            except Exception as e:
                print(f"下载图片 {img_url} 失败: {str(e)}")

        print(f"\n完成! 成功下载 {downloaded_count} 张图片到 {article_dir}")
        return downloaded_count

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return 0


if __name__ == "__main__":
    print(f"开始下载文章图片: {WECHAT_ARTICLE_URL}")
    print(f"图片将保存至: {OUTPUT_DIR}")
    print(f"图片尺寸要求: 宽度 >= {MIN_WIDTH} 或 高度 >= {MIN_HEIGHT} 像素\n")

    download_wechat_images(WECHAT_ARTICLE_URL, OUTPUT_DIR, MIN_WIDTH, MIN_HEIGHT)