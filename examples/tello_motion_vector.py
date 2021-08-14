from common_7 import *

TIMEOUT_SEC = 0.1

@timeout(TIMEOUT_SEC)
def input_with_timeout(msg=None):
   return input(msg)

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()
img = frame_read.frame
# motion vector可視化
# 縮小画像取得
frame1 = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)

hsv = np.zeros_like(frame1)
hsv[...,1] = 255

while True:
    img = frame_read.frame
    image = img.copy()
    image2 = img.copy()

    # motion vector可視化
    rgb2, next = get_motion_vector_img(img, prvs)

    # Telloの現在高度（ToFセンサ計測距離(cm)、高さ（cm)）とバッテリ残量を取得する
    #https://djitellopy.readthedocs.io/en/latest/tello/#djitellopy.tello.Tello.query_battery
    time_of_flight_distance_senser_val = tello.get_distance_tof()
    input_text_1 = "ToF Distane {0} cm".format(time_of_flight_distance_senser_val)
    
    height = tello.get_height()
    input_text_2 = "Height {0} cm".format(height)
    
    bettery = tello.query_battery()
    input_text_3 = "Battery {0} %".format(bettery)
    # ウィンドウのサイズが小さいので、大きくする
    height = rgb2.shape[0]
    width = rgb2.shape[1]
    motion_vector_img = cv2.resize(rgb2, (int(3.0*width), int(3.0*height)))

    prvs = next

    # 物体検出矩形表示と人物検出人数の文字列埋込み表示の画像を取得
    # 物体の運動ベクトルを線で書き込んだ画像（motion_vector_img)ではなく、
    # 何も書き込まれていないカメラ画像(image)をもとに解析を行う。
    # motion_vector_imgとimageは同じタイミングでTelloから取得済み。
    
    label_name  = "person"
    bbox, label, conf = cvl.detect_common_objects(image)
    obejct_detected_img = draw_bbox(image, bbox, label, conf)
    
    input_text_4 = "Num of detected {0}(s) is {1}".format(label_name, str(label.count(label_name)))
    
    # 2つの画像、motion_vector_imgとobejct_detected_imgを重ね合わせる
    # 最初に、2つの画像の縦横サイズを揃える
    height_0 = motion_vector_img.shape[0]
    width_0 = motion_vector_img.shape[1]
    resized_obejct_detected_img = cv2.resize(obejct_detected_img, (width_0, height_0))
    # 同じサイズになった2つの画像を重ね合わせる
    # https://atatat.hatenablog.com/entry/opencv3_overlay
    # https://code-graffiti.com/blending-images-with-opencv-in-python/
    blended_img = cv2.addWeighted(src1=motion_vector_img, alpha=0.5, src2=resized_obejct_detected_img, beta=0.5, gamma=0)

    # 画像にTelloの現在高度（ToFセンサ計測距離(cm)、高さ（cm)）とバッテリ（%）を埋込む
    cv2.putText(blended_img, str(input_text_1), (0, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blended_img, str(input_text_2), (0, 150), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blended_img, str(input_text_3), (0, 200), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    # カメラ画像に物体検出矩形表示と人物検出人数の文字列埋込み表示を埋込む
    cv2.putText(blended_img, str(input_text_4), (0, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

    # 重ね合わせた画像を1.7倍に縦横同じ比率で拡大する
    height_1 = blended_img.shape[0]
    width_1 = blended_img.shape[1]
    resized_blended_img = cv2.resize(blended_img, (int(1.7*width_1), int(1.7*height_1)))

    # Escキー押下で終了
    if cv2.waitKey(20) == ESC_KEY:
        break

    # 1.7倍に拡大した画像をウィンドウに出力する
    cv2.namedWindow("Blended", cv2.WINDOW_NORMAL)
    cv2.imshow("Blended", resized_blended_img)
    
    #次の行（key = cv2.・・・）を削除すると、画像が受信できなくなる。
    key = cv2.waitKey(1) & 0xff
    
    try:
        msg = input_with_timeout('\n{}秒以内に操作コマンドを入力して下さい :'.format(TIMEOUT_SEC))
        print('\n操作コマンド：　{} を受信しました。\n'.format(msg))
        if msg == "i":
            tello.takeoff()
        elif msg == "w":
            tello.move_forward(30)
        elif msg == "s":
            tello.move_back(30)
        elif msg == "a":
            tello.move_left(30)
        elif msg == "d":
            tello.move_right(30)
        elif msg == "e":
            tello.rotate_clockwise(30)
        elif msg == "q":
            tello.rotate_counter_clockwise(30)
        elif msg == "r":
            tello.move_up(30)
        elif msg == "f":
            tello.move_down(30)
        elif msg == "g":
            tello.land()
        elif msg == "p":
            dt_now = datetime.datetime.now()
            timestamp_str = dt_now.strftime('%Y年%m月%d日%H:%M:%S')
            file_name = "frame_img_shot_{0}.jpg".format(timestamp_str)
            cv2.imwrite(file_name, resized_blended_img)
            print("フレーム画像を保存しました。")
    except TimeoutError:
        print('\n操作コマンド入力時間切れ。次のフレーム画像を読み込みます。\n')

tello.land()
