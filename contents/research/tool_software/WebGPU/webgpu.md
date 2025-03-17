---
title: "WebGPUを用いた地震波解析"
date: "2025-03-16"
---

# 環境構築

2025/03/16時点での情報です。現在の環境は以下のとおりです。

- Node.js v22.14.0
- npm v10.9.2
- Visual Studio Code v1.98.1
- Google Chrome v134.0.6998.89
- Windows 11 Pro 24H2


## ツールと拡張機能のインストール

以下のツールをインストールしましょう。
- [Node.js](https://nodejs.org/ja/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Google Chrome](https://www.google.com/intl/ja_jp/chrome/)

またVSCodeの拡張機能として以下をインストールしてください。

- ESLint
- Prettier
- Live Server
- WebGPU Shader Language Highlighter

## Chromeの設定

WebGPUを使用するためには、Chromeの設定を変更する必要があります。

1. Chromeを開き、URLバーに`chrome://flags`と入力します。
2. 検索バーに`WebGPU`と入力し、`WebGPU Developer Features`を`Enabled`に変更します。
3. `chrome://gpu` にアクセスし、`WebGPU: enabled` になっているか確認
4. [WebGPU Samples](https://webgpu.github.io/webgpu-samples/)にアクセスし、WebGPUが有効になっているか確認

<details><summary>`WebGPU: enabled`になっていない場合</summary>

### `WebGPU: enabled`になっていない場合

以下のようなメッセージが表示されている場合、`WebGPU`が有効になっていません。

```
WebGPU: Software only, hardware acceleration unavailable
```

この場合、以下のいずれかの方法で`WebGPU`を有効にしてください。

1. Chromeを開き、URLバーに`chrome://settings/system`と入力します。
2. `Use hardware acceleration when available`を有効にします。

</details>

## VScodeでプロジェクトを作成

VSCodeで新しいフォルダを作成し、以下のコマンドを実行してプロジェクトを作成します。

```bash
node -v
npm -v
npm init -y
```

<details><summary>エラーが出た場合</summary>

### システムでのスクリプト実行のエラー
```
npm : このシステムではスクリプトの実行が無効になっているため、ファイル C:\Program Files\nodejs\npm.ps1 を読み込むことができません。
```

このエラーが出た場合、`npm`に関してのスクリプト実行ポリシーの権限を一部変更する必要があります。
以下のコマンドを実行してください。

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

</details>

## `npm`でパッケージをインストール

### VITEのインストール

VITEは、ESM（ECMAScript Modules）をサポートするビルドツールです。より具体的には、VITEは、ESMを使用して、開発中のアプリケーションを高速にビルドし、開発サーバーを立ち上げることができます。

```bash
npm install vite
```

その後、依存関係をインストールします。

```bash
npm install
```


### WebGPUのインストール

WebGPUは、Web上での高性能なグラフィックス処理を可能にするAPIです。

```bash
npm install webgpu
npm install --save-dev @webgpu/types
```

## 必要なフォルダとファイルの作成

以下のフォルダとファイルを作成します。

```
(root)
│── src/
│   ├── index.html
│   ├── main.js
│   ├── compute.wgsl
│── package.json
│── vite.config.js
```

### `index.html`の作成

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WebGPU Compute Shader Example</title>
</head>
<body>
  <h1>WebGPU Compute Shader</h1>
  <script type="module" src="./main.js"></script>
</body>
</html>
```

### `main.js`の作成

```javascript
// WebGPUの対応チェック
if (!navigator.gpu) {
  console.error("WebGPU not supported on this browser.");
  throw new Error("WebGPU is not supported.");
}

// WebGPUのデバイス取得
const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();

// GPUバッファの作成
const bufferSize = 64 * 4; // 64要素 * 4バイト (float32)
const buffer = device.createBuffer({
  size: bufferSize,
  usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_SRC | GPUBufferUsage.COPY_DST,
});

// シェーダーモジュールの作成
const shaderModule = device.createShaderModule({
  code: await (await fetch('./compute.wgsl')).text()
});

// パイプラインの作成
const pipeline = device.createComputePipeline({
  layout: "auto",
  compute: {
    module: shaderModule,
    entryPoint: "main",
  }
});

// バインドグループの作成
const bindGroup = device.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),
  entries: [{ binding: 0, resource: { buffer } }]
});

// コマンドエンコーダの作成
const commandEncoder = device.createCommandEncoder();
const passEncoder = commandEncoder.beginComputePass();
passEncoder.setPipeline(pipeline);
passEncoder.setBindGroup(0, bindGroup);
passEncoder.dispatchWorkgroups(1); // ワークグループ数
passEncoder.end();

// コマンドの送信
device.queue.submit([commandEncoder.finish()]);

console.log("Compute shader executed successfully!");
```

### `compute.wgsl`の作成

```wgsl
@group(0) @binding(0) var<storage, read_write> data : array<f32>;

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) id : vec3<u32>) {
    let index = id.x;
    data[index] = data[index] * 2.0;
}
```

### `package.json`の編集

`package.json`に以下の内容を追加します。


```json
{
  "scripts": {
    "dev": "vite"
  }
}
```

### `vite.config.js`の編集

```javascript
import { defineConfig } from 'vite';

export default defineConfig({
  base: '',
  build: {
    outDir: 'dist',
  },
});

```

<details><summary>vite.config.js</summary>



## プロジェクトの実行

以下のコマンドを実行して、プロジェクトを実行します。

```bash
npx run dev
```

<details><summary>エラーが出た場合</summary>

### `npx run dev`でエラーが出た場合


```
npm error Missing script: "dev"
npm error
```

`json`ファイルの中に以下のような記述があるか確認してください。

```json
"scripts": {
  "dev": "vite"
}
```

### `localhost:3000`にアクセスできない場合

Chromeは開くが、`http://localhost:3000/`にアクセスすると、`この localhost ページが見つかりません`と表示される場合、以下の手順で解決してください。

1. Chromeを開き、URLバーに`chrome://flags`と入力します。
2. 検索バーに`SameSite`と入力し、`SameSite by default cookies`を`Disabled`に変更します。
3. Chromeを再起動します。


</details>

