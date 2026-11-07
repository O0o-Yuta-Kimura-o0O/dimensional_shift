#import "/scripts/paper_style.typ": setup, m, eq
#show: setup.with(lang: "en")
// BEGIN PAPER CONTENT
*Abstract.* This paper defines a quotient as the solution set of a multiplication equation and examines the set-valued results of division by zero and dimension changes in solution sets. Specifying the field #m("K") for arithmetic and the candidate set #m("U") gives #m("Qzero") and the empty set for division of a nonzero number by zero. Repeated division by zero alone creates no new coordinates, so we separately define the independent coordinate generation operation #m("lift"). With all real numbers as candidates, each application increases the dimension of a nonempty real affine space by one. For the finite grids studied here, each application likewise increases both the independent coordinate count and the dimension of the real affine hull, the smallest real affine space containing the grid, by one. Distinguishing a grid from its real affine hull, we relate coordinate generation to releasing constraints on existing coordinates, dimension reduction through linear constraints, and 3D computer graphics. Coordinate structures extend through any finite number of stages without a fixed maximum coordinate count. The formulation uses standard set theory and linear algebra; it requires neither a multiplicative inverse of zero nor recovery of computational history.

*Keywords.* set-valued quotient, division by zero, solution set, independent coordinate generation, linear constraint, discrete grid

= Purpose and basic setting

The original note ［1］ proposed treating quotients involving division by zero as either the universe or the empty set, and expanding the value of an expression into points, lines, and planes. This paper formalizes that idea by combining a definition of division by zero through set-valued quotients with dimension changes in solution sets through independent coordinate generation and constraints. To distinguish repeated division by zero, release of constraints on existing axes, and generation of new axes, we first define coordinate structures and the operation that generates them, then establish their relation to set-valued quotients.

Coordinate generation uses a nonempty set #m("U"). When quotients are considered from Section 4 onward, the field #m("K") for ordinary multiplication is either the real or complex field, and #m("setting") is assumed. The set #m("U") is the universe of possible values for one coordinate; with #m("n") current coordinates, the coordinate space is #m("Un"). The number zero itself does not carry information about the universe. Instead, #m("U") is specified explicitly as part of the context of the operation.

Numbers are embedded into singleton sets when necessary, without identifying a number literally with its singleton. For a nonempty real affine space #m("affine"), we define #m("dimdef"). This definition is not applied unconditionally to arbitrary sets or discrete grids. No dimension is assigned to the empty set in this paper.

= An operation that generates independent coordinates

*Definition 1 (States with coordinate structure).* A state is a pair of the following form.
#eq("state")

Here #m("n") records the current number of coordinates, not previous expressions or dividends. We set #m("U0"), allowing the construction to start from the singleton consisting of the empty coordinate tuple.

*Definition 2 (Independent coordinate generation).* Define an operation on states by
#eq("lift")

The Cartesian product is interpreted by concatenating coordinates. Thus elements of the resulting set have the form
#eq("concat")

Each new coordinate takes values independently from #m("U"), with no additional relation imposed between it and the existing coordinates. Independence here is set-theoretic: all combinations are permitted. It is not an assumption of probabilistic independence.

#pagebreak()

*Proposition 1 (Recursive coordinate generation).* For every nonnegative integer k,
#eq("iterate")
#eq("initial")

*Proof.* For k equal to zero, the operation is the identity. Taking one further Cartesian product after k applications appends one element of #m("U") by coordinate concatenation. The result follows by induction. The coordinate count is finite at every stage, and the rule requires no fixed maximum count. □

Empty solution sets also retain their coordinate structure, so #m("emptylift"). The states #m("two_empty_states") have different coordinate counts, although neither contains a solution.

*Proposition 2 (Increase in real affine dimension).* If #m("U") is the set of all real numbers and S is a nonempty real affine space, then
#eq("real_lift_dim")

*Proof.* Writing #m("affine"), we have
#eq("affine_lift")

Embed a basis of V with zero in the new coordinate, and add the unit vector in the new coordinate direction. These vectors form a basis of the direction space, so the dimension increases by one. □

Starting from the initial state produces a point, the real line, a plane, and three-dimensional space.
#eq("real_sequence")

Coordinate count is distinct from the dimension of the set itself. For example, #m("pointa") is a zero-dimensional point in a one-coordinate ambient space. Likewise, #m("repeat_variable") is a line, whereas #m("independent_variables") is a plane. Copying the same variable is different from generating an independent coordinate.

= Distinction from releasing constraints on fixed axes

For a fixed number #m("n") of real coordinates and coefficients #m("d_setting"), consider the family
#eq("fixed_diag")

A coordinate with a nonzero coefficient is fixed at zero, while a coordinate with a zero coefficient is free. Consequently,
#eq("diag_dim")

This method changes the number of free directions within the same coordinate space. Definition 2 instead increases the coordinate count of the state itself. The two operations are different; the former alone cannot exceed the fixed coordinate count.

Here we assume #m("control_setting"). Using the quotient defined in Section 4, coordinate addition and its constraint can also be expressed in a single formula.
#eq("controlled_lift")
#eq("controlled_cases")

This operation always adds one coordinate. A nonzero coefficient fixes the new coordinate at zero, while a zero coefficient permits all candidates. Definition 2 is the zero-coefficient case.

#pagebreak()

= Defining division by zero through set-valued quotients

*Definition 3 (Quotients with a specified candidate set).* Under the assumption #m("setting"), define
#eq("Qdef")

Its type is #m("Qtype"). Using the map #m("multmap"), it can be written as the preimage #m("preimage"). Existence of a preimage does not imply existence of an inverse function ［2］.

*Proposition 3 (Three cases determined by the candidate set).*
#eq("Qcases")

*Proof.* For nonzero b, the equation has the unique solution a/b in the field #m("K"). This value is retained exactly when it belongs to #m("U"). If b is zero, the left-hand side is zero for every candidate x. Thus all candidates are solutions when a is zero, and no solution exists when a is nonzero. □

In particular, #m("Qzero") is not specific to the real numbers. Specifying the candidate set gives, for example,
#eq("example_universes")

The finite set Dₘ is defined in Section 6. Changing the candidate set also affects division by nonzero numbers: #m("integer_half"), whereas #m("real_half"). Ordinary real division must not be assumed to remain closed within the integers or a finite grid.

The Cartesian-product operation in Definition 2 also applies to an arbitrary abstract set. However, the equation bx=a cannot be applied directly to a set without specified multiplication and zero. A quotient requires the algebraic structure described here, or a separately defined relation.

*Definition 4 (Extension to sets).*
#eq("setQ")

*Proposition 4 (Repeated division by zero does not add coordinates).* With #m("Edef"),
#eq("Ecases")

*Proof.* An element a of A satisfying 0x=a exists exactly when A contains zero. In that case every candidate is a solution. Since #m("U") contains zero, applying the operation again leaves the output unchanged, whether that output is #m("U") or the empty set. □

Coordinate generation therefore does not follow automatically from the set-valued quotient. Substituting Proposition 3 into Definition 2 gives the connection
#eq("liftQ")

The quotient supplies the candidate set for the new coordinate, and the Cartesian-product operation adds that coordinate.

For the abbreviation #m("eta"), we have #m("eta_loss"), so an arbitrary original argument cannot be recovered from the set-valued result. Rules such as #m("bad_eta"), which subsequently operate on discarded arguments, are not adopted.

#pagebreak()

= Real linear systems and dimension reduction

In this section, #m("U") is the set of all real numbers. Let A be a real matrix with m rows and n columns, and let b be a real vector with m components. Define
#eq("fiber")

*Proposition 5 (General linear solution sets).* The solution set is nonempty if and only if #m("b_in_image"). If it is nonempty, choosing one solution x₀ gives
#eq("fiber_dim")

*Proof.* Nonemptiness follows from the definition of the image. Since Ax=b and Ax₀=b, the difference x−x₀ belongs to the kernel of A. Conversely, adding any element of that kernel to x₀ gives a solution. The dimension formula follows from the rank-nullity theorem ［3, Theorem 3.21］. □

This formula describes freedom within a fixed set of n coordinates. Definition 2 instead updates n. A rank decrease caused by coefficient changes can thus be distinguished from an increase in coordinate count caused by coordinate generation.

*Proposition 6 (Dimension reduction by linear constraints).* Add a condition given by a linear map T and a constant c to a nonempty real affine space #m("affine").
#eq("restriction")

If the constrained set remains nonempty, then
#eq("restriction_dim")

The restriction of T here describes its action on the original free directions V.

*Proof.* Choose one solution x₀ satisfying the added constraint. Then
#eq("restriction_affine")

The direction space is the kernel of T restricted to V, so the rank-nullity theorem applies. □

Thus adding r constraints that are independent on the existing free directions reduces the dimension by r, provided a solution remains. Redundant constraints leave the dimension unchanged; inconsistent constraints produce the empty solution set. A concrete example is
#eq("constraint_example")

Restricting a range by inequalities need not reduce dimension. The square defined by #m("square") is a two-dimensional region in the usual geometric sense. In contrast, imposing #m("paired_inequalities") simultaneously is equivalent to y=0 and restricts the plane to a line.

= Discrete universes and grid visualization

*Example 1 (A finite grid).* As a subset of the real field, take
#eq("Dm")

Proposition 3 gives #m("Qzero"). Three applications of independent coordinate generation therefore yield
#eq("finite_grid")

#pagebreak()

For example, m equal to two gives 125 points. Rendering each point #m("sample_points") as a position in 3D computer graphics produces a grid of points. The stages of generation are
#eq("grid_sequence")

They give a row of points, a planar point set, and a spatial point set. Automatic interpolation of line segments or surfaces is not part of this definition.

*Changing the range through m versus increasing coordinate count.* Changing m changes the number of candidates on each axis and the displayed range. Applying Definition 2 again increases the number of coordinates. These are different changes.

*Coordinate count and geometric dimension.* The integer grid #m("integer_grid") has three independent integer coordinates, but it is not continuous real space itself. In the usual Euclidean distance, each grid point is isolated within a neighborhood of radius 1/2. The same holds for the finite grid. We therefore describe these objects as three-coordinate grids, distinguishing them from the increase in real affine dimension in Proposition 2.

If instead we consider the real affine hull, the smallest real affine space containing the grid, then
#eq("grid_hull")

This follows because the grid contains zero and every standard basis vector. The grid itself is not identified with its affine hull.

*Degenerate candidate sets and complex numbers.* For #m("singletonU"), adding another coordinate position provides only one possible value and does not increase geometric freedom. For complex numbers,
#eq("complex_dims")

The underlying field must therefore be specified when discussing the dimension added by a complex coordinate.

*The CG display layer.* State generation and screen display are treated separately. A symbolic representation retains the coordinate count and constraints; actual rendering uses finitely many candidates, finite samples, or sections. A display map
#eq("display_map")

may be chosen as needed. Displaying a projection of a higher-dimensional object differs from reducing the coordinate count of the object itself. There is no need to enumerate every point of an infinite set. Resource limits of an implementation are also distinct from any upper bound in the mathematical generation rule.

= Scope of the operations and conclusions

If the candidate set #m("U") is finite, for example, sums and products may lie outside #m("U"). When set arithmetic is used, #m("sum_def") and #m("product_def") are operations on #m("powersetK"). Restricting quotient outputs to #m("U") is different from requiring every operation to be closed within #m("U"). No implicit truncation or rounding is introduced.

Shared variables must also be preserved. For example,
#eq("share_difference")

Set subtraction on the right chooses elements independently from the two sets. When an expression shares a variable, it is evaluated by extracting the output coordinates from the solution set of simultaneous conditions that preserve that sharing.

#pagebreak()

The set-valued quotient describes the result of division by zero in terms of the existence of solutions to a multiplication equation. Although #m("Qzero") supplies all candidates for a new coordinate, it does not by itself increase the coordinate count. Separately adopting a Cartesian-product operation that adds a new independent coordinate connects the set-valued result of division by zero with coordinate generation. This is not a theorem deriving dimension increase solely from the two possible values of division by zero.

The construction rests on standard set theory, preimages, Cartesian products, and linear algebra. It does not require a multiplicative inverse of zero or recovery of an original dividend. The ability to evaluate expressions as sets does not, by itself, establish continuity or differentiability with respect to coefficients.

Combining set-valued quotients, independent coordinate generation, and restriction of sets by constraints describes dimension changes in solution sets. Coordinate structures can extend through any finite number of stages without requiring a fixed higher-dimensional space at the outset. If the candidate set is the set of all real numbers, each application of the operation increases the dimension of a nonempty real affine space by one. The finite grids in Section 6 satisfy #m("grid_hull"). With m fixed, each application of independent coordinate generation increases both the independent coordinate count and the dimension of the real affine hull by one. Thus, even for discrete grids, the dimension that measures the spread of the point set through its real affine hull increases. The grid itself is not identified with a continuous real affine space, nor does the construction automatically interpolate between grid points. Dimension reduction through linear constraints depends on their independence on the existing free directions and on the existence of solutions.

== Author contributions

木村祐太 (Yuta Kimura): original concept and note; direction for independent coordinate generation and generalization of the universe. GPT-6 Astra (AI): formalization; organization of propositions and proofs; composition and editing of the Japanese and English manuscripts.

== References

［1］木村祐太 (Yuta Kimura). _Axioms of Division by Zero_ [in Japanese]. Unpublished note, ver. 20180228-, 2018. Preserved original: `output/reference/dimensional_shift_01_original.txt`.

［2］Seçkin Demirbaş and Andrew Rechnitzer. _PLP: An Introduction to Mathematical Proof_, §10.3, Definition 10.3.1 and Warning 10.3.3. University of British Columbia. #link("https://personal.math.ubc.ca/~PLP/book/ch-functions-5.html")[Authors' online text] (accessed 7 November 2026).

［3］Sheldon Axler. _Linear Algebra Done Right_, 4th ed. Springer, 2024. Theorem 3.21, pp. 62–63; Theorem 3.92, p. 97. #link("https://linear.axler.net/LADR4e.pdf")[Author's online PDF] (accessed 7 November 2026).
// END PAPER CONTENT
