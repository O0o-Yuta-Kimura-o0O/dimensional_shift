# Dimension Extension by Independent Coordinate Generation and Universe-Relative Set-Valued Quotients

A framework for variable-length coordinates, division by zero, and discrete grids

木村祐太 (Yuta Kimura) · GPT-6 Astra (AI)

2026-11-07 · v0.2.0

**Abstract.** This paper formulates dimension extension of solution sets around the operation $L_U(n,S):=(n+1,S\times U)$, which generates a new independent coordinate on each application. It recursively extends finite coordinate tuples without fixing an upper bound on their length. A set-valued quotient distinguishes the field $K$ in which arithmetic is performed from the candidate set $U$ for the quotient, giving $Q_U(0,0)=U$ for division of zero by zero. Real numbers, integers, and finite sets can serve as candidate sets within the same framework, while coordinate count, real affine dimension, and axes of discrete choice remain distinct. We relate independent coordinate generation, release of constraints on existing coordinates, and dimension reduction by additional constraints, and give an example of rendering a finite grid in 3D computer graphics. The construction uses standard set theory and linear algebra; it does not require multiplicative inverses of zero or recovery of computational history.

**Keywords.** independent coordinate generation, variable-length coordinates, set-valued quotient, universe, division by zero, discrete grid

## 1. Purpose and basic setting

The original note ［1］ proposed treating quotients involving division by zero as either the universe or the empty set, and expanding the value of an expression into points, lines, and planes. The first version formulated this idea using solution sets over the reals. This revision distinguishes releasing constraints on pre-existing axes from generating new axes, and places the latter operation at the center of the framework.

Coordinate generation uses a nonempty set $U$. When quotients are considered from Section 4 onward, the field $K$ for ordinary multiplication is either the real or complex field, and $0\in U\subseteq K$ is assumed. The set $U$ is the universe of possible values for one coordinate; with $n$ current coordinates, the coordinate space is $U^n$. The number zero itself does not carry information about the universe. Instead, $U$ is specified explicitly as part of the context of the operation.

Numbers are embedded into singleton sets when necessary, without identifying a number literally with its singleton. For a nonempty real affine space $S=p+V$, we define $\dim S:=\dim V$. This definition is not applied unconditionally to arbitrary sets or discrete grids. No dimension is assigned to the empty set in this paper.

## 2. An operation that generates independent coordinates

**Definition 1 (States with coordinate structure).** A state is a pair of the following form.

$$
(n,S),\qquad n\in\mathbb{N}_0,\qquad S\subseteq U^n\tag{1}
$$

Here $n$ records the current number of coordinates, not previous expressions or dividends. We set $U^0=\{()\}$, allowing the construction to start from the singleton consisting of the empty coordinate tuple.

**Definition 2 (Independent coordinate generation).** Define an operation on states by

$$
L_U(n,S):=(n+1,S\times U)\tag{2}
$$

The Cartesian product is interpreted by concatenating coordinates. Thus elements of the resulting set have the form

$$
(x_1,\ldots,x_n,t),\qquad(x_1,\ldots,x_n)\in S,\qquad t\in U\tag{3}
$$

Each new coordinate takes values independently from $U$, with no additional relation imposed between it and the existing coordinates. Independence here is set-theoretic: all combinations are permitted. It is not an assumption of probabilistic independence.

**Proposition 1 (Recursive coordinate generation).** For every nonnegative integer k,

$$
L_U^k(n,S)=(n+k,S\times U^k)\tag{4}
$$

$$
L_U^k(0,\{()\})=(k,U^k)\tag{5}
$$

**Proof.** For k equal to zero, the operation is the identity. Taking one further Cartesian product after k applications appends one element of $U$ by coordinate concatenation. The result follows by induction. The coordinate count is finite at every stage, and the rule requires no fixed maximum count. □

Empty solution sets also retain their coordinate structure, so $L_U(n,\varnothing)=(n+1,\varnothing)$. The states $(1,\varnothing)\ne(2,\varnothing)$ have different coordinate counts, although neither contains a solution.

**Proposition 2 (Increase in real affine dimension).** If $U$ is the set of all real numbers and S is a nonempty real affine space, then

$$
\dim(S\times\mathbb{R})=\dim S+1\tag{6}
$$

**Proof.** Writing $S=p+V$, we have

$$
S\times\mathbb{R}=(p,0)+(V\times\mathbb{R})\tag{7}
$$

Embed a basis of V with zero in the new coordinate, and add the unit vector in the new coordinate direction. These vectors form a basis of the direction space, so the dimension increases by one. □

Starting from the initial state produces a point, the real line, a plane, and three-dimensional space.

$$
(0,\{()\})\xrightarrow{L_{\mathbb{R}}}(1,\mathbb{R})\xrightarrow{L_{\mathbb{R}}}(2,\mathbb{R}^2)\xrightarrow{L_{\mathbb{R}}}(3,\mathbb{R}^3)\longrightarrow\cdots\tag{8}
$$

Coordinate count is distinct from the dimension of the set itself. For example, $\{a\}\subseteq\mathbb{R}$ is a zero-dimensional point in a one-coordinate ambient space. Likewise, $\{(t,t)\mid t\in\mathbb{R}\}$ is a line, whereas $\{(t,u)\mid t,u\in\mathbb{R}\}=\mathbb{R}^2$ is a plane. Copying the same variable is different from generating an independent coordinate.

## 3. Distinction from releasing constraints on fixed axes

For a fixed number $n$ of real coordinates and coefficients $d=(d_1,\ldots,d_n)\in\mathbb{R}^n$, consider the family

$$
S_d:=\{x\in\mathbb{R}^n\mid d_i x_i=0,\ i=1,\ldots,n\}\tag{9}
$$

A coordinate with a nonzero coefficient is fixed at zero, while a coordinate with a zero coefficient is free. Consequently,

$$
\dim S_d=\lvert\{i\in\{1,\ldots,n\}\mid d_i=0\}\rvert\tag{10}
$$

This method changes the number of free directions within the same coordinate space. Definition 2 instead increases the coordinate count of the state itself. The two operations are different; the former alone cannot exceed the fixed coordinate count.

Here we assume $0\in U\subseteq K,\qquad\lambda\in K$. Using the quotient defined in Section 4, coordinate addition and its constraint can also be expressed in a single formula.

$$
G_{U,\lambda}(n,S):=(n+1,S\times Q_U(0,\lambda))\tag{11}
$$

$$
G_{U,\lambda}(n,S)=\begin{cases}(n+1,S\times\{0\}),&\lambda\ne0,\\(n+1,S\times U),&\lambda=0.\end{cases}\tag{12}
$$

This operation always adds one coordinate. A nonzero coefficient fixes the new coordinate at zero, while a zero coefficient permits all candidates. Definition 2 is the zero-coefficient case.

## 4. Universe-relative set-valued quotients

**Definition 3 (Quotients with a specified candidate set).** Under the assumption $0\in U\subseteq K$, define

$$
Q_U(a,b):=\{x\in U\mid bx=a\},\qquad a,b\in K\tag{13}
$$

Its type is $Q_U:K^2\to\mathcal{P}(U)$. Using the map $m_b:U\to K,\qquad m_b(x)=bx$, it can be written as the preimage $Q_U(a,b)=m_b^{-1}(\{a\})$. Existence of a preimage does not imply existence of an inverse function ［2］.

**Proposition 3 (Three cases determined by the candidate set).**

$$
Q_U(a,b)=\begin{cases}\{a/b\}\cap U,&b\ne0,\\U,&a=b=0,\\\varnothing,&b=0,\ a\ne0.\end{cases}\tag{14}
$$

**Proof.** For nonzero b, the equation has the unique solution a/b in the field $K$. This value is retained exactly when it belongs to $U$. If b is zero, the left-hand side is zero for every candidate x. Thus all candidates are solutions when a is zero, and no solution exists when a is nonzero. □

In particular, $Q_U(0,0)=U$ is not specific to the real numbers. Specifying the candidate set gives, for example,

$$
Q_{\mathbb{R}}(0,0)=\mathbb{R},\qquad Q_{\mathbb{Z}}(0,0)=\mathbb{Z},\qquad Q_{D_m}(0,0)=D_m\tag{15}
$$

The finite set Dₘ is defined in Section 6. Changing the candidate set also affects division by nonzero numbers: $Q_{\mathbb{Z}}(1,2)=\varnothing$, whereas $Q_{\mathbb{R}}(1,2)=\{1/2\}$. Ordinary real division must not be assumed to remain closed within the integers or a finite grid.

The Cartesian-product operation in Definition 2 also applies to an arbitrary abstract set. However, the equation bx=a cannot be applied directly to a set without specified multiplication and zero. A quotient requires the algebraic structure described here, or a separately defined relation.

**Definition 4 (Extension to sets).**

$$
\mathcal{Q}_U(A,B):=\bigcup_{a\in A,\,b\in B}Q_U(a,b),\qquad A,B\subseteq K\tag{16}
$$

**Proposition 4 (Repeated division by zero does not add coordinates).** With $E_U(A):=\mathcal{Q}_U(A,\{0\})$,

$$
E_U(A)=\begin{cases}U,&0\in A,\\\varnothing,&0\notin A,\end{cases}\qquad E_U(E_U(A))=E_U(A)\tag{17}
$$

**Proof.** An element a of A satisfying 0x=a exists exactly when A contains zero. In that case every candidate is a solution. Since $U$ contains zero, applying the operation again leaves the output unchanged, whether that output is $U$ or the empty set. □

Coordinate generation therefore does not follow automatically from the set-valued quotient. Substituting Proposition 3 into Definition 2 gives the connection

$$
L_U(n,S)=(n+1,S\times Q_U(0,0))\tag{18}
$$

The quotient supplies the candidate set for the new coordinate, and the Cartesian-product operation adds that coordinate.

For the abbreviation $\eta_U(a):=Q_U(a,0)$, we have $\eta_U(1)=\eta_U(-1)=\varnothing$, so an arbitrary original argument cannot be recovered from the set-valued result. Rules such as $\eta_U(a)+\eta_U(b)=\eta_U(a+b)$, which subsequently operate on discarded arguments, are not adopted.

## 5. Real linear systems and dimension reduction

In this section, $U$ is the set of all real numbers. Let A be a real matrix with m rows and n columns, and let b be a real vector with m components. Define

$$
F_A(b):=\{x\in\mathbb{R}^n\mid Ax=b\}\tag{19}
$$

**Proposition 5 (General linear solution sets).** The solution set is nonempty if and only if $b\in\operatorname{im}A$. If it is nonempty, choosing one solution x₀ gives

$$
F_A(b)=x_0+\ker A,\qquad\dim F_A(b)=n-\operatorname{rank}A\tag{20}
$$

**Proof.** Nonemptiness follows from the definition of the image. Since Ax=b and Ax₀=b, the difference x−x₀ belongs to the kernel of A. Conversely, adding any element of that kernel to x₀ gives a solution. The dimension formula follows from the rank-nullity theorem ［3, Theorem 3.21］. □

This formula describes freedom within a fixed set of n coordinates. Definition 2 instead updates n. A rank decrease caused by coefficient changes can thus be distinguished from an increase in coordinate count caused by coordinate generation.

**Proposition 6 (Dimension reduction by linear constraints).** Add a condition given by a linear map T and a constant c to a nonempty real affine space $S=p+V$.

$$
S^{\prime}:=\{x\in p+V\mid Tx=c\}\tag{21}
$$

If the constrained set remains nonempty, then

$$
\dim S^{\prime}=\dim V-\operatorname{rank}(T|_V)\tag{22}
$$

The restriction of T here describes its action on the original free directions V.

**Proof.** Choose one solution x₀ satisfying the added constraint. Then

$$
S^{\prime}=x_0+(V\cap\ker T)\tag{23}
$$

The direction space is the kernel of T restricted to V, so the rank-nullity theorem applies. □

Thus adding r constraints that are independent on the existing free directions reduces the dimension by r, provided a solution remains. Redundant constraints leave the dimension unchanged; inconsistent constraints produce the empty solution set. A concrete example is

$$
\mathbb{R}^2\xrightarrow{y=0}\mathbb{R}\times\{0\}\xrightarrow{x=a}\{(a,0)\}\tag{24}
$$

Restricting a range by inequalities need not reduce dimension. The square defined by $0\le x\le1,\qquad0\le y\le1$ is a two-dimensional region in the usual geometric sense. In contrast, imposing $y\le0,\qquad y\ge0$ simultaneously is equivalent to y=0 and restricts the plane to a line.

## 6. Discrete universes and grid visualization

**Example 1 (A finite grid).** As a subset of the real field, take

$$
D_m:=\{-m,-m+1,\ldots,m\},\qquad m\in\mathbb{N},\quad m\ge1\tag{25}
$$

Proposition 3 gives $Q_U(0,0)=U$. Three applications of independent coordinate generation therefore yield

$$
L_{D_m}^{3}(0,\{()\})=(3,D_m^3),\qquad\lvert D_m^3\rvert=(2m+1)^3\tag{26}
$$

For example, m equal to two gives 125 points. Rendering each point $(i,j,k)\in D_m^3$ as a position in 3D computer graphics produces a grid of points. The stages of generation are

$$
D_m\longrightarrow D_m^2\longrightarrow D_m^3\tag{27}
$$

They give a row of points, a planar point set, and a spatial point set. Automatic interpolation of line segments or surfaces is not part of this definition.

**Changing the range through m versus increasing coordinate count.** Changing m changes the number of candidates on each axis and the displayed range. Applying Definition 2 again increases the number of coordinates. These are different changes.

**Coordinate count and geometric dimension.** The integer grid $\mathbb{Z}^3$ has three independent integer coordinates, but it is not continuous real space itself. In the usual Euclidean distance, each grid point is isolated within a neighborhood of radius 1/2. The same holds for the finite grid. We therefore describe these objects as three-coordinate grids, distinguishing them from the increase in real affine dimension in Proposition 2.

If instead we consider the real affine hull, the smallest real affine space containing the grid, then

$$
\operatorname{aff}_{\mathbb{R}}(D_m^n)=\mathbb{R}^n\tag{28}
$$

This follows because the grid contains zero and every standard basis vector. The grid itself is not identified with its affine hull.

**Degenerate candidate sets and complex numbers.** For $U=\{0\}$, adding another coordinate position provides only one possible value and does not increase geometric freedom. For complex numbers,

$$
\dim_{\mathbb{C}}\mathbb{C}=1,\qquad\dim_{\mathbb{R}}\mathbb{C}=2\tag{29}
$$

The underlying field must therefore be specified when discussing the dimension added by a complex coordinate.

**The CG display layer.** State generation and screen display are treated separately. A symbolic representation retains the coordinate count and constraints; actual rendering uses finitely many candidates, finite samples, or sections. A display map

$$
\pi_n:K^n\to\mathbb{R}^3\tag{30}
$$

may be chosen as needed. Displaying a projection of a higher-dimensional object differs from reducing the coordinate count of the object itself. There is no need to enumerate every point of an infinite set. Resource limits of an implementation are also distinct from any upper bound in the mathematical generation rule.

## 7. Scope of the operations and conclusions

If the candidate set $U$ is finite, for example, sums and products may lie outside $U$. When set arithmetic is used, $A+B:=\{a+b\mid a\in A,\ b\in B\}$ and $A\cdot B:=\{ab\mid a\in A,\ b\in B\}$ are operations on $\mathcal{P}(K)$. Restricting quotient outputs to $U$ is different from requiring every operation to be closed within $U$. No implicit truncation or rounding is introduced.

Shared variables must also be preserved. For example,

$$
\{x-x\mid x\in\mathbb{R}\}=\{0\},\qquad\mathbb{R}-\mathbb{R}=\mathbb{R}\tag{31}
$$

Set subtraction on the right chooses elements independently from the two sets. When an expression shares a variable, it is evaluated by extracting the output coordinates from the solution set of simultaneous conditions that preserve that sharing.

This paper explicitly adopts an operation that adds a new independent coordinate. It is not a theorem deduced solely from the two possible values of division by zero. The construction combines two roles: $Q_U(0,0)=U$ supplies all candidates for the new coordinate, and the Cartesian product generates that independent coordinate.

The construction rests on standard set theory, preimages, Cartesian products, and linear algebra. It does not require a multiplicative inverse of zero or recovery of an original dividend. The ability to evaluate expressions as sets does not, by itself, establish continuity or differentiability with respect to coefficients.

Placing independent coordinate generation at the center allows coordinate structures to be extended through any finite number of stages, without requiring a fixed higher-dimensional space at the outset. Real candidates increase the dimension of a nonempty real affine space by one; discrete candidates add a new independent axis of choice. Distinguishing the specified universe, coordinate count, and geometric dimension allows continuous figures and discrete grids to be described by the same generation rule.

## Author contributions

木村祐太 (Yuta Kimura): original concept and note; direction for independent coordinate generation and generalization of the universe. GPT-6 Astra (AI): formalization; organization of propositions and proofs; composition and editing of the Japanese and English manuscripts.

## References

［1］木村祐太 (Yuta Kimura). _Axioms of Division by Zero_ [in Japanese]. Unpublished note, ver. 20180228-, 2018. Preserved original: `output/reference/dimensional_shift_01_original.txt`.

［2］Seçkin Demirbaş and Andrew Rechnitzer. _PLP: An Introduction to Mathematical Proof_, §10.3, Definition 10.3.1 and Warning 10.3.3. University of British Columbia. [Authors' online text](https://personal.math.ubc.ca/~PLP/book/ch-functions-5.html) (accessed 7 November 2026).

［3］Sheldon Axler. _Linear Algebra Done Right_, 4th ed. Springer, 2024. Theorem 3.21, pp. 62–63; Theorem 3.92, p. 97. [Author's online PDF](https://linear.axler.net/LADR4e.pdf) (accessed 7 November 2026).
