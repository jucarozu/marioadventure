"""Módulo principal del juego Mario Adventure."""

import pygame as pg

from settings import *
from entities import Player, Enemy

class MarioAdventure:
    """Representa el bucle principal y la lógica del juego Mario Adventure."""

    def __init__(self):
        """Inicializa el juego, configura la pantalla, el reloj y los grupos de sprites."""

        pg.init()
        pg.display.set_caption(CAPTION)

        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

    def run(self):
        """Bucle principal del juego que maneja los eventos, actualiza el estado del juego y renderiza el juego."""

        player = Player()
        self.all_sprites.add(player)

        for i in range(8):
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        score = 0

        running = True
        menu = True

        while running:
            if menu:
                option = self.show_menu()
                if option == "start":
                    menu = False
                    self.all_sprites.empty()
                    self.enemies.empty()
                    self.bullets.empty()
                    
                    player = Player()
                    self.all_sprites.add(player)
                    
                    for i in range(8):
                        enemy = Enemy()
                        self.all_sprites.add(enemy)
                        self.enemies.add(enemy)

                    score = 0
                elif option == "instructions":
                    self.show_instructions()
                elif option == "credits":
                    self.show_credits()
            else:
                self.clock.tick(FPS)

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            bullet = player.shoot()
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)

                keys = pg.key.get_pressed()
                if keys[pg.K_LEFT]:
                    player.speed_x = -5
                elif keys[pg.K_RIGHT]:
                    player.speed_x = 5
                else:
                    player.speed_x = 0

                self.all_sprites.update()

                hits = pg.sprite.groupcollide(self.enemies, self.bullets, True, True)
                for hit in hits:
                    score += 10
                    enemy = Enemy()
                    self.all_sprites.add(enemy)
                    self.enemies.add(enemy)

                hits = pg.sprite.spritecollide(player, self.enemies, False)
                if hits:
                    self.show_game_over(score)
                    menu = True

                self.display.fill(BLACK)
                self.all_sprites.draw(self.display)
                self.draw_text(self.display, f"Puntaje: {score}", 18, WIDTH // 2, 10)
                pg.display.flip()

        pg.quit()

    def draw_text(self, surface, text, size, x, y, color = WHITE):
        """Dibuja texto en la superficie dada en la posición especificada.

        Args:
            surface (Surface): [Superficie donde se dibujará el texto]
            text (str): [Texto a dibujar]
            size (int): [Tamaño de la fuente]
            x (int): [Posición x del texto]
            y (int): [Posición y del texto]
            color (tuple, optional): [Color del texto]. Defaults to WHITE.
        
        """

        font = pg.font.SysFont(FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def show_menu(self):
        """Muestra el menú principal y maneja la navegación del menú."""

        menu = True
        selected = "start"

        while menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected = "start" if selected == "exit" else "credits" if selected == "instructions" else "start"
                    if event.key == pg.K_DOWN:
                        selected = "instructions" if selected == "start" else "credits" if selected == "instructions" else "exit"
                    if event.key == pg.K_RETURN:
                        if selected == "start":
                            return "start"
                        elif selected == "instructions":
                            return "instructions"
                        elif selected == "credits":
                            return "credits"
                        elif selected == "exit":
                            pg.quit()
                            quit()

            self.display.fill(BLACK)
            self.draw_text(self.display, CAPTION, 64, WIDTH // 2, HEIGHT // 4)

            self.draw_text(self.display, "Jugar", 36, WIDTH // 2, HEIGHT // 2, GREEN if selected == "start" else WHITE)
            self.draw_text(self.display, "Instrucciones", 36, WIDTH // 2, HEIGHT // 2 + 50, GREEN if selected == "instructions" else WHITE)
            self.draw_text(self.display, "Créditos", 36, WIDTH // 2, HEIGHT // 2 + 100, GREEN if selected == "credits" else WHITE)
            self.draw_text(self.display, "Salir", 36, WIDTH // 2, HEIGHT // 2 + 150, GREEN if selected == "exit" else WHITE)

            pg.display.flip()

    def show_instructions(self):
        """Muestra la pantalla de instrucciones y espera a que el usuario regrese al menú."""

        self.display.fill(BLACK)
        self.draw_text(self.display, "Instrucciones", 64, WIDTH // 2, HEIGHT // 4)
        self.draw_text(self.display, "Movimiento: Flecha izquierda y derecha", 22, WIDTH // 2, HEIGHT // 2)
        self.draw_text(self.display, "Disparar: Barra espaciadora", 22, WIDTH // 2, HEIGHT // 2 + 40)
        self.draw_text(self.display, "Presiona ESPACIO para volver al menú", 18, WIDTH // 2, HEIGHT * 3/4)
        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False

    def show_credits(self):
        """Muestra la pantalla de créditos y espera a que el usuario regrese al menú."""

        self.display.fill(BLACK)
        self.draw_text(self.display, "Créditos", 64, WIDTH // 2, HEIGHT // 4)
        self.draw_text(self.display, f"Desarrollado por: {AUTHOR}", 22, WIDTH // 2, HEIGHT // 2)
        self.draw_text(self.display, "Presiona ESPACIO para volver al menú", 18, WIDTH // 2, HEIGHT * 3/4)
        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False

    def show_game_over(self, score):
        """Muestra la pantalla de fin del juego con la puntuación final y espera a que el usuario regrese al menú.
        
        Args:
            score (int): [Puntuación final del jugador]
        
        """

        self.display.fill(BLACK)
        self.draw_text(self.display, "Game Over", 64, WIDTH // 2, HEIGHT // 4)
        self.draw_text(self.display, f"Puntaje final: {score}", 36, WIDTH // 2, HEIGHT // 2)
        self.draw_text(self.display, "Presiona ESPACIO para volver al menú", 18, WIDTH // 2, HEIGHT * 3/4)
        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False

if __name__ == '__main__':
    marioadventure = MarioAdventure()
    marioadventure.run()