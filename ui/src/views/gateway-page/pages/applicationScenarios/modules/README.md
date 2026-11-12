## 视觉模型检测对象行为异常

通过摄像头和麦克风采集的视频音频流进行识别（可基于opencv，yolov8等模型），检测面试者是否有异常行为（如玩手机、偷窥、睡觉、打架等）。

### 功能设计概览

| 模块            | 功能                                                             |
| --------------- | ---------------------------------------------------------------- |
| 🎥 全程录像     | 启动时开始录制，退出时停止，保存全场 exam_record.mp4。           |
| 🧠 异常检测     | 用 YOLOv8 检测“手机、人”等，结合 MMPose 识别头部角度，行为判断。 |
| 🚨 行为预警     | 检测到异常行为，立即弹窗或语音播报提醒。                         |
| 💾 异常录像存档 | 异常行为触发，单独保存10秒小视频（如：abnormal\_时间戳.mp4）。   |
| 🏷️ 行为标签记录 | 将检测时间、位置、行为类型写入日志文件。                         |

### 运行程序

<div style="border: 1px solid #4CAF50; padding: 10px; background-color: #f9fff9; color: #4CAF50; border-radius: 5px;">
<strong>提示：</strong>如您第一次使用，请先完成 本地部署 部分。
</div>

打开新的`powershell`终端，进入项目目录：

```powershell
cd D:\detection
```

新建虚拟环境：

```powershell
python -m venv .venv
```

激活虚拟环境：

```powershell
.\.venv\Scripts\activate
```

在命令行中执行以下命令：

```powershell
python load.py
```

### 使用说明

- 设备必须拥有一个摄像头且仅采集第一个摄像头数据。
- 程序启动后，会自动开始录像并检测异常行为。
- 如果检测到异常行为，在监视窗口左上角提示，另外`powershell`中也会输出日志。
- 异常行为触发，会单独保存10秒小视频，并记录行为标签。
- 光标选中`powershell`窗口，按下`Q`键退出程序。

### 演示画面

- 检测到画面有人使用手机

![使用手机](http://81.70.201.200:8100/20250523143752.png)

- 检测到有人拿刀具，疑似暴力行为

![暴力行为检测示例](http://81.70.201.200:8100/20250523143741.png)

### 本地部署

<div style="border: 1px solid #4CAF50; padding: 10px; background-color: #f9fff9; color: #4CAF50; border-radius: 5px;">
<strong>提示：</strong>本案例暂仅限windows系统演示使用，以下部署时需连接互联网环境。
</div>

#### 1. 安装Python 3.11

从官网下载python3.11，点击下载[链接](https://www.python.org/ftp/python/3.11.9/python-3.11.9.exe)可快速下载。

#### 2. 拉取项目代码

在`D:`盘根路径下新建一个目录`detection`。

新建文件`load.py`，复制以下代码到此文件保存：

```python
import os
import cv2
import time
import logging
import threading
import numpy as np
from collections import deque
from ultralytics import YOLO
import mediapipe as mp
import sounddevice as sd
import soundfile as sf
import subprocess

logging.getLogger("ultralytics").setLevel(logging.ERROR)

class BehaviorMonitor:
    def __init__(self, abnormal_folder='abnormal_behavior_videos'):
        os.makedirs(abnormal_folder, exist_ok=True)
        self.abnormal_folder = abnormal_folder

        self.model = YOLO('yolov8s.pt')
        # 初始化类别颜色映射
        self.class_colors = {}
        for cls_id in range(len(self.model.names)):
            hue = (cls_id * 50) % 180  # 通过调整步长控制色相差异
            hsv_color = np.uint8([[[hue, 255, 255]]])
            bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
            self.class_colors[cls_id] = tuple(map(int, bgr_color))

        self.cap = cv2.VideoCapture(0)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0

        self.temp_full_video = 'exam_video_temp.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        self.full_video_writer = cv2.VideoWriter(self.temp_full_video, fourcc, self.fps,
                                                 (self.frame_width, self.frame_height))

        self.pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.audio_data = []
        self.abnormal_recording = False
        self.record_start_time = None
        self.record_frames = []
        self.event_name = ""
        self.peek_counter = self.sleep_counter = self.violent_counter = 0
        self.pre_record_buffer = deque(maxlen=int(self.fps * 5))

        self.running = True
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.audio_thread.start()
        self.audio_stream = None

        self.log_queue = deque(maxlen=4)  # 新增日志队列
        self.log_font = cv2.FONT_HERSHEY_SIMPLEX  # 日志字体
        self.log_font_scale = 0.4                # 字体大小
        self.log_line_height = 14                 # 行高
        self.log_bg_color = (0, 0, 0, 0.6)        # 背景颜色及透明度（BGRα）

    def record_audio(self):
        def callback(indata, frames, time_info, status):
            if self.running:
                self.audio_data.append(indata.copy())
        try:
            self.audio_stream = sd.InputStream(samplerate=16000, channels=1, dtype='int16', callback=callback)
            with self.audio_stream:
                while self.running:
                    time.sleep(0.05)
        except Exception as e:
            logging.error(f"Audio thread error: {e}")

    def save_audio(self, filename):
        if self.audio_data:
            audio = np.concatenate(self.audio_data, axis=0)
            sf.write(filename, audio, 16000)
            self.audio_data.clear()

    def log_behavior(self, event_type, video_path=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] Detected: {event_type}"
        # 添加到日志队列
        self.log_queue.append(log_line)
        if video_path:
            log_line += f", Video: {video_path}"
        with open("behavior_log.txt", 'a') as f:
            f.write(log_line + "\n")
        print(log_line)

    def detect_head_pose(self, landmarks):
        nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE]
        left_eye = landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE]
        right_eye = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EYE]
        dx = abs(left_eye.x - right_eye.x)
        dy = abs(left_eye.y - right_eye.y)
        if dy > 0.12: return "Sleeping"
        if dx > 0.17: return "Peeking"
        return None

    def detect_violent_behavior(self, landmarks):
        left_hand = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
        right_hand = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]
        dist = ((left_hand.x - right_hand.x)**2 + (left_hand.y - right_hand.y)**2) ** 0.5
        return "Violent" if dist < 0.07 else None

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret: break

            # 绘制日志区域
            if self.log_queue:
                # 创建透明覆盖层
                overlay = frame.copy()
                y_start = 10
                max_width = 0

                # 先计算最大文本宽度
                for log in self.log_queue:
                    (text_width, _), _ = cv2.getTextSize(
                        log, self.log_font, self.log_font_scale, 1)
                    max_width = max(max_width, text_width)

                # 绘制半透明背景
                cv2.rectangle(overlay,
                            (10, y_start),
                            (20 + max_width, 15 + len(self.log_queue)*self.log_line_height),
                            self.log_bg_color[:3],
                            -1)

                # 实际绘制日志文本
                for i, log in enumerate(self.log_queue):
                    y = y_start + (i+1)*self.log_line_height
                    cv2.putText(overlay, log,
                            (15, y),
                            self.log_font,
                            self.log_font_scale,
                            (255, 255, 255),  # 白色文字
                            1, cv2.LINE_AA)

                # 融合覆盖层
                cv2.addWeighted(overlay, self.log_bg_color[3],
                            frame, 1 - self.log_bg_color[3],
                            0, frame)

            self.full_video_writer.write(frame)

            results = self.model(frame, verbose=False, stream=False)
            detected_classes = [self.model.names[int(cls)] for cls in results[0].boxes.cls.tolist()]
            boxes = results[0].boxes.xyxy.tolist()

            for i, (box, cls) in enumerate(zip(boxes, results[0].boxes.cls.tolist())):
                x1, y1, x2, y2 = map(int, box)
                cls_id = int(cls)
                color = self.class_colors.get(cls_id, (255, 0, 0))  # 获取类别对应颜色
                label = detected_classes[i]

                # 绘制边界框
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)

                # 字体大小为0.6，线宽为1
                font_scale = 0.6
                thickness = 1
                (text_width, text_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)

                # 调整背景框高度（减少垂直间距）
                bg_y1 = y1 - text_height - baseline - 5  # 上移5像素
                bg_y2 = y1

                # 绘制文本背景（更紧凑的高度）
                cv2.rectangle(
                    frame,
                    (x1, bg_y1),
                    (x1 + text_width, bg_y2),
                    color,
                    -1
                )

                # 计算文本位置（垂直居中）
                text_y = bg_y1 + text_height + baseline - 3  # 微调垂直位置

                # 绘制白色文本（调整字体参数）
                cv2.putText(
                    frame,
                    label,
                    (x1, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    (255, 255, 255),
                    thickness,
                    cv2.LINE_AA
                )

            if 'cell phone' in detected_classes:
                self.start_abnormal_recording(frame, "Using_Phone")
            if 'knife' in detected_classes:
                self.start_abnormal_recording(frame, "Violent")

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_results = self.pose.process(frame_rgb)

            if pose_results.pose_landmarks:
                event = self.detect_head_pose(pose_results.pose_landmarks.landmark)
                violent = self.detect_violent_behavior(pose_results.pose_landmarks.landmark)
                self.update_counters(event, violent)
                self.check_counters(frame)

                # 绘制姿态关键点
                # for landmark in pose_results.pose_landmarks.landmark:
                #     x = int(landmark.x * frame.shape[1])
                #     y = int(landmark.y * frame.shape[0])
                #     cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)

            self.pre_record_buffer.append(frame)

            if self.abnormal_recording:
                self.record_frames.append(frame)
                if time.time() - self.record_start_time >= 10:
                    self.save_abnormal_clip()

            cv2.imshow('Interview Monitoring', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("按Q退出...")
                self.running = False

        self.cleanup()

    def start_abnormal_recording(self, frame, event_name):
        self.log_behavior(f"{event_name.replace('_', ' ')}")
        if not self.abnormal_recording:
            self.abnormal_recording = True
            self.record_start_time = time.time()
            self.record_frames = list(self.pre_record_buffer) + [frame]
            self.event_name = event_name

    def update_counters(self, event, violent):
        self.peek_counter = self.peek_counter + 1 if event == "Peeking" else 0
        self.sleep_counter = self.sleep_counter + 1 if event == "Sleeping" else 0
        self.violent_counter = self.violent_counter + 1 if violent == "Violent" else 0

    def check_counters(self, frame):
        if self.peek_counter >= 3:
            self.start_abnormal_recording(frame, "Peeking")
        if self.sleep_counter >= 3:
            self.start_abnormal_recording(frame, "Sleeping")
        if self.violent_counter >= 3:
            self.start_abnormal_recording(frame, "Violent")

    def save_abnormal_clip(self):
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        video_path = f"{self.abnormal_folder}/{self.event_name}_{timestamp}.mp4"
        temp_video = f"temp_video_{timestamp}.mp4"
        temp_audio = f"temp_audio_{timestamp}.wav"

        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(temp_video, fourcc, self.fps, (self.frame_width, self.frame_height))
        for f in self.record_frames:
            out.write(f)
        out.release()

        self.save_audio(temp_audio)

        subprocess.run([
            "ffmpeg", "-y", "-i", temp_video, "-i", temp_audio,
            "-c:v", "copy", "-c:a", "aac", "-r", str(self.fps), video_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        self.log_behavior(self.event_name.replace("_", " "), video_path)

        os.remove(temp_video)
        os.remove(temp_audio)
        self.abnormal_recording = False
        self.record_frames.clear()
        self.event_name = ""

    def cleanup(self):
        self.running = False
        if self.audio_stream and self.audio_stream.active:
            self.audio_stream.close()
        self.audio_thread.join(timeout=1.0)

        if self.cap.isOpened():
            self.cap.release()
        if self.full_video_writer.isOpened():
            self.full_video_writer.release()

        audio_temp = "exam_audio_temp.wav"
        self.save_audio(audio_temp)

        # subprocess.run([
        #     "ffmpeg", "-y", "-i", self.temp_full_video, "-i", audio_temp,
        #     "-c:v", "copy", "-c:a", "aac", "exam_record.mp4"
        # ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        # if os.path.exists(audio_temp): os.remove(audio_temp)
        # if os.path.exists(self.temp_full_video): os.remove(self.temp_full_video)

        cv2.destroyAllWindows()
        cv2.waitKey(1)
        self.pose.close()
        print("全程录像已合并音频，程序已安全退出！")

if __name__ == "__main__":
    monitor = BehaviorMonitor()
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("手动中断，正在退出...")
        monitor.running = False
        monitor.cleanup()
```

#### 3. 新建python虚拟环境

然后打开`powershell`终端，进入项目目录：

```powershell
cd D:\detection
```

新建虚拟环境：

```powershell
python -m venv .venv
```

激活虚拟环境：

```powershell
.\.venv\Scripts\activate
```

#### 4. 安装依赖包

安装依赖包：

```powershell
pip install opencv-python ultralytics mediapipe soundfile -i https://pypi.tuna.tsinghua.edu.cn/simple
```

以上即安装部署完成，可执行`运行程序`部分，开始使用。
