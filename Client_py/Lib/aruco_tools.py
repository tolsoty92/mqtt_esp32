from math import sqrt, acos, degrees, pi
from random import randint
from cv2 import line

def line_middle(pt1, pt2):
    middle = tuple(map(lambda x: int(x), ((pt1[0] + pt2[0] ) / 2, (pt1[1] + pt2[1]) / 2)))
    return middle

def detect_direction(markers_cornres):
    front_left_corner = tuple(markers_cornres[0][0])
    front_right_corner = tuple(markers_cornres[0][1])
    behind_right_corner = tuple(markers_cornres[0][2])
    direction_point = line_middle(front_left_corner, front_right_corner)
    cntr= line_middle(front_left_corner, behind_right_corner)
    return direction_point, cntr

def find_direction_point(direction, center):
    x_cnt, y_cnt = center[0], center[1]
    x_dir, y_dir = direction[0], direction[1]
    x_3rd = x_dir + (x_dir - x_cnt)*1.5
    if (x_dir - x_cnt) != 0:
        y_3rd = (x_3rd - x_cnt) * (y_dir - y_cnt) / (x_dir - x_cnt) + y_cnt
    else:
        y_3rd = (x_3rd - x_cnt) * (y_dir - y_cnt) / 1 + y_cnt
    return tuple(map(lambda x: int(x), (x_3rd, y_3rd)))

def find_angle_error(direction, cntr, dist_pt):
    dir_vec = (direction[0] - cntr[0]), (direction[1] - cntr[1])
    trajectory_vec = (dist_pt[0] - cntr[0]), (dist_pt[1] - cntr[1])
    scalar_multiply = dir_vec[0] * trajectory_vec[0] + dir_vec[1] * trajectory_vec[1]
    dir_vec_module = sqrt(dir_vec[0] ** 2 + dir_vec[1] ** 2)
    trajectory_vec_module = sqrt(trajectory_vec[0] ** 2 + trajectory_vec[1] ** 2)
    if (trajectory_vec_module * dir_vec_module) != 0:
        cos_a = scalar_multiply / (trajectory_vec_module * dir_vec_module)
        angle = round(degrees(acos(min(1, max(cos_a, -1)))))
    else:
        angle = 0
    return angle

def find_point_to_check_angle(direction, center, dist_pt):
    x_cnt, y_cnt = center[0], center[1]
    x_dir, y_dir = direction[0], direction[1]
    x_dist, y_dist = dist_pt[0], dist_pt[1]
    x_3rd = x_dir
    if (x_dist - x_cnt) != 0:
        y_3rd = (x_3rd - x_cnt) * (y_dist - y_cnt) / (x_dist - x_cnt) + y_cnt
    else:
        y_3rd = (x_3rd - x_cnt) * (y_dist - y_cnt) / 1 + y_cnt
    return tuple(map(lambda x: int(x), (x_3rd, y_3rd)))

def find_angle_direction(direction, cntr, dist_pt, angle):
    pt3 = find_point_to_check_angle(direction, cntr, dist_pt)
    if cntr[0] <= dist_pt[0]:
        if direction[1] >= pt3[1]:
            res_angle = -angle
        else:
            res_angle = angle
    else:
        if direction[1] >= pt3[1]:
            res_angle = angle
        else:
            res_angle = -angle
    return res_angle

def is_it_checkpoint(platform_cntr, destination_point):
    eps = 80
    distance = sqrt((platform_cntr[0] - destination_point[0]) ** 2 + (platform_cntr[1] - destination_point[1]) ** 2)
    if distance > eps:
        return False
    else:
        return True

def generate_dst_pt(width, height):
    eps = 70
    x = randint(eps, width - eps)
    y = randint(eps, height - eps)
    return (x, y)

def draw_dst_pt(img, pt):
    size = 15
    pt1 = (pt[0] - size, pt[1])
    pt2 = (pt[0] + size, pt[1])
    pt3 = (pt[0], pt[1] - size)
    pt4 = (pt[0], pt[1] + size)
    line(img, pt1, pt2, (0, 50, 255), 2)
    line(img, pt3, pt4, (0, 50, 255), 2)


