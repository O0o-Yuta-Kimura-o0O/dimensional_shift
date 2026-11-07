#set document(
  title: "集合値の商による零除算の定義と解集合の次元変化",
  author: ("木村祐太", "GPT-6 Astra"),
  description: "逆像・直積・線形制約による定式化。v0.1.0",
  date: datetime(year: 2026, month: 11, day: 7),
)
#set page(paper: "a4", margin: (x: 24mm, top: 21mm, bottom: 21mm),
  numbering: "1", number-align: center,
  header: context if counter(page).get().first() > 1 {
    text(size: 8pt, fill: luma(110))[集合値の商と解集合の次元変化 #h(1fr) v0.1.0]
  },
)
#set text(font: ("Libertinus Serif", "Hiragino Mincho ProN", "Noto Serif CJK JP"), size: 10pt, lang: "ja")
#set par(justify: true, leading: 0.72em, first-line-indent: 1em)
#set heading(numbering: "1.")
#show heading: set text(font: ("Hiragino Sans", "Noto Sans CJK JP"), weight: "bold")
#show heading.where(level: 1): set block(above: 1.15em, below: 0.65em)
#show heading.where(level: 1): set text(size: 12pt)
#set math.equation(numbering: "(1)")
#set block(above: 0.65em, below: 0.65em)
#let rr = $bb(R)$
#let powset = math.cal("P")
#let claim(name, body) = block(breakable: false)[*#name* #body]
#let proof(body) = block[*証明.* #body #h(0.4em)$square$]
#let note(body) = block[#text(size: 9pt, body)]

#align(center)[
  #text(size: 18pt, weight: "bold")[集合値の商による零除算の定義と\ 解集合の次元変化]
  #v(0.7em)
  #text(size: 11pt)[逆像・直積・線形制約による定式化]
  #v(1em)
  木村祐太　・　GPT-6 Astra（AI）\
  #text(size: 9pt)[2026年11月7日　／　Version 0.1.0]
]
#v(0.7em)
#block(inset: (x: 0pt, y: 3pt))[
  *要旨*　商を乗算方程式の解集合として定義し、零除算を含む演算と解集合の次元変化を整理する。実数上で $Q(a,b)=\{x in rr | b x=a\}$ と置くと、非零除数の場合には通常の商の単集合を、零除数の場合には被除数に応じて全体集合または空集合を得る。この値は計算履歴を保持しない。集合への自然な拡張では零除算の反復だけで次元は増加しないことを示し、独立座標を加える直積によって次元上昇を定義する。さらに、対角係数の零化と一般の線形方程式系を用いて次元の切替を記述し、追加制約による次元低下の条件を明らかにする。本稿は、旧稿の構想を既存の集合論と線形代数の範囲で定式化する研究ノートである。
]
#text(size: 9pt)[*キーワード*　集合値の商、零除算、逆像、直積、アフィン空間、自由度]

= 目的と基本設定

旧稿［1］の中心的な着想は、「$0/0$ の商を全体集合、非零実数の零除算の商を空集合とし、点・線・面の間で式の値を移す」というものであった。本稿では、この着想に必要な定義だけを残す。除外集合の独自演算、多重度、式の履歴の復元は採用しない。

数の体系には通常の実数体 #rr を用いる。数 $a$ を集合として扱う場合は単集合 $\{a\}$ に埋め込み、$a=\{a\}$ を文字どおりの等式とはしない。$powset(rr)$ は #rr の部分集合全体である。$rr^n$ の点は順序を持つ座標の組であり、実数の積とは区別する。

次元に関する命題の対象は、非空の有限次元アフィン空間とする。$S=p+V$（$V$ は線形部分空間）に対し $dim S:=dim V$ と定める。空集合は「解なし」とし、本稿では次元を割り当てない。一般の部分集合も演算の入力にはできるが、そのすべてにこの次元の定義を適用するものではない。

= 集合値の商

#claim("定義1（集合値の商）.", [実数 $a,b$ に対し、
  $ Q(a,b):=\{x in rr | b x=a\} $ <quotient>
  と定める。これは $Q:rr^2 arrow powset(rr)$ という集合値関数である。])

写像 $m_b:rr arrow rr$, $m_b(x)=b x$ を用いると、$Q(a,b)=m_b^(-1)(\{a\})$ である。ここで $m_b^(-1)$ は集合の逆像を表し、逆関数や乗法的逆元の存在を意味しない［2］。定義の右辺は通常の乗算だけから構成される。

#pagebreak()

#claim("命題1（商の三つの場合）.", [
  $ Q(a,b)=cases(\{a/b\} & quad b != 0, rr & quad a=b=0, emptyset & quad b=0 "かつ" a != 0). $ <three-cases>
])
#proof([ $b != 0$ なら $b x=a$ の唯一の解は $a/b$ である。$b=0$ なら左辺は常に0であるため、$a=0$ ではすべての実数が解となり、$a != 0$ では解は存在しない。])

零除算だけを表す略記として $eta(a):=Q(a,0)$ を用いてよい。従って $eta(0)=rr$、$a != 0$ なら $eta(a)=emptyset$ である。本稿で零除算を含む商を書く際は、通常の実数除算との混同を避けるため $Q$ または $eta$ を用いる。

= 集合に対する演算と情報の扱い

#claim("定義2（集合への拡張）.", [ $A,B subset.eq rr$ に対し、
  $ cal(Q)(A,B):=union.big_(a in A, b in B) Q(a,b)
    =\{x in rr | exists a in A, exists b in B, b x=a\} $ <set-quotient>
  と定める。$cal(Q)(\{a\},\{b\})=Q(a,b)$ である。])

同様に、$A+B:=\{a+b | a in A,b in B\}$、$A-B:=\{a-b | a in A,b in B\}$、$A dot B:=\{a b | a in A,b in B\}$ と定める。ここで減算 $-$ は集合差ではない。この選択では、各入力から値を独立に選ぶ。空集合は和・積・集合値の商のどの入力位置に現れても、結果を空集合にする。

#claim("命題2（零除算の反復）.", [ $E(A):=cal(Q)(A,\{0\})$ と置くと、
  $ E(A)=cases(rr & quad 0 in A, emptyset & quad 0 in.not A), quad E(E(A))=E(A). $ <idempotent>
])
#proof([ $0x=a$ が成立する $a in A$ が存在する条件は $0 in A$ であり、その場合はすべての $x$ が解になる。また $E(rr)=rr$、$E(emptyset)=emptyset$ なので、反復しても結果は変わらない。])

従って $cal(Q)(rr,\{0\})=rr$ であり、集合値の零除算を反復するだけで $rr^2$ が得られるわけではない。本稿では、次節で定義する独立座標の追加によって次元上昇を実現する。

#claim("命題3（履歴を持たない評価）.", [ $eta$ の値から、任意の引数を復元する関数は存在しない。])
#proof([ 仮に $r(eta(a))=a$ がすべての実数 $a$ について成立すれば、$eta(1)=eta(2)=emptyset$ より $r(emptyset)=1$ かつ $r(emptyset)=2$ となり矛盾する。])

この情報の消失は本稿の仕様である。例えば $eta(a)+eta(b)=eta(a+b)$ という旧稿の変形規則は採用できない。$(a,b)=(1,1)$ と $(1,-1)$ では左辺が同じ集合値になる一方、右辺はそれぞれ $emptyset$ と #rr になるからである。

また、同一変数の共有は独立な集合演算と区別する。例えば $\{x-x | x in rr\}=\{0\}$ であるが、$rr-rr=rr$ である。共有変数を含む式は、その共有関係を保った連立条件で表し、解集合から出力座標を取り出して評価する。集合演算に、実数体のすべての変形規則を無条件に移すことはしない。

#pagebreak()

= 独立座標による次元上昇

#claim("定義3（座標の追加）.", [ $S subset.eq rr^n$ と $lambda in rr$ に対し、
  $ L_lambda (S):=S times Q(0,lambda), quad L(S):=L_0 (S)=S times rr $ <lift>
  と定める。$times$ は直積であり、実数の積 $dot$ と区別する。])

この定義は、新しい座標 $t$ に条件 $lambda t=0$ を課すことに相当する。$lambda != 0$ では $t=0$ に固定され、$lambda=0$ では $t$ が自由になる。元の座標を保持することは、$eta(a)$ が捨てた引数を復元することとは異なる。

#claim("命題4（次元上昇）.", [ $S$ が非空アフィン空間ならば、
  $ dim L_lambda (S)=cases(dim S & quad lambda != 0, dim S+1 & quad lambda=0). $ <lift-dim>
  また $L_lambda(emptyset)=emptyset$ である。])
#proof([ $S=p+V$ と書く。$lambda != 0$ では $L_lambda (S)=(p,0)+(V times\{0\})$ であり、方向空間の次元は $dim V$ である。$lambda=0$ では方向空間が $V times rr$ となる。$V$ の基底を新座標0で埋め込んだものに、新座標方向の単位ベクトルを加えると基底になるため、次元は $dim V+1$ である。空集合に関する主張は直積の定義による。])

例えば、任意の実数 $a$ に対し、
  $ underbrace(\{a\}, "0次元") arrow^L
    underbrace(\{a\} times rr, "1次元") arrow^L
    underbrace(\{a\} times rr^2, "2次元") $ <lift-example>
となる。最後の集合は、$rr^3$ 内の平面である。集合が置かれる周囲の空間の次元と、集合自身の次元は一致するとは限らない。

同じ周囲の空間の中で次元を切り替えることもできる。$d=(d_1,d_2)$ に対し、
  $ S_d:=Q(0,d_1) times Q(0,d_2)
    =\{(x,y) in rr^2 | d_1 x=0, d_2 y=0\} $ <switch2>
と定める。

#figure(
  table(columns: (1fr, 2.6fr, 0.7fr), inset: 7pt,
    stroke: (x: none, y: 0.4pt + luma(160)),
    table.header([*係数 $d$*], [*解集合 $S_d$*], [*次元*]),
    [$(1,1)$], [$\{(0,0)\}$：原点], [0],
    [$(0,1)$], [$rr times\{0\}$：$x$ 軸], [1],
    [$(0,0)$], [$rr^2$：平面全体], [2],
  ),
  caption: [係数の零化による、同じ平面内での次元の切替。],
) <switch-table>

係数が非零である限り、その大きさによらず対応する座標は0に固定される。係数が0になったとき、拘束が一つ消えて自由な方向が一つ増える。ここでいう次元の移動は、この解集合の自由度の変化を意味する。

#pagebreak()

= 線形方程式系としての一般化

#claim("命題5（対角係数による次元の切替）.", [ $d in rr^n$ に対し、
  $ S_d:=product_(i=1)^n Q(0,d_i)
    =ker op("diag")(d_1,dots,d_n) $ <diagonal>
  と定める。ただし $product$ は集合の直積を表す。このとき、
  $ dim S_d=|\{i in\{1,dots,n\} | d_i=0\}|. $ <diagonal-dim>
])
#proof([ $d_i != 0$ の座標は0に固定され、$d_i=0$ の座標は独立に任意の実数を取る。後者の座標に対応する標準基底ベクトルが $S_d$ の基底を与える。])

対角形に限らず、$A$ を実 $m times n$ 行列、$b in rr^m$ とし、
  $ F_A (b):=\{x in rr^n | A x=b\} $ <fiber>
と置く。これは線形写像の逆像であり、一変数の場合には $F_([beta]) (alpha)=Q(alpha,beta)$ と対応する。

#claim("命題6（一般の解集合の次元）.", [ $F_A (b)$ が非空であることと $b in op("im") A$ は同値である。非空の場合、一つの解 $x_0$ を用いて、
  $ F_A (b)=x_0+ker A, quad dim F_A (b)=n-op("rank") A $ <rank-nullity>
  と表せる。])
#proof([ 非空性は像の定義による。$A x=b=A x_0$ は $A(x-x_0)=0$ と同値なので、解集合は $x_0+ker A$ である。次元の式は階数・退化次数の定理［3, 定理3.21］による。])

零除算の二つの場合は、この命題の最小の例である。零写像の像は $\{0\}$ なので、右辺が0ならすべての入力が解となり、右辺が非零なら解は存在しない。一般の係数変更でも、解の存在が保たれる場合には階数の低下に応じて次元が増える。

= 条件の追加による次元低下

集合に条件を課す操作を、$R_C (S):=\{x in S | C(x)\}$ と表す。ここで $C(x)$ は指定した条件である。これは条件を満たす集合との共通部分を取る操作である。

#claim("命題7（線形制約の追加）.", [ $S=p+V$ を非空アフィン空間とする。線形写像 $T$ と定数 $c$ に対し $S':=\{x in S | T x=c\}$ が非空ならば、
  $ dim S'=dim V-op("rank")(T|_V). $ <restriction>
])
#proof([ $x_0 in S'$ を一つ取ると、$S'=x_0+(V inter ker T)$ である。方向空間は制限写像 $T|_V$ の核なので、階数・退化次数の定理を適用すればよい。])

従って、既存の自由方向に対して独立な制約を $r$ 個加え、なお解が存在するなら、次元は $r$ だけ下がる。冗長な制約は次元を下げず、矛盾する制約は空集合を生む。

#pagebreak()

具体例として、$rr^2$ に $y=0$ を課すと直線 $rr times\{0\}$ になり、さらに $x=a$ を課すと点 $\{(a,0)\}$ になる。

不等式による範囲の縮小は、次元低下とは区別する必要がある。例えば $0<=x<=1$、$0<=y<=1$ により得られる正方形は、通常の幾何学的意味では2次元の領域である。一方、$y<=0$ と $y>=0$ を同時に課せば $y=0$ と同値になり、平面から直線への制限を実現できる。本稿では、一般の不等式解集合の次元理論までは扱わない。

= 適用範囲と結論

本稿の構成では、実数体そのものの公理を変更せず、演算の出力を実数の集合に拡張する。$Q$ は零除算の結果を含めて定義されているが、0の乗法的逆元を導入するものではない。集合に対する演算の性質は、その定義から個別に導く必要がある。

例えば集合の積と直積は異なる。$rr dot rr=rr$ であるのに対し、$rr times rr=rr^2$ である。さらに、集合の分配則にも共有変数の問題が現れる。$A=\{1,2\}$、$B=\{1\}$、$C=\{-1\}$ なら、$A dot (B+C)=\{0\}$ だが、$A dot B+A dot C=\{-1,0,1\}$ である。後者では $A$ から二度独立に値を選ぶためである。

集合値の商は、式の評価を解集合として続ける方法を与える。しかし、これだけで係数に関する連続性や微分可能性が保証されるわけではない。命題5では係数が0になった点で次元が変化する。集合値関数の連続性を論じるには、別途その意味を定める必要がある。

以上により、旧稿の中心的な構想は、集合値の商 $Q$、独立座標を加える直積、条件による集合の制限という三つの操作で定式化できる。零除算における全体集合と空集合の区別は解の存在条件を表し、次元上昇は自由な座標の追加、次元低下は独立な制約の追加として記述される。この枠組みでは、計算前の数や式の履歴を復元することを要請しない。

#heading(numbering: none)[著者の役割]

木村祐太：原着想、旧稿の執筆、再構成の目的と方針の提示。GPT-6 Astra（AI）：定式化、命題と証明の整理、原稿の構成および編集。

#heading(numbering: none)[参考文献]
#set par(first-line-indent: 0pt)
#text(size: 9pt)[
  ［1］木村祐太．『0除算の公理』．未公刊メモ，ver. 20180228-，2018年．本リポジトリの原本保存版：`output/reference/dimensional_shift_01_original.txt`．

  ［2］Seçkin Demirbaş and Andrew Rechnitzer. _PLP: An Introduction to Mathematical Proof_, §10.3, Definition 10.3.1 and Warning 10.3.3. University of British Columbia.
  #link("https://personal.math.ubc.ca/~PLP/book/ch-functions-5.html")[著者公開テキスト：Images and preimages of sets]（2026年11月7日閲覧）．

  ［3］Sheldon Axler. _Linear Algebra Done Right_, 4th ed. Springer, 2024. Theorem 3.21, pp. 62–63; Theorem 3.92, p. 97.
  #link("https://linear.axler.net/LADR4e.pdf")[著者公開PDF]（2026年11月7日閲覧）．
]
