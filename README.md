# Display Tello Drone's 1st Person Camera's Detected Objection Information, those Objects' Motion Vector, and Drone's Status Information

- Telloをホバリング飛行させて、Tello自身の動きがない状況を作り、被写体の動きの方向を線で可視化できるか実験した
- テレビカメラの正面でホバリングを行い、テレビ画面の中の人物や物体の動きをTelloのカメラに見せた
- ウィンドウに表示される画像は、Telloの動きから5秒ほど遅延した （Macbookの計算速度のスペックの問題）
- MP4ファイルを入力したときは、物体の動きの方向（＋速度）をきれいに可視化できたが、今回はきれいに描画できなかった

![frame_img_shot_2021年08月15日00:02:34](https://user-images.githubusercontent.com/87643752/129451803-c307e57f-f89b-46a0-8f70-a71d7c211d0f.jpg)

![frame_img_shot_2021年08月14日23:21:16](https://user-images.githubusercontent.com/87643752/129451825-1dbd6458-e297-4d24-97ae-1f13ab9b7e90.jpg)

![frame_img_shot_2021年08月14日23:59:28](https://user-images.githubusercontent.com/87643752/129451839-927051d6-de42-4ed7-87f5-0ed01ccfc7d0.jpg)


## 解説記事

#### [作成中]()

## **使い方** 

1. このリポジトリの資源をgit cloneしたノートPCを、TelloにWifi接速する。
2. **examplesディレクトリ**に移動して、Python3系で、**python3 tello_motion_vector.py**を実行する。

> % python3 motion_arrow_flight_info.py


## 1. Telloドローンのキーボード操作

TelloとWifi回線でつながっているノートPCのキーボードから、Telloを操作します。

* i : 離陸
* w: 前進
* s : 後進
* a : 左移動
* d : 右移動
* e : 時計回り30度回転
* q : 反時計回り30度回転
* r :  上昇
* f :  降下
* g : 着地
* p : フレーム画像のファイル保存（※）

※ 画像ファイルは、カレントディレクトリ（exampleディレクトリ直下）に出力されます。

※ ファイル名は、**frame_img_shot_XXXX年XX月XX日XX/XX/XX.jpg**です。最後はhour, minutes, ミリ秒です。

## 2. Telloカメラ画像のウィドウ表示（左右２画面）

離陸前から、ノートPCにWindowが１つ立ち上がり、特徴点を検出した人物や動物、物体の運動ベクトル（方角＋速度）の推定結果を、矢印で表示します。（青矢印）
青矢印は、対象となる物体の内部や外周の複数の座標位置に表示されます。各矢印は、それぞれの位置における対象物体（人間、動物を含む）の運動ベクトルを示しています。

また、画面全体の移動の運動ベクトルを、赤矢印（１つだけ）表示します。

さらに画面の左上に、Telloドローンの現在高度が表示されます。

画面の左側に表示されるTelloカメラ画像の受信と、PCのキーボード入力によるTelloの操縦は、**DJITelloPyライブラリ**を使います。

- https://github.com/damiafuentes/DJITelloPy

## __事前準備__

### このリポジトリの資源の取得

このリポジトリ内の資源を、ここにある通りのディレクトリ構成でダウンロードしてください。
（git clone又は手動zipダウンロード）

