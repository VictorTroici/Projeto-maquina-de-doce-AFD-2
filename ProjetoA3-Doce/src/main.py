import pygame
import sys
from automato import MaquinaDocesAFD
import textwrap

# Inicialização do Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Máquina de Doces - AFD")
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 36)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
GREEN = (0, 255, 0)  # Para mensagem de sucesso

# Carregar imagens das notas
nota_1_img = None
nota_2_img = None
nota_5_img = None
try:
    nota_1_img = pygame.image.load("C:\\Users\\Victor Troici\\OneDrive\\Documentos\\ProjetoA3-Doce\\assets\\imagens\\nota_1.png").convert_alpha()
    nota_2_img = pygame.image.load("C:\\Users\\Victor Troici\\OneDrive\\Documentos\\ProjetoA3-Doce\\assets\\imagens\\nota_2.png").convert_alpha()
    nota_5_img = pygame.image.load("C:\\Users\\Victor Troici\\OneDrive\\Documentos\\ProjetoA3-Doce\\assets\\imagens\\nota_5.png").convert_alpha()
except pygame.error:
    print("Aviso: Algumas imagens das notas não encontradas. Usando texto nos botões.")

# Carregar a imagem de fundo (máquina de doces)
background_img = None
try:
    background_img = pygame.image.load("C:\\Users\\Victor Troici\\OneDrive\\Documentos\\ProjetoA3-Doce\\assets\\imagens\\maquina_de_doce.png").convert_alpha()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Ajustar ao tamanho da tela
    background_img.set_alpha(100)  # Opacidade ajustada
except pygame.error:
    print("Aviso: Imagem de fundo 'maquina_de_doce.png' não encontrada. Usando fundo branco.")

# Carregar imagens dos doces
doce_imgs = {}
try:
    doce_imgs["A"] = pygame.image.load("C:\\Users\\Victor Troici\\OneDrive\\Documentos\\ProjetoA3-Doce\\assets\\imagens\\doce_a.png").convert_alpha()
    doce_imgs["B"] = pygame.image.load("C:\\Users\\Victor Troici\\OneDrive\\Documentos\\ProjetoA3-Doce\\assets\\imagens\\doce_b.png").convert_alpha()
    doce_imgs["C"] = pygame.image.load("C:\\Users\\Victor Troici\\OneDrive\\Documentos\\ProjetoA3-Doce\\assets\\imagens\\doce_c.png").convert_alpha()
    # Ajustar o tamanho das imagens dos doces (40x40 pixels para animação e botões)
    for key in doce_imgs:
        doce_imgs[key] = pygame.transform.scale(doce_imgs[key], (50, 50))
except pygame.error:
    print("Aviso: Algumas imagens dos doces não encontradas. Usando retângulo vermelho como fallback.")

# Instância do AFD
maquina = MaquinaDocesAFD()
mensagem = "Insira uma nota/moeda: R$1, R$2 ou R$5"
button_hovered = None

# Botões para inserir dinheiro
button_width, button_height = 180, 120
spacing = 20  # Espaçamento entre os botões
total_buttons_width = 4 * button_width + 3 * spacing  # 4 botões com 3 espaçamentos
start_x = (WIDTH - total_buttons_width) // 2  # Centralizar os botões
buttons = [
    (nota_1_img if nota_1_img else "R$1", start_x, 600, button_width, button_height),
    (nota_2_img if nota_2_img else "R$2", start_x + button_width + spacing, 600, button_width, button_height),
    (nota_5_img if nota_5_img else "R$5", start_x + 2 * (button_width + spacing), 600, button_width, button_height),
    (None, start_x + 3 * (button_width + spacing), 600, button_width, button_height)  # Resetar
]

# Botões para escolher doces (com imagens)
doce_button_width, doce_button_height = 120, 80  # Mantive a altura para caber a imagem e o texto
doce_spacing = 10  # Espaçamento entre os botões de doces
total_doce_buttons_width = 3 * doce_button_width + 2 * doce_spacing  # 3 botões com 2 espaçamentos
doce_start_x = (WIDTH - total_doce_buttons_width) // 2  # Centralizar os botões de doces
doce_buttons = [
    ("Doce A", "A", doce_start_x, 500, doce_button_width, doce_button_height),  # (label, id_doce, x, y, w, h)
    ("Doce B", "B", doce_start_x + doce_button_width + doce_spacing, 500, doce_button_width, doce_button_height),
    ("Doce C", "C", doce_start_x + 2 * (doce_button_width + doce_spacing), 500, doce_button_width, doce_button_height)
]

# Tabela de preços
tabela_precos = [
    "Doce A: R$6,00",
    "Doce B: R$7,00",
    "Doce C: R$8,00"
]

# Variáveis para animação
doce_liberado = False
doce_anim_pos_y = 0
doce_anim_speed = 5
mensagem_compra = ""
mensagem_compra_timer = 0
doce_atual = None  # Armazena o ID do doce atual para a animação

def desenhar_tela():
    global mensagem_compra, mensagem_compra_timer, doce_liberado, doce_anim_pos_y, doce_atual
    screen.fill(WHITE)  # Preenche com branco como base
    
    # Desenhar a imagem de fundo (se carregada)
    if background_img:
        screen.blit(background_img, (0, 0))
    
    # Título
    title = font.render("Máquina de Doces - AFD", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))
    
    # Saldo
    saldo_texto = font.render(f"Saldo: R${maquina.saldo:.2f}", True, BLACK)
    screen.blit(saldo_texto, (WIDTH//2 - saldo_texto.get_width()//2, 100))
    
    # Mensagem
    mensagem_texto = small_font.render(mensagem, True, BLACK)
    screen.blit(mensagem_texto, (WIDTH//2 - mensagem_texto.get_width()//2, 160))
    
    # Tabela de preços
    y_offset = 220
    for preco in tabela_precos:
        preco_texto = small_font.render(preco, True, BLACK)
        screen.blit(preco_texto, (WIDTH//2 - preco_texto.get_width()//2, y_offset))
        y_offset += 40
    
    # Opções de doces
    opcoes = maquina.get_opcoes()
    wrapped_text = textwrap.wrap(opcoes, width=60)
    for line in wrapped_text:
        opcoes_texto = small_font.render(line, True, BLUE)
        screen.blit(opcoes_texto, (WIDTH//2 - opcoes_texto.get_width()//2, y_offset))
        y_offset += 40
    
    # Tabela de compras (ao lado direito)
    compras = maquina.get_compras()
    y_offset_compras = 100
    compras_title = small_font.render("Doces Comprados:", True, BLACK)
    screen.blit(compras_title, (WIDTH - 300, y_offset_compras))
    y_offset_compras += 40
    for item in compras:
        item_texto = small_font.render(item, True, BLACK)
        screen.blit(item_texto, (WIDTH - 300, y_offset_compras))
        y_offset_compras += 30
    
    # Mensagem de compra
    if mensagem_compra_timer > 0:
        compra_texto = small_font.render(mensagem_compra, True, GREEN)
        screen.blit(compra_texto, (WIDTH//2 - compra_texto.get_width()//2, HEIGHT - 100))
        mensagem_compra_timer -= 1
        if mensagem_compra_timer <= 0:
            mensagem_compra = ""
    
    # Animação do doce sendo liberado
    if doce_liberado:
        if doce_atual in doce_imgs:
            # Desenhar a imagem do doce correspondente
            doce_img = doce_imgs[doce_atual]
            screen.blit(doce_img, (WIDTH//2 - doce_img.get_width()//2, doce_anim_pos_y))
        else:
            # Fallback: retângulo vermelho se a imagem não estiver disponível
            pygame.draw.rect(screen, (255, 0, 0), (WIDTH//2 - 20, doce_anim_pos_y, 40, 20))
        doce_anim_pos_y += doce_anim_speed
        if doce_anim_pos_y > HEIGHT:
            doce_liberado = False
            doce_anim_pos_y = HEIGHT//2
            doce_atual = None
    
    # Desenhar botões de dinheiro
    mouse_pos = pygame.mouse.get_pos()
    global button_hovered
    
    for text_or_img, x, y, w, h in buttons:
        scale_factor = 1.1 if (x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h) else 1.0
        button_hovered = (x, y, w, h) if scale_factor == 1.1 else None
        
        if isinstance(text_or_img, pygame.Surface):
            scaled_img = pygame.transform.scale(text_or_img, (int(w * scale_factor), int(h * scale_factor)))
            screen.blit(scaled_img, (x - (w * (scale_factor - 1) / 2) if scale_factor > 1 else x, 
                                     y - (h * (scale_factor - 1) / 2) if scale_factor > 1 else y))
        else:
            # Botão "Resetar" sem retângulo cinza
            button_text = font.render("Resetar" if text_or_img is None else text_or_img, True, BLACK)
            text_rect = button_text.get_rect(center=(x + w/2, y + h/2))
            screen.blit(button_text, text_rect)

    # Desenhar botões de doces (sem retângulo cinza)
    for label, doce_id, x, y, w, h in doce_buttons:
        # Desenhar a imagem do doce (centralizada na parte superior do botão)
        if doce_id in doce_imgs:
            doce_img = doce_imgs[doce_id]
            img_x = x + (w - doce_img.get_width()) // 2  # Centralizar horizontalmente
            img_y = y + 5  # Posicionar a imagem 5 pixels abaixo do topo do botão
            screen.blit(doce_img, (img_x, img_y))
        
        # Desenhar o texto do botão (abaixo da imagem)
        label_text = small_font.render(label, True, BLACK)
        text_rect = label_text.get_rect(center=(x + w/2, y + h - 20))  # Posicionar o texto na parte inferior do botão
        screen.blit(label_text, text_rect)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Botões de inserir dinheiro
            if start_x <= x <= start_x + button_width and 600 <= y <= 720:
                maquina.inserir_dinheiro(1)
                mensagem = f"Nota de R$1 inserida. Saldo: R${maquina.saldo:.2f}"
            elif start_x + button_width + spacing <= x <= start_x + 2 * button_width + spacing and 600 <= y <= 720:
                maquina.inserir_dinheiro(2)
                mensagem = f"Nota de R$2 inserida. Saldo: R${maquina.saldo:.2f}"
            elif start_x + 2 * (button_width + spacing) <= x <= start_x + 3 * button_width + 2 * spacing and 600 <= y <= 720:
                maquina.inserir_dinheiro(5)
                mensagem = f"Nota de R$5 inserida. Saldo: R${maquina.saldo:.2f}"
            elif start_x + 3 * (button_width + spacing) <= x <= start_x + 4 * button_width + 3 * spacing and 600 <= y <= 720:
                maquina.resetar()
                mensagem = "Máquina resetada. Saldo: R$0.00"
                doce_liberado = False
                mensagem_compra = ""
                doce_atual = None
            
            # Botões de doces
            for label, doce_id, bx, by, bw, bh in doce_buttons:
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    sucesso, msg, troco = maquina.comprar_doce(doce_id)
                    mensagem = msg
                    if sucesso:
                        mensagem_compra = msg
                        mensagem_compra_timer = 120  # 2 segundos a 60 FPS
                        doce_liberado = True
                        doce_anim_pos_y = HEIGHT//2
                        doce_atual = doce_id  # Armazena o ID do doce para a animação

    desenhar_tela()
    pygame.display.flip()

pygame.quit()
sys.exit()