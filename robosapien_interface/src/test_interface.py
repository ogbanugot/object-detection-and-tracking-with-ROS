from robosapien import Robosapien, RobosapienSlow
import time


# move_map = {
#     "w" : Robosapien().walk_forward,
#     "s" : Robosapien.walk_backward,
#     "a" : Robosapien.turn_left,
#     "d" : Robosapien.turn_right,
#     "y" : Robosapien.left_hand_up,
#     "u" : Robosapien.left_hand_out,
#     "h" : Robosapien.left_hand_down,
#     "j" : Robosapien.left_hand_in,
#     "i" : Robosapien.right_hand_up,
#     "o" : Robosapien.right_hand_out,
#     "k" : Robosapien.right_hand_down,
#     "l" : Robosapien.right_hand_in,
#     "stop" : Robosapien.stop,
#     "JI" : Robosapien.JI_MASUN
# }
# # terminate = False

# while True:
#     move = raw_input("Enter a command")
#     print(move)
#     move_map[move](3)
#     Robosapien().stop()
#     time.sleep(0.5)
#     #    Robosapien.execute_command(Robosapien.CODE_RSWalkForward, 100)

move_map = {
    "w" : RobosapienSlow.walk_forward,
    "s" : RobosapienSlow.walk_backward,
    "a" : RobosapienSlow.turn_left,
    "d" : RobosapienSlow.turn_right,
    "y" : RobosapienSlow.left_hand_up,
    "u" : RobosapienSlow.left_hand_out,
    "h" : RobosapienSlow.left_hand_down,
    "j" : RobosapienSlow.left_hand_in,
    "i" : RobosapienSlow.right_hand_up,
    "o" : RobosapienSlow.right_hand_out,
    "k" : RobosapienSlow.right_hand_down,
    "l" : RobosapienSlow.right_hand_in,
    "stop" : RobosapienSlow.stop,
    "JI" : RobosapienSlow.JI_MASUN
}
# terminate = False

while True:
    move = raw_input("Enter a command: ")
    print(move)

    RobosapienSlow().stop()
    move_map[move](3)
    RobosapienSlow().stop()

    #    Robosapien.execute_command(Robosapien.CODE_RSWalkForward, 100)
