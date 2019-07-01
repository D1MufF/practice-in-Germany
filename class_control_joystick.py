import socket
import pygame
import pygame.joystick

import rospy

from marker_pos_angle.msg import id_pos_angle
import shapely

robot1_pos = None

start_marker_pos = None

# for debugging:
# rosrun image_view image_view image:=/fiducial_images

class robot:  # we have 4 arg for this class, because joysticks get the same (value, axis) events
    def __init__(self, joy, ip, port):
        self.joy = joy
        self.ip = ip
        self.port = port
        self.robot0_stopped_1 = True
        self.robot0_stopped_2 = True
        self.robot0_stopped_3 = True
        self.robot0_stopped_4 = True
        self.rc_socket = socket.socket()
        self.u1 = 0
        self.u2 = 0
        try:
            self.rc_socket.connect((self.ip, self.port))
        except socket.error():
            print("couldn't connect to socket")

        self.check_joystick = False
    def joystick_init(self):  # Joystick's initialisation
        joystick_count = pygame.joystick.get_count()
        for count in range(joystick_count):
            if joystick_count == 2:
                self.joystick = pygame.joystick.Joystick(self.joy)
                print("{}-->joystick count".format(joystick_count))
                self.joystick.init()
                self.check_joystick = True
            elif joystick_count == 1:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                print("connected only 1 joystick - {}".format(joystick))
                self.check_joystick = False
            elif not joystick_count:
                print("no joysticks connected")
                self.check_joystick = False





    def control(self, event):  # the control of two robots with joysticks
        joy = event.joy
        value = event.value
        axis = event.axis

        if joy == self.joy:
            if axis == 1:
                if abs(value) > 0.2:
                    u1 = u2 = -value
                    self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                    self.robot0_stopped_1 = False

                elif not self.robot0_stopped_1:
                    u1 = u2 = 0
                    self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                    self.robot0_stopped_1 = True
            elif axis == 3:
                if abs(value) > 0.2:
                    u1 = value
                    u2 = -value
                    self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                    self.robot0_stopped_2 = False

                elif not self.robot0_stopped_2:
                    u1 = u2 = 0
                    self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                    self.robot0_stopped_2 = True
            elif axis == 2:
                if value > 0.2:
                    u1 = value/1.9
                    u2 = value/1.2
                    self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                    self.robot0_stopped_3 = False

                elif not self.robot0_stopped_3:
                    u1 = u2 = 0
                    self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                    self.robot0_stopped_3 = True
            elif axis == 5:
                if value > 0.2:
                    u1 = value/1.2
                    u2 = value/1.9
                    self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                    self.robot0_stopped_4 = False

                elif not self.robot0_stopped_4:
                    u1 = u2 = 0
                    self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                    self.robot0_stopped_4 = True

    def control_keyboard(self, event):  # keyboard control for robot1

        if pressed[pygame.K_LEFT]:
            u1 = -1.0
            u2 = 1.0
            self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

        elif pressed[pygame.K_RIGHT]:
            u1 = 1.0
            u2 = -1.0
            self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

        elif pressed[pygame.K_UP]:
            u1 = -1.0
            u2 = -1.0
            self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

        elif pressed[pygame.K_DOWN]:
            u1 = 1.0
            u2 = 1.0
            self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

        elif event.type == pygame.KEYUP:
            self.rc_socket.send('({},{})\n'.format(self.u1, self.u2).encode())

    def control_keyboard_2(self, event):  # keyboard control for robot1

        if pressed[pygame.K_a]:
            u1 = -1.0
            u2 = 1.0
            self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

        elif pressed[pygame.K_d]:
            u1 = 1.0
            u2 = -1.0
            self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

        elif pressed[pygame.K_w]:
            u1 = -1.0
            u2 = -1.0
            self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

        elif pressed[pygame.K_s]:
            u1 = 1.0
            u2 = 1.0
            self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

        elif event.type == pygame.KEYUP:
            self.rc_socket.send('({},{})\n'.format(self.u1, self.u2).encode())


def measurement_callback(data):
    if data.id == 3:
        robot1_pos = (data.x, data.y)
    if data.id == 6:
        start_marker_pos = (data.x, data.y)

    print(data)


def main():
    pygame.init()
    pygame.display.set_mode((640, 480))

    rospy.init_node('game_node', anonymous=True)

    marker_sub = rospy.Subscriber("/marker_id_pos_angle", id_pos_angle, measurement_callback)

   # m = MeasurementClass()

    robot_1 = robot(0, '192.168.1.102', 1234)
    robot_1.joystick_init()
    robot_2 = robot(1, '192.168.1.103', 1234)
    robot_2.joystick_init()
    while True:
        events = pygame.event.get()
        global pressed
        pressed = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.JOYAXISMOTION:
                robot_1.control(event)
                robot_2.control(event)
            else:
                robot_1.control_keyboard(event)
                robot_2.control_keyboard_2(event)



if __name__ == '__main__':
    main()