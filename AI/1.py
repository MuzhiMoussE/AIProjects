import subprocess        
command = ['echo y |python', 'BackgroundMattingV2-master/inference_video.py',
                    '--model-type=mattingrefine',
                    '--model-backbone=resnet50',                    
                    '--model-backbone-scale=0.25',
                    '--model-refine-mode=sampling',
                    '--model-refine-sample-pixels=80000',
                    '--model-checkpoint=BackgroundMattingV2-master/model/PyTorch/pytorch_resnet50.pth',
                    '--video-src=BackgroundMattingV2-master/input/src.mp4', 
                    '--video-bgr=BackgroundMattingV2-master/input/bgr.png',
                    '--output-dir=BackgroundMattingV2-master/output',
                    '--output-type=com']

subprocess.run(' '.join(command), shell=True)

"""
Inference video: Extract matting on video.

Example:

    python inference_video.py \
        --model-type mattingrefine \
        --model-backbone resnet50 \
        --model-backbone-scale 0.25 \
        --model-refine-mode sampling \
        --model-refine-sample-pixels 80000 \
        --model-checkpoint "PATH_TO_CHECKPOINT" \
        --video-src "PATH_TO_VIDEO_SRC" \
        --video-bgr "PATH_TO_VIDEO_BGR" \
        --video-resize 1920 1080 \
        --output-dir "PATH_TO_OUTPUT_DIR" \
        --output-type com fgr pha err ref \
        --video-target-bgr "PATH_TO_VIDEO_TARGET_BGR"

"""