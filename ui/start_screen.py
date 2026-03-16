import pygame


def pantalla_inicio(pantalla, fuentes, ancho, alto):

    clock = pygame.time.Clock()

    # cargar imagen
    fondo = pygame.image.load("assets/ui/start_screen.png").convert()
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    subtitulo = fuentes["sm"].render("Presiona ENTER para comenzar", True, ( 72,  35,  10))

    # botón imagen
    boton_img = pygame.image.load("assets/ui/boton_start.png").convert_alpha()
    boton_img = pygame.transform.scale(boton_img, (210, 180))
    boton_rect = boton_img.get_rect(center=(ancho//2, alto//2+200))

    while True:

        pantalla.blit(fondo, (0, 0))
        # dibujar botón
        pantalla.blit(boton_img, boton_rect)

        pantalla.blit(subtitulo, (ancho//2 - subtitulo.get_width()//2, alto//2 + 350))
         
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ENTER
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

            # click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    return
        

        clock.tick(60)