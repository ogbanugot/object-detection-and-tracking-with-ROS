from time import time
from math import sqrt

import cv2
import numpy as np

class ColoredObjectDetector():
    object_color = None

    # take into account different possible color ranges
    # tweak via sensitivity 
    sensitivity = 45
    # Both valid blues
    old_hsv = {
        # [105, 37, 170] [118, 50, 183]
    #a1 'white' : (np.array([0,0,sensitivity]), np.array([0,0,255-sensitivity])),
    'white' : (np.array([0,0,255-sensitivity]), np.array([255,sensitivity,255])),
    #a2 'white' : (np.array([90,30,160]), np.array([130,60,210])),    
    'red' : (np.array([0,100,100]), np.array([10,255,255])),
    'red2' : (np.array([160,100,100]), np.array([179,255,255])),
    'red3' : (np.array([160, 139, 66]), np.array([179, 204, 116])),
    # a'blue' : (np.array([110, 50, 50]), np.array([130,255,255])),
    # a1'blue' : (np.array([60,120,120]), np.array([180,200,200])),
    # [104, 71, 169] [109, 114, 201]
    'blue' : (np.array([60, 140, 150]), np.array([120,255,255])),    
    'yellow' : (np.array([9, 0, 0]), np.array([40, 150, 255])),
    'violet' : (np.array([10,100,20]), np.array([20,255,200]))
    }

    color_hsv = {
        "yellow" : (np.array([19, 100, 110]), np.array([59, 255, 255])),
        "violet" : (np.array([158, 117, 164]), np.array([167, 147, 211])),
        # "violet" : (np.array([115, 160, 120]), np.array([165, 255, 170])),
        "blue" : (np.array([60, 180, 120]), np.array([120, 255, 255])),
        # "white" : ( np.array([55, 66, 170]), np.array([179, 120, 255]) ),
        "white" : (np.array([0, 0, 235]), np.array([20, 20, 255])),
        # "white" : ( np.array([100, 0,157]), np.array([179, 90, 197]) ),
        "red_low" : (np.array([158, 117, 164]), np.array([167, 147, 211])),
        "red_high" : (np.array([158, 117, 164]), np.array([167, 147, 211])),        
        #"red_low" : (np.array([0, 120, 125]), np.array([10, 255, 255])),
        #"red_high" : (np.array([170, 157, 125]), np.array([179, 255, 255])),        
        "bottom_red1" : (np.array([0, 120, 160]), np.array([23, 255, 240])),    
        #### "red" : (np.array([25, 231, 92]), np.array([52, 255, 255]))  
    }

    alt_color_hsv = {
        "yellow" : (np.array([0, 235, 235]), np.array([50, 255, 255])),
        "violet" : (np.array([130, 235, 235]), np.array([179, 255, 255])),
        "blue" : (np.array([70, 200, 200]), np.array([110, 255, 255])),
        "white" : (np.array([0, 0, 235]), np.array([20, 20, 255])),
        "red" : (np.array([0, 235, 235]), np.array([20, 255, 255]))

    }

    # rgb_sensitivity = 120
    color_bgr = {
        'yellow' : (np.array([0,110,120]), np.array([120,255,255])),
        'violet' : (np.array([150,0,150]), np.array([255,120,255])),
        'blue' : (np.array([170,170,0]), np.array([255,255,120])),
        'white' : (np.array([160,160,160]), np.array([255,255,255])),        
        'red' : (np.array([0,0,150]), np.array([120,120,255]))
    }

    alt_bgr = {
        'yellow' : (np.array([10,100,170]), np.array([70,255,255])),
        'violet' : (np.array([54, 2, 119]), np.array([93,17,255])),
        'blue' : (np.array([170,170,0]), np.array([255,255,120])),
        'white' : (np.array([160,160,160]), np.array([255,255,255])),        
        'red' : (np.array([0,0,150]), np.array([120,120,255]))
    }

    def __init__(self, color="yellow"):
        self.object_color =  color

    def get_color_range(self, color, color_space='hsv'):
        '''
        Function to hsv range of color from color name in specified color space.
        '''
        # # print "COLOR SPACE : ", color_space
        if color_space == "bgr":           
            return self.color_bgr.get(color)
        elif color_space == "alt_hsv":
            # return self.alt_color_hsv.get(color)
            return self.alt_color_hsv.get(color)
        
        return self.color_hsv.get(color)
    
    def preprocess_image(self, image):        
        start = time()
        image = cv2.medianBlur(image,5)
        image = cv2.bilateralFilter(image,9,75,75)
        image = cv2.GaussianBlur(image,(5,5),0)
        end = time()
        # # print "Preprocessing time"
        # # print end - start
        return image

    def find_objects(self, image, color=None, color_space=None, object=None):
        '''
        Finds every object in an image that matches the supplied color.
        The default value for color is the self.object_color.
        Returns a black and white image with contours as bounding boxes for each matched object.
        '''                

        color = color or self.object_color


        # Preprocess image (DO THIS SOMEWHERE ELSE TO PREVENT PREPROCESSING IMAGE FOR EVERY DIFFERENT DETECTOR)
        # image = self.preprocess_image(image)
        
        # Specify range of color in hsv
        lower_color_bound, upper_color_bound = self.get_color_range(color, color_space=color_space)
        
        # Gets all the pixels whose color is in the range of the supplied color
        res = cv2.inRange(image, lower_color_bound, upper_color_bound)        
        # res = cv2.bitwise_and(image, image, mask=res)

        ret, thresh = cv2.threshold(res, 127, 255, 0)
        res, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        valid_contours = []

        # Remove embedded contours ???
        bounding_boxes = []
        for contour in contours:            
            x, y, width, height = cv2.boundingRect(contour)              
            if(height*width < 650):
                continue

            if (y < 30):
                continue
            
            bounding_box = {
                "meta" : {
                    "color" : color
                },
                "object" : "ball",
                "coordinates" : {
                    "top_left" : (x, y),
                    "top_right" : (x + width, y),
                    "bottom_left" : (x, y + height),
                    "bottom_right" : (x + width, y + height),
                }
            }


            valid_contours.append(contour)
            bounding_boxes.append(bounding_box)   
        
        return res, valid_contours, bounding_boxes


class MarkerDetector():
    # A marker is a rectangle with two colors with one color being on top of the other

    def __init__(self, top_color, bottom_color):
        self.top_color = top_color
        self.bottom_color = bottom_color
        
        self.top_detector = ColoredObjectDetector(top_color)
        self.bottom_detector = ColoredObjectDetector(bottom_color)

    def compare_boxes(self, top_bounding_box="white", bottom_bounding_box="white"):
        confidence = 0        

        if (len(top_bounding_box.keys()) == 0 or len(bottom_bounding_box.keys()) == 0):
            return (None, None)

        x1 = top_bounding_box.get("bottom_left")[0]
        x2 = top_bounding_box.get("bottom_right")[0]        
        x3 = bottom_bounding_box.get("top_left")[0]
        x4 = bottom_bounding_box.get("top_right")[0]

        y1 = top_bounding_box.get("bottom_left")[1]
        y2 = top_bounding_box.get("bottom_right")[1]        
        y3 = bottom_bounding_box.get("top_left")[1]
        y4 = bottom_bounding_box.get("top_right")[1]    
        
        top_width = abs(x1 - x2)
        top_height = abs(y1 - top_bounding_box.get("top_left")[1])

        bottom_width = abs(x3 - x4)
        bottom_height = abs(y3 - bottom_bounding_box.get("bottom_left")[1])

        
        # # print(top_bounding_box, "\n", bottom_bounding_box)
        # Check if top box is on top
        # # print(y1, y3)
        error_margin_x = top_width if top_width < bottom_width else bottom_width
        error_margin_y = top_height if top_height < bottom_height else bottom_height
        error_margin_y *= 1.2
        
        # # print(y1, y3, abs(y1-y3))
        if abs(y1 - y3) > error_margin_y:    
            return (0, None)

        # Gets the absolute value of the difference between two numbers
        # and divides by the error margin, then subtracts the answer from
        # 1 to give a confidence between 0 and 1
        confidence_calc = lambda x, y, err=error_margin_x : max((1 - (float(abs(x-y))/err), 0) )


        confidence += confidence_calc(x1, x3)
        confidence += confidence_calc(x2, x4)
        confidence += confidence_calc(y1, y3, error_margin_y)
        confidence += confidence_calc(y2, y4, error_margin_y)        
        # confidence += 2 if y1 == y2 == y3 == y4 else 0
       
        
        # Python2 gives floor for integer division
        confidence = float(confidence)/4
        
        coordinates = None

        # print("CONFIDENCE : ", confidence)

        if confidence >= 0.65:
            coordinates = {
            "top_left" : top_bounding_box.get("top_left"),
            "bottom_left" : bottom_bounding_box.get("bottom_left"),
            "top_right" : top_bounding_box.get("top_right"),
            "bottom_right" : bottom_bounding_box.get("bottom_right")
            }

            # # print(top_bounding_box, bottom_bounding_box)
            # # print(confidence, coordinates)
            
        return (confidence, coordinates)

    def find_marker(self, image, top_color=None, bottom_color=None):
        top_color = top_color or self.top_color
        bottom_color = bottom_color or self.bottom_color
        
        _, _, top_bounding_boxes = self.top_detector.find_objects(image, color=top_color)
        _, _, bottom_bounding_boxes = self.bottom_detector.find_objects(image, color=bottom_color)
                
        # # print(len(top_bounding_boxes), len(bottom_bounding_boxes))
        # # print(top_bounding_boxes, "\n", bottom_bounding_boxes)
        markers = []
                
        for top_box in top_bounding_boxes:
            top_box = top_box.get("coordinates")        
            for bottom_box in bottom_bounding_boxes:
                bottom_box = bottom_box.get("coordinates")
                confidence, coordinates = self.compare_boxes(top_box, bottom_box)
                if coordinates:                    
                    markers.append({"confidence" : confidence, "coordinates" : coordinates, "object" : "marker", "meta" : {                        
                        "top_color" : top_color,
                        "bottom_color" : bottom_color
                    }})        
        
        max_bbox = (0, {})
        for marker in markers:            
            if marker.get("confidence") > max_bbox[0]:
                # # print "Max fo"
                max_bbox = (marker.get("confidence"), marker)
        return max_bbox[1]


def bgr_to_hsv(bgr_color):
    color = np.uint8([[bgr_color]])
    return cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

def measure_blur(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def preprocess_image(image):                
        image = cv2.medianBlur(image,5)
        image = cv2.bilateralFilter(image,9,75,75)
        image = cv2.GaussianBlur(image,(5,5),0)          
        
        return image

def draw_bounding_box(image, bounding_box, color, thickness=1):
    # # print(bounding_box)
    top_left = bounding_box.get("top_left")
    bottom_right = bounding_box.get("bottom_right")

    image = cv2.rectangle(image, top_left, bottom_right,color, thickness)
    return image

def detect_circles(image, boundingBox, minCircleRadius):
    '''
    Function to detect circles with a minimum radius of minCircleRadius in a 
    bounding box within a grayscale image.
    '''
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.2, minCircleRadius)

def find_ball(image, detector, ball_colors):
    options = []
    for number, ball_color in enumerate(ball_colors):
        _, contours, _ = detector.find_objects(image, color=ball_color)
        # print "INFO FOR BALL : ", number
        # print "NUMBER OF CONTOURS : ", len(contours)
        best_ball_contour = (0, None)
        for index, contour in enumerate(contours):
            # estimate contour shape
            accuracy = 0.03*cv2.arcLength(contour,True)
            approximate_shape = cv2.approxPolyDP(contour,accuracy,True)
            # print "CONTOUR : ", index + 1, 
            # # print "APPROX SHAPE VERTICES : ", approximate_shape

            num_of_vertices = len(approximate_shape)
            # print "NUMBER OF VERTICES : ", num_of_vertices
            if num_of_vertices > 3:
                confidence = 0

                # confidence calculation to determine closeness of num_vertices to 4(rectangle)
                confidence_calc = lambda num_of_vertices : float(num_of_vertices - 4)/4

                vertice_confidence = confidence_calc(num_of_vertices)
                # print "VERTICE CONFIDENCE : ", vertice_confidence
                # Get extreme points in contour
                left_most = tuple(contour[contour[:,:,0].argmin()][0])
                right_most = tuple(contour[contour[:,:,0].argmax()][0])
                top_most = tuple(contour[contour[:,:,1].argmin()][0])
                bottom_most = tuple(contour[contour[:,:,1].argmax()][0])

                # # print (left_most, right_most, top_most, bottom_most)

                distance = lambda point1, point2 : sqrt( (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 )
                # pointwise_confidence = lambda x, y : distance(x, y)
                width = distance(left_most, right_most)
                height = distance(top_most, bottom_most)
                error = 60
                pointwise_confidence = 1 - float(abs(height - width))/float(max(height, width))
                # print "WIDTH HEIGHT : ", abs(height - width)
                # print "POINTWISE CONFIDENCE : ", pointwise_confidence

                confidence = (vertice_confidence*2 + pointwise_confidence)/3
                # print "FINAL CONFIDENCE : ", confidence                
                # print "----------------------------------------------"
                if confidence > best_ball_contour[0]:
                    best_ball_contour = (confidence, contour)
                    
        confidence = best_ball_contour[0]
        contour = best_ball_contour[1]
        
        bounding_box = None
        if contour is not None:
            x, y, width, height = cv2.boundingRect(contour)              
            
            bounding_box = {
                "meta" : {
                    "color" : ball_color
                },
                "object" : "ball",
                "confidence" : confidence,
                "coordinates" : {
                    "top_left" : (x, y),
                    "top_right" : (x + width, y),
                    "bottom_left" : (x, y + height),
                    "bottom_right" : (x + width, y + height),
                }
            }                        
        
            options.append((confidence, bounding_box))

        # # print "======================================================================"
    
    # print "FOUND OPTIONS : ", options
    ball = (0, None)
    for option in options:
        if option[0] > ball[0]:
            ball = option

    if float(ball[0]) > 0.5:
        return ball[1]
    
    return {}
