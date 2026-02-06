import cv2
import time
import streamlit as st
from ultralytics import YOLO
from threading import Thread
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

# --- CONFIGURATION (UPDATE THESE) ---
INFLUX_TOKEN = "MLJNOTH-8g5UPHwnT4krjIiPMgHwBCetLQva5vvAViY7Eg6faX_og1LsPBEOcbC6fjgPC0jlndeyCvHVc8IlkA==" 
ORG = "my-org"
BUCKET = "jetson_data"
URL = "http://localhost:8086"

# Jetson Stream URL (Change this if using Jetson)
JETSON_URL = "tcp://192.168.1.162:5003" 

# --- STREAMLIT PAGE SETUP ---
st.set_page_config(page_title="Jetson Coral AI", layout="wide")
st.title("🪸 Live Coral Detection Dashboard")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Settings")
confidence = st.sidebar.slider("Model Confidence", min_value=0.1, max_value=1.0, value=0.4)
enable_db = st.sidebar.checkbox("Log to Database", value=True)

# Toggle Source
source_option = st.sidebar.radio("Select Video Source", ("Laptop Webcam", "Jetson Stream"))

# Determine Source
if source_option == "Laptop Webcam":
    src = 0
else:
    src = JETSON_URL

# --- CACHED RESOURCES (Load once) ---
@st.cache_resource
def load_model():
    return YOLO('yolov8n.pt')

@st.cache_resource
def get_db_client():
    client = InfluxDBClient(url=URL, token=INFLUX_TOKEN, org=ORG)
    return client.write_api(write_options=ASYNCHRONOUS)

model = load_model()
write_api = get_db_client()

# --- IMPROVED VIDEO CLASS (Fixes Windows Issues) ---
class VideoStream:
    def __init__(self, source):
        # Fix for Windows: Use DirectShow for local webcam (int), FFMPEG for streams (str)
        if isinstance(source, int):
            self.stream = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        else:
            self.stream = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
            
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()

# --- MAIN APP LOGIC ---
kpi1, kpi2 = st.columns(2)
with kpi1:
    fps_text = st.markdown("**FPS:** 0")
with kpi2:
    status_text = st.markdown("**Status:** Ready")

image_placeholder = st.empty()
stop_button = st.button("Stop Stream")

# START BUTTON LOGIC
if st.button("Start Live Feed"):
    # Initialize Camera
    try:
        vs = VideoStream(src).start()
        time.sleep(1.0) # Warmup
        
        # Check if camera opened correctly
        if vs.stream.isOpened() == False:
            st.error("🚨 Error: Could not open camera source. Check if another app is using it.")
            st.stop()
            
        status_text.markdown("**Status:** Running...")
        prev_time = 0

        while True:
            frame = vs.read()
            
            # --- ERROR CHECK ---
            if frame is None:
                st.warning(f"⚠️ No frame received from source: {src}. Retrying...")
                time.sleep(0.1)
                continue
            # -------------------
            
            # 1. Resize for speed
            frame = cv2.resize(frame, (640, 360))
            
            # 2. Inference
            results = model(frame, conf=confidence, verbose=False)
            
            # 3. Database Logging
            if enable_db:
                detections = results[0].boxes.cls.cpu().numpy()
                if len(detections) > 0:
                    from collections import Counter
                    counts = Counter([model.names[int(cls)] for cls in detections])
                    
                    point = Point("detection_log").tag("camera", "stream_v1")
                    for name, count in counts.items():
                        point.field(name, int(count))
                    write_api.write(bucket=BUCKET, org=ORG, record=point)

            # 4. Visualization (Convert BGR to RGB for Browser)
            annotated_frame = results[0].plot()
            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            
            image_placeholder.image(rgb_frame, channels="RGB")

            # Update FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            fps_text.markdown(f"**FPS:** {int(fps)}")

            # Stop Logic
            if stop_button:
                vs.stop()
                status_text.markdown("**Status:** Stopped")
                break
                
    except Exception as e:
        st.error(f"Error occurred: {e}")
        if 'vs' in locals():
            vs.stop()