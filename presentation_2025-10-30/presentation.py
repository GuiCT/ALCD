from manim import *
from manim_slides.slide import Slide
from manim.opengl import *

class Presentation(Slide):
    # ------------------------
    PRESENTATION_TITLE = "Métodos Kernel, Kernel PCA"
    COURSE = "Álgebra Linear para Ciência de Dados"
    AUTHORS = "Guilherme Tomiasi"
    DATE = "30/10/2025"
    BACKGROUND_COLOR = WHITE
    TEXT_COLOR = BLUE
    # ------------------------

    def construct(self):
        # Background
        frame_bg = FullScreenRectangle(
            fill_color=self.BACKGROUND_COLOR, fill_opacity=1)
        self.add(frame_bg)

        # Title and course
        title = Text(self.PRESENTATION_TITLE,
                     font_size=48, weight=BOLD, color=self.TEXT_COLOR)
        course = Text(self.COURSE, font_size=32, color=self.TEXT_COLOR, should_center=True)

        title_group = VGroup(title, course).arrange(
            DOWN, aligned_edge=ORIGIN, buff=0.6)
        title_group.to_edge(UP, buff=1.6)
        title_group.shift(LEFT * 0.3)

        # Authors, institute and date at lower part
        authors = Text(self.AUTHORS, font_size=24, color=self.TEXT_COLOR)
        date = Text(self.DATE, font_size=18, color=self.TEXT_COLOR)

        bottom_group = VGroup(authors, date).arrange(DOWN, buff=0.2)
        bottom_group.to_edge(DOWN, buff=0.8)

        # Compose master group (for clean animations)
        master = VGroup(title_group, bottom_group)

        # Entrance animation
        self.play(LaggedStart(FadeIn(title, course), lag_ratio=0.25))
        self.play(FadeIn(bottom_group, shift=DOWN))

        # Pause here as the title slide
        self.next_slide()

        # Small flourish when moving on
        self.play(FadeOut(master, shift=UP), run_time=0.6)


class FeatureMap(ThreeDScene, Slide):
    TEXT_COLOR = DARK_BLUE
    BACKGROUND_COLOR = WHITE
    RECTANGLE_COLOR = RED_C      

    def construct(self):  
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble("\\usepackage{ragged2e}\n\\usepackage{lmodern}")  
        self.tex_params = {
            "color": self.TEXT_COLOR,
            "font_size": 24,
            "tex_template": myTemplate,
            "tex_environment": "justify",
        }

        # Background
        frame_bg = FullScreenRectangle(
            fill_color=self.BACKGROUND_COLOR, fill_opacity=1)
        self.add(frame_bg)

        t = Title("Feature Map", color=self.TEXT_COLOR)
        t.underline.color = self.TEXT_COLOR
        self.play(FadeIn(t))
        par = Tex("Uma maneira de transformar dados não-lineares para cumprir propriedades necessárias para a aplicação de métodos lineares.", **self.tex_params).move_to(2 * UP)
        self.play(FadeIn(par))
        self.next_slide()
        ex_pre = Tex("Dado um conjunto de dados $\\mathbf{x_1}, \\dots, \\mathbf{x_m} \\in \\mathbb{R}^n$. Se aplicarmos uma transformação:", **self.tex_params).move_to(par.get_center()).shift(DOWN)
        self.play(FadeIn(ex_pre))
        self.next_slide()
        p = MathTex(r"\phi: \mathbb{R}^n \rightarrow \mathbb{R}^d", color=self.TEXT_COLOR, font_size=48, tex_template=myTemplate).move_to(ex_pre.get_center()).shift(DOWN)
        self.play(FadeIn(p))
        self.next_slide()
        ex_post = Tex("Obtemos os vetores de observações $\\mathbf{z_i} = \\phi(\\mathbf{x_i})$. Um exemplo de aplicação a transformação de um conjunto para aplicar métodos de regressão polinomial (quadrática, cúbica) sobre a fundação de regressão linear. Outro caso comum é a transformação de um conjunto não linearmente separável em linearmente separável.", **self.tex_params).move_to(p.get_center()).shift(1.5 * DOWN)
        self.play(FadeIn(ex_post))
        self.next_slide()
        self.clear()
        # self.show_concentric_data()
    
    def show_concentric_data(self):
        t = Title("Exemplo")

        inner_points_3d = self.get_circle_points_3d(radius=1, z_value=0, num_points=30, color=BLUE)
        outer_points_3d = self.get_circle_points_3d(radius=2, z_value=2, num_points=30, color=RED)

        # Display circles and points
        self.add(t)
        self.play(*[Create(point) for point in inner_points_3d])
        self.play(*[Create(point) for point in outer_points_3d])

        self.next_slide()
        
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        self.play(Create(axes))
        
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES, run_time=3)
        
        explanation_3d = Tex("Transformação para 3D via Feature Map $\\phi(x, y) = (x, y, x^2 + y^2)$", 
                            color=self.TEXT_COLOR, font_size=24).to_corner(DL)
        self.add_fixed_in_frame_mobjects(explanation_3d)
        self.play(FadeIn(explanation_3d))
        
        self.next_slide()
        
        # Add separating plane
        plane = Surface(
            lambda u, v: axes.c2p(u, v, 1),
            u_range=[-3, 3],
            v_range=[-3, 3],
            fill_opacity=0.3,
            fill_color=GREEN,
            checkerboard_colors=[GREEN_D, GREEN_E]
        )
        
        plane_label = Tex("Plano separador", color=GREEN, font_size=28)
        plane_label.to_corner(UR)
        self.add_fixed_in_frame_mobjects(plane_label)
        
        self.play(Create(plane), FadeIn(plane_label))
        
        self.next_slide()
        
        self.begin_ambient_camera_rotation(rate=1/3)
        self.wait(10)
        self.next_slide()
   
    def get_circle_points_3d(self, radius=1, z_value=0, num_points=30, color=WHITE):
        points = []
        for angle in np.linspace(0, 2 * np.pi, num_points):
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            # Apply feature map: z = x^2 + y^2 (or just use fixed z_value)
            z = z_value
            point = Dot3D(point=[x, y, z], color=color, radius=0.08)
            points.append(point)
        return points