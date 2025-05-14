---
title: "QGISの使い方 (Part 2)"
date: "2025/05/15"
---

# はじめに

QGISの使い方についてまとめたページです．内容については整理されておらず雑多である点をご承知おきください...

## 環境例
- OS: Windows 11 24H2 26100.4061
- QGIS: 3.40.3
- Python: 3.12.0

## VSCodeによるQGISにバンドルされたPythonを使用する方法

### Pythonインタープリターの設定

1. QGISにバンドルされたPythonのパスを確認
    - 自分の場合は`C:\Program Files\QGIS 3.40.3\apps\Python312\python3.exe`でした
    - QGISのバージョンによって異なるので，適宜変更してください
    - QGISのフォルダの中には複数のPythonがありますが、`bin`フォルダの中にあるものは使わないでください

1. VSCodeを開きます。
    - `Ctrl + Shift + P`でコマンドパレットを開きます
    - `Python: Select Interpreter`と入力し、クリックします
    - `Enter interpreter path...`を選択します
    - 先ほど確認したQGISにバンドルされたPythonのパスを指定します
    - `Enter`を押します
    - `Python 3.12.0 64-bit ('QGIS 3.40.3': venv)`のようなものが表示されるので，それを選択します

### settings.jsonの設定
1. `Ctrl + Shift + P`でコマンドパレットを開きます
1. `Preferences: Open Settings (JSON)`と入力し、クリックします
1. `settings.json`が開かれるので，以下のように編集します
    ```json
    {
        "python.analysis.extraPaths": [
        "C:/Program Files/QGIS 3.40.3/apps/qgis/python",
        "C:/Program Files/QGIS 3.40.3/apps/qgis/python/plugins",
        "C:/Program Files/QGIS 3.40.3/apps/Python312/Lib/site-packages"
        ],
        "python.defaultInterpreterPath": "C:/Program Files/QGIS 3.40.3/apps/Python312/python3.exe"
    }

    ```
    - `python.analysis.extraPaths`の部分は，QGISのバージョンによって異なるので，適宜変更してください
    - `python.defaultInterpreterPath`の部分は，QGISにバンドルされたPythonのパスを指定してください
        - 今回であれば上記で確認した`C:\Program Files\QGIS 3.40.3\apps\Python312\python3.exe`を指定します
    - また，`/`でパスを区切る必要があります
        - `\`で区切るとエラーが出ます
        - 例: `C:\Program Files\QGIS 3.40.3\apps\Python312\python3.exe`は`C:/Program Files/QGIS 3.40.3/apps/Python312/python3.exe`と書き換える必要があります
1. `settings.json`を保存します

### 初期化用モジュール ('qgis_env.py') の作成

qgis関連のモジュールをインポートするための初期化用モジュールを作成します．ここでは環境変数の設定を行います．

1. `qgis_env.py`という名前のファイルを作成し、以下のように記述します。

    ```python
    import os
    import sys

    # QGISインストールルート（必要に応じて変更）
    QGIS_ROOT = r"C:\Program Files\QGIS 3.40.3"

    # パス構成 (適宜変更)
    qgis_python = os.path.join(QGIS_ROOT, 'apps', 'qgis', 'python')
    qgis_plugins = os.path.join(qgis_python, 'plugins')
    qgis_prefix = os.path.join(QGIS_ROOT, 'apps', 'qgis')
    qt_plugins = os.path.join(QGIS_ROOT, 'apps', 'Qt6', 'plugins')
    qgis_bin = os.path.join(QGIS_ROOT, 'apps', 'qgis', 'bin')

    # sys.pathに追加
    sys.path.insert(0, qgis_python)
    sys.path.insert(0, qgis_plugins)

    # DLLパスを環境変数PATHに追加（これが非常に重要）
    os.environ['PATH'] = qgis_bin + os.pathsep + os.environ['PATH']

    # QGISランタイムのための環境変数
    os.environ['QGIS_PREFIX_PATH'] = qgis_prefix
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugins

    # QGISのimport（この時点でDLLが読めるようになっている必要がある）
    from qgis.core import QgsApplication

    def setup_qgis():
        qgs = QgsApplication([], False)
        qgs.initQgis()
        return qgs

    ```

    - 各パス (`qgis_python`, `qgis_plugins`, `qgis_prefix`, `qt_plugins`, `qgis_bin`) はQGISのインストールパスに基づいています。必要に応じて変更してください。
    - `QGIS_ROOT`はQGISのインストールパスを指定します。必要に応じて変更してください。

1. `qgis_env.py`を保存します
1. これが終わったら自分が書いたpythonスクリプトの最初に以下のように書きます

    ```python
    import qgis_env
    qgs = qgis_env.setup_qgis()
    ```

    例えば以下のように書きます

    ```python
    import qgis_env
    qgs = qgis_env.setup_qgis()
    
    from osgeo import gdal
    from qgis.core import QgsRasterLayer, QgsProject

    # 以下はQGISの処理
    # ...
    ```