"""
Gera as figuras do manual do HoloLens 2, em `figuras/`.

    python preparar_manual.py

Aqui nao ha CAD nenhum para rasterizar, ao contrario dos manuais dos
robos: as cinco figuras sao esquematicas e desenhadas em matplotlib. Elas
existem para dizer ONDE as coisas ficam e em QUE ORDEM acontecem, que e o
que falta num tutorial escrito so em texto corrido.

O desenho do aparelho e deliberadamente simplificado. Desenhar o HoloLens
com fidelidade daria uma figura bonita e inutil: quem precisa da figura
esta procurando o botao de volume, nao admirando o produto. Quem quer ver
o aparelho tem a foto da capa, que e outra coisa e esta em outro lugar.

ATENCAO: `figuras/foto-aparelho.png`, a da capa, e uma fotografia e nao
sai daqui. Rodar este script nao a recria e tambem nao a apaga, mas
apagar a pasta `figuras/` inteira perde o arquivo.

Dependencias: matplotlib.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, Polygon

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "figuras")

CINZA = "0.86"
ESCURO = "0.35"


def folha(largura_cm, altura_cm):
    fig = plt.figure(figsize=(largura_cm / 2.54, altura_cm / 2.54), dpi=300)
    eixo = fig.add_axes([0, 0, 1, 1])
    eixo.set_axis_off()
    return fig, eixo


def gravar(fig, nome):
    os.makedirs(SAIDA, exist_ok=True)
    caminho = os.path.join(SAIDA, nome)
    fig.savefig(caminho, dpi=300, facecolor="white")
    plt.close(fig)
    print("   ", os.path.relpath(caminho, AQUI))


def _chamada(eixo, xy_peca, xy_texto, texto, tamanho=7.5, ha=None):
    """Linha de chamada com bolinha na peca."""
    eixo.annotate(
        texto, xy=xy_peca, xytext=xy_texto, fontsize=tamanho,
        family="DejaVu Sans", color="black", va="center",
        ha=ha or ("left" if xy_texto[0] > xy_peca[0] else "right"),
        arrowprops=dict(arrowstyle="-", color="black", linewidth=0.6,
                        shrinkA=0, shrinkB=2),
    )
    eixo.plot([xy_peca[0]], [xy_peca[1]], marker="o", markersize=2.2,
              color="black", zorder=5)


def caixa(eixo, x, y, w, h, titulo, linhas, fundo="white", grossa=False):
    """Caixa de fluxograma, com barra de titulo preta."""
    eixo.add_patch(Rectangle((x, y), w, h, facecolor=fundo, edgecolor="black",
                             linewidth=1.4 if grossa else 0.9, zorder=2))
    eixo.add_patch(Rectangle((x, y + h - 5.2), w, 5.2, facecolor="black",
                             edgecolor="black", linewidth=0.9, zorder=3))
    eixo.text(x + w / 2, y + h - 2.6, titulo, fontsize=6.6, color="white",
              weight="bold", ha="center", va="center", family="DejaVu Sans",
              zorder=4)
    for i, linha in enumerate(linhas):
        eixo.text(x + w / 2, y + h - 9.0 - i * 4.0, linha, fontsize=5.6,
                  ha="center", va="center", color="0.12",
                  family="DejaVu Sans", zorder=4)


def seta(eixo, p, q, texto=None, tamanho=5.8, desvio=0.0):
    eixo.annotate("", xy=q, xytext=p,
                  arrowprops=dict(arrowstyle="-|>", color="black",
                                  linewidth=0.9, mutation_scale=9,
                                  shrinkA=1, shrinkB=1), zorder=1)
    if texto:
        eixo.text((p[0] + q[0]) / 2 + desvio, (p[1] + q[1]) / 2 + 2.2, texto,
                  fontsize=tamanho, ha="center", va="bottom", style="italic",
                  color="0.25", family="DejaVu Sans", zorder=4)


# ============================================================
# AS FIGURAS
# ============================================================

def fig_fluxo():
    """
    O caminho inteiro, do projeto ao aparelho.

    E a figura que o tutorial original nao tinha e da qual mais se sente
    falta: o texto descreve seis etapas em sequencia, e quem esta no meio
    perde a nocao de quanto falta e de onde a coisa pode dar errado.
    """
    fig, eixo = folha(16.0, 8.6)
    eixo.set_xlim(0, 160)
    eixo.set_ylim(0, 86)
    eixo.set_aspect("equal")
    eixo.set_axis_off()

    eixo.text(2, 83, "DO PROJETO AO APARELHO", fontsize=9, weight="bold",
              family="DejaVu Sans", va="top")

    caixa(eixo, 3, 46, 32, 26, "1.  UNITY",
          ["projeto 3D", "MRTK na cena", "plataforma UWP"])
    caixa(eixo, 43, 46, 32, 26, "2.  BUILD",
          ["gera uma PASTA", "com um .sln", "dentro"])
    caixa(eixo, 83, 46, 32, 26, "3.  VISUAL STUDIO",
          ["abrir o .sln", "Release + ARM64", "Criar pacote"])
    caixa(eixo, 123, 46, 34, 26, "4.  PACOTE",
          [".appx ou .msix", "+ a pasta de", "dependências"])

    seta(eixo, (35, 59), (43, 59))
    seta(eixo, (75, 59), (83, 59))
    seta(eixo, (115, 59), (123, 59))

    # Bifurcacao das duas rotas de instalacao.
    eixo.annotate("", xy=(140, 40), xytext=(140, 46),
                  arrowprops=dict(arrowstyle="-", color="black",
                                  linewidth=0.9))
    eixo.plot([48, 140], [40, 40], color="black", linewidth=0.9, zorder=1)
    eixo.plot([48, 48], [40, 34], color="black", linewidth=0.9, zorder=1)
    eixo.plot([140, 140], [40, 34], color="black", linewidth=0.9, zorder=1)
    eixo.text(94, 41.5, "duas rotas, e as duas terminam no mesmo lugar",
              fontsize=6, ha="center", va="bottom", style="italic",
              color="0.25", family="DejaVu Sans")

    caixa(eixo, 24, 8, 48, 26, "5a.  DEVICE PORTAL",
          ["navegador no IP do aparelho", "Views → Apps → Install",
           "marcar 'optional packages'"])
    caixa(eixo, 116, 8, 48, 26, "5b.  CABO USB",
          ["parear o aparelho no VS", "alvo Device, depois Run",
           "implanta e roda direto"], fundo="0.96")

    seta(eixo, (48, 34), (48, 34.1))
    seta(eixo, (140, 34), (140, 34.1))

    eixo.add_patch(FancyBboxPatch((80, 12), 30, 16,
                                  boxstyle="round,pad=0,rounding_size=3",
                                  facecolor="0.92", edgecolor="black",
                                  linewidth=1.4, zorder=2))
    eixo.text(95, 22, "HoloLens 2", fontsize=7.5, weight="bold", ha="center",
              va="center", family="DejaVu Sans", zorder=4)
    eixo.text(95, 16.5, "o app aparece na", fontsize=5.4, ha="center",
              va="center", color="0.3", zorder=4)
    eixo.text(95, 13.6, "lista de aplicativos", fontsize=5.4, ha="center",
              va="center", color="0.3", zorder=4)

    seta(eixo, (72, 20), (80, 20))
    seta(eixo, (116, 20), (110, 20))

    eixo.text(158, 2.5, "o emulador entra na mesma rota 5a, trocando ARM64 "
              "por x64", fontsize=5.8, ha="right", va="bottom", color="0.3",
              style="italic", family="DejaVu Sans")
    gravar(fig, "fig-01-fluxo.png")


def fig_dispositivo():
    """O aparelho de lado, com os botoes que importam."""
    fig, eixo = folha(14.0, 8.4)
    eixo.set_xlim(0, 140)
    eixo.set_ylim(0, 84)
    eixo.set_aspect("equal")
    eixo.set_axis_off()

    eixo.text(2, 81, "HOLOLENS 2  ·  VISTA DO LADO DIREITO", fontsize=8.5,
              weight="bold", family="DejaVu Sans", va="top")
    eixo.text(2, 74.5, "esquemático: as posições são aproximadas,\n"
              "confira no aparelho antes de apertar",
              fontsize=6, va="top", color="0.4", linespacing=1.4,
              style="italic")

    # Aro da cabeca, visto de lado: um anel achatado.
    eixo.add_patch(FancyBboxPatch((40, 26), 62, 34,
                                  boxstyle="round,pad=0,rounding_size=16",
                                  facecolor="white", edgecolor="black",
                                  linewidth=1.3))
    eixo.add_patch(FancyBboxPatch((49, 33), 44, 20,
                                  boxstyle="round,pad=0,rounding_size=9",
                                  facecolor="white", edgecolor="0.55",
                                  linewidth=0.7))

    # Visor, na frente.
    eixo.add_patch(Polygon([(40, 44), (24, 36), (22, 25), (32, 23),
                            (44, 30), (44, 42)],
                           closed=True, facecolor=ESCURO, edgecolor="black",
                           linewidth=1.1))
    _chamada(eixo, (30, 30), (12, 16), "visor", tamanho=7, ha="center")

    # Botoes de volume, no lado direito perto da tempora.
    for i, (y, sinal) in enumerate(((49, "+"), (42, "−"))):
        eixo.add_patch(FancyBboxPatch((60 + i * 0, y), 9, 4.6,
                                      boxstyle="round,pad=0,rounding_size=1.6",
                                      facecolor=CINZA, edgecolor="black",
                                      linewidth=0.9))
        eixo.text(64.5, y + 2.3, sinal, fontsize=6.5, ha="center",
                  va="center", weight="bold")
    _chamada(eixo, (69.5, 45.5), (90, 71),
             "1  volume + e −\n     os dois juntos = foto\n"
             "     segurando 3 s = vídeo", tamanho=7, ha="left")

    # Energia e USB-C, na traseira.
    eixo.add_patch(Circle((95, 51), 3.0, facecolor=CINZA, edgecolor="black",
                          linewidth=0.9))
    eixo.plot([95, 95], [49.6, 52.4], color="black", linewidth=1.0)
    eixo.add_patch(Circle((95, 50.9), 1.6, facecolor="none",
                          edgecolor="black", linewidth=0.8))
    _chamada(eixo, (97.5, 52), (118, 60), "2  energia", tamanho=7, ha="left")

    eixo.add_patch(FancyBboxPatch((92, 30), 10, 4,
                                  boxstyle="round,pad=0,rounding_size=1.6",
                                  facecolor="white", edgecolor="black",
                                  linewidth=0.9))
    _chamada(eixo, (97, 30), (112, 16),
             "3  USB-C\ncarga e dados", tamanho=7, ha="center")

    # Brilho, do outro lado (indicado, nao desenhado).
    eixo.text(50, 15, "os botões de brilho ficam do lado esquerdo,\n"
              "que não aparece nesta vista",
              fontsize=6.2, ha="center", va="top", color="0.35",
              style="italic", linespacing=1.4)
    gravar(fig, "fig-02-dispositivo.png")


def fig_build():
    """A janela de Build Settings do Unity, com os valores que importam."""
    fig, eixo = folha(13.0, 8.8)
    eixo.set_xlim(0, 130)
    eixo.set_ylim(0, 88)
    eixo.set_aspect("equal")
    eixo.set_axis_off()

    eixo.text(2, 85, "UNITY  ·  BUILD SETTINGS", fontsize=8.5, weight="bold",
              family="DejaVu Sans", va="top")

    eixo.add_patch(Rectangle((4, 6), 122, 72, facecolor="white",
                             edgecolor="black", linewidth=1.1))
    eixo.add_patch(Rectangle((4, 70), 122, 8, facecolor="0.85",
                             edgecolor="black", linewidth=1.1))
    eixo.text(8, 74, "Build Settings", fontsize=6.6, va="center",
              weight="bold", family="DejaVu Sans")

    # Lista de plataformas, a esquerda.
    eixo.add_patch(Rectangle((8, 12), 34, 54, facecolor="0.97",
                             edgecolor="black", linewidth=0.7))
    plataformas = ["Windows, Mac, Linux", "Universal Windows Platform",
                   "Android", "iOS", "WebGL"]
    for i, nome in enumerate(plataformas):
        y = 60 - i * 7
        ativa = i == 1
        if ativa:
            eixo.add_patch(Rectangle((8.5, y - 2.6), 33, 5.6,
                                     facecolor="black", edgecolor="none"))
        eixo.text(10.5, y, nome, fontsize=4.9, va="center",
                  color="white" if ativa else "0.15",
                  weight="bold" if ativa else "normal",
                  family="DejaVu Sans")
    eixo.text(25, 8.5, "escolha a plataforma e aperte Switch Platform",
              fontsize=5.2, ha="center", va="center", color="0.35",
              style="italic")

    # Campos, a direita.
    campos = [
        ("Target Device", "HoloLens"),
        ("Architecture", "ARM 64-bit"),
        ("Build Type", "D3D Project"),
        ("Target SDK Version", "Latest installed"),
        ("Minimum Platform Version", "10.0.10240.0"),
        ("Visual Studio Version", "Latest installed"),
        ("Build and Run on", "Local Machine"),
        ("Build configuration", "Release"),
    ]
    for i, (rotulo, valor) in enumerate(campos):
        y = 62 - i * 6.4
        eixo.text(48, y, rotulo, fontsize=5.4, va="center", color="0.15",
                  family="DejaVu Sans")
        eixo.add_patch(Rectangle((92, y - 2.4), 30, 4.8, facecolor="0.95",
                                 edgecolor="0.5", linewidth=0.6))
        eixo.text(107, y, valor, fontsize=5.2, va="center", ha="center",
                  family="DejaVu Sans",
                  weight="bold" if rotulo in ("Architecture",
                                              "Build configuration") else "normal")

    eixo.annotate("", xy=(91, 55.6), xytext=(84, 47),
                  arrowprops=dict(arrowstyle="-|>", color="black",
                                  linewidth=0.8, mutation_scale=8))
    eixo.text(83, 45, "x64 para o emulador,\nARM 64 para o aparelho",
              fontsize=5.6, ha="right", va="top", color="0.15",
              linespacing=1.4, family="DejaVu Sans")

    eixo.text(65, 2.5, "esquemático: a lista de campos varia com a versão "
              "do Unity", fontsize=5.6, ha="center", va="bottom", color="0.35",
              style="italic")
    gravar(fig, "fig-03-build.png")


def fig_portal():
    """A pagina de aplicativos do Device Portal."""
    fig, eixo = folha(13.5, 8.2)
    eixo.set_xlim(0, 135)
    eixo.set_ylim(0, 82)
    eixo.set_aspect("equal")
    eixo.set_axis_off()

    eixo.text(2, 79, "WINDOWS DEVICE PORTAL  ·  VIEWS → APPS", fontsize=8.5,
              weight="bold", family="DejaVu Sans", va="top")

    eixo.add_patch(Rectangle((4, 6), 127, 64, facecolor="white",
                             edgecolor="black", linewidth=1.1))

    # Barra de endereco.
    eixo.add_patch(Rectangle((4, 62), 127, 8, facecolor="0.88",
                             edgecolor="black", linewidth=1.1))
    eixo.add_patch(Rectangle((10, 63.6), 90, 4.8, facecolor="white",
                             edgecolor="0.5", linewidth=0.6))
    eixo.text(12, 66, "http://<IP do aparelho>/#Apps", fontsize=5.4,
              va="center", family="DejaVu Sans Mono")
    _chamada(eixo, (55, 66), (129, 75),
             "o IP sai do Wi-Fi do aparelho", tamanho=6.4, ha="right")

    # Menu lateral.
    eixo.add_patch(Rectangle((4, 6), 26, 56, facecolor="0.96",
                             edgecolor="black", linewidth=0.7))
    for i, item in enumerate(["Home", "3D View", "Mixed Reality Capture",
                              "Performance", "Apps", "File explorer",
                              "Logging"]):
        y = 56 - i * 7
        ativo = item == "Apps"
        if ativo:
            eixo.add_patch(Rectangle((4.5, y - 2.6), 25, 5.6,
                                     facecolor="black", edgecolor="none"))
        eixo.text(7, y, item, fontsize=4.9, va="center",
                  color="white" if ativo else "0.2",
                  weight="bold" if ativo else "normal")

    # Painel de instalacao.
    eixo.add_patch(Rectangle((34, 28), 93, 32, facecolor="0.97",
                             edgecolor="black", linewidth=0.8))
    eixo.text(37, 56, "Install app", fontsize=6.4, weight="bold",
              va="center", family="DejaVu Sans")

    linhas = [
        ("App package", "MeuApp_1.0.0.0_ARM64.appx", True),
        ("Certificate", "MeuApp_1.0.0.0_ARM64.cer", False),
        ("Dependency", "Microsoft.VCLibs...appx", True),
    ]
    for i, (rotulo, valor, forte) in enumerate(linhas):
        y = 50 - i * 6.0
        eixo.text(37, y, rotulo, fontsize=5.2, va="center", color="0.2")
        eixo.add_patch(Rectangle((60, y - 2.3), 52, 4.6, facecolor="white",
                                 edgecolor="0.5", linewidth=0.6))
        eixo.text(62, y, valor, fontsize=4.8, va="center",
                  family="DejaVu Sans Mono",
                  weight="bold" if forte else "normal")

    eixo.add_patch(Rectangle((37, 30.2), 17, 4.2, facecolor="0.80",
                             edgecolor="black", linewidth=0.7))
    eixo.text(45.5, 32.3, "Go", fontsize=5.6, ha="center", va="center",
              weight="bold")

    # A caixa que todo mundo esquece.
    eixo.add_patch(Rectangle((34, 16), 93, 10, facecolor="white",
                             edgecolor="black", linewidth=1.3))
    eixo.add_patch(Rectangle((37, 19.5), 3.6, 3.6, facecolor="black",
                             edgecolor="black", linewidth=0.7))
    eixo.text(42.5, 21.3, "Allow me to select optional packages",
              fontsize=5.6, va="center", weight="bold",
              family="DejaVu Sans")
    _chamada(eixo, (38.8, 21.3), (80, 10),
             "esta caixa é o que permite mandar a dependência junto",
             tamanho=6.4, ha="center")

    gravar(fig, "fig-04-portal.png")


def fig_pareamento():
    """A sequencia de pareamento por USB, em cinco quadros."""
    fig, eixo = folha(16.0, 5.8)
    eixo.set_xlim(0, 160)
    eixo.set_ylim(0, 58)
    eixo.set_aspect("equal")
    eixo.set_axis_off()

    eixo.text(2, 55, "PAREAR O APARELHO COM O VISUAL STUDIO", fontsize=8.5,
              weight="bold", family="DejaVu Sans", va="top")

    passos = [
        ("no HoloLens", "Settings →\nUpdate & Security"),
        ("no HoloLens", "For developers →\nativar as opções"),
        ("no HoloLens", "Pair →\nanotar o PIN"),
        ("no Visual Studio", "alvo Device,\ndepois Run"),
        ("no Visual Studio", "digitar o PIN\ne aguardar"),
    ]
    largura = 27
    for i, (onde, o_que) in enumerate(passos):
        x = 3 + i * (largura + 4.5)
        eixo.add_patch(Rectangle((x, 8), largura, 34, facecolor="white",
                                 edgecolor="black", linewidth=0.9))
        eixo.add_patch(Rectangle((x, 36), largura, 6, facecolor="black",
                                 edgecolor="black", linewidth=0.9))
        eixo.text(x + largura / 2, 39, onde, fontsize=5.4, color="white",
                  weight="bold", ha="center", va="center",
                  family="DejaVu Sans")
        eixo.text(x + largura / 2, 25, o_que, fontsize=6.0, ha="center",
                  va="center", linespacing=1.6, family="DejaVu Sans")
        eixo.add_patch(Circle((x + 4, 12), 2.6, facecolor="0.90",
                              edgecolor="black", linewidth=0.7))
        eixo.text(x + 4, 12, str(i + 1), fontsize=5.4, ha="center",
                  va="center", weight="bold")
        if i < len(passos) - 1:
            eixo.annotate("", xy=(x + largura + 4, 25),
                          xytext=(x + largura + 0.5, 25),
                          arrowprops=dict(arrowstyle="-|>", color="black",
                                          linewidth=0.9, mutation_scale=8))

    eixo.text(80, 4, "o PIN vale uma vez: se expirar, gere outro no aparelho",
              fontsize=6, ha="center", va="bottom", color="0.3",
              style="italic", family="DejaVu Sans")
    gravar(fig, "fig-05-pareamento.png")


def main():
    print("gerando figuras do manual:")
    fig_fluxo()
    fig_dispositivo()
    fig_build()
    fig_portal()
    fig_pareamento()
    print("pronto.")


if __name__ == "__main__":
    main()
