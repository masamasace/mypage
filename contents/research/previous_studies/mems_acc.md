---
title: "加速度MEMSセンサー"
date: "2024-01-17"
---

研究用で用いる加速度MEMSセンサーについて，少し調べたくなったのでメモとして残しておきます．現段階の用途としては地震計(微動計)への適用を考えています．

## [Analog Devices ADXL355](https://www.analog.com/en/products/adxl355.html)

- Analog Devices社製のMEMS型加速度センサー
    - AD変換器分解能：20bit
    - 低ノイズ密度：0.0245 cm/s^2/√Hz = 
        - 対象波形の上限周波数を100Hzとした場合にノイズレベルは0.245cm/s^2 (rms)程度となる．
- ODR(Output Data Rate)は Programmedの場合は4000Hzから3.96Hzまで11段階に設定可能
    - ローパスのデジタルフィルタは外すことができない一方で，ハイパスフィルタはバイパス可能
    - 最初にアナログ領域でローパス・アンチエイリアシングフィルタが作用する．(1.5kHzにおける固定帯域幅3dB)
    - 次に4000Hzで取得されたデータは1kHz付近で-3dBとなるようなデジタルフィルタが作用する
    - さらに4000Hz未満のODRが設定された場合には追加のデシメーションフィルタが作用する．
    - そして最後にハイパスフィルタをオプションで作用させることができる
        - 3ビットで7パターン設定可能
- データ取得の方式は直接読み取る方法とFIFOを用いる方法の2つがある？
    - DATA_RDYビットによってデータが取得可能になったのかを判断できる
    - FIFOメモリに入るデータと直接読み取るデータは全く同じなのか？
- 外部同期と外部クロックを有効にすることも可能で，この場合Programmed ODRを超えるが4000SPSを下回るデータ取得が可能？
    - SPSとODRのHzの違いがよくわからない．プログラム上でセットされたODRの値と実際に取得できるSPSは異なるということ？その場合にDATA_RDYビットやFIFOのEmpty Indicatorの値はどうなる？
> In this case, the data provided corresponds to the external SYNC signal, which can be greater than the set ODR and less than 4000 SPS, but the output pass band remains the same it was prior to the interpolation filter. 
- 適用事例もかなり豊富
    - [内田ら, 2023](https://www.jstage.jst.go.jp/article/jaee/23/2/23_2_58/_pdf/-char/ja)の論文にかなり豊富な知見が書かれている
        - 試作機では計測震度は±0.1以内に収まることを目標としていた
        - 気象庁検定では加振周波数は0.5Hzの一パターンのみ
        - モデル機(Type1)では最終的なサンプリング速度に見合った特性を越ためにデジタルフィルタを内装．
            - 「最終的なサンプリング速度に見合った特性」という言葉の意味は？
            - デジタルフィルタは800SPSのデータをサブCPUにて遮断周波数約40Hz，遮断特性-120dB (50Hz)の最小位相特性のフィルタ計算を実施
                - [気象庁の震動計算のためのフィルター特性](https://www.data.jma.go.jp/eqev/data/kyoshin/kaisetsu/calc_sindo.html)は20Hz以上の振動数成分に関しては1/40かそれ以下の補正係数がかかる
        - ケースの躯体はType1ではABS樹脂ケースを採用，Type2では鋼板を採用
        - ADXL355を3つ異なる方向に設置することによって，気象庁検定の審査項目である「センサーが直行して取り付けてあることを目視手で確認できる」をクリアした
    - 同型センサーのADXL354の検証では[栗田, 2019](https://www.jstage.jst.go.jp/article/jscejseee/75/4/75_I_657/_pdf)がある
    - 海外の論文だと[Datsyuk and Kuplovskyi, 2021](https://ieeexplore.ieee.org/document/9501105)など
        - Fig.4の結果はすごく魅力的ではあるけど本当かな…?
        - 全周波数帯域に渡って30μm/s^2 = 3.0×10-3 cm/s^2程度のフーリエ加速度振幅が出ている
            - スペックからするとかなり小さいのではないか？
    - またSpecsheetと同様の検討が[Ye et al., 2023](https://www.semanticscholar.org/reader/8dbc1d35a328af46f710ea0a3ea9874cb8c7639e)でも行われている．
        - Resolutionの定義をもう少し詳しく調べる必要があるが，0.655mgの解像度があるとしている．

## [EPSON M-A352AD10](https://www.epson.jp/prod/sensing_system/pdf/m-a352ad10_briefsheet_j_rev20220401.pdf)

[ナレッジフォーサイト社のHP](https://knowledgeforesight.com/jp/wp/wp-content/uploads/2022/09/YUREMON320220614.pdf)でADXL355を用いた地震計と並行してラインナップされているところから発見 (2024/01/17)
- ノイズ密度：0.2μg/√Hz
- 出力レンジ：±15G
- ビルトインローパスフィルタは9~460Hzまで選択可能
    - 可変ではないかもしれない
- ODRは最小50~最大1000SPS
- 3.3V入力電圧

## 現時点での疑問

- 検証用の振動台をどのように作成するのか
    - ステッピングモーターによる高周波ノイズは計測には影響しないのか？
    - どのような設計にすればいいのか？
