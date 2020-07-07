import cv2
from detector import find_ball, detect_circles, preprocess_image, MarkerDetector, ColoredObjectDetector
# from object_detector import detect_robosapien


home_color = "blue"
away_color = "violet"
neutral_color = "yellow"
neutral_color2 = "white"
markers = [
    (home_color, neutral_color),
    # (neutral_color, home_color),
    # (neutral_color, neutral_color2),
    # (neutral_color2, neutral_color),
    # (away_color, neutral_color),
    # (neutral_color, away_color),
]

ball_color = "red"

def get_markers(image):
    marker_detector = MarkerDetector("white", "yellow")

    found_markers = []

    for marker in markers:
        found_markers.append(marker_detector.find_marker(image, top_color=marker[0], bottom_color=marker[1]))
    return found_markers

def get_robosapiens(image):
    return None
    # return detect_robosapien(image)

def get_ball(image):   
    detector = ColoredObjectDetector() 
    bbox = find_ball(image, detector, ["red_low", "red_high"])  
    
    return bbox

def validate_ball_position(bounding_box, y_limit=380):
    top_left = bounding_box.get("top_left")
    bottom_right = bounding_box.get("bottom_right")

    if top_left is None or bottom_right is None:
        return False
    object_mid_y = (top_left[1] + bottom_right[1])/2
            
    if object_mid_y < y_limit:
        return True

    print "INVALID BALL POSITION : ", top_left, bottom_right
    return False
        

        

def get_image_features(image):
    '''
    Function to recognize all objects of 
    interest within image
    '''
    robosapiens = get_robosapiens(image)

    # UNCOMMENT IF HSV
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = preprocess_image(image)
    
    items = get_markers(image) or []
    print("ITEMS : ", items)
    
    # print("ROBOTS", robosapiens)
    ball = get_ball(image)
    print "BALL GOTTEN : ", ball
    if robosapiens:        
        for robot in robosapiens:
            confidence = robot.get("confidence")
            if confidence < 0.6:
                continue   
            top_left = robot.get("topleft")
            bottom_right = robot.get("bottomright")
            coordinates = {
                "top_left" : (top_left.get('x'), top_left.get('y')),
                "bottom_right" : (bottom_right.get('x'), bottom_right.get('y')),
            }
            items.append({ 
                "confidence" : str(confidence), 
                "coordinates" : coordinates,
                "object" : "robosapien"
            })        

    if ball:
        items.append(ball)

    # print("ITEMS : ", items)
    return items


def draw_bounding_box(image, bounding_box, color, thickness=1):    
    top_left = bounding_box.get("top_left")
    bottom_right = bounding_box.get("bottom_right")

    image = cv2.rectangle(image, top_left, bottom_right,color, thickness)
    return image

# o_image = cv2.imread("images/test.png")
# image = o_image.copy()
# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  
# bounding_boxes = get_image_features(image)
# # detector = ColoredObjectDetector("red_low")
# # image = detector.preprocess_image(image)
# # bbox = find_ball(image, detector, ["red_low", "red_high"])
# # res, contours, bounding_boxes = detector.find_objects(image, color_space="hsv")

# # cv2.imshow('cv_img', res)            
# # cv2.waitKey(0) 

# # bounding_boxes = get_image_features(image) or []

# # print "BBOX : ", bbox
# # if bbox:
# #     o_image = draw_bounding_box(o_image, bbox.get("coordinates", {}), (0, 0, 255), 2)
# for box in bounding_boxes:
#     # print circles
#     o_image = draw_bounding_box(image, box.get("coordinates", {}), (0, 0, 255), thickness=3)

# # print "Here"                           
# cv2.imshow('cv_img', o_image)            
# cv2.waitKey(0)
