# manual_hololens2

Manual de **conectar e instalar no HoloLens 2**, do zero: do build no Unity
ao aplicativo rodando no aparelho, passando pelo Visual Studio, pelo Device
Portal e pelo pareamento.

A base é o `hololens tutorial.txt` deste repositório, o registro cru do que
foi feito no laboratório durante o
[TCC](https://github.com/ricardobertolin/TCC_LASVII_1): uma lista de
tópicos, escrita enquanto a coisa acontecia. Ela funciona para quem já
passou pelo processo e serve de lembrete.

O que faltava ali era o que só se percebe na primeira vez: a ordem, o porquê
de cada passo e, principalmente, os pontos em que o processo **falha em
silêncio**. Marcar a arquitetura errada no build, abrir o `.sln` da raiz em
vez do da pasta gerada e esquecer de mandar a dependência junto com o pacote
são três erros que não produzem mensagem clara nenhuma, e cada um custa uma
tarde.

- [`manual.html`](manual.html) para ler na tela, com links.
- [`manual-impresso.pdf`](manual-impresso.pdf), 13 páginas em tamanho Carta,
  no formato de folha de fabricante, para imprimir e deixar na bancada.

O tutorial original continua aqui, intacto. O manual é uma camada por cima
dele, não um substituto.

## Refazer as figuras e o PDF

As figuras são esquemáticas, desenhadas em matplotlib: o fluxo inteiro, o
aparelho com os botões, a janela de Build Settings, a página de aplicativos
do Device Portal e a sequência de pareamento. Ao contrário dos manuais dos
robôs, aqui não há modelo de CAD por trás, e o `preparar_manual.py` roda
sozinho.

A exceção é `figuras/foto-aparelho.png`, que é uma fotografia e não é
gerada por script nenhum. Ela fica ao lado do esquemático em vez de no
lugar dele: a foto diz o que é o aparelho, o esquemático diz onde ficam os
botões, e um não substitui o outro.

```
pip install matplotlib playwright && python -m playwright install chromium
python preparar_manual.py     # as figuras, em figuras/
python preparar_pdf.py        # o PDF
```

A paginação do manual impresso é explícita, uma folha por `<section>`, para
não cortar procedimento no meio. O custo disso é que uma página que
transborda não vira duas, vira uma com o fim cortado e sem aviso: por isso o
`preparar_pdf.py` confere a altura de cada folha e **se recusa a gerar o
arquivo** se alguma estourar.

As figuras e o PDF vão versionados justamente para que ler o manual não
dependa de rodar nada.

## Os arquivos

| | |
|---|---|
| `manual.html` | O manual para ler na tela, com links. |
| `manual-impresso.html` | A edição impressa, paginada à mão em folhas de tamanho Carta. |
| `manual-impresso.pdf` | O resultado, pronto para imprimir. |
| `figuras/` | As figuras do manual. |
| `hololens tutorial.txt` | O registro cru do laboratório, de onde o manual saiu. |
| `preparar_manual.py` | Gera as figuras em `figuras/`. |
| `preparar_pdf.py` | Fecha o PDF, conferindo antes se alguma folha transbordou. |

## Marcas

Microsoft, HoloLens, Windows, Visual Studio e Mixed Reality Toolkit são
marcas da Microsoft Corporation. Unity é marca da Unity Technologies.
Documento independente, não produzido nem endossado por nenhuma delas.
