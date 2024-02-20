import cv2
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/upload_video', methods=['POST'])
def upload_video():
    file = request.files['file']
    filename = file.filename
    file.save('static/' + filename)
    
    source = cv2.VideoCapture('static/' + filename)
    
    frame_width = int(source.get(3))
    frame_height = int(source.get(4))
    size = (frame_width, frame_height)
    
    result = cv2.VideoWriter('static/blackandwhite.mp4', 
                             cv2.VideoWriter_fourcc(*'mp4v'), 
                             30, 
                             size,
                             0)
    
    try:
        while True:
            status, frame_image = source.read()
            if not status:
                break
            gray = cv2.cvtColor(frame_image, cv2.COLOR_RGB2GRAY)
            result.write(gray)
        
        video_file = 'blackandwhite.mp4'
    
    except:
        print('Completed reading all the Frames from the Video')
    
    return 'Video converted successfully!'

@app.route('/download')
def download_file():
    converted_video_path = "static/blackandwhite.mp4"
    return send_file(converted_video_path, as_attachment=True)

if __name__ == '__main__':
    app.run()
