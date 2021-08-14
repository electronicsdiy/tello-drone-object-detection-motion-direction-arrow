import numpy as np
import cv2

# オプティカルフロー解析描画
def drawOptFlow(img, gray, flow, step=16, dispsc=10):
    cimg    = img.copy()
    h, w    = img.shape[:2]
    y, x    = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    dx, dy  = flow[y,x].T * dispsc
    dist = np.sqrt(dx**2+dy**2)
    idx     = np.where(3 < dist)
    x, y    = x[idx], y[idx]
    dx, dy  = dx[idx], dy[idx]
    lines = np.vstack([x, y, x+dx, y+dy]).T.reshape(-1, 2, 2)
    lines = lines.astype(np.int32)
    fx, fy = flow[y,x].T
    cv2.polylines(cimg, lines, False, (255, 0, 255), 1, 8)
    return cimg

def get_motion_vector_img(frame, prvs):
    # 縮小画像取得
    frame2 = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    # オプティカルフロー解析
    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # オプティカルフロー解析描画
    rgb2 = drawOptFlow(frame2, next, flow, 16)
    
    return rgb2, next
