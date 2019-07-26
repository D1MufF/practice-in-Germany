import socket
import pygame
import pygame.joystick
import rospy
import pygame.freetype
from marker_pos_angle.msg import id_pos_angle
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from shapely.geometry import Point

from copy import deepcopy

import time


# for debugging:
# rosrun image_view image_view image:=/fiducial_images

class race_track:
    """
    This class existing for a checking position of robots on the track
    We have four aruco markers for outside rectangle and four for inside small rectangle
    If one of the robots stay inside of the big rectangle we can to control its, but in another case works
    only keyboard control - we use it for came back of robots in there
    """

    def __init__(self, robot_1, robot_2):

        marker_sub = rospy.Subscriber("/marker_id_pos_angle", id_pos_angle, self.measurement_callback)
        self.robot_1 = robot_1
        self.robot_2 = robot_2

        self.rectangle_pos = None
        self.rectangle_pos_2 = None
        self.rectangle_pos_3 = None
        self.rectangle_pos_4 = None
        self.rectangle_pos_5 = None
        self.rectangle_pos_6 = None
        self.rectangle_pos_7 = None
        self.rectangle_pos_8 = None
        self.robot_pos_1 = None
        self.robot_pos_2 = None
        self.start_line = None
        self.checkpoint_line = None
        self.check_number_markers = True


        self.debug_plot = False

        self.checkpoint_count = 0
        self.finish_line_count = 0

        self.checkpoint_count_2 = 0
        self.finish_line_count_2 = 0
        self.countdown = False
        self.countdown_2 = False
        self.time_start = False
        self.countdown_check = False
        self.robot_1_time = False

        self.print_robot_1_time = False
        self.print_robot_2_time = False

        self.count_down_start = 0

        self.time_circle_robot_1 = 0
        self.time_circle_robot_2 = 0
        self.print_GO = False
        self.protect_for_b = True
        self.press_b_phrase = True

        self.robot_1_second_circle = None
        self.robot_1_first_circle = None
        self.robot_2_second_circle = None
        self.robot_2_first_circle = None
        self.final_time = None
        self.final_time_2 = None
        self.print_winner_1 = False
        self.print_winner_2 = False
        self.d_highscore = {}
        self.name = ""
        self.name_highscore_1 = None
        self.name_highscore_2 = None
        self.vanishing_TAB_phrase_1 = False
        self.vanishing_TAB_phrase_2 = False
        self.player_1 = False
        self.player_2 = False
        self.protect_for_dictionary = False
        self.protect_for_dictionary_2 = False
        self.name_winner = False
        self.name_loser = False
        self.last_result_print = False
        self.protect_restart = False
        self.protect_top10 = False
        self.name_player_print = False


    def measurement_callback(self, data):
        # Aruco marker number 14 it's robot 102; Aruco 1,5,7,8 are drawn small rectangle Polygon
        # Aruco 2,4,0,11 are assembled big rectangle Polygon

        if data.id == 14:
            self.robot_pos_1 = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id, self.robot_pos_1))
        elif data.id == 15:
            self.robot_pos_2 = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id, self.robot_pos_1))
        elif data.id == 9:
            self.checkpoint_line = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id, self.start_line))
        elif data.id == 0:
            self.start_line = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id, self.start_line))
        elif data.id == 1:
            self.rectangle_pos = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id, self.rectangle_pos))

        elif data.id == 2:
            self.rectangle_pos_2 = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id, self.rectangle_pos_2))

        elif data.id == 3:
            self.rectangle_pos_3 = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id, start_marker_pos_3))

        elif data.id == 4:
            self.rectangle_pos_4 = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id,start_marker_pos_4))
        elif data.id == 5:
            self.rectangle_pos_5 = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id, self.rectangle_pos_5))

        elif data.id == 6:
            self.rectangle_pos_6 = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id,self.rectangle_pos_6))

        elif data.id == 7:
            self.rectangle_pos_7 = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id, self.rectangle_pos_7))

        elif data.id == 8:
            self.rectangle_pos_8 = (data.x, data.y)
            # print ("{}->ID MARKER, {}->POSITION".format(data.id,self.rectangle_pos_8))

    def check_number_marker(self):
        if self.rectangle_pos is None:
            self.check_number_markers = False
        elif self.rectangle_pos_2 is None:
            self.check_number_markers = False
        elif self.rectangle_pos_3 is None:
            self.check_number_markers = False
        elif self.rectangle_pos_4 is None:
            self.check_number_markers = False
        elif self.rectangle_pos_5 is None:
            self.check_number_markers = False
        elif self.rectangle_pos_6 is None:
            self.check_number_markers = False
        elif self.rectangle_pos_7 is None:
            self.check_number_markers = False
        elif self.rectangle_pos_8 is None:
            self.check_number_markers = False
        elif self.start_line is None:
            self.check_number_markers = False
        elif self.checkpoint_line is None:
            self.check_number_markers = False
        else:
            self.check_number_markers = True

    def polygon_rectangle(self):
        if self.check_number_markers:
            self.rectangle_track = Polygon([self.rectangle_pos, self.rectangle_pos_2,
                                            self.rectangle_pos_3, self.rectangle_pos_4])

            self.rectangle_track_2 = Polygon([self.rectangle_pos_5, self.rectangle_pos_6,
                                              self.rectangle_pos_7, self.rectangle_pos_8])

            self.start_strength_line = Polygon([(self.rectangle_pos_7[0]-0.08, self.rectangle_pos_7[1]),
                                                (self.start_line[0]-0.08, self.start_line[1]),
                                                (self.start_line[0]+0.08, self.start_line[1]),
                                                (self.rectangle_pos_7[0]+0.08, self.rectangle_pos_7[1])])

            self.checkpoint_strength_line = Polygon([self.checkpoint_line, self.rectangle_pos_5,
                                                (self.rectangle_pos_5[0]+0.1, self.rectangle_pos_5[1]),
                                                (self.checkpoint_line[0] + 0.1, self.checkpoint_line[1])])
            self.robot_pos_1_point = Point(self.robot_pos_1)
            self.robot_pos_2_point = Point(self.robot_pos_2)

            if self.debug_plot:
                x, y = (self.checkpoint_strength_line.exterior.xy)
                plt.plot(x, y)
                plt.show()



            if self.rectangle_track.contains(self.robot_pos_1_point) and not \
                    self.rectangle_track_2.contains(self.robot_pos_1_point):

                self.robot_1.controlling_allowed = True
            else:
                #print("robot outside track")
                self.robot_1.controlling_allowed = False

            if self.rectangle_track.contains(self.robot_pos_2_point) and not \
                    self.rectangle_track_2.contains(self.robot_pos_2_point):

                self.robot_2.controlling_allowed = True
            else:
                #print("robot_2 outside track")
                self.robot_2.controlling_allowed = False
        else:
            print("couldn't find the all ARUCO markers")

    def check_starting_position(self, robot_1, robot_2): # when you pressing B robot must staying on the start line for beginning of race
        if self.protect_for_b:
            button_robot_1 = robot_1.joystick.get_button(1)
            button_robot_2 = robot_2.joystick.get_button(1)
            if button_robot_1:
                if self.start_strength_line.contains(self.robot_pos_1_point):
                    print("MLS is on the start line")

                    self.countdown = True
                else:
                    print("put the MLS on the start line")
                    self.robot_1.controlling_allowed_2 = False
            if button_robot_2:
                if self.start_strength_line.contains(self.robot_pos_2_point):
                    print("BMW X6 is on the start line")

                    self.countdown_2 = True
                else:
                    print("put the BMW X6 on the start line")
                    self.robot_2.controlling_allowed_2 = False

    def start_countdown(self):
        if self.countdown and self.countdown_2:
            self.count_down_start = time.time()
            self.time_start = True
            self.countdown_check = True
            self.press_b_phrase = False
            self.countdown = False
            self.countdown_2 = False

    def check_countdown(self):
        # if countdown reaches 0 -> allow control
        if self.countdown_check:
            if time.time() - self.count_down_start < 5:
                self.robot_1.controlling_allowed_2 = False
                self.robot_2.controlling_allowed_2 = False

            else:
                self.print_GO = True
                self.protect_for_b = False
    def print_countdown(self):
        # prints countdown to screen
        if self.time_start:
            countdown_font = pygame.font.Font(None, 80)
            ready_font= pygame.freetype.SysFont(None, 42)
            ready_font.render_to(screen, (170, 200), "ARE YOU READY?", (255, 160, 30))
            output_string = "{: 6.2f}".format(time.time() - self.count_down_start)
            text = countdown_font.render(output_string, True, (0, 255, 0))
            screen.blit(text, [260, 270])

    def time_robot_1_2(self):
        if self.robot_1_time and time.time() - self.count_down_start < 7.1:
            self.time_circle_robot_1 = time.time()
            self.time_circle_robot_2 = time.time()
            self.print_robot_1_time = True
            self.print_robot_2_time = True

    def print_time_robot_1_2(self):
        if self.print_robot_1_time:
            time_robot_2_font_1 = pygame.freetype.SysFont(None, 42)
            time_robot_2_font_1.render_to(screen, (30, 20), "TIME MLS", (255, 0, 0))
            time_robot_1_font = pygame.font.Font(None, 52)
            output_time_robot_1 = "{: 6.2f}".format(time.time() - self.time_circle_robot_1)
            text = time_robot_1_font.render(output_time_robot_1, True, (255, 0, 0))
            screen.blit(text, [120, 90])
        if not self.final_time is None:
            self.print_robot_1_time = False

        if self.print_robot_2_time:
            time_robot_2_font_2 = pygame.freetype.SysFont(None, 42)
            time_robot_2_font_2.render_to(screen, (380, 20), "TIME BMW X6", (150, 50, 255))
            time_robot_2_font = pygame.font.Font(None, 52)
            output_time_robot_2 = "{: 6.2f}".format(time.time() - self.time_circle_robot_2)
            text = time_robot_2_font.render(output_time_robot_2, True, (150, 50, 255))
            screen.blit(text, [470, 90])
        if not self.final_time_2 is None:
            self.print_robot_2_time = False

    def print_result(self):
        if self.final_time and self.final_time_2 is not None:
            self.print_winner_1 = False
            self.print_winner_2 = False
            self.vanishing_TAB_phrase_1 = True
            self.vanishing_TAB_phrase_2 = True

        if not self.final_time is None:
            if self.print_winner_1:
                final_time_robot_1_font = pygame.font.Font(None, 36)
                final_time_robot_1 = "FINAL TIME MLS  {: 6.2f}".format(self.final_time)
                text = final_time_robot_1_font.render(final_time_robot_1, True, (0, 255, 0))
                screen.blit(text, [30, 300])

        if not self.robot_1_second_circle is None:
            second_circle_robot_1_font = pygame.font.Font(None, 32)
            second_circle_robot_1 = "SECOND LAP  {: 6.2f}".format(self.robot_1_second_circle)
            text = second_circle_robot_1_font.render(second_circle_robot_1, True, (255, 0, 0))
            screen.blit(text, [30, 200])


        if not self.robot_1_first_circle is None:
            first_circle_robot_1_font = pygame.font.Font(None, 32)
            first_circle_robot_1 = "FIRST LAP  {: 6.2f}".format(self.robot_1_first_circle)
            text = first_circle_robot_1_font.render(first_circle_robot_1, True, (255, 0, 0))
            screen.blit(text, [30, 150])

        if not self.final_time_2 is None:
            if self.print_winner_2:
                final_time_robot_2_font = pygame.font.Font(None, 36)
                final_time_robot_2 = "FINAL TIME BMW X6  {: 6.2f}".format(self.final_time_2)
                text = final_time_robot_2_font.render(final_time_robot_2, True, (0, 255, 0))
                screen.blit(text, [380, 300])
        if not self.robot_2_second_circle is None:
            second_circle_robot_2_font = pygame.font.Font(None, 32)
            second_circle_robot_2 = "SECOND LAP  {: 6.2f}".format(self.robot_2_second_circle)
            text = second_circle_robot_2_font.render(second_circle_robot_2, True, (150, 50, 255))
            screen.blit(text, [380, 200])

        if not self.robot_2_first_circle is None:
            first_circle_robot_2_font = pygame.font.Font(None, 32)
            first_circle_robot_2 = "FIRST LAP  {: 6.2f}".format(self.robot_2_first_circle)
            text = first_circle_robot_2_font.render(first_circle_robot_2, True, (150, 50, 255))
            screen.blit(text, [380, 150])

    def first_phrase(self):

        if self.press_b_phrase:
            robot_font_2 = pygame.freetype.SysFont(None, 30)
            robot_font_2.render_to(screen, (240, 240), "BOTH PLAYERS!", (255, 160, 30))
            robot_font_2.render_to(screen, (30, 300), "PUT DOWN TWO ROBOTS ON THE START LINE", (255, 160, 30))
            robot_font_2.render_to(screen, (110, 360), "AND PRESS 'B' FOR THE BEGINNING", (255, 160, 30))
        if self.print_GO:
            if time.time() - self.count_down_start > 5 and time.time() - self.count_down_start < 7:
                print_go_font = pygame.freetype.SysFont(None, 152)
                print_go_font.render_to(screen, (230, 200), "GO!", (255, 160, 30))
                self.time_start = False
            else:
                self.robot_1.controlling_allowed_2 = True
                self.robot_2.controlling_allowed_2 = True
                self.robot_1_time = True


    def checkpoint(self):
        if self.check_number_markers:
            if self.checkpoint_strength_line.contains(self.robot_pos_1_point):
                if self.finish_line_count == self.checkpoint_count:
                    self.checkpoint_count += 1
                    print("Player 1 reached checkpoint, checkpoint count = {}".format(self.checkpoint_count))
            if self.checkpoint_strength_line.contains(self.robot_pos_2_point):
                if self.finish_line_count_2 == self.checkpoint_count_2:
                    self.checkpoint_count_2 += 1
                    print("Player 2 reached checkpoint, checkpoint count = {}".format(self.checkpoint_count_2))

    def finish_line(self):
        if self.check_number_markers:
            if self.start_strength_line.contains(self.robot_pos_1_point):
                if self.finish_line_count < self.checkpoint_count:
                    self.finish_line_count += 1

                elif self.finish_line_count == self.checkpoint_count and self.finish_line_count == 1:
                    if self.final_time is None:
                        self.final_time = time.time() - self.time_circle_robot_1
                    self.robot_1.controlling_allowed = False
                    self.print_winner_1 = True
                    self.robot_1.controlling_keyboard = False



                # elif self.finish_line_count == self.checkpoint_count and self.finish_line_count == 2:
                #     if self.robot_1_second_circle is None:
                #         self.robot_1_second_circle = time.time() - self.time_circle_robot_1
                #
                # elif self.finish_line_count == self.checkpoint_count and self.finish_line_count == 1:
                #     if self.robot_1_first_circle is None:
                #         self.robot_1_first_circle = time.time() - self.time_circle_robot_1

            if self.start_strength_line.contains(self.robot_pos_2_point):
                if self.finish_line_count_2 < self.checkpoint_count_2:
                    self.finish_line_count_2 += 1
                    print("Player 2 reached finish line, finish line count = {}".format(self.finish_line_count_2))

                elif self.finish_line_count_2 == self.checkpoint_count_2 and self.finish_line_count_2 == 1:
                    if self.final_time_2 is None:
                        self.final_time_2 = time.time() - self.time_circle_robot_2
                    self.robot_2.controlling_allowed = False
                    self.print_winner_2 = True
                    self.robot_2.controlling_keyboard = False

                # elif self.finish_line_count_2 == self.checkpoint_count_2 and self.finish_line_count_2 == 2:
                #     if self.robot_2_second_circle is None:
                #         self.robot_2_second_circle = time.time() - self.time_circle_robot_2
                #
                # elif self.finish_line_count_2 == self.checkpoint_count_2 and self.finish_line_count_2 == 1:
                #     if self.robot_2_first_circle is None:
                #         self.robot_2_first_circle = time.time() - self.time_circle_robot_2


    def restart(self):
        if self.protect_restart:
            self.robot_1.controlling_keyboard = True
            self.robot_2.controlling_keyboard = True
            loop = False
            return loop
        return True

    def print_winner(self):
        if self.final_time and self.final_time_2 is not None:
            if self.vanishing_TAB_phrase_1 and self.vanishing_TAB_phrase_2:
                robot_font_2 = pygame.freetype.SysFont(None, 30)
                robot_font = pygame.freetype.SysFont(None, 46)
                if self.final_time < self.final_time_2:
                    robot_font.render_to(screen, (180, 180), "MLS winner!", (255, 160, 30))
                elif self.final_time > self.final_time_2:
                    robot_font.render_to(screen, (200, 180), "BMW X6 winner!", (255, 160, 30))

                robot_font_2.render_to(screen, (140, 300), "Who were drivers? ", (255, 160, 30))
                robot_font_2.render_to(screen, (100, 350), "Press TAB and record your name", (255, 160, 30))
            if pressed[pygame.K_TAB]:
                self.player_1 = True
                self.name_player_print = True
                self.name_winner = True


    def player_name(self, event):
        if self.player_1:
            winner = min(self.final_time, self.final_time_2)
            loser = max(self.final_time, self.final_time_2)
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if len(self.name) < 10:
                        if event.unicode == 10:
                            self.name += 0
                        else:
                            self.name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:

                    if len(self.d_highscore.keys()) == 1:
                        self.d_highscore[self.name] = loser
                        self.protect_for_dictionary_2 = True
                        self.name_loser = False
                        self.name = ""
                        self.last_result_print = True
                        self.player_2 = False
                        self.player_1 = False

                    if len(self.d_highscore.keys()) < 1:
                        self.name_winner = False
                        self.name_loser = True

                        self.d_highscore[self.name] = winner
                        self.protect_for_dictionary = True
                        self.name = ""

                self.player_2 = True
    def player_name_print_font(self):
        font = pygame.font.SysFont(None, 36)
        if self.player_2:
            block = font.render(self.name, True, (255, 255, 255))
            rect = block.get_rect()
            rect.center = screen.get_rect().center
            screen.blit(block, rect)
    def player_name_print(self):
        if self.name_player_print:
            self.vanishing_TAB_phrase_1 = False
            self.vanishing_TAB_phrase_2 = False
            font_2 = pygame.freetype.SysFont(None, 30)

            if self.name_winner:
                font_2.render_to(screen, (240, 190), "Winner's name: ", (255, 160, 30))
            if self.name_loser:
                font_2.render_to(screen, (240, 190), "Loser's name: ", (255, 160, 30))
            if self.last_result_print:
                dict_1 = self.d_highscore
                font_2.render_to(screen, (50, 60), "{}:{:5.2f}".format(dict_1.keys()[0],dict_1.values()[0]),
                                 (255, 160, 30))

                font_2.render_to(screen, (50, 90), "{}:{:5.2f}".format(dict_1.keys()[1], dict_1.values()[1]),
                                 (255, 160, 30))

                font_2.render_to(screen, (70, 220), "Press TAB for views TOP 10 HOT", (255, 160, 30))
                font_2.render_to(screen, (70, 270), "Press SPACE for restart the RACE", (255, 160, 30))
                if pressed[pygame.K_SPACE]:
                    self.protect_restart = True
                if pressed[pygame.K_TAB]:
                    self.protect_top10 = True
    def highscore_write(self):
        if self.final_time_2 and self.final_time is not None:
            if self.protect_for_dictionary and self.protect_for_dictionary_2:
                with open("highscore.txt", "a") as inp:
                    for T, I in self.d_highscore.items():
                        inp.write("{}:{:5.2f}\n".format(T,I))
                inp.close()
                self.protect_for_dictionary = False


    def top_10_list(self):
        if self.protect_top10:
                self.last_result_print = False
                bx = 480
                by = 400
                WHITE = (255, 255, 255)
                GREY = (200, 200, 200)
                BLACK = (0, 0, 0)
                font = pygame.font.SysFont(None, 32)
                file = open("highscore.txt", 'r')
                lines = file.readlines()
                all_score = []
                for line in lines:
                    sep = line.index(':')
                    name = line[:sep]
                    score = line[sep + 1:-1]
                    all_score.append((score, name))
                file.close()
                all_score.sort(reverse=False)  # sort from smallest to largest
                best = all_score[:10]  # top 10 values
                # make the presentation box
                box = pygame.Surface((bx, by))
                box.fill(GREY)
                pygame.draw.rect(box, WHITE, (50, 12, bx - 100, 35), 0)
                pygame.draw.rect(box, WHITE, (50, by - 60, bx - 100, 42), 0)
                pygame.draw.rect(box, BLACK, (0, 0, bx, by), 1)
                txt_surf = font.render("HIGHSCORE", True, BLACK)  # headline
                txt_rect = txt_surf.get_rect(center=(bx // 2, 30))
                box.blit(txt_surf, txt_rect)
                txt_surf = font.render("Press ESC to continue", True, BLACK)  # bottom line
                txt_rect = txt_surf.get_rect(center=(bx // 2, 360))
                box.blit(txt_surf, txt_rect)
                for entry, i in enumerate(best):
                    txt_surf = font.render(i[1] + "  " + str(i[0]), True, BLACK)
                    txt_rect = txt_surf.get_rect(center=(bx // 2, 30 * entry + 60))
                    box.blit(txt_surf, txt_rect)
                    screen.blit(box, (0, 0))
                if pressed[pygame.K_ESCAPE]:
                    self.protect_top10 = False
                    self.last_result_print = True
                self.name_winner = False


class robot:  # we have 4 arg for this class, because joysticks get the same (value, axis) events

    def __init__(self, joy, ip, port):
        self.joy = joy
        self.ip = ip
        self.port = port
        self.robot_stopped = True
        self.rc_socket = socket.socket()

        self.update_control = False

        self.controlling_allowed = True
        self.controlling_allowed_2 = False
        self.controlling_keyboard = True

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

    def check_control(self):
        if not self.controlling_allowed:
            if self.robot_stopped:
                pass
                #print("check control -> already stopped")
            else:
                self.u1 = self.u2 = 0
                self.robot_stopped = True
                self.rc_socket.send('({},{})\n'.format(self.u1, self.u2).encode())

                print("check control -> stop")


    def control_alt(self):
        if self.controlling_allowed and self.controlling_allowed_2:
            ax1 = self.joystick.get_axis(1) * 0.75
            ax2 = self.joystick.get_axis(2) * 0.75
            ax3 = self.joystick.get_axis(3) * 0.75
            ax5 = self.joystick.get_axis(5) * 0.75

            u1_old = deepcopy(self.u1)
            u2_old = deepcopy(self.u2)

            threshold = 0.2
            if abs(ax1) < threshold and ax2 < threshold and abs(ax3) < threshold and ax5 < threshold and not self.robot_stopped:
                self.robot_stopped = True
                #print("all axis in neutral -> stopping")
                self.u1 = self.u2 = 0
                #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
            else:
                self.robot_stopped = False
                if abs(ax1) > threshold and abs(ax3) > threshold:
                    self.u1 = (-ax1 + ax3)/2.0
                    self.u2 = (-ax1 - ax3)/2.0
                    #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                elif abs(ax1) > threshold:
                    self.u1 = self.u2 = -ax1
                    #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                elif abs(ax3) > threshold:
                    self.u1 = ax3
                    self.u2 = -ax3
                elif ax2 > threshold:
                    self.u1 = ax2
                    self.u2 = ax2*0.75
                    #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())
                elif ax5 > threshold:
                    self.u1 = ax5*0.75
                    self.u2 = ax5
            if u1_old != self.u1 or u2_old != self.u2:
                #print("update_control = True")
                self.update_control = True


    def send_control(self):
        if self.update_control:
            #print("sending..({},{})\n".format(self.u1, self.u2))
            self.rc_socket.send('({},{})\n'.format(self.u1, self.u2).encode())


    def control_keyboard(self, event):  # keyboard control for robot1

        u1_old = deepcopy(self.u1)
        u2_old = deepcopy(self.u2)
        if self.controlling_keyboard:
            if pressed[pygame.K_LEFT]:
                self.u1 = -1.0
                self.u2 = 1.0
                #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

            elif pressed[pygame.K_RIGHT]:
                self.u1 = 1.0
                self.u2 = -1.0
                #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

            elif pressed[pygame.K_UP]:
                self.u1 = 1.0
                self.u2 = 1.0
                #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

            elif pressed[pygame.K_DOWN]:
                self.u1 = -1.0
                self.u2 = -1.0
                #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

            elif event.type == pygame.KEYUP:
                self.u1 = 0.0
                self.u2 = 0.0
                #selfd.rc_socket.send('({},{})\n'.format(self.u1, self.u2).encode())

            if u1_old != self.u1 or u2_old != self.u2:
                print("update_control = True")
                self.update_control = True

    def control_keyboard_2(self, event):  # keyboard control for robot2

        u1_old = deepcopy(self.u1)
        u2_old = deepcopy(self.u2)
        if self.controlling_keyboard:
            if pressed[pygame.K_a]:
                self.u1 = -1.0
                self.u2 = 1.0
                #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

            elif pressed[pygame.K_d]:
                self.u1 = 1.0
                self.u2 = -1.0
                #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

            elif pressed[pygame.K_w]:
                self.u1 = 1.0
                self.u2 = 1.0
                #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

            elif pressed[pygame.K_s]:
                self.u1 = -1.0
                self.u2 = -1.0
                #self.rc_socket.send('({},{})\n'.format(u1, u2).encode())

            elif event.type == pygame.KEYUP:
                self.u1 = 0.0
                self.u2 = 0.0
                #self.rc_socket.send('({},{})\n'.format(self.u1, self.u2).encode())

            if u1_old != self.u1 or u2_old != self.u2:
                print("update_control = True")
                self.update_control = True


def main():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((720, 576))
    rospy.init_node('game_node', anonymous=True)
    robot_1 = robot(0, '192.168.1.102', 1234)
    robot_1.joystick_init()
    robot_2 = robot(1, '192.168.1.101', 1234)
    robot_2.joystick_init()

    while True:

        robot_track = race_track(robot_1, robot_2)
        loop = True
        time.sleep(0.5)
        while loop:
            robot_track.check_number_marker()
            robot_track.polygon_rectangle()
            robot_track.checkpoint()
            robot_track.finish_line()
            robot_1.check_control()
            robot_2.check_control()

            robot_track.check_countdown()
            screen.fill((0, 0, 0))

            events = pygame.event.get()
            global pressed
            pressed = pygame.key.get_pressed()
            loop = robot_track.restart()
            robot_1.update_control = False
            robot_2.update_control = False
            input_1_recorded = False
            input_2_recorded = False
            for event in events:
                if event.type == pygame.JOYBUTTONDOWN:
                    robot_track.check_starting_position(robot_1, robot_2)
                    robot_track.start_countdown()
                if event.type == pygame.JOYAXISMOTION:
                    if event.joy == robot_2.joy:
                        robot_2.control_alt()
                        input_2_recorded = True

                    if event.joy == robot_1.joy:
                        robot_1.control_alt()
                        input_1_recorded = True

                else:

                    robot_track.player_name(event)

                    robot_1.control_keyboard(event)
                    robot_2.control_keyboard_2(event)
                    input_1_recorded = True
                    input_2_recorded = True


            if input_2_recorded:
                robot_2.send_control()
            if input_1_recorded:
                robot_1.send_control()

            robot_track.player_name_print_font()
            robot_track.highscore_write()
            robot_track.print_winner()
            robot_track.print_result()
            robot_track.top_10_list()
            robot_track.player_name_print()
            robot_track.time_robot_1_2()
            robot_track.print_countdown()
            robot_track.print_time_robot_1_2()
            robot_track.first_phrase()
            pygame.display.flip()


if __name__ == '__main__':
    main()