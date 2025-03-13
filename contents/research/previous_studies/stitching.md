---
title: "スティッチングについて"
date: "2024-04-12"
---

## スティッチングとは
- スティッチングとは、複数の画像を結合して1枚の画像にする処理のこと
- 画像の重なり具合を調整することで、自然な画像を作成できる

## スティッチングの手順
- スティッチングの手順は以下の通り
1. 画像のひずみを除去する
    1. 歪み補正を行う
    1. 画像を正距円筒画像に変換する
1. 特徴点を抽出する
    1. SIFTやSURFなどのアルゴリズムを使用する
1. 特徴点をマッチングする
    1. k近傍法やRANSACなどのアルゴリズムを使用する
1. 画像を変換する
    1. ホモグラフィ行列を計算する
    1. 透視変換を行う
    1. 画像を結合する

## それぞれのアルゴリズムについて
### 歪補正
- 歪み補正とは、レンズの歪みを補正する処理のこと
- 歪み補正を行うことで、画像の歪みを除去し、自然な画像を作成できる
- Pythonでのコード例
```python
import cv2
def undistort_image(image_path):
    # 画像の読み込み
    image = cv2.imread(image_path)

    # 歪み補正のためのパラメータを設定
    K = np.array([[focal_length, 0, image_width / 2],
                  [0, focal_length, image_height / 2],
                  [0, 0, 1]])
    D = np.array([k1, k2, p1, p2, k3])

    # 歪み補正を行う
    undistorted_image = cv2.undistort(image, K, D)

    return undistorted_image
```
- 正距円筒画像に変換する
    - 正距円筒画像とは、球面を平面に投影した画像のこと
    - 360度カメラの画像をスティッチングする際には、正距円筒画像に変換することが一般的
    - Pythonでのコード例
    ```python
    import cv2
    def equirectangular_image(image_path):
        # 画像の読み込み
        image = cv2.imread(image_path)

        # 正距円筒画像に変換
        equirectangular_image = cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR)

        return equirectangular_image
    ```
- 画像のひずみを除去するためには、カメラのキャリブレーションを行う必要がある
- キャリブレーションとは、カメラの内部パラメータ（焦点距離、レンズの歪みなど）を推定する処理のこと
- キャリブレーションを行うことで、画像のひずみを除去するためのパラメータを取得できる
- キャリブレーションの手順は以下の通り
    1. 平面にチェッカーボード(白黒の格子状のパターン)を置く
    1. 画像を撮影する
    1. チェッカーボードのコーナーを検出する
    1. 内部パラメータを推定する
- Pythonでのコード例
```python
import cv2
def calibrate_camera(image_paths):
    # チェッカーボードのサイズ
    pattern_size = (8, 6)

    # チェッカーボードのコーナーを検出するためのパラメータ
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # チェッカーボードのコーナーを検出する
    objpoints = []
    imgpoints = []
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    for image_path in image_paths:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

    # 内部パラメータを推定する
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return mtx, dist
```

### 特徴点抽出
- SIFTやSURFなどのアルゴリズムを使用する
- SIFTのアルゴリズムの詳細
    - SIFTはScale-Invariant Feature Transformの略
        - スケール不変特徴変換と訳せる
    - SIFT以前ではHarrisの手法などを用いることによって回転不変(回転に対してロバスト)なエッジ検出が可能であった
    - しかし，スケール不変性については，Harrisの手法では対応できなかった
    - 特徴点の抽出は以下のように行う
        - 極値検出
            - ある画像に対してガウシアンフィルタを作用させ，その後にラプラシアンフィルタを作用させる
                - ラプラシアンフィルタとは，画像の輪郭を抽出するフィルタ
                - ある画像の位置$(i, j)$におけるピクセルの値を$f(i, j)$とすると，ラプラシアンフィルタを作用させた後の画像の位置$(i, j)$におけるピクセルの値は，$f(i, j) - \frac{1}{4}(f(i+1, j) + f(i-1, j) + f(i, j+1) + f(i, j-1))$となる
                    - なおこれは4近傍カーネルの場合であり，8近傍カーネルの場合は，$f(i, j) - \frac{1}{8}(f(i+1, j) + f(i-1, j) + f(i, j+1) + f(i, j-1) + f(i+1, j+1) + f(i-1, j-1) + f(i+1, j-1) + f(i-1, j+1))$となる
            - ただ実際には計算量が大きくなるためラプラシアンフィルタの代わりに差分フィルタを作用させる
                - 何と何の差分を取るのかはよくわからない

        - 特徴点の局所領域の特定
    - Pythonでのコード例
    ```python
    import cv2
    def sift_feature(image_path):
        # 画像の読み込み
        image = cv2.imread(image_path)

        # SIFTのインスタンスを生成
        sift = cv2.SIFT_create()

        # 画像から特徴点を抽出
        keypoints, descriptors = sift.detectAndCompute(image, None)

        return keypoints, descriptors
    ```
- SURFのアルゴリズムの詳細
    - SURFは、SIFTの高速版
    - Pythonでのコード例
    ```python
    import cv2
    def surf_feature(image_path):
        # 画像の読み込み
        image = cv2.imread(image_path)

        # SURFのインスタンスを生成
        surf = cv2.xfeatures2d.SURF_create()

        # 画像から特徴点を抽出
        keypoints, descriptors = surf.detectAndCompute(image, None)

        return keypoints, descriptors
    ```

### 特徴点マッチング
- 特徴点の距離を計算して、最も近い特徴点同士をマッチングする
- マッチングのアルゴリズムには、k近傍法やRANSACなどがある
- k近傍法
    - ある特徴点に対して、最も近いk個の特徴点を見つけるアルゴリズム
    - Pythonでのコード例
    ```python
    import cv2
    import numpy as np
    def knn_match(des1, des2):
        # k近傍法のインスタンスを生成
        bf = cv2.BFMatcher()
        
        # 特徴量同士をマッチング
        matches = bf.knnMatch(des1, des2, k=2)
        
        # 良いマッチング点を選択
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)
        
        return good
    ```
- RANSAC
    - ランダムに特徴点を選択して、モデルを推定するアルゴリズム
    - Pythonでのコード例
    ```python
    import cv2
    import numpy as np
    def ransac_match(keypoints1, keypoints2, good_matches):
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        
        # RANSACを適用
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        
        return M, mask
    ```

### 画像変換
- ホモグラフィ行列を計算する
    - ホモグラフィ行列とは:
        - 2つの画像の特徴点同士の対応関係を表す行列
- 透視変換を行う
    - 透視変換とは:
        - 画像を平面から見た視点を変換する処理
- Pythonでのコード例
```python
import cv2
import numpy as np
def warp_image(image1, image2, M):
    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]
    
    # 画像1を変換
    image1_warp = cv2.warpPerspective(image1, M, (w1+w2, h1))
    
    # 画像2をコピー
    image2_copy = image2.copy()
    
    # 画像1と画像2を結合
    image2_copy[:h1, :w1] = image1_warp
    
    return image2_copy
```

## 疑問



## 参考文献・リンク
- C++ベースのスティッチングライブラリ
    - https://github.com/drNoob13/fisheyeStitcher
- 360度カメラの画像をスティッチングするためのリポジトリ
    - https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
- OpenCVの公式ドキュメント
    - https://docs.opencv.org/4.x/d2/d8d/classcv_1_1Stitcher.html




