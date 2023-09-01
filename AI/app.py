from flask import Flask, render_template, request, send_file
import subprocess
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 图片处理
@app.route('/photo/photo', methods=['GET', 'POST'])
def photo():   
    return render_template('./photo/photo.html')

@app.route('/photo/object_detection', methods=['GET', 'POST'])
def photo_object_detection():
    original_image_data = None
    processed_image_data = None

    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            image_path = 'yolov7-main/runs/detect/uploaded_image.jpg'
            image.save(image_path)

            # subprocess.run(['python', 'detect.py'])
            command = ['python', 'yolov7-main/detect.py', '--source=yolov7-main/runs/detect/uploaded_image.jpg', '--outpath=yolov7-main/runs/detect/processed_image.jpg', '--weights=yolov7-main/weights/yolov7.pt']
            subprocess.run(command)

            original_image_path = image_path
            processed_image = 'yolov7-main/runs/detect/processed_image.jpg'
            with open(original_image_path, 'rb') as image_file:
                original_image_data = base64.b64encode(image_file.read()).decode('utf-8')
            with open(processed_image, 'rb') as image_file:
                processed_image_data = base64.b64encode(image_file.read()).decode('utf-8')

    if request.method == 'GET' and request.args.get('download') == 'true':
        return send_file('yolov7-main/runs/detect/processed_image.jpg', as_attachment=True)

    return render_template('./photo/object_detection.html', original_image_data=original_image_data, processed_image_data=processed_image_data)

@app.route('/photo/face_detection', methods=['GET', 'POST'])
def photo_face_detection():   
    return render_template('./photo/face_detection.html')

@app.route('/photo/change_background', methods=['GET', 'POST'])
def photo_change_background():   
    return render_template('./photo/change_background.html')

@app.route('/photo/expression', methods=['GET', 'POST'])
def photo_expression():   
    return render_template('./photo/expression.html')

@app.route('/photo/face', methods=['GET', 'POST'])
def photo_face():   
    return render_template('./photo/face.html')

# 视频处理
@app.route('/video/video', methods=['GET', 'POST'])
def video():   
    return render_template('./video/video.html')

@app.route('/video/object_detection', methods=['GET', 'POST'])
def video_object_detection():   
    return render_template('./video/object_detection.html')

@app.route('/video/face_detection', methods=['GET', 'POST'])
def video_face_detection():   
    return render_template('./video/face_detection.html')

@app.route('/video/change_face', methods=['GET', 'POST'])
def video_change_face():   
    return render_template('./video/change_face.html')

@app.route('/video/change_background', methods=['GET', 'POST'])
def video_change_background():   
    src = None
    bgr = None
    tar = None
    out = None

    if request.method == 'POST':
        video = request.files['video']
        original_background = request.files['original_background']
        replacement_background = request.files['replacement_background']

        video_path = 'BackgroundMattingV2-master/input/src.mp4'
        original_background_path = 'BackgroundMattingV2-master/input/bgr.png'
        replacement_background_path = 'BackgroundMattingV2-master/input/tar.png'

        video.save(video_path)
        original_background.save(original_background_path)
        replacement_background.save(replacement_background_path)

        command = ['python', 'BackgroundMattingV2-master/inference_video.py',
                    '--model-type=mattingrefine',
                    '--model-backbone=resnet50',
                    '--model-refine-sample-pixels=320_000',
                    '--model-checkpoint=BackgroundMattingV2-master/model/PyTorch/pytorch_resnet50.pth',
                    '--video-src=BackgroundMattingV2-master/input/src.mp4', 
                    '--video-bgr=BackgroundMattingV2-master/input/bgr.png',
                    '--output-dir=BackgroundMattingV2-master/output',
                    '--output-type=com',
                    #'--video-target-bgr=BackgroundMattingV2-master/input/tar.png']
                    ]
        subprocess.run(command)
        
    if request.method == 'GET' and request.args.get('download') == 'true':
        return send_file('BackgroundMattingV2-master/output/com.mp4', as_attachment=True)

    return render_template('./video/change_background.html', src=src, bgr=bgr, tar=tar, out=out)

# 语音生成
@app.route('/voice/voice', methods=['GET', 'POST'])
def voice():   
    return render_template('./voice/voice.html')

@app.route('/voice/speech_forgery', methods=['GET', 'POST'])
def voice_speech_forgery():   
    return render_template('./voice/speech_forgery.html')

@app.route('/voice/talking_head', methods=['GET', 'POST'])
def voice_talking_head():   
    return render_template('./voice/talking_head.html')

@app.route('/voice/lip_drive', methods=['GET', 'POST'])
def voice_lip_drive():   
    return render_template('./voice/lip_drive.html')

# 自动配乐
@app.route('/auto_compose', methods=['GET', 'POST'])
def auto_compose():   
    return render_template('./auto_compose.html')

# 关于我们
@app.route('/about_us', methods=['GET', 'POST'])
def about_us():   
    return render_template('./about_us.html')

@app.route('/sharpen', methods=['GET', 'POST'])
def sharpen():
    original_image_data = None
    processed_image_data = None

    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            image_path = 'uploaded_image.jpg'
            image.save(image_path)
            output_path = 'processed_image.jpg'

            # 调用本地的sharp.py脚本进行处理
            subprocess.run(['python', 'sharp.py', image_path, output_path])

            original_image_path = image_path
            processed_image = 'processed_image.jpg'
            with open(original_image_path, 'rb') as image_file:
                original_image_data = base64.b64encode(image_file.read()).decode('utf-8')
            with open(processed_image, 'rb') as image_file:
                processed_image_data = base64.b64encode(image_file.read()).decode('utf-8')

    if request.method == 'GET' and request.args.get('download') == 'true':
        return send_file('processed_image.jpg', as_attachment=True)

    return render_template('sharpen.html', original_image_data=original_image_data, processed_image_data=processed_image_data)




if __name__ == '__main__':
    app.run(debug=True)