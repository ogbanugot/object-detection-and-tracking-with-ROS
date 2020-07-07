from scripts.robo import Robo
from threading import Timer
import time

timer = None

class Robosapien():
    '''
    Interface between ROS and the robosapien. Can be used to send movement
    commands to the robot.
    '''
    # Hex codes for specific robosapien movements:
    CODE_RSTurnRight       = 0x80
    CODE_RSRightArmUp      = 0x81
    CODE_RSRightArmOut     = 0x82
    CODE_RSTiltBodyRight   = 0x83
    CODE_RSRightArmDown    = 0x84
    CODE_RSRightArmIn      = 0x85
    CODE_RSWalkForward     = 0x86
    CODE_RSWalkBackward    = 0x87
    CODE_RSTurnLeft        = 0x88
    CODE_RSLeftArmUp       = 0x89
    CODE_RSLeftArmOut      = 0x8A
    CODE_RSTiltBodyLeft    = 0x8B
    CODE_RSLeftArmDown     = 0x8C
    CODE_RSLeftArmIn       = 0x8D
    CODE_RSStop            = 0x8E
    CODE_RSWakeUp          = 0xB1
    CODE_RSBurp            = 0xC2
    CODE_RSRightHandStrike = 0xC0
    CODE_RSNoOp            = 0xEF

    ROBOT = Robo(21) # Create Robo object for GPIO 21

    IS_MOVING = False

    @staticmethod
    def stop(*args, **kwargs):
        # print "Stopped"
        Robosapien.ROBOT.send_code(Robosapien.CODE_RSStop)
    
    @staticmethod
    def execute_command(code, number_of_times):
        if not Robosapien.IS_MOVING:
            Robosapien.IS_MOVING = True
            Robosapien.ROBOT.send_code(code)
            time.sleep(3)
            Robosapien.stop()
            Robosapien.IS_MOVING = False
    
    @staticmethod
    def JI_MASUN(*args, **kwargs):
        Robosapien.ROBOT.send_code(Robosapien.CODE_RSWakeUp)

    @staticmethod
    def wake_up(*args, **kwargs):
        Robosapien.ROBOT.send_code(Robosapien.CODE_RSWakeUp)

    @staticmethod
    def left_hand_up(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSLeftArmUp, number_of_times)

    @staticmethod
    def left_hand_out(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSLeftArmOut, number_of_times)

    @staticmethod
    def left_hand_down(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSLeftArmDown, number_of_times)

    @staticmethod
    def left_hand_in(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSLeftArmIn, number_of_times)
    
    @staticmethod
    def right_hand_up(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSRightArmUp, number_of_times)

    @staticmethod
    def right_hand_out(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSRightArmOut, number_of_times)

    @staticmethod
    def right_hand_down(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSRightArmDown, number_of_times)

    @staticmethod
    def right_hand_in(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSRightArmIn, number_of_times)

    @staticmethod
    def walk_forward(number_of_times = 1):
        Robosapien.execute_command(Robosapien.CODE_RSWalkForward, number_of_times)
    
    @staticmethod
    def walk_backward(number_of_times = 1):
        Robosapien.execute_command(Robosapien.CODE_RSWalkBackward, number_of_times)

    @staticmethod
    def turn_right(number_of_times = 1):
        Robosapien.execute_command(Robosapien.CODE_RSTurnRight, number_of_times)
    
    @staticmethod
    def turn_left(number_of_times = 1):
        Robosapien.execute_command(Robosapien.CODE_RSTurnLeft, number_of_times)
    
    # 
    # def stop(number_of_times = 1):
    #     Robosapien.execute_command(Robosapien.CODE_RSStop, number_of_times)



class RobosapienSlow():
    '''
    Interface between ROS and the robosapien. Can be used to send movement
    commands to the robot.
    '''
    # Hex codes for specific robosapien movements:
    CODE_RSTurnRight       = 0x80
    CODE_RSRightArmUp      = 0x81
    CODE_RSRightArmOut     = 0x82
    CODE_RSTiltBodyRight   = 0x83
    CODE_RSRightArmDown    = 0x84
    CODE_RSRightArmIn      = 0x85
    CODE_RSWalkForward     = 0x86
    CODE_RSWalkBackward    = 0x87
    CODE_RSTurnLeft        = 0x88
    CODE_RSLeftArmUp       = 0x89
    CODE_RSLeftArmOut      = 0x8A
    CODE_RSTiltBodyLeft    = 0x8B
    CODE_RSLeftArmDown     = 0x8C
    CODE_RSLeftArmIn       = 0x8D
    CODE_RSStop            = 0x8E
    CODE_RSWakeUp          = 0xB1
    CODE_RSBurp            = 0xC2
    CODE_RSRightHandStrike = 0xC0
    CODE_RSNoOp            = 0xEF

    ROBOT = Robo(21) # Create Robo object for GPIO 21

    IS_MOVING = False

    @staticmethod
    def stop(*args, **kwargs):
        # print "Stopped"
        Robosapien.ROBOT.send_code(Robosapien.CODE_RSStop)
    
    @staticmethod
    def execute_command(code, number_of_times):
        Robosapien.ROBOT.send_code(code)
        Robosapien.stop()
    
    @staticmethod
    def JI_MASUN(*args, **kwargs):
        Robosapien.ROBOT.send_code(Robosapien.CODE_RSWakeUp)

    @staticmethod
    def wake_up(*args, **kwargs):
        Robosapien.ROBOT.send_code(Robosapien.CODE_RSWakeUp)

    @staticmethod
    def left_hand_up(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSLeftArmUp, number_of_times)

    @staticmethod
    def left_hand_out(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSLeftArmOut, number_of_times)

    @staticmethod
    def left_hand_down(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSLeftArmDown, number_of_times)

    @staticmethod
    def left_hand_in(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSLeftArmIn, number_of_times)
    
    @staticmethod
    def right_hand_up(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSRightArmUp, number_of_times)

    @staticmethod
    def right_hand_out(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSRightArmOut, number_of_times)

    @staticmethod
    def right_hand_down(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSRightArmDown, number_of_times)

    @staticmethod
    def right_hand_in(number_of_times=1):
        Robosapien.execute_command(Robosapien.CODE_RSRightArmIn, number_of_times)

    @staticmethod
    def walk_forward(number_of_times = 3):
        # Robosapien.execute_command(Robosapien.CODE_RSWalkForward, number_of_times)
        Robosapien.ROBOT.send_code(Robosapien.CODE_RSWalkForward)
    
    @staticmethod
    def walk_backward(number_of_times = 1):
        Robosapien.execute_command(Robosapien.CODE_RSWalkBackward, number_of_times)

    @staticmethod
    def turn_right(number_of_times = 1):
	Robosapien.ROBOT.send_code(Robosapien.CODE_RSTurnRight)
        #Robosapien.execute_command(Robosapien.CODE_RSTurnRight, number_of_times)
    
    @staticmethod
    def turn_left(number_of_times = 1):
    	Robosapien.ROBOT.send_code(Robosapien.CODE_RSTurnLeft)
     	#  Robosapien.execute_command(Robosapien.CODE_RSTurnLeft, number_of_times)
    
