# -*- coding: utf-8 -*-

import cv2
import numpy as np
import collections

# 減色処理
def sub_color(src, K):
    # 次元数を1落とす
    Z = src.reshape((-1,3))

    # float32型に変換
    Z = np.float32(Z)

    # 基準の定義
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # K-means法で減色
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # UINT8に変換
    center = np.uint8(center)

    res = center[label.flatten()]

    # 配列の次元数と入力画像と同じに戻す
    return res.reshape((src.shape))

# モザイク処理
def mosaic(img, width, height):
    # 画像の高さ、幅、チャンネル数
    h, w, ch = img.shape

    # 縮小→拡大でモザイク加工
    img = cv2.resize(img,(int(width), int(height)))

    return img

# ドット絵化
def pixel_art(img, width, height, K):
    # モザイク処理
    img = mosaic(img, width, height)

    # 減色処理
    img = sub_color(img, K)

    return img

# ラベル化
def num3label(x, y, z):
    label = str(x)+'+'+str(y)+'+'+str(z)
    return label


if __name__ == '__main__':

    width = 32
    height = 32
    colornum = 16

    step_hue = 32 # 色相段数
    step_stc = 16 # 彩度段数
    step_vlb = 16 # 明度段数

    # 入力画像を取得
    img = cv2.imread("./raw.png")

    # ドット絵化
    img = pixel_art(img, width, height, colornum)
        
    # ドット絵をファイル出力
    cv2.imwrite("./dot.png", img)

    # 色配列の変換(BGR->HSV)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 色カウント(多く使われている色から降順ソート)
    dict_color = {}
    img_array = np.asarray(img) #numpyで扱える配列をつくる
    for x in range(0, width):
        for y in range(0, height):
            print(img_array[x,y,])
            color = num3label(int(img_array[x,y,0]*2),int(img_array[x,y,1]/step_stc),int(img_array[x,y,2]/step_vlb))
            if color not in dict_color:
                dict_color[color] = 0
            else:
                dict_color[color] = dict_color[color] + 1
    dict_color = sorted(dict_color.items(), key=lambda x:-x[1])
    print(dict_color)

# Excelファイル出力

