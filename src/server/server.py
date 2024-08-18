####################
# server.py
from flask import Flask
from flask_socketio import SocketIO
import cv2
import base64
import numpy as np
import mediapipe as mp
from experta import KnowledgeEngine, Fact, Rule
import matplotlib.pyplot as plt
import time
import datetime
from collections import deque


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


class PoseFact(Fact):
    """Info about the detected pose."""

    pass


class PoseExpertSystem(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.advice = None

    def set_advice(self, movement_name, advice):
        self.advice = {"movement": movement_name, "advice": advice}

    @Rule(PoseFact(hand_on_head=True))
    def hand_on_head(self):
        self.declare(PoseFact(standing_straight=False))
        self.set_advice(
            "Hand on Head",
            "Placing your hand on your head while speaking can be perceived as a sign of stress, confusion, or deep thought. Try to maintain a relaxed posture with your hands by your sides or gesturing naturally to emphasize your points. Remember, ‘Your body speaks as loudly as your words.’",
        )

    @Rule(PoseFact(straight_down_hands=True))
    def straight_down_hands(self):
        self.declare(PoseFact(standing_straight=False))
        self.set_advice(
            "Hands Straight Down",
            "This gesture reflects confidence and stability. It conveys calmness and control, and helps in presenting a professional and reliable image. Continue with this style, as it adds great value to your communication style.",
        )

    @Rule(PoseFact(hand_in_pocket=True))
    def hand_in_pocket(self):
        self.set_advice(
            "Hand in Pocket",
            "You tend to put your hand in your pocket while speaking. This gesture can be a sign of ambiguity or withdrawal. Don’t rely on it continuously, and remember, ‘confidence and openness are the key to effective communication.’",
        )

    @Rule(PoseFact(crossed_hands=True))
    def crossed_hands(self):
        self.declare(PoseFact(standing_straight=False))
        self.declare(PoseFact(hand_on_waist=False))
        self.set_advice(
            "Crossed Hands",
            "I notice that you often cross your forearms while speaking. This gesture may indicate defensiveness or closure. I would like to suggest some tips that might help you: Try to adopt an open posture while speaking. You can place your hands on your sides or on your knees in an uncrossed manner. This can help project a more open and confident image. Try to look directly at the audience. This can increase confidence and reduce the need for crossing your arms.",
        )

    @Rule(PoseFact(standing_straight=True))
    def standing_straight(self):
        self.declare(PoseFact(body_lean=False))
        self.set_advice(
            "Standing Straight",
            "Maintaining a straight posture while speaking is a powerful cue. It conveys confidence and authority. Remember, ‘Stand tall and let your presence be felt.’",
        )

    @Rule(PoseFact(hand_on_waist=True, crossed_hands=False))
    def hand_on_waist(self):
        self.declare(PoseFact(standing_straight=False))
        self.set_advice(
            "Hand on Waist",
            "Putting your hand on the waist while talking can be explained by a challenge or loss of patience. Remember, 'Stand up straight and let your presence feel.’",
        )

    @Rule(PoseFact(body_lean=True))
    def body_lean(self):
        self.declare(PoseFact(standing_straight=False))
        self.set_advice(
            "Body Lean",
            "Remember, bending over while talking may be a sign of distrust or relying on something for support. Try to maintain a straight and steady posture while speaking. This reflects confidence and stability. But, don't forget to be natural and comfortable to reflect confidence and professionalism.",
        )

    @Rule(PoseFact(open_palm_fw=True))
    def open_palm_fw(self):
        self.set_advice(
            "Open Palms Forward",
            "You tend to use 'OPEN_PALMS_FORWARD' movement while speaking, this movement expresses openness, honesty and willingness to communicate. But, remember, it's a good idea to use this movement in a balanced and contextual way.",
        )

    @Rule(PoseFact(triangle_power_gesture=True))
    def triangle_power_gesture(self):
        self.declare(PoseFact(standing_straight=False))
        self.set_advice(
            "Triangle Power Gesture",
            "Most people use the 'Triangle Power Gesture' movement to show authority and control. But you need to use them with caution: excessive use of this movement may make you look domineering or aggressive. Use them in key moments to emphasize a certain point or to introduce oneself.",
        )


engine = PoseExpertSystem()

# إعداد Mediapipe
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
hands = mp_hands.Hands(
    static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8
)


def update_performance_plot(time_points, performance_scores):
    plt.clf()
    plt.plot(
        time_points,
        performance_scores,
        marker="o",
        linestyle="-",
        color="b",
        label="Performance",
    )
    plt.xlabel("Time")
    plt.ylabel("Performance Score")
    plt.title("Real-Time Performance Tracking")
    plt.legend()
    plt.grid(True)
    plt.pause(0.001)


# Function to enhance lighting using CLAHE
def apply_clahe(image):
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    yuv[:, :, 0] = clahe.apply(yuv[:, :, 0])
    return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)


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

    if not results.multi_hand_landmarks or len(results.multi_hand_landmarks) < 2:
        return False

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

    right_landmarks = right_hand_landmarks.landmark
    right_thumb_tip = right_landmarks[mp_hands.HandLandmark.THUMB_TIP]
    right_index_tip = right_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    right_middle_tip = right_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    right_ring_tip = right_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    right_pinky_tip = right_landmarks[mp_hands.HandLandmark.PINKY_TIP]
    right_wrist = right_landmarks[mp_hands.HandLandmark.WRIST]

    left_landmarks = left_hand_landmarks.landmark
    left_thumb_tip = left_landmarks[mp_hands.HandLandmark.THUMB_TIP]
    left_index_tip = left_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    left_middle_tip = left_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    left_ring_tip = left_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    left_pinky_tip = left_landmarks[mp_hands.HandLandmark.PINKY_TIP]
    left_wrist = left_landmarks[mp_hands.HandLandmark.WRIST]

    thumb_tip_distance = calc_distance(right_thumb_tip, left_thumb_tip)
    index_tip_distance = calc_distance(right_index_tip, left_index_tip)
    middle_tip_distance = calc_distance(right_middle_tip, left_middle_tip)
    ring_tip_distance = calc_distance(right_ring_tip, left_ring_tip)
    pinky_tip_distance = calc_distance(right_pinky_tip, left_pinky_tip)
    wrist_distance = calc_distance(right_wrist, left_wrist)

    thumb_tip_distance /= max(image_width, image_height)
    index_tip_distance /= max(image_width, image_height)
    middle_tip_distance /= max(image_width, image_height)
    ring_tip_distance /= max(image_width, image_height)
    pinky_tip_distance /= max(image_width, image_height)
    wrist_distance /= max(image_width, image_height)

    norm_distance_threshold = 0.1

    thumbs_touching = thumb_tip_distance < norm_distance_threshold
    index_fingers_touching = index_tip_distance < norm_distance_threshold
    middle_fingers_touching = middle_tip_distance < norm_distance_threshold
    ring_fingers_touching = ring_tip_distance < norm_distance_threshold
    pinky_fingers_touching = pinky_tip_distance < norm_distance_threshold

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

    fingers_same_level = (
        abs(right_index_tip.y - left_index_tip.y) < 0.05
        and abs(right_middle_tip.y - left_middle_tip.y) < 0.05
        and abs(right_ring_tip.y - left_ring_tip.y) < 0.05
        and abs(right_pinky_tip.y - left_pinky_tip.y) < 0.05
    )

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


##########################################################


# Route for server status
@app.route("/")
def index():
    return "Server is running"


# Buffer for detecting body lean over time
body_lean_buffer = []
body_lean_threshold = 30  # Number of frames to confirm body lean

start_time = time.time()
last_time = start_time
duration_limit = 15 * 60  # 10 دقائق بالثواني
start_time_all = datetime.datetime.now()


expert_system_statements = []

time_points = []
performance_scores = []
movement_history = []

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

buffer_size = 10
detection_buffer = deque(maxlen=buffer_size)

buffer_size_w = 10
detection_buffer_w = deque(maxlen=buffer_size_w)


def update_movement(movement, video_time_formatted):
    if movement_start_times[movement] is None:
        movement_start_times[movement] = video_time_formatted
    elif movement_end_times[movement] is None:
        movement_end_times[movement] = video_time_formatted
        movement_times[movement].append(
            (movement_start_times[movement], movement_end_times[movement])
        )
        movement_start_times[movement] = None
        movement_end_times[movement] = None


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


@socketio.on("frame")
def handle_frame(data):
    current_score = 0
    global last_time, weighted_sum, total_weight

    # Decode image data from the client
    image_data = base64.b64decode(data.split(",")[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Preprocess the frame
    frame = apply_clahe(frame)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the image with Mediapipe
    results_pose = pose.process(image)
    results_hands = hands.process(image)

    # Convert the image back to BGR for OpenCV
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Define variables
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
        if detect_body_lean(results_pose.pose_landmarks):
            body_lean = True
        if detect_open_palms_with_correct_finger_order(results_hands):
            open_palm_fw = True
        if detect_triangle_power_gesture(results_hands, frame.shape[1], frame.shape[0]):
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

        hand_on_head_avg = apply_moving_average(movement_buffers["HAND_ON_HEAD"])
        crossed_hands_avg = apply_moving_average(movement_buffers["HAND_CROSSED"])
        hand_on_waist_avg = apply_moving_average(movement_buffers["HAND_ON_WAIST"])
        straight_down_hands_avg = apply_moving_average(
            movement_buffers["HAND_STRAIGHT_DOWN"]
        )
        body_lean_avg = apply_moving_average(movement_buffers["BODY_LEAN"])
        open_palm_fw_avg = apply_moving_average(movement_buffers["OPEN_PALMS_FORWARD"])
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
            socketio.emit(
                "server_message", {"message": "Motion detected: HAND_CROSSED"}
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
            socketio.emit(
                "server_message", {"message": "Motion detected: hand_on_waist"}
            )

        if hand_on_head_avg > 0.5:
            standing_straight = False
            current_score -= weights["HAND_ON_HEAD"]
            movement_history.append("HAND_ON_HEAD")
            update_movement("HAND_ON_HEAD", video_time_formatted)
            expert_system_statements.append((elapsed_time, "Hand on head"))
            socketio.emit(
                "server_message", {"message": "Motion detected: hand_on_head"}
            )

        if straight_down_hands_avg > 0.5:
            standing_straight = False
            current_score += weights["HAND_STRAIGHT_DOWN"]
            movement_history.append("HAND_STRAIGHT_DOWN")
            update_movement("HAND_STRAIGHT_DOWN", video_time_formatted)
            expert_system_statements.append((elapsed_time, "Hand straight down"))
            socketio.emit(
                "server_message", {"message": "Motion detected: HAND_STRAIGHT_DOWN"}
            )

        if body_lean_avg > 0.5:
            body_lean_buffer.append(body_lean)
            if len(body_lean_buffer) > body_lean_threshold:
                body_lean_buffer.pop(0)
            if len(body_lean_buffer) == body_lean_threshold and all(body_lean_buffer):
                standing_straight = False
                current_score -= weights["BODY_LEAN"]
                movement_history.append("BODY_LEAN")
                update_movement("BODY_LEAN", video_time_formatted)
                expert_system_statements.append((elapsed_time, "Body lean"))
                socketio.emit(
                    "server_message", {"message": "Motion detected: body_lean"}
                )
        else:
            body_lean_buffer.clear()

        if open_palm_fw_avg > 0.5:
            current_score += weights["OPEN_PALMS_FORWARD"]
            movement_history.append("OPEN_PALMS_FORWARD")
            update_movement("OPEN_PALMS_FORWARD", video_time_formatted)
            expert_system_statements.append((elapsed_time, "Open palms forward"))
            socketio.emit(
                "server_message", {"message": "Motion detected: open_palm_fw"}
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
                socketio.emit(
                    "server_message",
                    {"message": "Motion detected: triangle_power_gesture"},
                )

            if current_score != previous_score:
                time_points.append(current_time)
                performance_scores.append(current_score)
                update_performance_plot(time_points, performance_scores)

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

        # if standing_straight:
        #     current_score += weights["STANDING_STRAIGHT"]

        # weighted_sum += current_score
        # total_weight += 1
        # performance = weighted_sum / total_weight
        # performance_scores.append(performance)
        # time_points.append(time.time() - start_time)
        # last_time = current_time

    # Display the image (optional)
    cv2.imshow("frame", image)
    print(image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        pose.close()
        hands.close()
        cv2.destroyAllWindows()


@socketio.on("stop_video")
def handle_stop_video():
    socketio.emit("server_message", {"message": "Video feed stopped"})
    cv2.destroyAllWindows()


@socketio.on("connect")
def handle_connect():
    socketio.emit(
        "server_message", {"message": "Welcome! You are connected to the server."}
    )


@socketio.on("disconnect")
def handle_disconnect():
    cv2.destroyAllWindows()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
