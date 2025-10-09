(...)

Vamos considerar observações $(X_i, y_i), i = 1, 2, dots, s$ e o modelo

$ y_i = tr(X_i^T M) + xi_i $

onde $x_i in RR^(m times n)$ são matrizes, $y_i$ e $xi_i$ escalares.

Nesta regressão matricial, vamos considerar também o problema de complementação matricial.

Para isso, iniciamos considerando a notação $[a(i), b(i)]$ como sendo índices linha-coluna de uma entrada da matriz na onbservação $i$.

Seja $x_i = e^n_(a(i)) (e^m_(b(i)))^T$, onde $e^m_l in RR^m$ é um vetor unitário, com elemento $1$ na posição $l$, tal que $X_i$ tem zeros em todos os lugares exceto na posição $[a(i), b(i)]$.

Portanto,

$ tr(X_i^T M) = m_(a(i) b(i)) $

Objetivo: predizer as entradas não-...

(Assuma que ${X_i}$ represente uma matriz de covariância)

Considerando a regressão multivariáveis, o problema de otimização via LASSO será:

$ min {1/(2N) sum_(i=1)^N sum_(j=1)^K (y_(i j) - tr(X_(i j)^T Theta))^2 + lambda norm(Theta)_* } $

onde $Theta in RR^(p times k)$ é a matriz dos coeficientes da regressão.

$X_(i j) = x_i (e_j^k)^T$, onde $e_j^k in RR^k$ é um vetor unitário com o valor $1$ na posição $j$.

$y_(i j)$ é a j-ésima componente de $y_i$ tal que a forma de regressão seja definida como:
$ y_(i j) = tr(X_(i j)^T Theta) + epsilon_(i j) $

#line(length: 100%)
= Decomposição Matricial Penalizada

Vamos considerar o seguinte problema de otimização na forma Lagrangiana:

$ min_(U, D, V) {norm(Z - U D V^T)_F^2 + lambda_1 norm(U)_1 + lambda_2 norm(V)_1} $
onde $U in RR^(m times r), V in RR^(r times r), D in RR^(r times r)$. Note a existência de penalizações em norma-1 para os vetores singulares à esquerda e a direita da decomposição.

Para facilitar o entendimento desse problema de otimização, vamos considerar o caso 1-D na forma de restrição:

$ min norm(Z - d u v^T)_F^2 " sujeito a " norm(u)_1 lt.eq.slant c_1 $

...

Observação. As restrições impostas simultâneamente em $norm(.)_2$ e $norm(.)_1$ resultam em soluções que são esparsas.

$ min norm(Z - d u v^T)_p^2 " sujeito a " norm(u)_1 lt.eq.slant c_1, norm(v)_1 lt.eq.slant c_1 dots $

*Algoritmo*

1. Seja $v$ o vetor singular à esquerda da decomposição SVD em $Z$
2. Atualize
$ u = S_(lambda_1) (Z_v) \/ norm(S_(lambda_1) (Z_v))_2 $
com $lambda_1$ sendo um valor tão pequeno tal que $norm(u)_1 lt.eq.slant c_1$
3. Atualize a outra direção
$ v = S_(lambda_2) (Z^T u) \/ norm(S_(lambda_2) (Z^T u))_2 $
com $lambda_2$ sendo o menor tal que $norm(v)_1 lt.eq.slant c_2$.
4. Repita os passos 2. e 3. até convergência.
5. Retorne $u,v$ e $d=u^T Z v$.

*Algoritmo (Generalizado)*

#set enum(numbering: "1.a.")

1. Seja $R = Z$
2. Para $k=1,2,dots,k$ faça
  1. Determine $u_k, v_k, d_k$ aplicando o algoritmo anterior na matriz de dados $R$.
  2. Atualize
  $ R = R - d_k u_k v_k^T $

*Comentários*: Decomposição Matrizial Esparsa e Complementação Matricial.

== Decomposição Matricial Aditiva

Vamos considerar o modelo
$ Z = L^* + S^* + W $
onde o par $(L^*, S^*)$ representa uma matriz de posto reduzido e uma matriz esparsa, sendo $W$ uma matriz de ruídos.

*Observação* $P_r (L^* + S^*)$ é usado em problemas de complementação matricial.

O problema de otimização neste caso pode ser definido:
$ min_(L,S) {1\/2 norm(Z - (L + S))_F^2 + lambda_1 Phi_1 (L) + Phi_2 (S)} $

$L in RR^(m times n); S in RR^(m times n)$

Em particular, para garantir posto reduzido, impomos:
$ Phi_1 (L) = norm(L)_* $
e para garantirmos uma matriz esparsa:
$ Phi_2 (S) = norm(S)_1 $

== Aprendizado não-supervisionado

Conceitos e ideias sobre aprendizado supervisionado e não-supervisionado.

*Clusterização via _K-means_ (agrupamento)*

Notação: Vamos caracterizar usando vetores com $N$ posições, denotados como $c_i$ a posição do vetor $c$ relacionado a $x_i$.

Exemplo: $N=5 quad k=3 quad c = (3, 1, 1, 1, 2) = (x_1, x_2, x_3, x_4, x_5)$

$G_1 = {2, 3, 4}, quad, G_2 = {5}, quad, G_3 = {1}$
...

Agora, para cada grupo usaremos um grupo associado, denotado como grupo representativo $z_1, z_2, dots, z_k$.

Intuitivamente, podemos considerar que desejamos que cada grupo representativo esteja próximo aos vetores no seu grupo associado, por exemplo, $norm(x_i - z_(c_i))$ precisa ser pequeno.

Vamos definir
$ J = (norm(x_i - z_(c_1))_2^2 + norm(x_2 - z_(c_2))_2^2 + dots) \/ N $

...
// TODO: escrever o restante