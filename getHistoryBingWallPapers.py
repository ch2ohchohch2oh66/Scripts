import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime


def download_file(url, filepath):
    """从指定的 URL 下载文件并保存到指定的文件路径。

    参数:
        url (str): 要下载的文件的 URL。
        filepath (str): 文件保存的路径。

    返回:
        bool: 如果下载成功返回 True，否则返回 False。
    """
    try:
        # 发送 GET 请求以获取文件内容
        response = requests.get(url, stream=True)
        # 检查请求是否成功，如果不成功则引发异常
        response.raise_for_status()

        # 以二进制写入模式打开文件
        with open(filepath, 'wb') as file:
            # 逐块读取响应内容并写入文件
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 确保读取的块不为空
                    file.write(chunk)  # 将块写入文件

        return True  # 下载成功，返回 True
    except Exception as e:
        # 捕获异常并打印错误信息
        print(f"Error downloading {url}: {e}")
        return False  # 下载失败，返回 False


def get_wallpaper_urls(year, month):
    """从 GitHub 页面获取壁纸下载 URL。

    参数:
        year (int): 年份。
        month (int): 月份。

    返回:
        list: 包含壁纸下载 URL 的列表。
    """
    # 构建 GitHub 页面 URL
    github_url = f"https://github.com/niumoo/bing-wallpaper/tree/main/picture/{year}-{month:02d}"

    try:
        # 发送 GET 请求以获取页面内容
        response = requests.get(github_url)
        response.raise_for_status()

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = []

        # 查找所有包含 'UHD.jpg' 和 'bing.com' 的链接
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if 'UHD.jpg' in href and 'bing.com' in href:
                urls.append(href)

        # 移除第一个 URL（重复的封面图）
        if urls:
            urls.pop(0)

        return urls  # 返回壁纸 URL 列表

    except Exception as e:
        # 捕获异常并打印错误信息
        print(f"Error fetching wallpaper URLs: {e}")
        return []  # 返回空列表


def create_download_directory(year, month):
    """为下载壁纸创建目录。

    参数:
        year (int): 年份。
        month (int): 月份。

    返回:
        str: 创建的目录路径。
    """
    base_dir = f"{year}{month:02d}"  # 基础目录名

    # 如果目录不存在，则创建目录
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        return base_dir

    # 如果目录已存在，创建带时间戳的新目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_name = f"{base_dir}_{timestamp}"
    os.makedirs(dir_name)
    return dir_name  # 返回新创建的目录路径


def download_monthly_wallpapers(year, month):
    """下载特定月份的所有壁纸。

    参数:
        year (int): 年份。
        month (int): 月份。
    """
    download_dir = create_download_directory(year, month)  # 创建下载目录
    print(f"Created directory: {download_dir}")

    urls = get_wallpaper_urls(year, month)  # 获取壁纸 URL
    print(f"\nFound {len(urls)} wallpapers for {year}-{month:02d}")

    successful_downloads = 0  # 记录成功下载的数量
    total_days = len(urls)  # 总壁纸数量

    # 遍历每个 URL 下载壁纸
    for index, url in enumerate(urls):
        # 计算日期：从月末往前数
        day = total_days - index
        filename = f"{year}{month:02d}{day:02d}.jpg"  # 文件名格式
        filepath = os.path.join(download_dir, filename)  # 完整文件路径

        print(f"\nDownloading wallpaper {index + 1}/{len(urls)}...")
        print(f"URL: {url}")
        print(f"Saving as: {filename}")

        # 下载文件并检查是否成功
        if download_file(url, filepath):
            print(f"Successfully downloaded wallpaper {filename}")
            successful_downloads += 1  # 成功下载计数

    # 打印下载总结
    print("\nDownload Summary:")
    print(f"Download directory: {download_dir}")
    print(f"Total wallpapers found: {len(urls)}")
    print(f"Successfully downloaded: {successful_downloads}")


if __name__ == "__main__":
    print("Script started")

    year = 2025  # 设置年份
    month = 2  # 设置月份
    download_monthly_wallpapers(year, month)  # 下载指定月份的壁纸

    print("\nScript completed")