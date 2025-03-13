---
title: "Blenderの基本的な使用方法"
date: "2024-03-22"
---

## CLIでの操作
BlenderはCLIの操作も可能です。具体的にはBlenderのインストールが完了した状態でターミナルを開き、以下のコマンドを実行するとBlender内のPythonスクリプトを実行することができます。

```bash
blender -b -P /path/to/script.py
```

以下に、VSCodeでの環境設定方法を示します。

### VSCodeでの環境設定

1. VSCodeを開く。
1. `ctrl + shift + p`を押し、`tasks: Configure Task`を選択する。
1. `Create tasks.json file from template`を選択する。
1. `Others`を選択する。
1. 以下のように記述する。

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Blender Python Script",
            "type": "shell",
            "command": "C:\\Program Files\\Blender Foundation\\Blender 4.2\\blender.exe",
            "args": [
                "-b",
                "-P",
                "${file}"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher": [],
            "detail": "Run Blender Python script in background mode"
        }
    ]
}
```
    - `command`の部分はblenderのバージョンとインストール位置に合わせて変更してください。
1. 保存する。
1. `ctrl + shift + p`を押し、`preferences: Open Keyboard Shortcuts (JSON)`を選択する。
1. 以下のように記述する。

```json
{
    "key": "ctrl+shift+b",
    "command": "workbench.action.tasks.runTask",
    "args": "Run Blender Python Script"
}
```
    - `key`の部分は好みのショートカットキーに変更してください。
1. 保存する。

これで、pythonファイルを開いた状態で`ctrl + shift + b`を押すことで、BlenderのPythonスクリプトを実行することができます。


## 移動・回転・拡大縮小
- 拡大縮小はマウスホイール
- 回転はマウスホイールの押し込みドラッグ
- 平行移動はshift+マウスホイールの押し込みドラッグ

## 物体にテクスチャ(チェッカーボード)を貼る
- 右側の画面でCube>Cube>Materialというところをクリックする
- 左上の平面にボールが置かれているアイコン(Editor Type)からGeneral>Shader Editorをクリックする
- 何も表示されていない場合は左上のView>Frame Allで正しい画面が表示される
- 画面真ん中に表示されているものは右側の画面のセントロイド球のようなものをクリックして出てくるMaterialの画面と同じ
- 左上のWindow->New Windowをクリックすると同じような画面がもう一つ表示される．
- 一番左上のアイコンをクリックして，3D View Portをクリックするといつもの画面になる．
- テクスチャの結果を見たいので，右上の白丸のアイコン(View Port Shading)をクリックすると結果がすぐに反映される
    - 試しにもともとのShader EditorのBase Colorの部分を変えてみると色が変わるはず
- 左上のAdd>Texture>Checker Textureをクリックする
- 出てきたChecker TextureとPrincipled BSDFのBase Colorをマウスでドラッグしてつなぐ
- colorを変えるとchecker textureを変化させることができる
- scaleは一つの面に何マスの模様を生じさせるか
    - 2であれば2×2の模様が出現する

### ワイヤーフレームを表示させる
- 左上のAdd>Texture>Checker Textureの代わりにAdd>Input>WireFrameをクリックする
- 出てきたWireframeのFacとMaterial OutputのSurfaceをつなぐ

## 物体の連続配置
### Array Modifierの適用
- 左上のModelingをクリック
- 右側のスパナ(Modifiers)をクリック
- Add Modifiersをクリック
- Arrayをクリック
- パラメータを設定
- もう一度Array Modifiersをクリックすることで重ねがけも可能
- 終わったらObjectモードにした状態でカメラの横にある下三角のマークをクリックして，Applyする

### 物体をバラバラにする
- 参考URL：https://blender.stackexchange.com/questions/109/how-can-i-use-an-array-modifier-to-create-individually-manipulatable-objects
- 複製が終わったらEdit Modeに入り，複製した物体をすべて選択する
- キーボードのpを押し，出てきたウインドウのSeperate by Loose Partsを押す
- Object Modeに入り，左上のObject>SEt Origin>Origin to Geometryを押す
    - こうすることでそれぞれの物体の初期位置が原点となった状態で物体が配置される

## 寸法が見たい！
- 左側の画面で寸法が見たい物体を選択
- 左真ん中の■にフォーカスがあたったようなアイコン(Object)をクリック
- Transformの中に色々情報が詰まっている


## 魚眼レンズへの設定
- まずレンダリングエンジンをCyclesに変更する必要がある
    - https://www.reddit.com/r/blenderhelp/comments/11f6r7h/why_isnt_the_panorama_type_showing_up_in_my/
    - BlenderにはEEVEEとCyclesという2つのレンダリングエンジンがある
        - 違いについてはよくわかっていない
    - 初期画面の右側>上から2つ目の後ろからのカメラのアイコン(Render)>Render Engine>Cyclesに変更
    - Edit>PreferencesでPreferencesの画面に入る
    - 左側下から3つ目のSystemでCUDAを選択し，搭載されているGPUにチェックマークをいれる
- 初期画面の右側>下から2つ目の映画用カメラの横からのアイコン(Camera)>Lens>Type>Panoramicに変更
    - Panorama Typeで色々選択できる
    - 目的に一番近そうなFisheye Lens Polynomialを選択
        - パラメータを変える
- 画面右上のテカテカしたボールのアイコン(Viewport Shading)をクリック
    - すると簡易的なレンダリングの結果が表示される．パラメータを変えるとレンダリング画像が変わる

## カメラを動かしたい
- カメラを選択
- 左側のObjectアイコンをクリック
- Transformの中のLocationとRotationを初期位置の値に変える
- 鍵の横の小さい点のマークをクリックする
    - こうすると画面下のタイムラインという場所に点が現れる + クリックした値が黄色にハイライトされる
- (続きを書く)

