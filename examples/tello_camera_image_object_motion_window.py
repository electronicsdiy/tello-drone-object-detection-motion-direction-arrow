from common_2 import *

TIMEOUT_SEC = 0.1

@timeout(TIMEOUT_SEC)
def input_with_timeout(msg=None):
   return input(msg)


tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

# 表示ウィンドウの初期化
#cv2.namedWindow("motion")
# ビデオデータの読み込み
#video = cv2.VideoCapture(VIDEO_DATA)
video = tello.get_frame_read()

# 最初のフレームの読み込み
#end_flag, frame_next = video.read()
frame_next = frame_read.frame

height, width, channels = frame_next.shape
motion_history = np.zeros((height, width), np.float32)
frame_pre = frame_next.copy()

while True:
    img = frame_read.frame
    #cv2.imshow("drone", img)
    #cv2.imshow('Canny', cv2.Canny(img, 100, 200))
    #bitwised_img = cv2.bitwise_not(img)
    #cv2.imshow('Bitwised', bitwised_img)
    # 新しいフレームの読み込み
    #end_flag, frame_next = video.read()
    frame_next = img.copy()
    
    image = img.copy()
    
    #######特徴点を検出した物体の運動ベクトルを矢印表示する処理（開始）
        # フレーム間の差分計算
    color_diff = cv2.absdiff(frame_next, frame_pre)

    # グレースケール変換
    gray_diff = cv2.cvtColor(color_diff, cv2.COLOR_BGR2GRAY)

    # ２値化
    retval, black_diff = cv2.threshold(gray_diff, 30, 1, cv2.THRESH_BINARY)

    # プロセッサ処理時間(sec)を取得
    # Python 3.9系ではtime.clock()はない。
    # proc_time = time.clock()
    # https://stackoverflow.com/questions/58569361/attributeerror-module-time-has-no-attribute-clock-in-python-3-8
    
    proc_time = time.process_time()

    # モーション履歴画像の更新
    #https://qiita.com/hitomatagi/items/d5d475a446ec9c73261e
    #https://qiita.com/fiftystorm36/items/1a285b5fbf99f8ac82eb
    #pip install opencv-contrib-python
    cv2.motempl.updateMotionHistory(black_diff, motion_history, proc_time, DURATION)
    # 古いモーションの表示を経過時間に応じて薄くする
    hist_color = np.array(np.clip((motion_history - (proc_time - DURATION)) / DURATION, 0, 1) * 255, np.uint8)

    # グレースケール変換
    hist_gray = cv2.cvtColor(hist_color, cv2.COLOR_GRAY2BGR)

    # モーション履歴画像の変化方向の計算
    #   ※ orientationには各座標に対して変化方向の値（deg）が格納されます
    mask, orientation = cv2.motempl.calcMotionGradient(motion_history, 0.25, 0.05, apertureSize = 5)

    # 各座標の動きを緑色の線で描画
    width_i = GRID_WIDTH
    while width_i < width:
        height_i = GRID_WIDTH
        while height_i < height:
            # 座標点の描画を削除
            angle_deg = orientation[height_i - 1][width_i - 1]
            if angle_deg > 0:
                angle_rad = math.radians(angle_deg)
                cv2.arrowedLine(frame_pre, \
                pt1=(width_i, height_i), \
                pt2=(int(width_i + math.cos(angle_rad) * LINE_LENGTH_GRID), int(height_i + math.sin(angle_rad) * LINE_LENGTH_GRID)), \
                color=(255, 0, 0),
                thickness=2,
                line_type=cv2.LINE_4,
                shift=0,
                tipLength=0.5)
            else:
                #追記
                angle_rad = 10

            height_i += GRID_WIDTH

        width_i += GRID_WIDTH


    # 全体的なモーション方向を計算
    angle_deg = cv2.motempl.calcGlobalOrientation(orientation, mask, motion_history, proc_time, DURATION)

    # 全体の動きを黄色い線で描画
    # 座標点を削除する
    cv2.arrowedLine(frame_pre, \
                pt1=(int(width / 2), int(height / 2)), \
                pt2=(int(width / 2 + math.cos(angle_rad) * LINE_LENGTH_ALL), int(height / 2 + math.sin(angle_rad) * LINE_LENGTH_ALL)), \
                color=(0, 0, 255),
                thickness=3,
                line_type=cv2.LINE_4,
                shift=0,
                tipLength=0.5)

    # モーション画像を表示
    # frame_preに変更
    #cv2.imshow("motion", frame_pre)

    # Escキー押下で終了
    if cv2.waitKey(20) == ESC_KEY:
        break

    # 現在のフレームを別名で保存
    current_motion_arrow_engraved_frame = frame_pre.copy()
    #（次のフレームを読み込むときには、現在のフレームは過去のフレームとなるため）
    frame_pre = frame_next.copy()
    #######特徴点を検出した物体の運動ベクトルを矢印表示する処理（以上）

    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    cv2.imshow("Video", current_motion_arrow_engraved_frame)
    
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
            cv2.imwrite(file_name, current_motion_arrow_engraved_frame)
            print("フレーム画像を保存しました。")
    except TimeoutError:
        print('\n操作コマンド入力時間切れ。次のフレーム画像を読み込みます。\n')

tello.land()
