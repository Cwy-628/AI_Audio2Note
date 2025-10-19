"""
Video download API (only /api/process/video endpoint)
"""

import os
from flask import Blueprint, request, jsonify

# Create blueprint
process_bp = Blueprint('process', __name__)

# 确保导入并实例化了 ProcessService
from process_service import ProcessService  # 根据你的实际路径调整
process_service = ProcessService()


@process_bp.route('/api/process/video', methods=['POST'])
def process_video():
    """视频下载接口：接收视频 URL，调用服务层进行下载"""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"success": False, "error": "URL is required"}), 400

    url = data['url']
    page_number = data.get('page_number')  # 可选分页参数

    if not url or len(url.strip()) < 10:
        return jsonify({"success": False, "error": "Invalid URL"}), 400

    # 调用服务层下载视频
    result = process_service.process_video(url=url, page_number=page_number)
    if result.get("success"):
        return jsonify(result)
    else:
        return jsonify(result), 500