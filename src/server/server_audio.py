from flask_socketio import SocketIO, emit
import librosa
from array import array
import wave
import pickle
from sys import byteorder
from io import BytesIO
import soundfile
import pyaudio
from struct import pack
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import cv2
from collections import deque
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import time
from experta import KnowledgeEngine, Fact, Rule
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
RECORDING = 1
db = SQLAlchemy(app)
# session_data = {}


# إنشاء جدول المستخدمين
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)


# إنشاء جدول الفيديوهات
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    video_name = db.Column(db.String(150), nullable=False)
    recorded_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    score = db.Column(db.Float, nullable=False)


class SessionReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    end_time = db.Column(db.String(20), nullable=False)
    final_score = db.Column(db.Float, nullable=False)
    hand_crossed = db.Column(db.String(255), nullable=True)
    hand_on_waist = db.Column(db.String(255), nullable=True)
    hand_on_head = db.Column(db.String(255), nullable=True)
    hand_straight_down = db.Column(db.String(255), nullable=True)
    standing_straight = db.Column(db.String(255), nullable=True)
    body_lean = db.Column(db.String(255), nullable=True)
    open_palms_forward = db.Column(db.String(255), nullable=True)
    triangle_power = db.Column(db.String(255), nullable=True)
    evaluation = db.Column(db.String(20), nullable=False)
    positive_tips = db.Column(db.Text, nullable=True)
    negative_tips = db.Column(db.Text, nullable=True)

    # إضافات لإحصائيات الحركات
    hand_crossed_percentage = db.Column(db.Float, nullable=True)
    hand_on_waist_percentage = db.Column(db.Float, nullable=True)
    hand_on_head_percentage = db.Column(db.Float, nullable=True)
    hand_straight_down_percentage = db.Column(db.Float, nullable=True)
    standing_straight_percentage = db.Column(db.Float, nullable=True)
    body_lean_percentage = db.Column(db.Float, nullable=True)
    open_palms_forward_percentage = db.Column(db.Float, nullable=True)
    triangle_power_percentage = db.Column(db.Float, nullable=True)
    audio_result = db.Column(db.Text, nullable=True)

    video = db.relationship("Video", backref=db.backref("reports", lazy=True))


# # إنشاء قاعدة البيانات والجداول
with app.app_context():
    db.create_all()


class PoseFact(Fact):
    """Info about the detected pose."""

    pass


class PoseExpertSystem(KnowledgeEngine):

    @Rule(PoseFact(hand_on_head=True))
    def hand_on_head(self):
        self.declare(PoseFact(standing_straight=False))
        print("Detected: Hand on Head")
        print(
            "“Placing your hand on your head while speaking can be perceived as a sign of stress, confusion, or deep thought. Try to maintain a relaxed posture with your hands by your sides or gesturing naturally to emphasize your points. Remember, ‘Your body speaks as loudly as your words.’”"
        )
        socketio.emit(
            "video_message",
            {
                "message": "“Placing your hand on your head while speaking can be perceived as a sign of stress, confusion, or deep thought. Try to maintain a relaxed posture with your hands by your sides or gesturing naturally to emphasize your points. Remember, ‘Your body speaks as loudly as your words.’”"
            },
        )

    @Rule(PoseFact(straight_down_hands=True))
    def straight_down_hands(self):
        self.declare(PoseFact(standing_straight=False))
        print("Detected: Hands Straight Down")
        print(
            "This gesture reflects confidence and stability. It conveys calmness and control, and helps in presenting a professional and reliable image. Continue with this style, as it adds great value to your communication style."
        )
        socketio.emit(
            "video_message",
            {
                "message": "This gesture reflects confidence and stability. It conveys calmness and control, and helps in presenting a professional and reliable image. Continue with this style, as it adds great value to your communication style."
            },
        )

    @Rule(PoseFact(hand_in_pocket=True))
    def hand_in_pocket(self):
        print("Detected: Hand in Pocket")
        print(
            "“You tend to put your hand in your pocket while speaking. This gesture can be a sign of ambiguity or withdrawal. Don’t rely on it continuously, and remember, ‘confidence and openness are the key to effective communication.’”"
        )

    @Rule(PoseFact(crossed_hands=True))
    def crossed_hands(self):
        self.declare(PoseFact(standing_straight=False))
        self.declare(PoseFact(hand_on_waist=False))
        print("Detected: Crossed Hands")
        print(
            "I notice that you often cross your forearms while speaking.This gesture may indicate defensiveness or closure."
        )
        print(
            "I would like to suggest some tips that might help you:Try to adopt an open posture while speaking. You can place your hands on your sides or on your knees in an uncrossed manner. This can help project a more open and confident image. Try to look directly at the audience./ This can increase confidence and reduce the need for crossing your arms."
        )

    @Rule(PoseFact(standing_straight=True))
    def standing_straight(self):
        self.declare(PoseFact(body_lean=False))
        print("Detected: Standing Straight")
        print(
            "“Maintaining a straight posture while speaking is a powerful  cue. It  conveys confidence and authority,. Remember, ‘Stand tall and let your presence be felt.’”"
        )

    @Rule(PoseFact(hand_on_waist=True, crossed_hands=False))
    def hand_on_waist(self):
        self.declare(PoseFact(standing_straight=False))
        print("Detected: Hand on Waist")
        print(
            "“Putting your hand on the waist while talking can be explained by a challenge or loss of patience. Remember, 'Stand up straight and let your presence feel’”"
        )
        socketio.emit(
            "video_message",
            {
                "message": "“Putting your hand on the waist while talking can be explained by a challenge or loss of patience. Remember, 'Stand up straight and let your presence feel’”"
            },
        )

    @Rule(PoseFact(body_lean=True))
    def body_lean(self):
        self.declare(PoseFact(standing_straight=False))
        print("Detected: Body Lean")
        print(
            "Remember, bending over while talking may be a sign of distrust or relying on something for support. Try to maintain a straight and steady posture while speaking. This reflects confidence and stability. But, don't forget to be natural and comfortable to reflect confidence and professionalism."
        )

    @Rule(PoseFact(open_palm_fw=True))
    def open_palm_fw(self):
        print("Detected: Open Palms Forward")
        print(
            "You tend to use 'OPEN_PALMS_FORWARD' movement while speaking, this movement expresses openness, honesty and willingness to communicate. But, remember, it's a good idea to use this movement in a balanced and contextual way. "
        )

    @Rule(PoseFact(triangle_power_gesture=True))
    def triangle_power_gesture(self):
        self.declare(PoseFact(standing_straight=False))
        print("Detected: Triangle Power Gesture ")
        print(
            "Most people use the 'Triangle Power Gesture'  movement to show authority and control. But you need to use them with caution: excessive use of this movement may make you look domineering or aggressive. Use them in key moments to emphasize a certain point or to introduce oneself . "
        )


# إعداد Mediapipe

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
hands = mp_hands.Hands(
    static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8
)


def update_performance_plot(time_points, performance_scores):
    print("plot update")
    # plt.clf()
    # plt.plot(
    #     time_points,
    #     performance_scores,
    #     marker="o",
    #     linestyle="-",
    #     color="b",
    #     label="Performance",
    # )
    # plt.xlabel("Time")
    # plt.ylabel("Performance Score")
    # plt.title("Real-Time Performance Tracking")
    # plt.legend()
    # plt.grid(True)
    # plt.pause(0.001)


# تحسين الإضاءة باستخدام CLAHE
def apply_clahe(image):
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    yuv[:, :, 0] = clahe.apply(yuv[:, :, 0])
    return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)


# دوال الحسابات الأساسية (كما هي في الكود السابق)
def euclidean_distance(point1, point2):
    return np.linalg.norm(point1 - point2)


def calculate_angle(point1, point2, point3):
    vector1 = point1 - point2
    vector2 = point3 - point2
    cosine_angle = np.dot(vector1, vector2) / (
        np.linalg.norm(vector1) * np.linalg.norm(vector2)
    )
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)


def calculate_distance(point1, point2):
    return np.sqrt(
        (point1.x - point2.x) ** 2
        + (point1.y - point2.y) ** 2
        + (point1.z - point2.z) ** 2
    )


def get_landmark_array(pose_landmarks):
    if not pose_landmarks:
        return np.array([])
    return np.array(
        [[landmark.x, landmark.y, landmark.z] for landmark in pose_landmarks.landmark]
    )


# Calculate slope between two points
def calculate_slope(a, b):
    return (b[1] - a[1]) / (b[0] - a[0]) if (b[0] - a[0]) != 0 else np.inf


def calc_distance(pt1, pt2):
    return ((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2 + (pt1.z - pt2.z) ** 2) ** 0.5


# اكتشاف وضع اليد على الرأس
def detect_hand_on_head(pose_landmarks):
    if not pose_landmarks:
        return False

    # نقاط الرأس العليا
    upper_head_points = [
        np.array(
            [
                pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x,
                pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y,
            ]
        ),
        np.array(
            [
                pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE].x,
                pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE].y,
            ]
        ),
        np.array(
            [
                pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE].x,
                pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE].y,
            ]
        ),
        np.array(
            [
                pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].x,
                pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].y,
            ]
        ),
        np.array(
            [
                pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].x,
                pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].y,
            ]
        ),
    ]

    # نقاط الرأس السفلى
    lower_head_points = [
        np.array(
            [
                pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT].x,
                pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT].y,
            ]
        ),
        np.array(
            [
                pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].x,
                pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].y,
            ]
        ),
    ]

    # نقاط اليدين
    left_wrist = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y,
        ]
    )
    right_wrist = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y,
        ]
    )
    left_elbow = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y,
        ]
    )
    right_elbow = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y,
        ]
    )
    left_shoulder = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
        ]
    )
    right_shoulder = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
        ]
    )

    # حساب المسافة بين الأكتاف (كمرجع لحجم الجسم)
    shoulder_width = euclidean_distance(left_shoulder, right_shoulder)

    # حساب المسافات بين اليدين والرأس
    left_wrist_to_upper_head = min(
        euclidean_distance(left_wrist, point) for point in upper_head_points
    )
    right_wrist_to_upper_head = min(
        euclidean_distance(right_wrist, point) for point in upper_head_points
    )
    left_wrist_to_lower_head = min(
        euclidean_distance(left_wrist, point) for point in lower_head_points
    )
    right_wrist_to_lower_head = min(
        euclidean_distance(right_wrist, point) for point in lower_head_points
    )

    # حساب الزوايا بين نقاط الرأس واليدين
    left_wrist_head_angle = min(
        calculate_angle(left_wrist, point, left_elbow)
        for point in upper_head_points + lower_head_points
    )
    right_wrist_head_angle = min(
        calculate_angle(right_wrist, point, right_elbow)
        for point in upper_head_points + lower_head_points
    )

    # تحديد إذا كانت اليد على الرأس بناءً على المسافات والزوايا
    upper_distance_threshold = (
        0.2 * shoulder_width
    )  # نسبة إلى عرض الكتف لضبط الحساسية للمناطق العليا
    lower_distance_threshold = (
        0.3 * shoulder_width
    )  # نسبة إلى عرض الكتف لضبط الحساسية للمناطق السفلى
    angle_threshold = 60  # يمكن تعديل هذا القيم لضبط حساسية الاكتشاف

    left_hand_on_head = (
        left_wrist_to_upper_head < upper_distance_threshold
        or left_wrist_to_lower_head < lower_distance_threshold
    ) and left_wrist_head_angle < angle_threshold
    right_hand_on_head = (
        right_wrist_to_upper_head < upper_distance_threshold
        or right_wrist_to_lower_head < lower_distance_threshold
    ) and right_wrist_head_angle < angle_threshold

    return left_hand_on_head or right_hand_on_head


# اكتشاف وضع اليدين بشكل مستقيم إلى الأسفل
def detect_straight_down_hands(pose_landmarks):
    if not pose_landmarks:
        return False

    left_wrist = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y,
        ]
    )
    right_wrist = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y,
        ]
    )
    left_elbow = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y,
        ]
    )
    right_elbow = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y,
        ]
    )
    left_shoulder = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
        ]
    )
    right_shoulder = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
        ]
    )
    left_hip = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y,
        ]
    )
    right_hip = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y,
        ]
    )

    # حساب المسافة بين الأكتاف (كمرجع لحجم الجسم)
    shoulder_width = euclidean_distance(left_shoulder, right_shoulder)

    # حساب الزوايا بين نقاط الكوع والكتف والمعصم
    left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

    # تحديد إذا كانت اليدين مستقيمتين إلى الأسفل
    distance_threshold = 0.3 * shoulder_width  # نسبة إلى عرض الكتف لضبط الحساسية
    angle_threshold = (
        170  # الزاوية بين الذراع العلوي والسفلي يجب أن تكون قريبة من 180 درجة
    )

    # تحديد إذا كانت المعصمين عند الورك تقريباً
    min_hip_threshold = 0.2 * shoulder_width  # الحد الأدنى للمسافة من الورك
    max_hip_threshold = 0.4 * shoulder_width  # الحد الأقصى للمسافة من الورك
    left_wrist_at_hip = (
        left_hip[1] - max_hip_threshold
        < left_wrist[1]
        <= left_hip[1] + max_hip_threshold
    )
    right_wrist_at_hip = (
        right_hip[1] - max_hip_threshold
        < right_wrist[1]
        <= right_hip[1] + max_hip_threshold
    )

    left_hand_straight_down = (
        left_wrist_at_hip
        and (abs(left_wrist[0] - left_shoulder[0]) < distance_threshold)
        and (left_arm_angle > angle_threshold)
    )

    right_hand_straight_down = (
        right_wrist_at_hip
        and (abs(right_wrist[0] - right_shoulder[0]) < distance_threshold)
        and (right_arm_angle > angle_threshold)
    )

    return left_hand_straight_down and right_hand_straight_down


def detect_hands_on_waist(pose_landmarks):
    if not pose_landmarks:
        return False

    landmarks = np.array(
        [[landmark.x, landmark.y, landmark.z] for landmark in pose_landmarks.landmark]
    )

    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

    # Calculate bounding box height to normalize distances
    bbox_height = max(landmarks[:, 1]) - min(landmarks[:, 1])

    # Calculate distances and normalize by bounding box height
    right_wrist_to_right_hip = np.linalg.norm(right_wrist - right_hip) / bbox_height
    left_wrist_to_left_hip = np.linalg.norm(left_wrist - left_hip) / bbox_height

    # Calculate angles for checking elbow bend
    right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

    # Check if one or both hands are on the waist with elbows bent
    right_hand_on_waist = (
        (right_wrist_to_right_hip < 0.22)
        and (abs(right_wrist[1] - right_hip[1]) < 0.22)
        and (right_arm_angle < 160)
    )
    left_hand_on_waist = (
        (left_wrist_to_left_hip < 0.22)
        and (abs(left_wrist[1] - left_hip[1]) < 0.22)
        and (left_arm_angle < 160)
    )

    both_hands_on_waist = right_hand_on_waist and left_hand_on_waist

    return both_hands_on_waist or right_hand_on_waist or left_hand_on_waist


# Detect body leaning with sensitivity to small leans
def detect_body_lean(pose_landmarks, threshold=0.05):
    if not pose_landmarks:
        return False

    landmarks = get_landmark_array(pose_landmarks)

    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]

    # حساب ميل الكتفين والوركين
    shoulder_slope = calculate_slope(right_shoulder, left_shoulder)
    hip_slope = calculate_slope(right_hip, left_hip)

    # حساب ارتفاع المربع المحيط لتطبيع المسافات
    bbox_height = max(landmarks[:, 1]) - min(landmarks[:, 1])

    # تطبيع الميل
    shoulder_slope /= bbox_height
    hip_slope /= bbox_height

    # التحقق من ميلان الجسم
    leaning_left = (abs(shoulder_slope) > threshold or abs(hip_slope) > threshold) and (
        shoulder_slope > threshold or hip_slope > threshold
    )
    leaning_right = (
        abs(shoulder_slope) > threshold or abs(hip_slope) > threshold
    ) and (shoulder_slope < -threshold or hip_slope < -threshold)

    return leaning_left or leaning_right


# اكتشاف حركة اليدين المتقاطعتين
def detect_crossed_hands(pose_landmarks):
    if not pose_landmarks:
        return False

    left_wrist = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y,
        ]
    )

    right_wrist = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y,
        ]
    )

    left_elbow = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y,
        ]
    )

    right_elbow = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y,
        ]
    )

    left_shoulder = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
        ]
    )

    right_shoulder = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
        ]
    )

    torso_center = (left_shoulder + right_shoulder) / 2

    left_to_right_distance = np.linalg.norm(left_wrist - right_wrist)
    left_elbow_to_right_wrist = np.linalg.norm(left_elbow - right_wrist)
    right_elbow_to_left_wrist = np.linalg.norm(right_elbow - left_wrist)

    crossed_threshold = 0.2  # يمكن تعديل هذا القيم لضبط حساسية الاكتشاف

    crossed = (
        left_to_right_distance < crossed_threshold
        and left_elbow_to_right_wrist < crossed_threshold
        and right_elbow_to_left_wrist < crossed_threshold
    )

    return crossed


# اكتشاف الوقوف بشكل مستقيم (الحركة الجيدة)
def detect_standing_straight(pose_landmarks):
    if not pose_landmarks:
        return False

    left_shoulder = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
        ]
    )

    right_shoulder = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
        ]
    )

    left_hip = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y,
        ]
    )

    right_hip = np.array(
        [
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x,
            pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y,
        ]
    )

    shoulder_width = np.linalg.norm(left_shoulder - right_shoulder)
    hip_width = np.linalg.norm(left_hip - right_hip)

    straight_threshold = 0.2  # يمكن تعديل هذا القيم لضبط حساسية الاكتشاف

    straight = abs(shoulder_width - hip_width) < straight_threshold

    return straight


def detect_open_palms_with_correct_finger_order(results):
    if not results.multi_hand_landmarks or len(results.multi_hand_landmarks) < 2:
        return False

    # Initialize variables to store handedness and landmarks
    right_hand_landmarks = None
    left_hand_landmarks = None

    for hand_landmarks, handedness in zip(
        results.multi_hand_landmarks, results.multi_handedness
    ):
        if handedness.classification[0].label == "Right":
            right_hand_landmarks = hand_landmarks
        elif handedness.classification[0].label == "Left":
            left_hand_landmarks = hand_landmarks

    if not right_hand_landmarks or not left_hand_landmarks:
        return False

    # Extract necessary landmarks for right hand
    right_landmarks = right_hand_landmarks.landmark
    right_thumb_tip = right_landmarks[mp_hands.HandLandmark.THUMB_TIP]
    right_index_tip = right_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    right_middle_tip = right_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    right_ring_tip = right_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    right_pinky_tip = right_landmarks[mp_hands.HandLandmark.PINKY_TIP]
    right_wrist = right_landmarks[mp_hands.HandLandmark.WRIST]

    # Extract necessary landmarks for left hand
    left_landmarks = left_hand_landmarks.landmark
    left_thumb_tip = left_landmarks[mp_hands.HandLandmark.THUMB_TIP]
    left_index_tip = left_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    left_middle_tip = left_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    left_ring_tip = left_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    left_pinky_tip = left_landmarks[mp_hands.HandLandmark.PINKY_TIP]
    left_wrist = left_landmarks[mp_hands.HandLandmark.WRIST]

    # Check if all finger tips are below their respective wrists in the y-axis for both hands
    right_palm_facing_forward = (
        right_thumb_tip.y > right_wrist.y
        and right_index_tip.y > right_wrist.y
        and right_middle_tip.y > right_wrist.y
        and right_ring_tip.y > right_wrist.y
        and right_pinky_tip.y > right_wrist.y
    )

    left_palm_facing_forward = (
        left_thumb_tip.y > left_wrist.y
        and left_index_tip.y > left_wrist.y
        and left_middle_tip.y > left_wrist.y
        and left_ring_tip.y > left_wrist.y
        and left_pinky_tip.y > left_wrist.y
    )

    # Check if the fingers are in the correct order from right to left
    finger_positions = [
        (right_thumb_tip.x, "right_thumb"),
        (right_index_tip.x, "right_index"),
        (right_middle_tip.x, "right_middle"),
        (right_ring_tip.x, "right_ring"),
        (right_pinky_tip.x, "right_pinky"),
        (left_pinky_tip.x, "left_pinky"),
        (left_ring_tip.x, "left_ring"),
        (left_middle_tip.x, "left_middle"),
        (left_index_tip.x, "left_index"),
        (left_thumb_tip.x, "left_thumb"),
    ]

    # Sort fingers based on their x-coordinates
    finger_positions.sort()

    # Expected order of fingers
    expected_order = [
        "left_thumb",
        "left_index",
        "left_middle",
        "left_ring",
        "left_pinky",
        "right_pinky",
        "right_ring",
        "right_middle",
        "right_index",
        "right_thumb",
    ]
    actual_order = [finger[1] for finger in finger_positions]

    # print("Actual Order:", actual_order)

    return (
        right_palm_facing_forward
        and left_palm_facing_forward
        and actual_order == expected_order
    )


# Detect the specific hand gesture "Triangle Power"
def detect_triangle_power_gesture(results, image_width, image_height):
    if not results.multi_hand_landmarks or len(results.multi_hand_landmarks) < 2:
        return False

    # Initialize variables to store handedness and landmarks
    right_hand_landmarks = None
    left_hand_landmarks = None

    for hand_landmarks, handedness in zip(
        results.multi_hand_landmarks, results.multi_handedness
    ):
        if handedness.classification[0].label == "Right":
            right_hand_landmarks = hand_landmarks
        elif handedness.classification[0].label == "Left":
            left_hand_landmarks = hand_landmarks

    if not right_hand_landmarks or not left_hand_landmarks:
        return False

    # Extract necessary landmarks for right hand
    right_landmarks = right_hand_landmarks.landmark
    right_thumb_tip = right_landmarks[mp_hands.HandLandmark.THUMB_TIP]
    right_index_tip = right_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    right_middle_tip = right_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    right_ring_tip = right_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    right_pinky_tip = right_landmarks[mp_hands.HandLandmark.PINKY_TIP]
    right_wrist = right_landmarks[mp_hands.HandLandmark.WRIST]

    # Extract necessary landmarks for left hand
    left_landmarks = left_hand_landmarks.landmark
    left_thumb_tip = left_landmarks[mp_hands.HandLandmark.THUMB_TIP]
    left_index_tip = left_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    left_middle_tip = left_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    left_ring_tip = left_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    left_pinky_tip = left_landmarks[mp_hands.HandLandmark.PINKY_TIP]
    left_wrist = left_landmarks[mp_hands.HandLandmark.WRIST]

    # Calculate distances between corresponding points on both hands
    thumb_tip_distance = calc_distance(right_thumb_tip, left_thumb_tip)
    index_tip_distance = calc_distance(right_index_tip, left_index_tip)
    middle_tip_distance = calc_distance(right_middle_tip, left_middle_tip)
    ring_tip_distance = calc_distance(right_ring_tip, left_ring_tip)
    pinky_tip_distance = calc_distance(right_pinky_tip, left_pinky_tip)
    wrist_distance = calc_distance(right_wrist, left_wrist)

    # Normalize distances by image width and height
    thumb_tip_distance /= max(image_width, image_height)
    index_tip_distance /= max(image_width, image_height)
    middle_tip_distance /= max(image_width, image_height)
    ring_tip_distance /= max(image_width, image_height)
    pinky_tip_distance /= max(image_width, image_height)
    wrist_distance /= max(image_width, image_height)

    # Define the acceptable ranges for the normalized distances
    norm_distance_threshold = (
        0.1  # Adjust this value to be a percentage of the maximum image dimension
    )

    # Check if normalized distances are within the acceptable ranges
    thumbs_touching = thumb_tip_distance < norm_distance_threshold
    index_fingers_touching = index_tip_distance < norm_distance_threshold
    middle_fingers_touching = middle_tip_distance < norm_distance_threshold
    ring_fingers_touching = ring_tip_distance < norm_distance_threshold
    pinky_fingers_touching = pinky_tip_distance < norm_distance_threshold

    # Check if thumbs are behind the fingers in the z-axis (facing forward)
    right_thumb_behind_fingers = (
        right_thumb_tip.z > right_index_tip.z
        and right_thumb_tip.z > right_middle_tip.z
        and right_thumb_tip.z > right_ring_tip.z
        and right_thumb_tip.z > right_pinky_tip.z
    )

    left_thumb_behind_fingers = (
        left_thumb_tip.z > left_index_tip.z
        and left_thumb_tip.z > left_middle_tip.z
        and left_thumb_tip.z > left_ring_tip.z
        and left_thumb_tip.z > left_pinky_tip.z
    )

    # Check if fingers are on the same horizontal level (y-axis)
    fingers_same_level = (
        abs(right_index_tip.y - left_index_tip.y) < 0.05
        and abs(right_middle_tip.y - left_middle_tip.y) < 0.05
        and abs(right_ring_tip.y - left_ring_tip.y) < 0.05
        and abs(right_pinky_tip.y - left_pinky_tip.y) < 0.05
    )

    # Check if index, middle, and thumb tips form a triangle
    triangle_formed = calc_distance(right_thumb_tip, right_index_tip) > calc_distance(
        right_thumb_tip, right_middle_tip
    ) and calc_distance(left_thumb_tip, left_index_tip) > calc_distance(
        left_thumb_tip, left_middle_tip
    )

    return (
        thumbs_touching
        and index_fingers_touching
        and middle_fingers_touching
        and ring_fingers_touching
        and pinky_fingers_touching
        and right_thumb_behind_fingers
        and left_thumb_behind_fingers
        and fingers_same_level
        and triangle_formed
    )


def evaluate_session(final_score):
    if final_score <= 1:
        return "Very Poor"
    elif final_score <= 2:
        return "Poor"
    elif final_score <= 3:
        return "Fair"
    elif final_score <= 4:
        return "Good"
    else:
        return "Excellent"


def convert_durations_to_string(duration_list):
    formatted_durations = []
    for duration in duration_list:
        if isinstance(duration, tuple) and len(duration) == 2:
            start_time, end_time = duration
            formatted_durations.append(f"start {start_time} end {end_time}")
    return ", ".join(formatted_durations) if formatted_durations else "na"


# صفحة تسجيل حساب جديد
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


# صفحة تسجيل الدخول
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    user = User.query.filter_by(email=email).first()
    # print(f"{user.id}")

    if user and check_password_hash(user.password, password):
        user_details = {"id": user.id, "email": user.email}
        session["user_id"] = user.id
        return jsonify(user_details), 200
    return jsonify({"message": "Invalid credentials"}), 401


def calculate_weighted_average_all_sessions():
    # قراءة البيانات من قاعدة البيانات
    sessions = SessionReport.query.all()

    if not sessions:
        return jsonify({"average_score": 0}), 200

    # حساب المجموع والعدد الإجمالي
    total_weighted_score = sum([session.final_score for session in sessions])
    session_count = len(sessions)

    # حساب المتوسط المرجح
    average_score = total_weighted_score / session_count if session_count > 0 else 0

    # الحصول على أسماء الفيديوهات والتقييمات
    video_details = []
    for session in sessions:
        video = Video.query.get(session.video_id)
        video_details.append(
            {
                "video_name": video.video_name,
                "evaluation": session.evaluation,
                "final_score": session.final_score,
            }
        )

    result = {"average_score": average_score, "video_details": video_details}

    return jsonify(result), 200


@app.route("/average_score", methods=["GET"])
def get_average_score():
    return calculate_weighted_average_all_sessions()


@app.route("/videos", methods=["GET"])
# @app.route("/videos", methods=["GET"])
def get_videos():
    user_id = request.headers.get("User-ID")
    print(f"Session user_id: {user_id}")  # Debugging line

    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    videos = Video.query.filter_by(user_id=user_id).all()
    videos_list = [
        {
            "user_id": user_id,
            "id": v.id,
            "video_name": v.video_name,
            "recorded_at": v.recorded_at,
            "score": v.score,
        }
        for v in videos
    ]

    return jsonify(videos_list), 200


# last video report
@app.route("/video/latest", methods=["GET"])
def get_latest_video():
    user_id = request.headers.get("User-ID")
    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    # Query to get the latest video for the user
    latest_video = (
        Video.query.filter_by(user_id=user_id)
        .order_by(Video.recorded_at.desc())
        .first()
    )

    if not latest_video:
        return jsonify({"message": "No videos found"}), 404

    video_details = {
        "id": latest_video.id,
        "video_name": latest_video.video_name,
        "recorded_at": latest_video.recorded_at,
        "score": latest_video.score,
    }

    return jsonify(video_details), 200


# عرض تفاصيل الفيديو
@app.route("/video/<int:video_id>", methods=["GET"])
def get_video(video_id):
    user_id = request.headers.get("User-ID")
    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    video = Video.query.filter_by(id=video_id, user_id=user_id).first()
    if not video:
        return jsonify({"message": "Video not found"}), 404

    video_details = {
        "id": video.id,
        "video_name": video.video_name,
        "recorded_at": video.recorded_at,
        "score": video.score,
    }

    return jsonify(video_details), 200


@app.route("/report/<int:video_id>", methods=["GET"])
def get_report(video_id):
    user_id = request.headers.get("User-ID")
    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    report = SessionReport.query.filter_by(video_id=video_id).first()
    if not report:
        return jsonify({"message": "Report not found"}), 404

    report_details = {
        "id": report.id,
        "video_id": report.video_id,
        "start_time": report.start_time,
        "end_time": report.end_time,
        "final_score": report.final_score,
        "hand_crossed": report.hand_crossed,
        "hand_on_waist": report.hand_on_waist,
        "hand_on_head": report.hand_on_head,
        "hand_straight_down": report.hand_straight_down,
        "standing_straight": report.standing_straight,
        "body_lean": report.body_lean,
        "open_palms_forward": report.open_palms_forward,
        "triangle_power": report.triangle_power,
        "evaluation": report.evaluation,
        "positive_tips": report.positive_tips,
        "negative_tips": report.negative_tips,
        # إحصائيات الحركات
        "hand_crossed_percentage": report.hand_crossed_percentage,
        "hand_on_waist_percentage": report.hand_on_waist_percentage,
        "hand_on_head_percentage": report.hand_on_head_percentage,
        "hand_straight_down_percentage": report.hand_straight_down_percentage,
        "standing_straight_percentage": report.standing_straight_percentage,
        "body_lean_percentage": report.body_lean_percentage,
        "open_palms_forward_percentage": report.open_palms_forward_percentage,
        "triangle_power_percentage": report.triangle_power_percentage,
        "audio_data": report.audio_result
    }

    return jsonify(report_details), 200


# audio start code
# model = pickle.load(open("mlp_classifier.model", "rb"))
audio_frames = []
BUFFER_DURATION = 5  # seconds (adjust according to your needs)
RATE = 16000
THRESHOLD = 500


@app.route("/")
def index():
    return "Socket.IO Flask Server"


def extract_feature(file_name, **kwargs):
    """
    Extract feature from audio file `file_name`
        Features supported:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
        e.g:
        `features = extract_feature(path, mel=True, mfcc=True)`
    """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(
                librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0
            )
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(
                librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0
            )
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)

            result = np.hstack((result, mel))
        if contrast:
            contrast = np.mean(
                librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0
            )
            result = np.hstack((result, contrast))
        if tonnetz:
            tonnetz = np.mean(
                librosa.feature.tonnetz(
                    y=librosa.effects.harmonic(X), sr=sample_rate
                ).T,
                axis=0,
            )
            result = np.hstack((result, tonnetz))
    return result


recording_flag = True
THRESHOLD = 500
CHUNK_SIZE = 1024  # Adjust chunk size if needed
RECORD_SECONDS = 30  # Total recording duration
FORMAT = pyaudio.paInt16
RATE = 16000
MODEL = pickle.load(open("mlp_classifier.model", "rb"))
SILENCE = 30


def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)

    r = array("h")
    for i in snd_data:
        r.append(int(i * times))
    return r


def trim(snd_data):
    "Trim the blank spots at the start and end"

    def _trim(snd_data):
        snd_started = False
        r = array("h")

        for i in snd_data:
            if not snd_started and abs(i) > THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data


def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array("h", [0 for i in range(int(seconds * RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds * RATE))])
    return r


def record():
    global recording_flag
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=1,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    r = array("h")

    while recording_flag:
        snd_data = array("h", stream.read(CHUNK_SIZE))
        if byteorder == "big":
            snd_data.byteswap()
        r.extend(snd_data)

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r


advice = {
    "angry": "It's important to channel your passion into your speech, but try not to let anger take over. Take a few deep breaths and try to calm down before continuing. Remember, you want to persuade your audience, not alienate them.",
    "sad": "It's okay to show vulnerability in your speech, but don't let sadness dominate. Try to bring in some positive or hopeful elements to balance it out. Remember, your audience will likely mirror your emotions.",
    "calm": "You're doing great! A calm demeanor can help your audience focus on your message. Just make sure you're also showing enthusiasm where appropriate to keep your audience engaged.",
    "happy": "Your positive energy is infectious and can help engage your audience. Just make sure your happiness is appropriate for the topic of your speech.",
    "fearful": "It's natural to feel nervous, especially when speaking in public. Try to take some deep breaths and slow down your speech. Remember, it's okay to take a few moments to collect your thoughts.",
    "motivation": "You're doing an excellent job! Your improvement is clearly noticeable. Keep practicing and challenging yourself, and remember that every great speaker was once a beginner. Keep up the good work!",
}


def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack("<" + ("h" * len(data)), *data)

    wf = wave.open(path, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


all_chunks = []
emotion_count = {emotion: 0 for emotion in MODEL.classes_}  # Initialize emotion count


@socketio.on("start_recording")
def start_recording():
    global recording_flag, all_chunks
    recording_flag = True
    all_chunks = []  # Reset chunks
    emotion_count = {emotion: 0 for emotion in MODEL.classes_}  # Reset emotion count
    print("Recording started")
    socketio.emit("audio_status", {"status": "Recording started"})

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=1,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    chunk_count = 0
    total_chunks = int(RATE / CHUNK_SIZE * RECORD_SECONDS)

    try:
        while recording_flag:
            accumulated_data = []
            print("Recording chunk...")
            for _ in range(total_chunks):
                snd_data = array("h", stream.read(CHUNK_SIZE))
                if byteorder == "big":
                    snd_data.byteswap()
                accumulated_data.extend(snd_data)
                if not recording_flag:
                    break

            all_chunks.extend(accumulated_data)
            filename = "temp_chunk.wav"
            save_audio(filename, accumulated_data, p.get_sample_size(FORMAT))
            process_audio(filename)

    except Exception as e:
        print(f"Error processing audio: {e}")
        socketio.emit("server_message", {"message": "Error processing audio."})

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Recording stopped")
        socketio.emit("audio_status", {"status": "Recording stopped"})


@socketio.on("stop_recording")
def stop_recording():
    #######  for audio handling #######
    global recording_flag
    recording_flag = False
    print("Stop audio received")

    # # Save all accumulated chunks to a single audio file
    # if all_chunks:
    #     filename = "full_recording.wav"
    #     save_audio(filename, all_chunks, pyaudio.PyAudio().get_sample_size(FORMAT))
    #     print(f"Full recording saved as {filename}")
    # # Calculate the percentage of each detected emotion
    # total_emotions = sum(emotion_count.values())
    # emotion_percentage = {
    #     emotion: (count / total_emotions) * 100 if total_emotions > 0 else 0
    #     for emotion, count in emotion_count.items()
    # }
    # audio_result = "good"

    # # Access the global session_data
    # global session_data

    # # Add or update the audio_result in session_data
    # session_data["audio_data"] = audio_result
    # print(f"Emotion percentages: {emotion_percentage}")


def save_audio(path, data, sample_width):
    """Save the accumulated audio data to a file."""
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(pack("<" + ("h" * len(data)), *data))


def process_audio(filename):
    """Process the audio file and emit the result."""
    global emotion_count  # Access the global emotion_count dictionary
    try:
        # Load and preprocess the audio file
        features = extract_feature(filename, mfcc=True, chroma=True, mel=True).reshape(
            1, -1
        )

        # Predict emotion
        result = MODEL.predict(features)[0]

        emotion_count[result] += 1
        # Prepare the response
        response = {
            "emotion": result,
            "advice": advice.get(result, "No advice available for this emotion."),
        }
        print(f"{response}")
        # Emit the result to the client
        socketio.emit(
            "audio_message",
            {"message": advice.get(result, "No advice available for this emotion.")},
        )
    except Exception as e:
        print(f"Error processing audio: {e}")
        socketio.emit("server_message", {"message": "Error processing audio."})


# @socketio.on("start_video_recording")
# def start_video(id):

#     print(f"{id}")

session_data = {}


@socketio.on("start_video_recording")
def start_video(id):
    print(f"{id}")
    user_id = id

    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    # استرداد عدد الفيديوهات المسجلة للمستخدم
    video_count = Video.query.filter_by(user_id=user_id).count()

    # تسمية الفيديو الجديد بناءً على عدد الفيديوهات
    video_name = f"output_{uuid.uuid4().hex}.avi"

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(video_name, fourcc, 20.0, (640, 480))

    current_score = 0

    # إعداد متغيرات التقييم
    weights = {
        "HAND_CROSSED": 1,
        "HAND_ON_WAIST": 2,
        "HAND_ON_HEAD": 1,
        "HAND_STRAIGHT_DOWN": 1,
        "STANDING_STRAIGHT": 3,
        "BODY_LEAN": 2,
        "OPEN_PALMS_FORWARD": 2,
        "TRIANGLE_POWER": 3,
    }

    movement_start_times = {
        "HAND_ON_HEAD": None,
        "HAND_STRAIGHT_DOWN": None,
        "HAND_ON_WAIST": None,
        "HAND_CROSSED": None,
        "STANDING_STRAIGHT": None,
        "BODY_LEAN": None,
        "OPEN_PALMS_FORWARD": None,
        "TRIANGLE_POWER": None,
    }

    movement_end_times = {
        "HAND_ON_HEAD": None,
        "HAND_STRAIGHT_DOWN": None,
        "HAND_ON_WAIST": None,
        "HAND_CROSSED": None,
        "STANDING_STRAIGHT": None,
        "BODY_LEAN": None,
        "OPEN_PALMS_FORWARD": None,
        "TRIANGLE_POWER": None,
    }

    movement_times = {
        "HAND_ON_HEAD": [],
        "HAND_STRAIGHT_DOWN": [],
        "HAND_ON_WAIST": [],
        "HAND_CROSSED": [],
        "STANDING_STRAIGHT": [],
        "BODY_LEAN": [],
        "OPEN_PALMS_FORWARD": [],
        "TRIANGLE_POWER": [],
    }

    expert_system_statements = []
    time_points = []
    performance_scores = []
    movement_history = []

    weighted_sum = 0
    total_weight = 0

    plt.ion()
    plt.figure()

    start_time = time.time()
    last_time = start_time
    duration_limit = 15 * 60  # 10 دقائق بالثواني

    start_time_all = datetime.datetime.now()
    # إنشاء النظام الخبير
    engine = PoseExpertSystem()
    engine.reset()
    # Buffer to hold the last N detection results
    buffer_size = 10
    detection_buffer = deque(maxlen=buffer_size)

    # Buffer to hold the last N detection results
    buffer_size_w = 10
    detection_buffer_w = deque(maxlen=buffer_size_w)

    # Buffer for detecting body lean over time
    body_lean_buffer = []
    body_lean_threshold = 30  # Number of frames to confirm body lean

    def is_movement_detected(movement_name):
        return movement_start_times[movement_name] is not None

    def update_movement(movement, video_time_formatted):
        if movement_start_times[movement] is None:
            movement_start_times[movement] = video_time_formatted
        elif movement_end_times[movement] is None:
            movement_end_times[movement] = video_time_formatted
            movement_times[movement].append(
                (movement_start_times[movement], movement_end_times[movement])
            )
            # إعادة تعيين أوقات البداية والنهاية بعد تسجيلها
            movement_start_times[movement] = None
            movement_end_times[movement] = None

    # Function to check if a movement has stopped
    def movement_has_stopped(movement, detection_flag, grace_period=0.5):
        return (
            not detection_flag
            and is_movement_detected(movement)
            and (time.time() - start_time) - last_time >= grace_period
        )

    # Buffer to hold the last N detection results for each movement
    buffer_size = 10
    movement_buffers = {
        "HAND_CROSSED": deque(maxlen=buffer_size),
        "HAND_ON_WAIST": deque(maxlen=buffer_size),
        "HAND_ON_HEAD": deque(maxlen=buffer_size),
        "HAND_STRAIGHT_DOWN": deque(maxlen=buffer_size),
        "BODY_LEAN": deque(maxlen=buffer_size),
        "OPEN_PALMS_FORWARD": deque(maxlen=buffer_size),
        "TRIANGLE_POWER": deque(maxlen=buffer_size),
    }

    def apply_moving_average(buffer):
        return sum(buffer) / len(buffer) if len(buffer) > 0 else 0

    with mp_pose.Pose(
        min_detection_confidence=0.8, min_tracking_confidence=0.8
    ) as pose, mp_hands.Hands(
        min_detection_confidence=0.8, min_tracking_confidence=0.8
    ) as hands:
        while cap.isOpened() and recording_flag:
            ret, frame = cap.read()
            if not ret:
                break

            frame = apply_clahe(frame)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results_pose = pose.process(image)
            results_hands = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # تعريف المتغيرات خارج الشرط
            hand_on_head = False
            straight_down_hands = False
            hand_on_waist = False
            crossed_hands = False
            standing_straight = False
            body_lean = False
            open_palm_fw = False
            triangle_power_gesture = False

            if results_pose.pose_landmarks or results_hands.multi_hand_landmarks:
                current_time = time.time() - start_time
                elapsed_time = current_time - last_time
                video_time_formatted = str(datetime.timedelta(seconds=current_time))

                if detect_hand_on_head(results_pose.pose_landmarks):
                    hand_on_head = True
                if detect_crossed_hands(results_pose.pose_landmarks):
                    crossed_hands = True
                # if detect_standing_straight(results_pose.pose_landmarks):
                #     standing_straight = True
                if detect_body_lean(results_pose.pose_landmarks):
                    body_lean = True
                if detect_open_palms_with_correct_finger_order(results_hands):
                    open_palm_fw = True
                if detect_triangle_power_gesture(
                    results_hands, frame.shape[1], frame.shape[0]
                ):
                    triangle_power_gesture = True
                if detect_hands_on_waist(results_pose.pose_landmarks):
                    hand_on_waist = True
                if detect_straight_down_hands(results_pose.pose_landmarks):
                    straight_down_hands = True

                engine.declare(
                    PoseFact(
                        hand_on_head=hand_on_head,
                        straight_down_hands=straight_down_hands,
                        hand_on_waist=hand_on_waist,
                        crossed_hands=crossed_hands,
                        # standing_straight=standing_straight,
                        body_lean=body_lean,
                        open_palm_fw=open_palm_fw,
                        triangle_power_gesture=triangle_power_gesture,
                    )
                )

                engine.run()

                previous_score = current_score

                # Update buffers and calculate moving averages
                movement_buffers["HAND_ON_HEAD"].append(hand_on_head)
                movement_buffers["HAND_CROSSED"].append(crossed_hands)
                movement_buffers["HAND_ON_WAIST"].append(hand_on_waist)
                movement_buffers["HAND_STRAIGHT_DOWN"].append(straight_down_hands)
                movement_buffers["BODY_LEAN"].append(body_lean)
                movement_buffers["OPEN_PALMS_FORWARD"].append(open_palm_fw)
                movement_buffers["TRIANGLE_POWER"].append(triangle_power_gesture)

                hand_on_head_avg = apply_moving_average(
                    movement_buffers["HAND_ON_HEAD"]
                )
                crossed_hands_avg = apply_moving_average(
                    movement_buffers["HAND_CROSSED"]
                )
                hand_on_waist_avg = apply_moving_average(
                    movement_buffers["HAND_ON_WAIST"]
                )
                straight_down_hands_avg = apply_moving_average(
                    movement_buffers["HAND_STRAIGHT_DOWN"]
                )
                body_lean_avg = apply_moving_average(movement_buffers["BODY_LEAN"])
                open_palm_fw_avg = apply_moving_average(
                    movement_buffers["OPEN_PALMS_FORWARD"]
                )
                triangle_power_gesture_avg = apply_moving_average(
                    movement_buffers["TRIANGLE_POWER"]
                )

                if crossed_hands_avg > 0.5:
                    standing_straight = False
                    hand_on_waist = False
                    current_score -= weights["HAND_CROSSED"]
                    movement_history.append("HAND_CROSSED")
                    update_movement("HAND_CROSSED", video_time_formatted)
                    expert_system_statements.append((elapsed_time, "Hand crossed"))
                    cv2.putText(
                        image,
                        "Hand crossed",
                        (10, 170),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA,
                    )

                if hand_on_waist_avg > 0.5 and not crossed_hands:
                    standing_straight = False
                    detection_buffer_w.append(hand_on_waist)
                    if detection_buffer_w:
                        most_common_detection_w = max(
                            set(detection_buffer_w), key=detection_buffer_w.count
                        )
                    most_common_detection_wstr = str(most_common_detection_w)
                    current_score -= weights["HAND_ON_WAIST"]
                    movement_history.append("HAND_ON_WAIST")
                    update_movement("HAND_ON_WAIST", video_time_formatted)
                    expert_system_statements.append((elapsed_time, "Hand on waist"))
                    cv2.putText(
                        image,
                        "Hand on waist",
                        (10, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA,
                    )

                if hand_on_head_avg > 0.5:
                    standing_straight = False
                    current_score -= weights["HAND_ON_HEAD"]
                    movement_history.append("HAND_ON_HEAD")
                    update_movement("HAND_ON_HEAD", video_time_formatted)
                    expert_system_statements.append((elapsed_time, "Hand on head"))
                    cv2.putText(
                        image,
                        "Hand on head",
                        (10, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA,
                    )

                if straight_down_hands_avg > 0.5:
                    standing_straight = False
                    current_score += weights["HAND_STRAIGHT_DOWN"]
                    movement_history.append("HAND_STRAIGHT_DOWN")
                    update_movement("HAND_STRAIGHT_DOWN", video_time_formatted)
                    expert_system_statements.append(
                        (elapsed_time, "Hand straight down")
                    )
                    cv2.putText(
                        image,
                        "Hand straight down",
                        (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )

                # Buffering for body lean
                if body_lean_avg > 0.5:
                    body_lean_buffer.append(body_lean)
                    if len(body_lean_buffer) > body_lean_threshold:
                        body_lean_buffer.pop(0)
                    if len(body_lean_buffer) == body_lean_threshold and all(
                        body_lean_buffer
                    ):
                        standing_straight = False
                        current_score -= weights["BODY_LEAN"]
                        movement_history.append("BODY_LEAN")
                        update_movement("BODY_LEAN", video_time_formatted)
                        expert_system_statements.append((elapsed_time, "Body lean"))
                        cv2.putText(
                            image,
                            "Body lean",
                            (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2,
                            cv2.LINE_AA,
                        )
                else:
                    body_lean_buffer.clear()

                if open_palm_fw_avg > 0.5:
                    current_score += weights["OPEN_PALMS_FORWARD"]
                    movement_history.append("OPEN_PALMS_FORWARD")
                    update_movement("OPEN_PALMS_FORWARD", video_time_formatted)
                    expert_system_statements.append(
                        (elapsed_time, "Open palms forward")
                    )
                    cv2.putText(
                        image,
                        "Both Palms Facing Forward with Correct Finger Order",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )

                if triangle_power_gesture_avg > 0.5 and not standing_straight:
                    if current_time <= 300:
                        current_score += weights["TRIANGLE_POWER"]
                    else:
                        current_score -= weights["TRIANGLE_POWER"]
                    movement_history.append("TRIANGLE_POWER")
                    update_movement("TRIANGLE_POWER", video_time_formatted)
                    expert_system_statements.append(
                        (elapsed_time, "Triangle Power Gesture")
                    )
                    cv2.putText(
                        image,
                        "TRIANGLE_POWER",
                        (50, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )

                if current_score != previous_score:
                    time_points.append(current_time)
                    performance_scores.append(current_score)
                    # update_performance_plot(time_points, performance_scores)
                    socketio.emit('performance_update', { "score": current_score, "time": current_time })

                performance_score_final = (
                    weights["HAND_ON_HEAD"] * hand_on_head_avg
                    + weights["HAND_STRAIGHT_DOWN"] * straight_down_hands_avg
                    + weights["HAND_ON_WAIST"] * hand_on_waist_avg
                    + weights["HAND_CROSSED"] * crossed_hands_avg
                    + weights["BODY_LEAN"] * body_lean_avg
                    + weights["OPEN_PALMS_FORWARD"] * open_palm_fw_avg
                    + weights["TRIANGLE_POWER"]
                    * (1 if triangle_power_gesture_avg and current_time <= 300 else -1)
                )

                weighted_sum += performance_score_final * elapsed_time
                total_weight += elapsed_time
                average_weighted_score = (
                    weighted_sum / total_weight if total_weight != 0 else 0
                )

            if results_hands.multi_hand_landmarks:
                for hand_landmarks in results_hands.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

            if results_pose.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image, results_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS
                )

            out.write(image)
            cv2.imshow("Live Video", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    out.release()

    def calculate_weighted_average(time_points, performance_scores):
        if len(time_points) < 2:
            return (
                0  # لا يمكن حساب المتوسط الموزون إذا كان هناك نقطة زمنية واحدة أو أقل
            )

        weighted_sum = 0
        total_weight = 0

        for i in range(1, len(time_points)):
            time_interval = time_points[i] - time_points[i - 1]
            weighted_sum += performance_scores[i] * time_interval
            total_weight += time_interval

        weighted_average = weighted_sum / total_weight if total_weight != 0 else 0
        return weighted_average

    # حساب المتوسط الموزون بعد انتهاء الفيديو
    average_weighted_score = calculate_weighted_average(time_points, performance_scores)
    print("Weighted Average Performance Score:", average_weighted_score)

    # أعلى وأقل قيمة للمتوسط الموزون لفيديو مدته 15 دقيقة
    max_score = 3683.827913548159
    min_score = -2451.8276908782093

    def normalize_score(score, min_score, max_score):
        if score == 0:
            return 0
        return ((score - min_score) / (max_score - min_score)) * 5

    normalize_score_avg = normalize_score(average_weighted_score, min_score, max_score)

    new_video = Video(user_id=user_id, video_name=video_name, score=normalize_score_avg)
    db.session.add(new_video)
    db.session.commit()

    # حساب إحصائيات كل حركة
    movement_counts = {
        movement: movement_history.count(movement) for movement in weights.keys()
    }
    total_movement_count = sum(movement_counts.values())
    movement_percentages = {
        movement: (
            (count / total_movement_count * 100) if total_movement_count > 0 else 0
        )
        for movement, count in movement_counts.items()
    }

    evaluation = evaluate_session(normalize_score_avg)
    end_time_all = datetime.datetime.now()

    movement_history_set = set(movement_history)

    # تحديد النصائح الإيجابية والسلبية
    positive_tips = []
    negative_tips = []

    # نصائح إيجابية
    if "STANDING_STRAIGHT" in movement_history_set:
        positive_tips.append("Good posture! Keep standing straight")
    if "HAND_STRAIGHT_DOWN" in movement_history_set:
        positive_tips.append("Good motion! Keep hand straight down")
    if "OPEN_PALMS_FORWARD" in movement_history_set:
        positive_tips.append("Good motion! Open palms forward")
    if "TRIANGLE_POWER" in movement_history_set:
        positive_tips.append("Good motion! Perform triangle power")

    # نصائح سلبية
    if "HAND_CROSSED" in movement_history_set:
        negative_tips.append("Hand crossed")
    if "BODY_LEAN" in movement_history_set:
        negative_tips.append("Body lean")
    if "HAND_ON_HEAD" in movement_history_set:
        negative_tips.append(" hand on head")
    if "HAND_ON_WAIST" in movement_history_set:
        negative_tips.append("Hand on waist")
    # save audio when stop
    print("Stop audio received")

    # Save all accumulated chunks to a single audio file
    if all_chunks:
        filename = "full_recording.wav"
        save_audio(filename, all_chunks, pyaudio.PyAudio().get_sample_size(FORMAT))
        print(f"Full recording saved as {filename}")
    # Calculate the percentage of each detected emotion
    total_emotions = sum(emotion_count.values())
    emotion_percentage = {
        emotion: (count / total_emotions) * 100 if total_emotions > 0 else 0
        for emotion, count in emotion_count.items()
    }
    audio_result = "good"
    # Add or update the audio_result in session_data
    print(f"Emotion percentages: {emotion_percentage}")
    session_data = {
        "start_time": start_time_all.strftime("%m/%d/%Y %I:%M:%S %p"),
        "end_time": end_time_all.strftime("%m/%d/%Y %I:%M:%S %p"),
        "final_score": normalize_score_avg,
        "HAND_CROSSED": convert_durations_to_string(
            movement_times.get("HAND_CROSSED", [])
        ),
        "HAND_ON_WAIST": convert_durations_to_string(
            movement_times.get("HAND_ON_WAIST", [])
        ),
        "HAND_ON_HEAD": convert_durations_to_string(
            movement_times.get("HAND_ON_HEAD", [])
        ),
        "HAND_STRAIGHT_DOWN": convert_durations_to_string(
            movement_times.get("HAND_STRAIGHT_DOWN", [])
        ),
        "STANDING_STRAIGHT": convert_durations_to_string(
            movement_times.get("STANDING_STRAIGHT", [])
        ),
        "BODY_LEAN": convert_durations_to_string(movement_times.get("BODY_LEAN", [])),
        "OPEN_PALMS_FORWARD": convert_durations_to_string(
            movement_times.get("OPEN_PALMS_FORWARD", [])
        ),
        "TRIANGLE_POWER": convert_durations_to_string(
            movement_times.get("TRIANGLE_POWER", [])
        ),
        "evaluation": evaluation,
        "positive_tips": "\n".join(positive_tips),
        "negative_tips": "\n".join(negative_tips),
        # إحصائيات الحركات
        "hand_crossed_percentage": movement_percentages.get("HAND_CROSSED", 0),
        "hand_on_waist_percentage": movement_percentages.get("HAND_ON_WAIST", 0),
        "hand_on_head_percentage": movement_percentages.get("HAND_ON_HEAD", 0),
        "hand_straight_down_percentage": movement_percentages.get(
            "HAND_STRAIGHT_DOWN", 0
        ),
        "standing_straight_percentage": movement_percentages.get(
            "STANDING_STRAIGHT", 0
        ),
        "body_lean_percentage": movement_percentages.get("BODY_LEAN", 0),
        "open_palms_forward_percentage": movement_percentages.get(
            "OPEN_PALMS_FORWARD", 0
        ),
        "triangle_power_percentage": movement_percentages.get("TRIANGLE_POWER", 0),
        "audio_data": audio_result,
    }

    # حفظ التقرير في قاعدة البيانات
    video = Video.query.filter_by(user_id=user_id, video_name=video_name).first()
    if not video:
        return jsonify({"message": "Video not found"}), 404
    # print(session_data["audio_data"])
    print(f"{session_data}")
    report = SessionReport(
        video_id=video.id,
        start_time=session_data["start_time"],
        end_time=session_data["end_time"],
        final_score=session_data["final_score"],
        hand_crossed=session_data["HAND_CROSSED"],
        hand_on_waist=session_data["HAND_ON_WAIST"],
        hand_on_head=session_data["HAND_ON_HEAD"],
        hand_straight_down=session_data["HAND_STRAIGHT_DOWN"],
        standing_straight=session_data["STANDING_STRAIGHT"],
        body_lean=session_data["BODY_LEAN"],
        open_palms_forward=session_data["OPEN_PALMS_FORWARD"],
        triangle_power=session_data["TRIANGLE_POWER"],
        evaluation=session_data["evaluation"],
        positive_tips=session_data["positive_tips"],
        negative_tips=session_data["negative_tips"],
        hand_crossed_percentage=session_data["hand_crossed_percentage"],
        hand_on_waist_percentage=session_data["hand_on_waist_percentage"],
        hand_on_head_percentage=session_data["hand_on_head_percentage"],
        hand_straight_down_percentage=session_data["hand_straight_down_percentage"],
        standing_straight_percentage=session_data["standing_straight_percentage"],
        body_lean_percentage=session_data["body_lean_percentage"],
        open_palms_forward_percentage=session_data["open_palms_forward_percentage"],
        triangle_power_percentage=session_data["triangle_power_percentage"],
        audio_result=session_data["audio_data"],
    )

    db.session.add(report)
    db.session.commit()
    socketio.emit(
        "server_message",
        {
            "message": "Video and report recorded and saved",
            "video_id": new_video.id,
            "report_id": report.id,
        },
    )
    # return jsonify({'message': 'Video and report recorded and saved', 'video_id': new_video.id, 'report_id': report.id}), 200


@socketio.on("connect")
def handle_connect():
    print("connect called")
    socketio.emit(
        "server_message", {"message": "Welcome! You are connected to the server."}
    )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)
