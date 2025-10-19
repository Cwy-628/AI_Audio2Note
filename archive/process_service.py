"""
Minimal ProcessService: Only keeps video download functionality
"""

import os
from audio_downloader import AudioDownloader


class ProcessService:
    """仅保留视频下载相关功能的服务类"""

    def __init__(self):
        self.temp_dir = "temp"  # 用于存放下载的会话文件夹

    def process_video(self, url: str, page_number: int = None) -> dict:
        """
        下载视频（或音频，根据你的实际业务逻辑）
        Args:
            url: 视频页面 URL 或视频直链
            page_number: 可选分页参数，用于批量下载等场景
        Returns:
            dict: {
                "success": bool,
                "files": list[下载的文件路径],
                "session_folder": 下载文件所在目录,
                "video_title": 视频标题
            } 或者错误信息
        """
        try:
            downloader = AudioDownloader()
            video_title = downloader.get_video_title(url)
            if not video_title:
                return {"success": False, "error": "无法获取视频标题"}

            # 创建以视频标题命名的文件夹，用于存放下载内容
            session_folder = os.path.join(self.temp_dir, video_title)
            os.makedirs(session_folder, exist_ok=True)

            # 使用指定目录的 downloader 实例进行下载
            downloader = AudioDownloader(session_folder)
            download_success = downloader.download_audio(url, page_number)

            if not download_success:
                return {"success": False, "error": "视频下载失败"}

            # 列出下载的文件
            files = [os.path.join(session_folder, f) for f in os.listdir(session_folder)]

            return {
                "success": True,
                "files": files,
                "session_folder": session_folder,
                "video_title": video_title
            }

        except Exception as e:
            return {"success": False, "error": str(e)}