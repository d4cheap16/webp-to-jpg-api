from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

# 首頁檢查用
@app.route('/', methods=['GET'])
def home():
    return "WebP to JPG API is running!"

# 轉檔核心
@app.route('/convert', methods=['POST'])
def convert_image():
    # 檢查有沒有收到名為 'image' 的檔案
    if 'image' not in request.files:
        return "No image provided", 400
    
    file = request.files['image']
    try:
        # 用 Pillow 開啟圖片 (原生支援 WebP 解碼)
        img = Image.open(file)
        
        # 強制轉換為 RGB 色彩模式 (去除 WebP 可能帶有的透明背景)
        rgb_im = img.convert('RGB')
        
        # 將轉換後的 JPG 存在記憶體中
        img_io = io.BytesIO()
        rgb_im.save(img_io, 'JPEG', quality=90)
        img_io.seek(0)
        
        # 回傳乾淨的 JPG 檔案
        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
