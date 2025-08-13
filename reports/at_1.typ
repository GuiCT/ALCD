#import "@preview/subpar:0.2.2"

#set text(lang: "pt", region: "br")
#set par(justify: true)

#grid(
  columns: (1fr, 1fr),
  align: center,
  [Aluno: Guilherme Cesar Tomiasi],
  [Data de entrega: 14/08/2025]
)

= Atividade 1: Teorema da Melhor Aproximação de uma matriz
== Caso 1: Imagem única

Dada a @fig_cologne, de dimensões $1684 times 1500$, foram realizadas as reduções com $r in {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024}$. As fotos reconstruídas (em formato monocromático) foram todas dispostas na @full, com os erros obtidos na @erros_sole.

#figure(
  image("../resources/a_1_sole.jpg"),
  caption: "Catedral de Colônia, na Alemanha"
) <fig_cologne>

#subpar.grid(
  figure(image("../results/at_1/sole/r=1.jpg"), caption: [
    $r=1$
  ]), <r_1>,
  figure(image("../results/at_1/sole/r=2.jpg"), caption: [
    $r=2$
  ]), <r_2>,
  figure(image("../results/at_1/sole/r=4.jpg"), caption: [
    $r=4$
  ]), <r_4>,
  figure(image("../results/at_1/sole/r=8.jpg"), caption: [
    $r=8$
  ]), <r_8>,
  figure(image("../results/at_1/sole/r=16.jpg"), caption: [
    $r=16$
  ]), <r_16>,
  figure(image("../results/at_1/sole/r=32.jpg"), caption: [
    $r=32$
  ]), <r_32>,
  figure(image("../results/at_1/sole/r=64.jpg"), caption: [
    $r=64$
  ]), <r_64>,
  figure(image("../results/at_1/sole/r=128.jpg"), caption: [
    $r=128$
  ]), <r_128>,
  figure(image("../results/at_1/sole/r=256.jpg"), caption: [
    $r=256$
  ]), <r_256>,
  figure(image("../results/at_1/sole/r=512.jpg"), caption: [
    $r=512$
  ]), <r_512>,
  figure(image("../results/at_1/sole/r=1024.jpg"), caption: [
    $r=1024$
  ]), <r_1024>,
  columns: (1fr, 1fr, 1fr),
  caption: [Todas as reconstruções realizadas para a figura única],
  label: <full>,
)

#figure(
  image("../results/at_1/sole/errors.png"),
  caption: "Erros obtidos e a tendência de diminuição com aumento do posto"
) <erros_sole>

== Caso 2: Montagem com 25 fotos

Dada a @fig_montage, de dimensões $710 times 810$, foram realizadas as reduções com $r in {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024}$. As fotos reconstruídas (em formato monocromático) foram todas dispostas na @full_montage, com os erros obtidos na @erros_montage. O erro médio percentual foi omitido nesse caso pois foram observadas muitas divisões por zero, ocasionando valores inválidos.

#figure(
  image("../resources/a_1_montage.jpg"),
  caption: "Montagem com 25 fotos de jogadores de CS2; Fonte: HLTV.org"
) <fig_montage>

#subpar.grid(
  figure(image("../results/at_1/montage/r=1.jpg"), caption: [
    $r=1$
  ]), <r_1>,
  figure(image("../results/at_1/montage/r=2.jpg"), caption: [
    $r=2$
  ]), <r_2>,
  figure(image("../results/at_1/montage/r=4.jpg"), caption: [
    $r=4$
  ]), <r_4>,
  figure(image("../results/at_1/montage/r=8.jpg"), caption: [
    $r=8$
  ]), <r_8>,
  figure(image("../results/at_1/montage/r=16.jpg"), caption: [
    $r=16$
  ]), <r_16>,
  figure(image("../results/at_1/montage/r=32.jpg"), caption: [
    $r=32$
  ]), <r_32>,
  figure(image("../results/at_1/montage/r=64.jpg"), caption: [
    $r=64$
  ]), <r_64>,
  figure(image("../results/at_1/montage/r=128.jpg"), caption: [
    $r=128$
  ]), <r_128>,
  figure(image("../results/at_1/montage/r=256.jpg"), caption: [
    $r=256$
  ]), <r_256>,
  figure(image("../results/at_1/montage/r=512.jpg"), caption: [
    $r=512$
  ]), <r_512>,
  figure(image("../results/at_1/montage/r=1024.jpg"), caption: [
    $r=1024$
  ]), <r_1024>,
  columns: (1fr, 1fr, 1fr),
  caption: [Todas as reconstruções realizadas para a figura única],
  label: <full_montage>,
)

#figure(
  image("../results/at_1/montage/errors.png"),
  caption: "Erros obtidos e a tendência de diminuição com aumento do posto"
) <erros_montage>