"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

@arkanoid_method
def cargar_nivel(self) -> list[str]:
    """Lee el fichero de nivel y devuelve la cuadrícula como lista de filas."""
    # Compruebo que el fichero existe
    if not self.level_path.exists() or not self.level_path.is_file():
        raise FileNotFoundError("El fichero no es válido")

    # Leo el contenido y lo separo en lineas
    contenido = self.level_path.read_text(encoding="utf-8")
    lineas = contenido.splitlines()

    # Me quedo solo con las lineas que tienen algo
    lineas_filtradas = []
    for linea in lineas:
        if linea.strip() != "":
            lineas_filtradas.append(linea)

    # Si no hay ninguna linea, error
    if not lineas_filtradas:
        raise ValueError("Lista vacía")

    # Todas las lineas tienen que medir lo mismo
    ancho = len(lineas_filtradas[0])
    for linea in lineas_filtradas:
        if len(linea) != ancho:
            raise ValueError("Las líneas deben tener el mismo ancho")

    # Guardo y devuelvo
    self.layout = lineas_filtradas
    return self.layout


@arkanoid_method
def preparar_entidades(self) -> None:
    """Posiciona paleta y bola, y reinicia puntuación y vidas."""
    # Pongo la paleta abajo en el centro
    self.paddle.size = self.PADDLE_SIZE
    self.paddle.midbottom = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.PADDLE_OFFSET)

    # Reseteo marcadores
    self.score = 0
    self.lives = 3
    self.end_message = ""

    # Coloco la bola encima de la paleta, con un poco de diagonal para que no vaya recta
    self.reiniciar_bola((1, -1))


@arkanoid_method
def crear_bloques(self) -> None:
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    # Vacío las listas por si acaso
    self.blocks = []
    self.block_colors = []
    self.block_symbols = []

    # Recorro la cuadricula fila a fila
    for fila, contenido in enumerate(self.layout):
        for columna, simbolo in enumerate(contenido):
            # Solo creo bloque si el simbolo es uno de los validos
            if simbolo in self.BLOCK_COLORS:
                bloque = self.calcular_posicion_bloque(fila, columna)
                self.blocks.append(bloque)
                self.block_colors.append(self.BLOCK_COLORS[simbolo])
                self.block_symbols.append(simbolo)


@arkanoid_method
def procesar_input(self) -> None:
    """Gestiona la entrada de teclado para mover la paleta."""
    teclas = self.obtener_estado_teclas()

    # Muevo la paleta a izquierda o derecha
    if teclas[self.KEY_LEFT] or teclas[self.KEY_A]:
        self.paddle.x -= int(self.PADDLE_SPEED)
    if teclas[self.KEY_RIGHT] or teclas[self.KEY_D]:
        self.paddle.x += int(self.PADDLE_SPEED)

    # Que no se salga de la pantalla
    if self.paddle.left < 0:
        self.paddle.left = 0
    if self.paddle.right > self.SCREEN_WIDTH:
        self.paddle.right = self.SCREEN_WIDTH


@arkanoid_method
def actualizar_bola(self) -> None:
    """Actualiza la posición de la bola y resuelve colisiones."""
    # Muevo la bola
    self.ball_pos += self.ball_velocity
    ball_rect = self.obtener_rect_bola()

    # Rebote en la pared izquierda
    if ball_rect.left <= 0:
        self.ball_velocity.x = abs(self.ball_velocity.x)
    # Rebote en la pared derecha
    if ball_rect.right >= self.SCREEN_WIDTH:
        self.ball_velocity.x = -abs(self.ball_velocity.x)
    # Rebote en el techo
    if ball_rect.top <= 0:
        self.ball_velocity.y = abs(self.ball_velocity.y)

    # Rebote en la paleta
    if self.ball_velocity.y > 0 and ball_rect.colliderect(self.paddle):
        self.ball_pos.y = self.paddle.top - self.BALL_RADIUS - 1
        self.ball_velocity.y = -abs(self.ball_velocity.y)

    # Choque con bloques
    for i in range(len(self.blocks)):
        if ball_rect.colliderect(self.blocks[i]):
            self.score += self.BLOCK_POINTS[self.block_symbols[i]]
            del self.blocks[i]
            del self.block_colors[i]
            del self.block_symbols[i]
            self.ball_velocity.y *= -1
            break

    # Si no quedan bloques, gano
    if not self.blocks:
        self.running = False
        self.end_message = "¡Has ganado!"
        return

    # Si la bola se cae, pierdo vida
    if ball_rect.top > self.SCREEN_HEIGHT:
        self.lives -= 1
        if self.lives <= 0:
            self.running = False
            self.end_message = "Game Over"
        else:
            self.reiniciar_bola((1, -1))


@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""
    # Fondo
    self.screen.fill(self.BACKGROUND_COLOR)

    # Bloques
    for i in range(len(self.blocks)):
        self.dibujar_rectangulo(self.blocks[i], self.block_colors[i])

    # Paleta
    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)

    # Bola
    centro = (int(self.ball_pos.x), int(self.ball_pos.y))
    self.dibujar_circulo(centro, self.BALL_RADIUS, self.BALL_COLOR)

    # Textos
    self.dibujar_texto(f"Puntos: {self.score}", (10, 10))
    self.dibujar_texto(f"Vidas: {self.lives}", (10, 40))

    if self.end_message:
        self.dibujar_texto(self.end_message, (280, 280), grande=True)


@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""
    # Preparo todo
    self.inicializar_pygame()
    self.cargar_nivel()
    self.preparar_entidades()
    self.crear_bloques()

    self.running = True

    # Bucle principal
    while self.running:
        # Eventos (cerrar ventana o pulsar Escape)
        for evento in self.iterar_eventos():
            if evento.type == self.EVENT_QUIT:
                self.running = False
            elif evento.type == self.EVENT_KEYDOWN and evento.key == self.KEY_ESCAPE:
                self.running = False

        # Actualizo y dibujo
        self.procesar_input()
        self.actualizar_bola()
        self.dibujar_escena()
        self.actualizar_pantalla()

        # Limito los FPS
        if self.clock:
            self.clock.tick(self.FPS)

    # Al salir, pinto la pantalla final un momento
    self.dibujar_escena()
    self.actualizar_pantalla()
    self.esperar(2000)

    self.finalizar_pygame()


def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()


if __name__ == "__main__":
    main()
