from flask import Flask
from flask_cors import CORS
from api import process_bp  # 替换成你实际导入蓝图的名字

app = Flask(__name__)
CORS(app)  # ✅ 允许所有来源跨域访问（开发阶段）

app.register_blueprint(process_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)