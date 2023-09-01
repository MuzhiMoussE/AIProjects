from flask import Flask, render_template, request, send_file
import subprocess
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    original_image_data = None
    processed_image_data = None

    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            image_path = 'yolov7-main/runs/detect/uploaded_image.jpg'
            image.save(image_path)
            output_path = 'yolov7-main/runs/detect/processed_image.jpg'

            # subprocess.run(['python', 'detect.py'])
            command = ['python', 'yolov7-main/detect.py', '--source=yolov7-main/runs/detect/uploaded_image.jpg', '--weights=yolov7-main/weights/yolov7.pt']
            subprocess.run(command)

            original_image_path = image_path
            processed_image = 'yolov7-main/runs/detect/processed_image.jpg'

            with open(original_image_path, 'rb') as image_file:
                original_image_data = base64.b64encode(image_file.read()).decode('utf-8')

            with open(processed_image, 'rb') as image_file:
                processed_image_data = base64.b64encode(image_file.read()).decode('utf-8')


    if request.method == 'GET' and request.args.get('download') == 'true':
        return send_file('yolov7-main/runs/detect/processed_image.jpg', as_attachment=True)

    return render_template('index0.html', original_image_data=original_image_data, processed_image_data=processed_image_data)

if __name__ == '__main__':
    app.run(debug=True)