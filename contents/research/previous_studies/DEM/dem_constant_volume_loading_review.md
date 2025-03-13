# DEM 非排水条件の設定法に関する簡易レビュー

# 懸念・疑問

- $\sigma_2 = \sigma_3$の場合
    - 構造異方性がある場合、側応力の変化に対して異なるひずみ増分が出る
- $\sigma_2 \neq \sigma_3$の場合
    - 構造異方性の有無にかかわらず、側応力の変化に対して異なるひずみ増分が出る
- いずれにしても異なるひずみ増分が出る場合、その拘束条件は $\Delta \varepsilon_{ii} = 0$では足りないのでは？
- 構造異方性の議論をしているのに、外部から与えるひずみ増分の条件は $\Delta \varepsilon_{22} = \Delta \varepsilon_{33} = -\frac{1}{2} \Delta \varepsilon_{11}$でいいのか？
- 円柱供試体の場合常に$\sigma_2 = \sigma_3$であるが、水平方向の構造異方性はでないという仮定がある？
- 本来の条件はdex+dey+dez=0であるのに、それよりも強いdex=dey=-dez/2を与えてしまうことは、暗にx,y方向に対しては等方的な構造であるというのを仮定してしまうことにならないか？
    - 上は森本さんへのメールの一部

# 中井先生の授業資料113pからの引用

- [http://zhang.web.nitech.ac.jp/lecture/2015-nakai-Text(haifushiryou).pdf](http://zhang.web.nitech.ac.jp/lecture/2015-nakai-Text(haifushiryou).pdf)
- (全?)応力変化は弾性ひずみ増分と弾性係数テンソルから求まる + 弾性ひずみは全ひずみから塑性ひずみを引いたものである
    
    $$
    d \boldsymbol{\sigma}=\mathbf{D}^{\mathbf{e}} d \boldsymbol{\varepsilon}^{\mathbf{e}}=\mathbf{D}^{\mathrm{e}}\left(d \boldsymbol{\varepsilon}-d \boldsymbol{\varepsilon}^{\mathrm{p}}\right)
    $$
    
    - 成分表示をすると
        
        $$
        \begin{align*}
        \begin{bmatrix}
        d\sigma_{11} \\
        d\sigma_{22} \\
        d\sigma_{33} \\
        d\sigma_{23} \\
        d\sigma_{13} \\
        d\sigma_{12}
        \end{bmatrix}
        -
        \begin{bmatrix}
        du_{11} \\
        du_{22} \\
        du_{33} \\
        du_{23} \\
        du_{13} \\
        du_{12}
        \end{bmatrix}
        =
        \begin{bmatrix}
        d\sigma'_{11} \\
        d\sigma'_{22} \\
        d\sigma'_{33} \\
        d\sigma'_{23} \\
        d\sigma'_{13} \\
        d\sigma'_{12}
        \end{bmatrix}
        &=
        \frac{E}{(1+v)(1-2v)}
        \begin{bmatrix}
        1-v & v & v & 0 & 0 & 0 \\
        v & 1-v & v & 0 & 0 & 0 \\
        v & v & 1-v & 0 & 0 & 0 \\
        0 & 0 & 0 & \frac{1-2v}{2} & 0 & 0 \\
        0 & 0 & 0 & 0 & \frac{1-2v}{2} & 0 \\
        0 & 0 & 0 & 0 & 0 & \frac{1-2v}{2}
        \end{bmatrix}
        \left(
        \begin{bmatrix}
        d\varepsilon_{11} \\
        d\varepsilon_{22} \\
        d\varepsilon_{33} \\
        2d\varepsilon_{23} \\
        2d\varepsilon_{13} \\
        2d\varepsilon_{12}
        \end{bmatrix}
        -
        \begin{bmatrix}
        d\varepsilon^p_{11} \\
        d\varepsilon^p_{22} \\
        d\varepsilon^p_{33} \\
        2d\varepsilon^p_{23} \\
        2d\varepsilon^p_{13} \\
        2d\varepsilon^p_{12}
        \end{bmatrix}
        \right)
        \end{align*}
        $$
        
- 塑性ひずみ増分は硬化係数(?)と塑性ポテンシャルの応力空間における勾配から求まる

$$
d \boldsymbol{\varepsilon}^{\mathrm{p}}=\Lambda \frac{\partial F}{\partial \boldsymbol{\sigma}} \quad
$$

- 硬化係数は $h_p$(降伏応力 $\sigma_y$が塑性ひずみの関数であるとした場合の

$$
\quad \Lambda=\frac{\frac{\partial F}{\partial \boldsymbol{\sigma}} d \boldsymbol{\sigma}}{h^p} 
$$

# 既往研究

- Kevin J. Hanley, Xin Huang, Catherine O'Sullivan, Fiona Kwok; Challenges of simulating undrained tests using the constant volume method in DEM. *AIP Conference Proceedings* 18 June 2013; 1542 (1): 277–280. [https://doi.org/10.1063/1.4811921](https://doi.org/10.1063/1.4811921)
    - Lammpsを用いた解析
    - UndrainedとConstant Volumeは厳密にいうと違うよ
        - 一つは流体モデルとのカップリングによるシミュレーション
        - もう一つは完全飽和と非圧縮性を仮定してConstant Volumeとする場合
    - Thornton (1979)によって検証された
    - 高い応力環境での問題
        - 高い応力になるほど水の非圧縮性の仮定が無視できなくなる
        - 二つの粒子のオーバーラップも問題になる
    - 速いひずみ速度が結果に有意な影響を与える可能性がある
- Keishing, J., Hanley, K.J. Improving constant-volume simulations of undrained behaviour in DEM. *Acta Geotech.* **15**, 2545–2558 (2020). https://doi.org/10.1007/s11440-020-00949-1
    - 基本的な研究背景では上と同じことが書かれている
    - この論文では不飽和まで拡張した間隙の体積弾性率 $K_f$ を定義して、土全体の体積変化量 $\Delta V$ を次のように定義した。
    
    $$
    \Delta V = -\frac{\Delta u}{K_f}\left(V_{current} - V_{particles}\right), \frac{1}{K_f} = \frac{1}{K_w} + \frac{1-S_r}{P_a}
    $$
    
    - 解析モデルを見てもCubicであるのに、 $\Delta V$をどのように与えたのかについては書かれていない…
- Zhang, W., & Rothenburg, L. (2020). Comparison of undrained behaviors of granular media using fluid-coupled discrete element method and constant volume method. *Journal of rock mechanics and geotechnical engineering*.
    - 伝統的には2Dでは定体積条件は片方を押したら片方を引くことで達成されてきた
    - この論文では流体－粒子カップリングによる手法を適用している
        - *Wei Zhang (2018). A Micromechanical Study of Undrained Granular Media Using Fluid-coupled Discrete Numerical Simulations. UWSpace. [http://hdl.handle.net/10012/14203](http://hdl.handle.net/10012/14203)*
        - ベースのなったのは上記の論文
- Ng, T. -., & Dobry, R. (1994). Numerical simulations of monotonic and cyclic loading of granular soil. Journal of Geotechnical Engineering, 120(2), 388-403. doi:10.1061/(ASCE)0733-9410(1994)120:2(388)

# 現時点での理解

- 結局、2Dであろうが3Dであろうが**応力制御**をしている
- ある時間ステップにおいて次の2つの条件を満たすように動かしている
    - 偏差応力の増分が指定値になるように
    - 等体積条件を満たすように、3鉛直応力を全て等しく増減させる
-