"""
视记 - 音频下载工具模块

功能：
- 使用 yt-dlp 从 B站 和 YouTube 下载视频并提取为 MP3 音频文件
- 支持平台：B站 (bilibili.com)、YouTube (youtube.com)
- 分P选择和URL验证

安全特性：
- URL域名白名单验证
- 文件路径安全处理
- 错误处理和异常管理

作者：视记开发团队
版本：1.0.0
"""

import os
from typing import Optional

import yt_dlp


class AudioDownloader:
    """
    视记音频下载器类

    支持从 B站 和 YouTube 平台下载视频并提取为 MP3 音频文件
    提供分P选择、URL验证、错误处理等功能
    """

    def __init__(self, session_folder: str = None):
        """
        初始化视记音频下载器

        配置 yt-dlp 下载选项，包括输出格式、音频质量等
        自动创建 temp 目录用于保存下载的文件

        Args:
            session_folder (str, optional): 会话文件夹路径
        """
        # 创建 temp 目录
        self.temp_dir = "temp"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        # 设置输出目录
        if session_folder:
            self.output_dir = session_folder
        else:
            self.output_dir = self.temp_dir

        self.ydl_opts = {
            # 输出目录：保存到指定文件夹
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),

            # 选择最佳音频质量进行下载
            'format': 'bestaudio/best',

            # 后处理器配置：提取音频并转换为 MP3
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # 使用 FFmpeg 提取音频
                'preferredcodec': 'mp3',  # 音频编码格式为 MP3
                'preferredquality': '192',  # 音频质量 192 kbps
            }],
        }

    def download_audio(self, url: str, page_number: Optional[int] = None) -> bool:
        """
        下载视频并提取为 MP3 音频文件

        Args:
            url (str): 视频 URL 地址
                - B站: https://www.bilibili.com/video/...
                - YouTube: https://www.youtube.com/watch?v=...
            page_number (int, optional): 分P编号（从1开始）
                - None: 下载所有分P
                - 数字: 下载指定分P

        Returns:
            bool: 下载成功返回 True，失败返回 False
        """
        # 验证 URL 是否支持
        if not self._is_supported_url(url):
            print("❌ 不支持的平台！")
            print("💡 目前只支持：")
            print("   - B站: https://www.bilibili.com/video/...")
            print("   - YouTube: https://www.youtube.com/watch?v=...")
            return False

        # 复制配置选项
        ydl_opts = self.ydl_opts.copy()

        # 如果指定了分P编号，则只下载该分P
        if page_number is not None:
            ydl_opts['playlist_items'] = f'{page_number}:{page_number}'

        try:
            # 创建 yt-dlp 下载器实例
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"🎵 开始下载音频: {url}")
                print("📥 正在获取视频信息...")

                # 执行下载
                ydl.download([url])

                print("✅ 音频下载完成！")
                return True

        except Exception as e:
            print(f"❌ 下载失败: {str(e)}")
            print("💡 请确保网络连接正常、已安装FFmpeg、视频链接有效")
            return False

    def get_video_title(self, url: str) -> Optional[str]:
        """
        获取视频标题

        Args:
            url (str): 视频 URL 地址

        Returns:
            Optional[str]: 视频标题，获取失败返回 None
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('title', '未知标题')
        except Exception as e:
            print(f"❌ 获取视频标题失败: {str(e)}")
            return None

    def _is_supported_url(self, url: str) -> bool:
        """
        检查 URL 是否支持（内部方法）

        Args:
            url (str): 视频 URL

        Returns:
            bool: 支持返回 True，不支持返回 False
        """
        supported_domains = [
            'bilibili.com',
            'youtube.com',
            'youtu.be'
        ]

        return any(domain in url.lower() for domain in supported_domains)
