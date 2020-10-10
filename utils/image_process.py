#!/usr/bin/env python
# encoding: utf-8
"""
@author: czm
@file: image_process.py
@time: 2020/7/8 13:33
@desc:
"""
from pyzbar.pyzbar import decode
import datetime
import os
import time
import cv2
from skimage.measure import compare_ssim
from utils.air_cv import aircv
from utils.air_cv.transform import TargetPos
from utils.cv import Template


screenshot_dir = ""             # 截图保存的路径
img_recog_path = ""               # 用于比对的图片存放的路径

SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79


def exists(image_path, target_image=None, driver=None, timeout=20, need_completing_img_path=True):
    """
        图片是否存在
    :param image_path: 截取的图片的存放路径
    :param target_image:
    :param driver:
    :param timeout:
    :return: pos if exists,else False
    """
    try:
        pos = find_image(image_path, target_image=target_image, driver=driver, timeout=timeout,
                         need_completing_img_path=need_completing_img_path)
    except Exception as e:
        print(e.args)
        return False
    else:
        return pos


def completing_image_path(image_name, need_completing_img_path):
    """
        用于补全图片路径
    :param image_name: 图片文件名
    :return: 图片的路径
    """
    if need_completing_img_path:
        if "." in image_name:  # 如果传入带后缀名的文件名，直接使用传入的文件名
            return img_recog_path + image_name
        else:  # 如果不带后缀名，默认为png格式
            return img_recog_path + image_name + ".png"
    else:
        return image_name


def find_image(image_name, target_image=None, driver=None, target_pos=TargetPos.MID, timeout=20, threshold=None,
               interval=0.5,
               intervalfunc=None,
               need_completing_img_path=True):
    """
        用于查找图片对应坐标
    :param need_completing_img_path:
    :param image_name: 要查找坐标的图片文件名
    :param target_image: 用于比对的图片
    :param driver:
    :param target_pos: 目标坐标位置，默认中心位置
    :param timeout:
    :param threshold:
    :param interval:
    :param intervalfunc:
    :return: 匹配到的坐标信息
    """
    # 根据图片名称，补全图片路径
    image_path = completing_image_path(image_name, need_completing_img_path)
    start_time = time.time()    # 记录开始查找时间
    query = Template(image_path, target_pos=target_pos, resolution=(1920, 1080))        # 默认在1920*1080分辨率截图
    while True:
        if target_image:    # 如果传入target,直接进行比对
            if need_completing_img_path:
                if os.path.isabs(target_image):  # 如果传入的target是绝对路径，直接使用，否则，默认在img_recog_path路径下
                    imread_path = target_image
                else:
                    imread_path = completing_image_path(target_image)
            else:
                imread_path = target_image
            screen = aircv.imread(imread_path)
        else:           # 如果不传入target，自动获取当前设备屏幕截图用于比对
            screen = take_screenshot(driver)
        if screen is None:
            print("Screen is None, may be locked")
        else:
            if threshold:
                query.threshold = threshold
            match_pos = query.match_in(screen)      # 进行图像比对，返回对应坐标信息
            if match_pos:
                return match_pos

        if intervalfunc is not None:
            intervalfunc()

        # 超时则raise，未超时则进行下次循环:
        if (time.time() - start_time) > timeout:
            raise Exception('Picture %s not found in screen' % query)
        else:
            time.sleep(interval)


def image_compare(image1, image2):
    """
        两图像进行比对
    :param image1:
    :param image2:
    :return:
    """
    image_a = cv2.imread(image1)
    image_b = cv2.imread(image2)
    gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(gray_a, gray_b, full=True)
    print(score, diff)
    return score, diff


def mk_screenshot_dir():
    """创建截图保存目录"""
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)


def screenshot(file_path, driver):

    driver.get_screenshot_as_file(file_path)
    pic = aircv.imread(file_path)
    return pic


def take_screenshot(driver, filename=None):
    """
        获取屏幕截图
    :param driver: appium webdriver
    :param filename: 指定文件名
    :return:
    """
    mk_screenshot_dir()
    if filename:
        image_path = screenshot_dir + filename + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ".png"
        return driver.get_screenshot_as_file(image_path)
    image_path = screenshot_dir + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ".png"
    return screenshot(image_path, driver)


def qrcode_recongnize(filename):
    image = cv2.imread(filename)
    result = decode(image)
    # result = 1
    if len(result) > 0:
        return True
    else:
        return False


if __name__ == '__main__':
    a = exists("pen.png", "1.png", need_completing_img_path=False)
    print(a)
