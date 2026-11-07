// Shared layout and equations for the two language editions.
#let config = json("/output/current/paper_config.json")
#let formulas = json("/output/current/equations.json")
#let m(id) = math.equation(block: false, eval(formulas.at(id).typst, mode: "math"))
#let eq(id) = math.equation(block: true, numbering: "(1)", eval(formulas.at(id).typst, mode: "math"))

#let setup(lang: "ja", body) = {
  let ja = lang == "ja"
  let title = config.titles.at(lang)
  let subtitle = config.subtitles.at(lang)
  let dateparts = config.date.split("-").map(int)
  set document(title: title.replace("\n", " "), author: config.authors,
    description: subtitle + ". " + config.version,
    date: datetime(year: dateparts.at(0), month: dateparts.at(1), day: dateparts.at(2)))
  set page(paper: "a4", margin: (x: 24mm, top: 21mm, bottom: 21mm),
    numbering: "1", number-align: center,
    header: context if counter(page).get().first() > 1 {
      text(size: 8pt, fill: luma(110))[#config.headers.at(lang) #h(1fr) #config.version]
    })
  set text(font: ("Libertinus Serif", "Hiragino Mincho ProN", "Noto Serif CJK JP"), size: 10pt, lang: lang)
  set par(justify: true, leading: if ja { 0.68em } else { 0.6em }, first-line-indent: 1em)
  set heading(numbering: "1.")
  show heading: set text(font: if ja { ("Hiragino Sans", "Noto Sans CJK JP") } else { ("Libertinus Sans", "Hiragino Sans") }, weight: "bold")
  show heading.where(level: 1): set block(above: 1.1em, below: 0.55em)
  show heading.where(level: 1): set text(size: 12pt)
  show heading.where(level: 2): set heading(numbering: none)
  show heading.where(level: 2): set text(size: 11pt)
  set block(above: 0.6em, below: 0.6em)
  set math.equation(numbering: "(1)")
  align(center)[
    #text(size: if ja { 17pt } else { 16pt }, weight: "bold", title.split("\n").map(s => text(s)).join(linebreak()))
    #v(0.6em)
    #text(size: 10.5pt, subtitle)
    #v(0.8em)
    #if ja { [木村祐太　・　GPT-6 Astra（AI）] } else { [木村祐太 (Yuta Kimura) · GPT-6 Astra (AI)] }
    #linebreak()
    #text(size: 9pt)[#config.date #h(1em) #config.version]
  ]
  v(0.6em)
  body
}
