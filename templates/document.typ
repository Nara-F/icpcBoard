// The builder inlines styles above this file and appends converted content.
#set document(title: {{ title }}, author: "Nara-F")
#show: book
#set page(paper: "a4", margin: (x: 25mm, top: 25mm, bottom: 24mm),
          header-ascent: 7mm, fill: luma(95%), header: none, footer: none)
#align(center + horizon)[
  #text(font: sans-font, size: 14pt, tracking: 2pt)[ICPC]
  #v(12mm)
  #text(font: serif-font, size: 36pt, weight: 700, {{ title }})
  #v(6mm)
  #text(size: 16pt, {{ subtitle }})
  #v(35mm)
  #text(size: 12pt)[竞赛算法模板与调试速查]
  #v(3mm)
  #text(size: 11pt)[Nara-F]
]
#pagebreak()
#set page(fill: none, footer: context align(center, text(9pt, counter(page).display())))
#text(font: sans-font, size: 20pt, weight: 600)[目录]
#v(6mm)
#show outline.entry.where(level: 1): it => block(above: 1em, below: .4em, text(font: sans-font, weight: 600, it))
#outline(title: none, depth: 2, indent: 1.6em)
#pagebreak()
#set page(header: running-header, footer: none)
