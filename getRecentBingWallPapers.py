import requests
import os
from datetime import datetime, timedelta
import json


def download_file(url, filepath):
    """Download a file from URL to the specified filepath"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


def get_bing_wallpaper(idx):
    """Get Bing wallpaper information starting from specific index"""
    try:
        # Bing API URL
        bing_api_url = "https://www.bing.com/HPImageArchive.aspx"

        params = {
            "format": "js",
            "idx": str(idx),  # Starting index
            "n": "8",  # Number of images to return (max 8)
            "mkt": "en-US"
        }

        response = requests.get(bing_api_url, params=params)
        response.raise_for_status()
        data = response.json()

        # 打印API返回的原始数据（调试用）
        # print(f"API Response for idx={idx}: {json.dumps(data, indent=2)}")

        return data.get('images', [])
    except Exception as e:
        print(f"Error getting wallpaper info for idx={idx}: {e}")
        return []


def download_wallpapers(days=30):
    """
    下载指定天数的必应壁纸
    参数:
    days: 想要下载的天数，建议不超过30天
    """
    # Create download directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    download_dir = f"bing_wallpapers_{timestamp}"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory: {download_dir}")

    successful_downloads = 0
    downloaded_dates = set()  # 用于追踪已下载的日期，避免重复

    # 由于API每次最多返回8张图片，我们需要多次调用来获取更多天数的图片
    for idx in range(0, days, 8):
        images = get_bing_wallpaper(idx)
        print(f"\nFetching images batch starting from {idx} days ago...")
        print(f"Found {len(images)} images in this batch")

        for image in images:
            # 获取图片日期
            date = datetime.strptime(image['startdate'], '%Y%m%d').strftime('%Y-%m-%d')

            # 检查是否已经下载过这个日期的图片
            if date in downloaded_dates:
                print(f"Skipping {date} - already downloaded")
                continue

            # 构建完整的4K图片URL
            base_url = "https://www.bing.com"
            image_url = base_url + image['urlbase'] + "_UHD.jpg"

            # 使用日期作为文件名
            filepath = os.path.join(download_dir, f"{date}.jpg")

            print(f"Downloading image for {date}...")
            if download_file(image_url, filepath):
                print(f"Successfully downloaded image for {date}")
                successful_downloads += 1
                downloaded_dates.add(date)

            # 打印图片的一些信息（调试用）
            # print(f"Image details for {date}:")
            # print(f"Title: {image.get('title')}")
            # print(f"Copyright: {image.get('copyright')}")

    # 打印下载汇总
    print("\nDownload Summary:")
    print(f"Download directory: {download_dir}")
    print(f"Requested days: {days}")
    print(f"Successfully downloaded: {successful_downloads}")
    print(f"Unique dates downloaded: {len(downloaded_dates)}")
    print("\nDownloaded dates:")
    for date in sorted(downloaded_dates):
        print(date)


if __name__ == "__main__":
    print("Script started")
    # 这里可以指定想要下载的天数，Bing的API支持最多15天壁纸，超过此值无意义。
    download_wallpapers(15)
    print("Script completed")