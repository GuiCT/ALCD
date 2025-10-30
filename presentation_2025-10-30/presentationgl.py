from manimlib import *
from manim_slides.slide import Slide
import numpy as np


class TitleScene(Slide):
    # ------------------------
    COURSE = "Álgebra Linear para Ciência de Dados"
    PRESENTATION_TITLE = "Métodos Kernel, Kernel PCA"
    AUTHORS = "Guilherme Tomiasi"
    DATE = "30/10/2025"
    BACKGROUND_COLOR = WHITE
    TEXT_COLOR = "#00008B"
    # ------------------------

    def construct(self):
        self.camera.background_rgba = list(color_to_rgba(WHITE, 1))

        # Title and course
        course = TexText(self.COURSE, font_size=48, fill_color=self.TEXT_COLOR, tex_environment="justify")
        title = TexText(self.PRESENTATION_TITLE, font_size=32,
                        fill_color=self.TEXT_COLOR, tex_environment="justify")

        title_group = VGroup(course, title).arrange(
            DOWN, aligned_edge=ORIGIN, buff=0.6)
        title_group.to_edge(UP, buff=1.6)

        # Authors, institute and date at lower part
        authors = Text(self.AUTHORS, font_size=24, fill_color=self.TEXT_COLOR)
        date = Text(self.DATE, font_size=18, fill_color=self.TEXT_COLOR)

        bottom_group = VGroup(authors, date).arrange(DOWN, buff=0.2)
        bottom_group.to_edge(DOWN, buff=0.8)

        # Compose master group (for clean animations)
        master = VGroup(title_group, bottom_group)

        # Entrance animation
        self.play(FadeIn(course))
        self.play(FadeIn(bottom_group))
        self.next_slide()
        self.play(LaggedStart(FadeIn(title), lag_ratio=0.25))

        self.next_slide()
        # Small flourish when moving on
        self.play(FadeOut(master, shift=UP), run_time=0.6)


class FeatureMapExplanation(ThreeDScene, Slide):
    TEXT_COLOR = "#00008B"
    default_frame_orientation = (0, 0)

    def construct(self):
        self.camera.background_rgba = list(color_to_rgba(WHITE, 1))
        additional_preamble = "\\usepackage{ragged2e}\n\\usepackage{stackengine}"
        tex_config = {
            "fill_color": self.TEXT_COLOR,
            "additional_preamble": additional_preamble,
            "font_size": 32,
        }
        tex_exclude_font = tex_config.copy()
        tex_exclude_font.pop("font_size")

        t = Title("Feature Map", fill_color=self.TEXT_COLOR)
        self.play(FadeIn(t))
        par = Tex("Uma maneira de transformar dados não-lineares para cumprir propriedades necessárias para a aplicação de métodos lineares.",
                  tex_environment="justify", **tex_config).move_to(2 * UP)
        self.play(FadeIn(par))
        self.next_slide()
        ex_pre = Tex("Dado um conjunto de dados $\\mathbf{x_1}, \\dots, \\mathbf{x_m} \\in \\mathbb{R}^n$. Se aplicarmos uma transformação:",
                     tex_environment="justify", **tex_config).move_to(par.get_center()).shift(DOWN)
        self.play(FadeIn(ex_pre))
        self.next_slide()
        p = Tex(r"\phi: \mathbb{R}^n \rightarrow \mathbb{R}^d \quad d \stackanchor{>}{>>} n",
                font_size=50, **tex_exclude_font).move_to(ex_pre.get_center()).shift(DOWN)
        self.play(FadeIn(p))
        self.next_slide()
        ex_post = Tex("Obtemos os vetores de observações $\\mathbf{z_i} = \\phi(\\mathbf{x_i})$. Um exemplo de aplicação a transformação de um conjunto para aplicar métodos de regressão polinomial (quadrática, cúbica) sobre a fundação de regressão linear. Outro caso comum é a transformação de um conjunto não linearmente separável em linearmente separável.",
                      tex_environment="justify", **tex_config).move_to(p.get_center()).shift(1.5 * DOWN)
        self.play(FadeIn(ex_post))
        self.next_slide()


class FeatureMap3DExample(ThreeDScene, Slide):
    default_frame_orientation = (0, 0)

    def construct(self):
        self.camera.background_rgba = list(color_to_rgba(BLACK, 1))
        t2 = Title("Exemplo", fill_color=WHITE)
        self.play(FadeIn(t2))
        inner_r, outer_r = 1.0, 2.0

        axes_2d = Axes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
        )
        axes = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(-1, 4, 1),
        )

        inner_pts_3d = self.circle_points_3d(inner_r, z=0.0, axes_ref=axes, n=30, color=BLUE)
        outer_pts_3d = self.circle_points_3d(outer_r, z=2.0, axes_ref=axes, n=30, color=RED)

        self.play(FadeIn(axes_2d))
        self.play(*[FadeIn(p, scale=0.5) for p in inner_pts_3d])
        self.play(*[FadeIn(p, scale=0.5) for p in outer_pts_3d])

        self.next_slide()

        self.play(Transform(axes_2d, axes))
        frame = self.camera.frame
        self.play(
            frame.animate.set_euler_angles(
                theta=60 * DEGREES, phi=70 * DEGREES),
            run_time=2
        )

        # Separating plane z = 1
        plane = ParametricSurface(
            lambda u, v: np.array([u, v, 1.0]),
            u_range=(-2, 2), v_range=(-2, 2),
        )
        self.play(FadeOut(t2))
        self.play(FadeIn(plane))

        plane_text = Tex("\\text{Plano em } z=1 \\text{ acaba por separar as duas classes.}", font_size=24, fill_color=WHITE).to_corner(UR).fix_in_frame()
        self.play(FadeIn(plane_text))

        self.next_slide(loop=True)
        self.play(
            frame.animate.increment_theta(180 * DEGREES),
            run_time=5,
            rate_func=smooth,
        )
        self.play(
            frame.animate.increment_theta(180 * DEGREES),
            run_time=5,
            rate_func=smooth,
        )
        self.next_slide()

    def circle_points_3d(self, r, z, axes_ref, n=30, color=WHITE):
        # Use Sphere in ManimGL instead of Dot3D
        spheres = []
        for a in np.linspace(0, TAU, n, endpoint=False):
            noisex = np.random.rand() * 0.25
            noisey = np.random.rand() * 0.25
            noisez = np.random.rand() * 0.25
            x, y = r * np.cos(a), r * np.sin(a)
            noisy_x = x + noisex
            noisy_y = y + noisey
            noisy_z = z + noisez
            position = axes_ref.c2p(noisy_x, noisy_y, noisy_z)
            s = Sphere(radius=0.06, color=color)
            s.move_to(position)
            spheres.append(s)
        return spheres


class FeatureMapCons(Slide):
    TEXT_COLOR = "#00008B"
    default_frame_orientation = (0, 0)
    TEXT_LIST = [
        "Dificuldade de formular uma expressão de forma manual",
        "Aumento considerável do espaço vetorial utilizado (quando $d \\gg n$), tornando o cálculo inviável.",
        "Dessa maneira, a forma de contornar esse problema é simplesmente \\textbf{não utilizar} essa técnica específica, mas uma alternativa chamada \\textbf{funções kernel}."
    ]

    def construct(self):
        self.camera.background_rgba = list(color_to_rgba(WHITE, 1))
        additional_preamble = "\\usepackage{ragged2e}\n\\usepackage{stackengine}"
        tex_config = {
            "fill_color": self.TEXT_COLOR,
            "additional_preamble": additional_preamble,
            "font_size": 32,
        }
        tex_exclude_font = tex_config.copy()
        tex_exclude_font.pop("font_size")

        t = Title(
            "Problemas do \\textit{Feature Map}", fill_color=self.TEXT_COLOR)
        self.play(FadeIn(t))
        start = Tex("O uso de \\textit{Feature Maps} é inviabilizado por alguns motivos:",
                    tex_environment="justify", **tex_config).move_to(2 * UP)
        self.play(FadeIn(start))
        self.next_slide()
        current_list_of_cons = []
        anchor = start
        for i in range(len(self.TEXT_LIST)):
            tex_string = f"\\item {self.TEXT_LIST[i]}"
            con_item = Tex(tex_string, tex_environment="itemize", font_size=24,
                           **tex_exclude_font).move_to(anchor.get_left(), LEFT)
            total_height = anchor.get_height() + con_item.get_height()
            con_item = con_item.shift(total_height * DOWN)
            self.play(FadeIn(con_item))
            current_list_of_cons.append(con_item)
            anchor = con_item
            self.next_slide()


class KernelFunctionDefinition(Slide):
    TEXT_COLOR = "#00008B"
    default_frame_orientation = (0, 0)
    TEXT_LIST = [
        "Costuma ser utilizada para denotar a similaridade entre pares de pontos. Por exemplo, a função de distância: $\\mathcal{K}(\\mathbf{x}, \\mathbf{y}) = \\norm{\\mathbf{x} - \\mathbf{y}}^p$, ou o produto interno usual: $\\mathcal{K}(\\mathbf{x}, \\mathbf{y}) = \\mathbf{x}^T \\mathbf{y}$, também chamado de kernel linear.",
        "Traduzindo o conceito de \\textit{feature map} para funções kernel, chama-se de kernel associado $\\mathcal{K}_\\phi$ a expressão dada por\n$$ \\mathcal{K}_\\phi(\\mathbf{x}, \\mathbf{y}) = \\phi(\\mathbf{x}) \\cdot \\phi(\\mathbf{y}) = \\sum_{i=1}^d \\phi_i (\\mathbf{x}) \\phi_i(\\mathbf{y}) $$",
    ]

    def construct(self):
        self.camera.background_rgba = list(color_to_rgba(WHITE, 1))
        additional_preamble = "\\usepackage{ragged2e}\n\\usepackage{stackengine}"
        additional_preamble_geometry = f"{additional_preamble}\n\\usepackage{{geometry}}\\geometry{{textwidth=170mm}}"
        tex_config = {
            "fill_color": self.TEXT_COLOR,
            "additional_preamble": additional_preamble,
            "font_size": 32,
        }
        tex_excludes = tex_config.copy()
        tex_excludes.pop("font_size")
        tex_excludes["additional_preamble"] = additional_preamble_geometry

        t = Title("\\textit{Kernel Function} (Funções Kernel)",
                  fill_color=self.TEXT_COLOR)
        self.play(FadeIn(t))
        start = Tex("Definição: uma função kernel é uma função \\textbf{simétrica} dada por $\\mathcal{K}: \\mathbb{R}^n \\times \\mathbb{R}^n \\rightarrow \\mathbb{R}$",
                    tex_environment="justify", **tex_config).move_to(2 * UP)
        self.play(FadeIn(start))
        self.next_slide()
        current_list_of_cons = []
        anchor = start
        for i in range(len(self.TEXT_LIST)):
            tex_string = f"\\item {self.TEXT_LIST[i]}"
            con_item = Tex(tex_string, tex_environment="itemize",
                           font_size=24, **tex_excludes).move_to(anchor.get_left(), LEFT)
            total_height = anchor.get_height() + con_item.get_height()
            con_item = con_item.shift(total_height * DOWN)
            self.play(FadeIn(con_item))
            current_list_of_cons.append(con_item)
            anchor = con_item
            self.next_slide()


class KernelMatrixDefinition(Slide):
    TEXT_COLOR = "#00005F"
    default_frame_orientation = (0, 0)
    TEXT_LIST = [
        "Ao utilizar o kernel linear, a matriz kernel é igual a matriz Gram.",
        "Caso definirmos a matriz de entrada após a aplicação de um \\textit{feature map}:\n$$ Z = \\begin{bmatrix} \\phi(\\mathbf{x}_1)^T \\\\ \\phi(\\mathbf{x}_2)^T \\\\ \\vdots \\\\ \\phi(\\mathbf{x}_m)^T \\end{bmatrix} = \\begin{bmatrix} \\mathbf{z}_1^T \\\\ \\mathbf{z}_2^T \\\\ \\vdots \\\\ \\mathbf{z}_m^T \\end{bmatrix} $$\nlogo obtemos a equivalência $K = Z Z^T$, de forma que garantimos que $K$ é semi-definida positiva.",
    ]

    def construct(self):
        self.camera.background_rgba = list(color_to_rgba(WHITE, 1))
        additional_preamble = "\\usepackage{ragged2e}\n\\usepackage{stackengine}"
        additional_preamble_geometry = f"{additional_preamble}\n\\usepackage{{geometry}}\\geometry{{textwidth=170mm}}"
        tex_config = {
            "fill_color": self.TEXT_COLOR,
            "additional_preamble": additional_preamble,
            "font_size": 32,
        }
        tex_excludes = tex_config.copy()
        tex_excludes.pop("font_size")
        tex_excludes["additional_preamble"] = additional_preamble_geometry

        t = Title("Matriz kernel",
                  fill_color=self.TEXT_COLOR)
        self.play(FadeIn(t))
        start = Tex("Definição: dada uma função kernel, é possível construir uma matriz $K \\in \\mathbb{R}^{m \\times m}$ onde o valor na posição $(i, j)$ é dado por $\\mathcal{K}(\\mathbf{x}_i, \\mathbf{x}_j)$. Como a função \\textit{kernel} é por si só simétrica, logo $K = K^T$.",
                    tex_environment="justify", **tex_config).move_to(2 * UP)
        self.play(FadeIn(start))
        self.next_slide()
        current_list_of_cons = []
        anchor = start
        for i in range(len(self.TEXT_LIST)):
            tex_string = f"\\item {self.TEXT_LIST[i]}"
            con_item = Tex(tex_string, tex_environment="itemize",
                           font_size=24, **tex_excludes).move_to(anchor.get_left(), LEFT)
            total_height = anchor.get_height() + 1/2 * con_item.get_height()
            con_item = con_item.shift(total_height * DOWN)
            self.play(FadeIn(con_item))
            current_list_of_cons.append(con_item)
            anchor = con_item
            self.next_slide()


class MercerKernelExplanation(Slide):
    TEXT_COLOR = "#00005F"
    default_frame_orientation = (0, 0)
    TEXT_LIST = [
        "Em 1909, \\textbf{James Mercer} publicou um artigo acerca de funções contínuas simétricas de ``tipo positivo ou negativo'', esse artigo e seu autor dão nome a esse conjunto específico de funções kernel.",
        "Um kernel de Mercer deve satisfazer a seguinte expressão:\n $$ \\mathbf{c}^T K \\mathbf{c} = \\sum_{i,j=1}^m c_i c_j \\mathcal{K} (\\mathbf{x}_i, \\mathbf{x}_j) \\geqslant 0 $$\npara qualquer conjunto de $m$ vetores $\\mathbf{x}_i \\in \\mathbb{R}^n$ e $\\mathbf{c}_i \\in \\mathbb{R}^m$, para qualquer $m \\in \\mathbb{Z}^+$",
        "Todo kernel de Mercer pode ser expresso a partir da aplicação de um \\textit{feature map}:\n$$ \\mathcal{K}(\\mathbf{x}, \\mathbf{y}) = \\sum_{i=1}^\\infty \\phi_i (\\mathbf{x}) \\phi_i (\\mathbf{y})\\quad \\forall \\mathbf{x},\\mathbf{y} \\in \\mathbb{R}^n $$"
    ]

    def construct(self):
        self.camera.background_rgba = list(color_to_rgba(WHITE, 1))
        additional_preamble = "\\usepackage{ragged2e}\n\\usepackage{stackengine}"
        additional_preamble_geometry = f"{additional_preamble}\n\\usepackage{{geometry}}\\geometry{{textwidth=170mm}}"
        tex_config = {
            "fill_color": self.TEXT_COLOR,
            "additional_preamble": additional_preamble,
            "font_size": 32,
        }
        tex_excludes = tex_config.copy()
        tex_excludes.pop("font_size")
        tex_excludes["additional_preamble"] = additional_preamble_geometry

        t = Title("Kernel de Mercer",
                  fill_color=self.TEXT_COLOR)
        self.play(FadeIn(t))
        start = Tex("Uma função kernel é chamada de \\textit{Kernel de Mercer} caso as matrizes kernel associadas a ela sejam semi-definida positivas para qualquer conjunto de vetores $\\{\\mathbf{x}_1, \\dots, \\mathbf{x}_m\\} \\in \\mathbb{R}^n$ e qualquer $ m \\geqslant 1$",
                    tex_environment="justify", **tex_config).move_to(2 * UP)
        self.play(FadeIn(start))
        self.next_slide()
        current_list_of_cons = []
        anchor = start
        for i in range(len(self.TEXT_LIST)):
            tex_string = f"\\item {self.TEXT_LIST[i]}"
            con_item = Tex(tex_string, tex_environment="itemize",
                           font_size=24, **tex_excludes).move_to(anchor.get_left(), LEFT)
            total_height = 2/3 * anchor.get_height() + 1/2 * con_item.get_height()
            con_item = con_item.shift(total_height * DOWN)
            self.play(FadeIn(con_item))
            current_list_of_cons.append(con_item)
            anchor = con_item
            self.next_slide()


class MercerKernelProperties(Slide):
    TEXT_COLOR = "#00005F"
    default_frame_orientation = (0, 0)
    TEXT_LIST = [
        "$\\alpha \\mathcal{K}, \\forall \\alpha > 0$",
        "$\\mathcal{K}_1 + \\mathcal{K}_2$",
        "$\\mathcal{K}_1 (\\mathbf{x}, \\mathbf{y}) \\mathcal{K}_2 (\\mathbf{x}, \\mathbf{y})$",
        "$\\mathcal{K} (\\mathbf{x}, \\mathbf{y})^d, \\forall d \\in \\mathbb{Z}^+$",
        "$\\exp(\\mathcal{K}(\\mathbf{x}, \\mathbf{y}))$",
        "$F(\\mathbf{x}) \\mathcal{K}(\\mathbf{x}, \\mathbf{y}) F(\\mathbf{y}), \\forall F: \\mathbb{R}^n \\rightarrow \\mathbb{R}$"
    ]

    def construct(self):
        self.camera.background_rgba = list(color_to_rgba(WHITE, 1))
        additional_preamble = "\\usepackage{ragged2e}\n\\usepackage{stackengine}"
        additional_preamble_geometry = f"{additional_preamble}\n\\usepackage{{geometry}}\\geometry{{textwidth=170mm}}"
        tex_config = {
            "fill_color": self.TEXT_COLOR,
            "additional_preamble": additional_preamble,
            "font_size": 32,
        }
        tex_excludes = tex_config.copy()
        tex_excludes.pop("font_size")
        tex_excludes["additional_preamble"] = additional_preamble_geometry

        t = Title("Kernel de Mercer",
                  fill_color=self.TEXT_COLOR)
        self.play(FadeIn(t))
        start = Tex("Sejam $\\mathcal{K}, \\mathcal{K}_1, \\mathcal{K}_2$ kernels de Mercer. Logo, as seguintes expressões também representam kernels de Mercer:",
                    tex_environment="justify", **tex_config).move_to(2 * UP)
        self.play(FadeIn(start))
        self.next_slide()
        current_list_of_cons = []
        anchor = start
        for i in range(len(self.TEXT_LIST)):
            tex_string = f"\\item {self.TEXT_LIST[i]}"
            con_item = Tex(tex_string, tex_environment="itemize",
                           font_size=24, **tex_excludes).move_to(anchor.get_left(), LEFT)
            total_height = 2/3 * anchor.get_height() + 1/2 * con_item.get_height()
            con_item = con_item.shift(total_height * DOWN)
            self.play(FadeIn(con_item))
            current_list_of_cons.append(con_item)
            anchor = con_item
            self.next_slide()


class KernelPCAOverview(Slide):
    TEXT_COLOR = "#00005F"
    default_frame_orientation = (0, 0)

    def construct(self):
        self.camera.background_rgba = list(color_to_rgba(WHITE, 1))

        additional_preamble = "\\usepackage{ragged2e}\n\\usepackage{stackengine}"
        additional_preamble_geometry = f"{additional_preamble}\n\\usepackage{{geometry}}\\geometry{{textwidth=170mm}}"

        tex_config = {
            "additional_preamble": additional_preamble,
            "font_size": 32,
            "fill_color": self.TEXT_COLOR,
        }
        tex_excludes = tex_config.copy()
        tex_excludes.pop("font_size")
        tex_excludes["additional_preamble"] = additional_preamble_geometry

        # Título
        title = Title("Kernel PCA", fill_color=self.TEXT_COLOR)
        self.play(FadeIn(title))

        # Ideia geral
        intro = Tex("""O Método da Análise das Componentes Principais (PCA) visa analisar as direções
                    de maior variância, a partir de autovetores da covariância. Quando observa-se uma estrutura
                    não-linear, é possível aplicar um \\textit{feature map} $\\phi$ a partir do uso de funções kernel, ou seja,
                    sem computar $\\phi$ explicitamente.""",
                    tex_environment="justify",
                    **tex_config
                    ).move_to(2 * UP)
        self.play(FadeIn(intro))
        self.next_slide()

        # Passos (bullets)
        steps = [
            r"Construa a matriz kernel $K \in \mathbb{R}^{m\times m}$, $K_{ij}=\mathcal{K}(\mathbf{x}_i,\mathbf{x}_j)$.",
            r"Centralize: $\tilde K = H K H,\quad H=I-\frac{1}{m}\mathbf{1}\mathbf{1}^T$.",
            r"Autodecomposição: $\tilde K\,\alpha_k = m\,\lambda_k\,\alpha_k$ com $\norm{\alpha_k}=1$.",
            r"Projeção de novo ponto $x$: $z_k(x)=\frac{1}{\sqrt{\lambda_k}}\sum_{i=1}^m \alpha_{ik}\,\mathcal{K}(\mathbf{x}_i,x)$.",
            r"Escolha do kernel (linear, polinomial, RBF) define a geometria no espaço $\phi$.",
        ]
        separators = {
            4: {
                "linear": RED,
                "polinomial": GREEN,
                "RBF": BLUE,
            }
        }
        kernels = {
            "linear": r"\mathcal{K} (\mathbf{x}, \mathbf{y}) = \mathbf{x}^T \mathbf{y}",
            "polinomial": r"\mathcal{K} (\mathbf{x}, \mathbf{y}) = (\mathbf{x}^T \mathbf{y} + \mathbf{r})^n",
            "RBF": r"\mathcal{K} (\mathbf{x}, \mathbf{y}) = \exp(-\frac{1}{2 \sigma^2} \norm{\mathbf{x} - \mathbf{y}}^2)",
        }

        anchor = intro
        for i, s in enumerate(steps):
            bullet = Tex(
                rf"\item {s}",
                tex_environment="itemize",
                font_size=24,
                tex_to_color_map=separators.get(i, {}),
                base_color=self.TEXT_COLOR,
                **tex_excludes
            ).move_to(anchor.get_left(), LEFT)

            # Espaçamento vertical e alinhamento à esquerda do parágrafo inicial
            total_h = (2/3) * anchor.get_height() + (2/3) * bullet.get_height()
            bullet = bullet.shift(total_h * DOWN)
            self.play(FadeIn(bullet))
            self.next_slide()
            if i == 4:
                for i, (k, v) in enumerate(kernels.items()):
                    rect = SurroundingRectangle(bullet.select_part(k), 0.1, separators[4][k])
                    arrow_destination = rect.get_bottom() + DOWN
                    mathtex = Tex(v, fill_color=separators[4][k], font_size=32).move_to(arrow_destination)
                    arrow = CurvedArrow(rect.get_bottom(), mathtex.get_top(), color=separators[4][k], tip_width=0.2, tip_length=0.2)
                    self.play(FadeIn(rect), FadeIn(arrow), FadeIn(mathtex))
                    self.next_slide()
                    self.play(FadeOut(rect, final_alpha_value=0.2), FadeOut(arrow, final_alpha_value=0.2), FadeOut(mathtex, final_alpha_value=0.2))
            anchor = bullet