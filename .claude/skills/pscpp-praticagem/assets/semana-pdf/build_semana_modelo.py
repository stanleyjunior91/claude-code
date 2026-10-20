#!/usr/bin/env python3
"""Gera semana1.html e o CSV de cartões (Noji) a partir dos dados abaixo."""
import html, pathlib

OUT = pathlib.Path(__file__).parent
L = "abcde"

def esc(s): return html.escape(s, quote=False)

def question(n, text, opts, ans):
    o = "".join(f'<p class="o">({L[i]}) {esc(t)}</p>' for i, t in enumerate(opts))
    return f'<div class="q"><p class="t">{n}. {esc(text)}</p>{o}</div>', L[ans]

SVG_TOP = '''<svg viewBox="0 -14 200 300" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">
<path d="M100,12 C132,45 148,100 148,160 L148,235 Q148,262 130,265 L70,265 Q52,262 52,235 L52,160 C52,100 68,45 100,12 Z" fill="#dbe7f3" stroke="#12355b" stroke-width="2"/>
<line x1="100" y1="12" x2="100" y2="265" stroke="#12355b" stroke-width="0.8" stroke-dasharray="4 3"/>
<line x1="52" y1="139" x2="148" y2="139" stroke="#12355b" stroke-width="0.8" stroke-dasharray="4 3"/>
<text x="100" y="0" font-size="11" font-weight="bold" text-anchor="middle" fill="#12355b">PROA</text>
<text x="100" y="283" font-size="11" font-weight="bold" text-anchor="middle" fill="#12355b">POPA</text>
<text x="100" y="95" font-size="8.5" text-anchor="middle" fill="#12355b">↑ vante</text>
<text x="100" y="190" font-size="8.5" text-anchor="middle" fill="#12355b">↓ ré</text>
<text x="100" y="133" font-size="8" text-anchor="middle" fill="#12355b">meia-nau</text>
<text x="100" y="153" font-size="7" text-anchor="middle" fill="#4a5a6a">linha de centro</text>
<line x1="52" y1="139" x2="10" y2="139" stroke="#12355b" stroke-width="1"/>
<line x1="148" y1="139" x2="190" y2="139" stroke="#12355b" stroke-width="1"/>
<text x="31" y="134" font-size="8" text-anchor="middle" fill="#12355b">través</text>
<text x="169" y="134" font-size="8" text-anchor="middle" fill="#12355b">través</text>
<circle cx="70" cy="62" r="2.5" fill="#12355b"/><text x="64" y="60" font-size="8" text-anchor="end" fill="#12355b">amura</text>
<circle cx="130" cy="62" r="2.5" fill="#12355b"/><text x="136" y="60" font-size="8" fill="#12355b">amura</text>
<circle cx="53" cy="248" r="2.5" fill="#12355b"/><text x="47" y="251" font-size="8" text-anchor="end" fill="#12355b">alheta</text>
<circle cx="147" cy="248" r="2.5" fill="#12355b"/><text x="153" y="251" font-size="8" fill="#12355b">alheta</text>
<text x="4" y="196" font-size="9" font-weight="bold" fill="#b91c1c">BOMBORDO</text>
<text x="4" y="207" font-size="8" fill="#b91c1c">esquerda</text>
<text x="2" y="217" font-size="7" fill="#b91c1c">luz vermelha</text>
<text x="196" y="196" font-size="9" font-weight="bold" text-anchor="end" fill="#15803d">BORESTE</text>
<text x="196" y="207" font-size="8" text-anchor="end" fill="#15803d">direita</text>
<text x="196" y="217" font-size="8" text-anchor="end" fill="#15803d">luz verde</text>
</svg>'''

SVG_SIDE = '''<svg viewBox="0 0 240 150" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">
<defs><marker id="m" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L6,3 L0,6 z" fill="#12355b"/></marker></defs>
<rect x="22" y="22" width="44" height="30" fill="#eef2f7" stroke="#12355b" stroke-width="1.2"/>
<path d="M14,52 L180,52 Q215,56 228,84 L210,124 L40,124 Q22,118 14,98 Z" fill="#dbe7f3" stroke="#12355b" stroke-width="2"/>
<rect x="0" y="104" width="240" height="40" fill="#5aa9dd" opacity="0.45"/>
<line x1="0" y1="104" x2="240" y2="104" stroke="#1d6fa5" stroke-width="1.2" stroke-dasharray="5 3"/>
<text x="8" y="14" font-size="10" font-weight="bold" fill="#12355b">POPA</text>
<text x="236" y="44" font-size="10" font-weight="bold" text-anchor="end" fill="#12355b">PROA</text>
<text x="34" y="82" font-size="8.5" fill="#12355b">obras mortas</text>
<text x="38" y="118" font-size="8.5" fill="#12355b">obras vivas</text>
<line x1="96" y1="52" x2="96" y2="124" stroke="#12355b" stroke-width="1" marker-start="url(#m)" marker-end="url(#m)"/>
<text transform="translate(105,90) rotate(-90)" font-size="8.5" text-anchor="middle" fill="#12355b">pontal</text>
<line x1="128" y1="52" x2="128" y2="104" stroke="#b45309" stroke-width="1" marker-start="url(#m)" marker-end="url(#m)"/>
<text x="132" y="81" font-size="8.5" fill="#b45309">borda-livre</text>
<line x1="128" y1="104" x2="128" y2="124" stroke="#0b6e6e" stroke-width="1" marker-start="url(#m)" marker-end="url(#m)"/>
<text x="132" y="118" font-size="8.5" fill="#0b6e6e">calado</text>
<text x="34" y="100" font-size="8" fill="#1d6fa5">linha d'água</text>
<text x="120" y="139" font-size="8.5" text-anchor="middle" fill="#12355b">quilha (fundo)</text>
</svg>'''

SVG_SECTION = '''<svg viewBox="-25 0 250 165" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">
<path d="M20,24 L20,112 Q20,138 46,138 L154,138 Q180,138 180,112 L180,24" fill="#dbe7f3" stroke="#12355b" stroke-width="3"/>
<line x1="12" y1="24" x2="188" y2="24" stroke="#12355b" stroke-width="4"/>
<line x1="20" y1="40" x2="180" y2="40" stroke="#12355b" stroke-width="2"/>
<line x1="31" y1="122" x2="169" y2="122" stroke="#12355b" stroke-width="2"/>
<line x1="28" y1="44" x2="28" y2="116" stroke="#12355b" stroke-width="1.2" stroke-dasharray="3 3"/>
<line x1="172" y1="44" x2="172" y2="116" stroke="#12355b" stroke-width="1.2" stroke-dasharray="3 3"/>
<rect x="94" y="138" width="12" height="8" fill="#12355b"/>
<text x="100" y="16" font-size="9" font-weight="bold" text-anchor="middle" fill="#12355b">convés</text>
<text x="100" y="35" font-size="8.5" text-anchor="middle" fill="#12355b">vaus (vigas sob o convés)</text>
<text x="100" y="86" font-size="8.5" text-anchor="middle" fill="#12355b">porão / carga</text>
<text x="100" y="133" font-size="8" text-anchor="middle" fill="#12355b">duplo-fundo (tanques)</text>
<text x="100" y="159" font-size="9" text-anchor="middle" fill="#12355b">quilha</text>
<text x="15" y="75" font-size="8.5" text-anchor="end" fill="#12355b">costado</text>
<text x="185" y="75" font-size="8.5" fill="#12355b">costado</text>
<text x="34" y="62" font-size="7.5" fill="#12355b">caverna</text>
</svg>'''

# ---------------------------------------------------------------- lições
lessons = []

lessons.append(dict(
    key="D1", tag="Dia 1 · ter 20/10", title="O navio visto de cima: direções e lados",
    meta="Programa: II.16 · Livro: Arte Naval V1 cap. 1 · Vídeo, busque: “nomenclatura náutica proa popa bombordo boreste”",
    idea="Antes de qualquer manobra, é preciso falar a mesma língua: onde é a frente, onde é cada lado.",
    pre=[("Qual é a cor da luz de navegação do lado esquerdo do navio?", "vermelha"),
         ("Você está na popa e caminha até a proa. Para onde foi: vante ou ré?", "para vante")],
    body='''<ul>
<li><b>Proa</b>: a frente. <b>Popa</b>: a parte de trás. <b>Meia-nau</b>: o meio, no sentido do comprimento.</li>
<li><b>Linha de centro</b> (plano diametral): a linha imaginária que vai da proa à popa, no meio.</li>
<li>Olhando para a proa: <b>bombordo (BB)</b> é a <b>esquerda</b>; <b>boreste (BE)</b> é a <b>direita</b>.</li>
<li><b>Vante</b>: em direção à proa. <b>Ré</b>: em direção à popa.</li>
<li><b>Amura</b>: trecho do costado perto da proa, onde ele se curva. <b>Alheta</b>: o equivalente perto da popa.</li>
<li><b>Través</b>: a direção perpendicular à linha de centro, ou seja, de lado (90°).</li>
</ul>''',
    fig=SVG_TOP,
    memo="Bombordo = esquerda = vermelho. O vinho do porto é tinto, e “port” é o lado esquerdo em inglês. Boreste fica com o verde.",
    tab="""<table><tr><th>Marcação relativa</th><th>Onde está o objeto</th></tr>
<tr><td>000°</td><td>pela proa (à frente)</td></tr>
<tr><td>045° BE</td><td>pela amura de boreste (aprox.)</td></tr>
<tr><td>090° BE</td><td>pelo través de boreste</td></tr>
<tr><td>135° BE</td><td>pela alheta de boreste (aprox.)</td></tr>
<tr><td>180°</td><td>pela popa (atrás)</td></tr></table>""",
    aord="O prático diz: “vejo um cargueiro pela amura de boreste”. Ele está à frente e à direita, a uns 45° da proa. Esse é o idioma de todo o concurso e da vida a bordo.",
    fey="Explique a um amigo, sem usar as palavras “esquerda” nem “direita”, como se descreve onde está um barco ao redor do seu navio.",
    cards=[("Proa", "Extremidade dianteira (frente) do navio."),
           ("Popa", "Extremidade traseira do navio."),
           ("Meia-nau", "O meio do navio, no sentido do comprimento."),
           ("Bombordo (BB)", "Lado esquerdo de quem olha para a proa. Luz de navegação vermelha."),
           ("Boreste (BE)", "Lado direito de quem olha para a proa. Luz de navegação verde."),
           ("Vante / ré", "Vante: em direção à proa. Ré: em direção à popa."),
           ("Amura e alheta", "Amura: costado perto da proa. Alheta: costado perto da popa."),
           ("Través", "Direção perpendicular à linha de centro (90°, de lado)."),
           ("Marcação relativa 045° BE", "Pela amura de boreste (aproximadamente).")],
    qs=[("O lado direito de quem está a bordo olhando para a proa chama-se:", ["bombordo", "vante", "boreste", "ré", "meia-nau"], 2, "Boreste é a direita."),
        ("Pelo COLREG, a luz de navegação de bombordo é:", ["verde", "vermelha", "branca", "amarela", "azul"], 1, "Bombordo é vermelha; boreste, verde."),
        ("Uma pessoa a bordo caminha da proa para a popa. Ela vai:", ["para vante", "para ré", "para o través", "para bombordo", "para a amura"], 1, "Em direção à popa é “para ré”."),
        ("Um objeto “pelo través de boreste” está:", ["à frente, na linha de centro", "a cerca de 90° da proa, do lado direito", "atrás, na linha de centro", "a cerca de 45° à esquerda", "a 180° da proa"], 1, "Través é de lado (90°); boreste é a direita."),
        ("Marque a INCORRETA:", ["Meia-nau é o meio do navio no sentido do comprimento.", "Alheta é a região do costado próxima à popa.", "Amura é a região do costado próxima à proa.", "Bombordo é o lado direito de quem olha para a proa.", "A proa é a extremidade dianteira do navio."], 3, "Bombordo é o lado ESQUERDO.")],
))

lessons.append(dict(
    key="D2", tag="Dia 2 · qua 21/10", title="Por dentro do casco: a estrutura",
    meta="Programa: II.16.2 a 16.4 · Livro: Arte Naval V1 cap. 1 · Vídeo, busque: “ship structure keel frames bulkhead explained”",
    idea="O casco é uma caixa de aço que flutua. Ele tem esqueleto, pele, paredes e piso.",
    pre=[("Como se chama a “espinha dorsal” no fundo do navio?", "quilha"),
         ("Para que servem as paredes estanques (anteparas) dentro do casco?", "dividem o casco; limitam o alagamento")],
    body='''<ul>
<li><b>Quilha</b>: peça longitudinal no fundo, ao longo da linha de centro. É a “espinha dorsal”.</li>
<li><b>Roda de proa</b>: peça que forma a proa. <b>Cadaste</b>: peça estrutural da popa, onde se apoiam o leme e o hélice.</li>
<li><b>Cavernas</b>: peças transversais curvas, as “costelas” que dão forma e força ao costado.</li>
<li><b>Vaus</b>: vigas transversais que sustentam o convés.</li>
<li><b>Chapeamento</b>: as chapas de aço que formam a “pele” do casco e do convés.</li>
<li><b>Anteparas</b>: paredes estanques que dividem o casco em compartimentos. Se um alaga, os outros seguram o navio.</li>
<li><b>Duplo-fundo</b>: um segundo fundo interno. O espaço entre os dois forma tanques de lastro e de combustível.</li>
<li><b>Convés</b>: piso superior, exposto. <b>Cobertas</b>: pisos internos abaixo do convés. <b>Plataformas</b>: pisos parciais dentro de um compartimento.</li>
</ul>''',
    fig=SVG_SECTION,
    memo="Esqueleto: quilha (coluna) e cavernas (costelas). Pele: chapeamento. Teto: vaus e convés. Paredes: anteparas.",
    tab="",
    aord="O lastro nos tanques do duplo-fundo muda o calado e o trim do navio. Por isso o prático pergunta ao comandante como o navio está lastrado. As anteparas, num alagamento, decidem se o navio fica de pé.",
    fey="Explique a um amigo por que um navio não afunda inteiro quando um compartimento alaga.",
    cards=[("Quilha", "Peça longitudinal no fundo do casco, na linha de centro: a “espinha dorsal”."),
           ("Roda de proa", "Peça estrutural que forma a proa."),
           ("Cadaste", "Peça estrutural da popa, onde se apoiam o leme e o hélice."),
           ("Cavernas", "Peças transversais curvas: as “costelas” do casco."),
           ("Vaus", "Vigas transversais que sustentam o convés."),
           ("Chapeamento", "Chapas de aço que formam a “pele” do casco e do convés."),
           ("Antepara", "Parede estanque que divide o casco em compartimentos e limita o alagamento."),
           ("Duplo-fundo", "Segundo fundo interno; o espaço forma tanques de lastro e combustível."),
           ("Convés, coberta, plataforma", "Convés: piso superior exposto. Coberta: piso interno. Plataforma: piso parcial.")],
    qs=[("Peça longitudinal que forma a “espinha dorsal” no fundo do casco:", ["vau", "caverna", "quilha", "antepara", "convés"], 2, "É a quilha."),
        ("As peças transversais curvas que formam as “costelas” do casco são:", ["quilhas", "cavernas", "anteparas", "vaus", "cadastes"], 1, "Cavernas."),
        ("Vigas transversais que sustentam o convés:", ["vaus", "cavernas", "quilhas", "rodas de proa", "tanques"], 0, "Vaus."),
        ("A principal vantagem de dividir o casco em compartimentos por anteparas estanques é:", ["aumentar a velocidade", "limitar o alagamento a poucos compartimentos em caso de avaria", "reduzir o calado", "dispensar o lastro", "aumentar a boca"], 1, "Limita o alagamento."),
        ("Marque a INCORRETA:", ["Cadaste é peça estrutural da popa onde se apoiam o leme e o hélice.", "Roda de proa é a peça que forma a proa.", "O duplo-fundo forma tanques entre os dois fundos.", "Abaulamento é a curvatura longitudinal do convés.", "Chapeamento é a “pele” de aço do casco."], 3, "Abaulamento é a curvatura TRANSVERSAL do convés (a longitudinal é o tosamento).")],
))

lessons.append(dict(
    key="D3", tag="Dia 3 · qui 22/10", title="A linha d'água: calado, obras vivas e borda-livre",
    meta="Programa: II.16.5 a 16.7 · Livro: Arte Naval V1 cap. 2 · Vídeo, busque: “ship draft freeboard plimsoll explained”",
    idea="Quase tudo na manobra depende de quanto do navio está dentro da água.",
    pre=[("O calado é medido entre a linha d'água e qual parte do navio?", "a quilha"),
         ("Um navio que entra num rio de água doce sobe ou afunda um pouco?", "afunda um pouco")],
    body='''<ul>
<li><b>Linha d'água</b> (de flutuação): onde a superfície da água toca o casco.</li>
<li><b>Obras vivas</b> (carena): parte do casco <b>abaixo</b> da linha d'água. <b>Obras mortas</b>: parte <b>acima</b>.</li>
<li><b>Calado</b>: distância vertical entre a linha d'água e a quilha. Há calado de proa, de popa e médio (os números pintados no casco).</li>
<li><b>Trim</b> = calado de popa − calado de proa. Se a popa está mais funda, o navio está <b>apopado</b>; se a proa, <b>aproado</b>. <b>Banda</b> é a inclinação para um dos lados.</li>
<li><b>Borda-livre</b>: distância vertical entre a linha d'água e o convés, a meia-nau. Mais borda-livre, mais reserva de flutuabilidade.</li>
<li><b>Pontal</b>: altura da quilha ao convés. Em conta rápida: <b>pontal ≈ calado + borda-livre</b>.</li>
</ul>''',
    fig=SVG_SIDE,
    memo="Calado: para baixo (até a quilha). Borda-livre: para cima (até o convés). Os dois somados dão o pontal.",
    tab="""<div class="box key"><p><b>Água doce x salgada:</b> a água doce é menos densa (1,000 contra 1,025 t/m³), então o calado cresce cerca de 2,5% (aproximado). Ex.: 10,0 m no mar, cerca de 10,25 m no rio.</p></div>""",
    aord="Antes da barra, o prático pergunta o calado de proa e de popa. O trim muda como o navio responde ao leme, e o calado define se há água sob a quilha.",
    fey="Explique a um amigo a diferença entre calado, borda-livre e pontal, desenhando um navio.",
    cards=[("Linha d'água", "Linha em que a superfície da água toca o casco."),
           ("Obras vivas", "Parte do casco abaixo da linha d'água."),
           ("Obras mortas", "Parte do casco acima da linha d'água."),
           ("Calado", "Distância vertical da linha d'água à quilha."),
           ("Trim", "Calado de popa menos calado de proa. Popa mais funda: apopado."),
           ("Banda", "Inclinação transversal (para um bordo)."),
           ("Borda-livre", "Distância vertical da linha d'água ao convés, a meia-nau."),
           ("Pontal", "Altura da quilha ao convés. Aproximadamente calado + borda-livre."),
           ("Do mar para água doce", "O calado aumenta cerca de 2,5% (aproximado).")],
    qs=[("O calado é a distância vertical entre:", ["o convés e a quilha", "a linha d'água e a quilha", "a linha d'água e o convés", "a proa e a popa", "a quilha e a roda de proa"], 1, "Da linha d'água à quilha."),
        ("Calado de proa 8,0 m e de popa 9,0 m. O trim é:", ["1,0 m pela proa", "1,0 m pela popa (navio apopado)", "8,5 m", "17,0 m", "zero"], 1, "Trim = 9,0 − 8,0 = 1,0 m, popa mais funda."),
        ("Calado 9,0 m e borda-livre 3,5 m. O pontal vale aproximadamente:", ["5,5 m", "6,0 m", "12,5 m", "31,5 m", "9,0 m"], 2, "9,0 + 3,5 = 12,5 m."),
        ("Ao passar do mar para um rio de água doce, sem mudar a carga, o calado:", ["diminui", "permanece igual", "aumenta", "zera", "muda só na popa"], 2, "Água doce é menos densa; o navio afunda mais."),
        ("Marque a INCORRETA:", ["Obras vivas são a parte do casco abaixo da linha d'água.", "Obras mortas são a parte do casco acima da linha d'água.", "Obras mortas são a parte submersa do casco.", "Borda-livre é medida da linha d'água ao convés.", "Banda é uma inclinação transversal."], 2, "Obras mortas ficam ACIMA da linha d'água.")],
))

lessons.append(dict(
    key="D4", tag="Dia 4 · sex 23/10", title="As medidas do navio e o coeficiente de bloco",
    meta="Programa: II.16.7 · Livro: Arte Naval V1 cap. 2 · Vídeo, busque: “block coefficient ship explained”",
    idea="Cada navio tem um tamanho e um “quão cheio” é o casco. Isso aparece depois no squat e na manobra.",
    pre=[("Como se chama a largura máxima do casco?", "boca"),
         ("Um VLCC tem casco “fino” ou “gordo”?", "gordo (Cb alto)")],
    body='''<ul>
<li><b>Comprimento total (LOA)</b>: de uma ponta à outra do navio.</li>
<li><b>Comprimento entre perpendiculares (Lpp)</b>: entre a perpendicular de vante (na roda de proa, na linha d'água) e a de ré (em geral no eixo do leme). É o “L” usado nas fórmulas e nos critérios de manobra da IMO.</li>
<li><b>Boca (B)</b>: largura máxima. <b>Pontal (D)</b>: da quilha ao convés. <b>Calado (T)</b>: da linha d'água à quilha.</li>
<li><b>Coeficiente de bloco (Cb)</b>: mede o quão “cheio” é o casco.<br>
<b>Cb = volume submerso ÷ (Lpp × B × T)</b>. Cb = 1 seria uma caixa retangular.</li>
</ul>
<div class="box"><p><b>Exemplo resolvido:</b> Lpp = 200 m, B = 30 m, T = 10 m, volume submerso = 42 000 m³.<br>
Lpp × B × T = 200 × 30 × 10 = 60 000. Cb = 42 000 ÷ 60 000 = <b>0,70</b>.</p></div>
<table><tr><th>Tipo</th><th>Cb típico</th></tr>
<tr><td>Petroleiros e graneleiros grandes</td><td>0,80 a 0,85</td></tr>
<tr><td>Porta-contêineres</td><td>0,60 a 0,70</td></tr></table>''',
    fig="",
    memo="Cb alto = casco “gordo” = navio lento, grande e carregado, e mais squat (aparece na Parte I).",
    tab="""<table><tr><th>Ordem de grandeza (aprox.)</th><th>Comp. x boca</th></tr>
<tr><td>Rebocador</td><td>~30 m x ~10 m</td></tr>
<tr><td>Graneleiro Panamax</td><td>~225 m x ~32 m</td></tr>
<tr><td>Graneleiro Capesize</td><td>~290 m x ~45 m</td></tr>
<tr><td>Petroleiro VLCC</td><td>~330 m x ~60 m</td></tr></table>""",
    aord="O prático olha o comprimento, a boca e o calado para escolher rebocadores, planejar a aproximação ao cais e saber se o navio cabe no canal. Sempre pergunta o Cb do navio, que está nas informações do passadiço.",
    fey="Explique a um amigo o que significa dizer que um navio tem Cb de 0,8, e dê um exemplo de navio com Cb baixo.",
    cards=[("LOA", "Comprimento total: de uma ponta à outra do navio."),
           ("Lpp", "Comprimento entre perpendiculares (usado em fórmulas e critérios IMO)."),
           ("Boca", "Largura máxima do casco."),
           ("Pontal", "Altura da quilha ao convés."),
           ("Coeficiente de bloco (Cb)", "Volume submerso ÷ (Lpp × B × T). Mede o quão “cheio” é o casco."),
           ("Cb de petroleiros grandes", "Alto, cerca de 0,80 a 0,85."),
           ("Cb de porta-contêineres", "Mais baixo, cerca de 0,60 a 0,70.")],
    qs=[("A largura máxima do casco chama-se:", ["calado", "pontal", "boca", "Lpp", "LOA"], 2, "Boca."),
        ("O comprimento total (LOA) é medido:", ["entre as perpendiculares", "de uma extremidade à outra do navio", "só na linha d'água", "do convés à quilha", "só na parte submersa"], 1, "De ponta a ponta."),
        ("Lpp 150 m, boca 25 m, calado 8 m, volume submerso 21 000 m³. O Cb vale:", ["0,50", "0,60", "0,70", "0,80", "0,90"], 2, "150 × 25 × 8 = 30 000; 21 000 ÷ 30 000 = 0,70."),
        ("Qual navio costuma ter o maior coeficiente de bloco?", ["porta-contêiner rápido", "petroleiro gigante (VLCC)", "lancha de prático", "navio de passageiros", "rebocador"], 1, "O VLCC tem casco cheio (Cb alto)."),
        ("Marque a INCORRETA:", ["Pontal é a altura da quilha ao convés.", "Boca é a largura máxima.", "Calado é a distância vertical do convés à quilha.", "Cb = 1 representaria um bloco retangular.", "Lpp é medido entre as perpendiculares."], 2, "Calado é da linha d'água à quilha. Da quilha ao convés é o pontal.")],
))

lessons.append(dict(
    key="D5", tag="Dia 5 · sáb 24/10", title="Como o navio se movimenta: os seis movimentos",
    meta="Programa: I.8.3 · Livro: Santos, A manobrabilidade do navio no século 21, cap. 2 (se tiver; senão só a lição) · Vídeo, busque: “6 degrees of freedom ship motion roll pitch yaw”",
    idea="Um navio pode se mover de 6 formas. Leme e hélice mexem em algumas; vento e onda, em outras.",
    pre=[("O leme faz o navio girar para os lados. Esse giro tem nome em inglês. Você conhece?", "yaw (guinada)"),
         ("A proa sobe e desce com as ondas. Qual é o nome?", "caturro (pitch)")],
    body='''<p><b>3 movimentos de ir</b> (translações) e <b>3 movimentos de girar</b> (rotações):</p>
<table><tr><th>Movimento</th><th>Em inglês</th><th>O que é</th></tr>
<tr><td>Avanço</td><td>surge</td><td>para vante e para ré</td></tr>
<tr><td>Deriva</td><td>sway</td><td>de lado, para BB ou BE</td></tr>
<tr><td>Arfagem</td><td>heave</td><td>para cima e para baixo</td></tr>
<tr><td>Balanço</td><td>roll</td><td>gira em torno do eixo longitudinal: inclina de um bordo ao outro</td></tr>
<tr><td>Caturro</td><td>pitch</td><td>gira em torno do eixo transversal: a proa sobe e a popa desce</td></tr>
<tr><td>Guinada</td><td>yaw</td><td>gira em torno do eixo vertical: a proa vai para BB ou BE</td></tr></table>
<div class="box warn"><p>Os nomes em português variam de autor para autor. <b>Guarde os termos em inglês também</b> (surge, sway, heave, roll, pitch, yaw), porque aparecem nas provas e nos livros.</p></div>''',
    fig="",
    memo="Roll rola como um tronco (de lado). Pitch cabeceia (proa). Yaw é guinar, o que o leme faz.",
    tab="""<table><tr><th>Quem causa o quê</th><th>Movimentos</th></tr>
<tr><td>Leme e hélice</td><td>avanço e guinada</td></tr>
<tr><td>Ondas</td><td>arfagem, balanço e caturro</td></tr>
<tr><td>Vento e correnteza</td><td>deriva (e guinada)</td></tr></table>""",
    aord="Quando o prático manda “leme a 20 de boreste”, quer uma guinada. Com vento de través forte, o navio sofre deriva, e quem não percebe vai parar fora da derrota. As ondas, em compensação, quase não mudam o rumo, mas mudam o calado e o conforto.",
    fey="Explique em voz alta os seis movimentos usando o seu próprio corpo ou um copo na mesa.",
    cards=[("Avanço (surge)", "Movimento para vante ou para ré."),
           ("Deriva (sway)", "Movimento lateral do navio inteiro."),
           ("Arfagem (heave)", "Movimento vertical, para cima e para baixo."),
           ("Balanço (roll)", "Rotação em torno do eixo longitudinal: inclina de um bordo ao outro."),
           ("Caturro (pitch)", "Rotação em torno do eixo transversal: a proa sobe e desce."),
           ("Guinada (yaw)", "Rotação em torno do eixo vertical: a proa vai para BB ou BE."),
           ("Quem produz a guinada?", "Principalmente o leme (com ajuda do hélice).")],
    qs=[("A rotação em torno do eixo vertical (a proa vai para um bordo) é:", ["balanço", "caturro", "guinada (yaw)", "avanço", "arfagem"], 2, "Guinada (yaw)."),
        ("O leme age principalmente provocando:", ["arfagem", "guinada", "caturro", "balanço", "avanço"], 1, "Guinada."),
        ("Quando a proa sobe e desce com as ondas, o movimento é:", ["balanço (roll)", "caturro (pitch)", "guinada", "deriva", "avanço"], 1, "Caturro (pitch)."),
        ("O deslocamento lateral do navio inteiro, sem girar, empurrado pelo vento, é:", ["deriva (sway)", "avanço (surge)", "arfagem (heave)", "caturro", "guinada"], 0, "Deriva (sway)."),
        ("Marque a INCORRETA:", ["Balanço (roll) é rotação em torno do eixo longitudinal.", "Caturro (pitch) é rotação em torno do eixo transversal.", "Guinada (yaw) é rotação em torno do eixo vertical.", "Arfagem (heave) é o movimento vertical.", "Balanço (roll) é rotação em torno do eixo transversal."], 4, "Roll é em torno do eixo LONGITUDINAL; o transversal é o pitch.")],
))

# ---------------------------------------------------------------- sábado
sat_qs = [
 ("A luz vermelha de navegação fica no lado de:", ["boreste", "bombordo", "proa", "popa", "meia-nau"], 1, "Bombordo."),
 ("Parede estanque que divide o casco em compartimentos:", ["vau", "caverna", "antepara", "quilha", "cadaste"], 2, "Antepara."),
 ("A distância vertical entre a linha d'água e a quilha é o:", ["pontal", "borda-livre", "boca", "calado", "trim"], 3, "Calado."),
 ("Pontal 14,0 m e calado 10,5 m. A borda-livre é, aproximadamente:", ["3,5 m", "4,5 m", "24,5 m", "10,5 m", "1,4 m"], 0, "14,0 − 10,5 = 3,5 m."),
 ("Lpp 180 m, boca 28 m, calado 9 m, volume submerso 36 288 m³. O Cb é:", ["0,60", "0,65", "0,70", "0,75", "0,80"], 4, "180 × 28 × 9 = 45 360; 36 288 ÷ 45 360 = 0,80."),
 ("Um navio com 10,0 m de calado no mar entra em rio de água doce. O calado passa a ser, aproximadamente:", ["9,75 m", "10,00 m", "10,25 m", "11,50 m", "12,00 m"], 2, "Aumenta cerca de 2,5%."),
 ("A proa sobe e desce com a ondulação. O movimento é:", ["guinada", "caturro", "balanço", "deriva", "avanço"], 1, "Caturro (pitch)."),
 ("Peça que sustenta o convés:", ["quilha", "caverna", "vau", "roda de proa", "hélice"], 2, "Vau."),
 ("Marque a INCORRETA:", ["Trim é a diferença entre calado de popa e de proa.", "Banda é a inclinação transversal.", "Trim é a inclinação transversal do navio.", "Navio apopado tem o calado de popa maior.", "Navio aproado tem o calado de proa maior."], 2, "A inclinação transversal é a banda. Trim é a diferença entre calados."),
 ("“Pelo través de bombordo” é:", ["90° à esquerda da proa", "90° à direita da proa", "pela proa", "pela popa", "45° à direita"], 0, "Través = 90°; bombordo = esquerda."),
]

aula0_cards = [("ZP (zona de praticagem)", "Área geográfica onde, por peculiaridades locais, há serviço de praticagem permanentemente disponível."),
               ("Serviço de praticagem: o que compõe", "Prático, lancha de prático e atalaia."),
               ("Quem é responsável pelo navio com o prático a bordo?", "O Comandante. O prático o assessora; a presença dele não desobriga o Comandante."),
               ("Prático x Praticante de Prático", "Praticante é o aprovado no PSCPP que está em qualificação (12 a 18 meses). Depois do exame de habilitação, vira Prático.")]

# ---------------------------------------------------------------- HTML
parts = []
parts.append('''<section class="first cover">
<span class="tag">Semana 0 e Semana 1</span>
<h1>Começando pelo navio</h1>
<p class="big">Lições de 20/10 a 26/10 (e a Aula 0)</p>
<div class="box key"><p><b>Como usar:</b> uma lição por dia, na ordem. Cada dia tem 2 páginas: a lição e os exercícios. O gabarito fica no fim, para você tentar antes.</p></div>
<h3>Roteiro</h3>
<ul class="small">
<li>Aula 0: o que é um prático</li>
<li>Dia 1: direções e lados</li>
<li>Dia 2: estrutura do casco</li>
<li>Dia 3: calado e borda-livre</li>
<li>Dia 4: medidas e Cb</li>
<li>Dia 5: os seis movimentos</li>
<li>Segunda: revisão e teste (10 questões)</li>
<li>Gabarito comentado</li>
</ul>
<p class="tiny">Os cartões desta semana estão no arquivo .csv que acompanha este PDF (para importar no Noji).</p>
</section>''')

parts.append('''<section class="pg">
<span class="tag">Aula 0 · 20 min</span>
<h2>O que é um prático?</h2>
<div class="box"><p>Quando um navio grande entra num porto, canal ou rio, quem o ajuda a passar com segurança é o <b>prático</b>.</p></div>
<ul>
<li>O prático é um profissional <b>civil</b>, habilitado pela Autoridade Marítima, que <b>assessora o Comandante</b> na condução do navio em águas de risco.</li>
<li>Quem comanda continua sendo o <b>Comandante</b>. A presença do prático não o desobriga (NORMAM-311, art. 2.30.1).</li>
<li>A Lei 14.813/2024 diz que as orientações de rumo e velocidade, em assessoria ao Comandante, são transmitidas <b>exclusivamente por práticos</b> (art. 15-B).</li>
<li>Cada <b>Zona de Praticagem (ZP)</b> tem seus práticos, sua lancha e sua atalaia (a base em terra). Tudo isso é o <b>serviço de praticagem</b>.</li>
<li>A praticagem é obrigatória, em regra, para navios com arqueação bruta acima de 500.</li>
</ul>
<h3>O caminho até ser prático</h3>
<table>
<tr><td><b>1</b></td><td><b>PSCPP</b>: o processo seletivo, com 4 etapas (prova escrita, saúde e teste físico, títulos, prova prático-oral em inglês).</td></tr>
<tr><td><b>2</b></td><td><b>Praticante de Prático</b>: qualificação de 12 a 18 meses, acompanhando práticos em fainas reais.</td></tr>
<tr><td><b>3</b></td><td><b>Exame de habilitação</b>, a bordo, e então <b>Prático</b>.</td></tr>
</table>
<div class="box key"><p>Você está na etapa 1. Toda a Fase 0 serve para a prova escrita fazer sentido: antes de calcular forças, é preciso saber o que é a proa, o calado e a ZP.</p></div>
<h3>Cards da Aula 0</h3>
<table class="cards small">''' + "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in aula0_cards) + '''</table>
</section>''')

answers = []

for i, ls in enumerate(lessons, start=1):
    pre = "".join(f'<li>{esc(q)} <span class="tiny">(resposta: {esc(a)})</span></li>' for q, a in ls["pre"])
    fig = f'<div>{ls["fig"]}</div>' if ls["fig"] else ""
    tab = ls["tab"]
    parts.append(f'''<section class="pg">
<span class="tag">{esc(ls["tag"])}</span>
<h2>{esc(ls["title"])}</h2>
<p class="meta">{esc(ls["meta"])}</p>
<div class="box key"><p><b>Ideia do dia:</b> {esc(ls["idea"])}</p></div>
<h3>Antes de ler (chute)</h3>
<ol class="small">{pre}</ol>
<h3>A lição</h3>
{ls["body"]}
{fig}
{tab}
<div class="box"><p><b>Lembre assim:</b> {esc(ls["memo"])}</p></div>
<div class="box warn"><p><b>A bordo:</b> {esc(ls["aord"])}</p></div>
</section>''')
    cards = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in ls["cards"])
    qhs = []
    ans = []
    for n, (t, o, a, why) in enumerate(ls["qs"], start=1):
        h, letter = question(n, t, o, a)
        qhs.append(h)
        ans.append((n, letter, why))
    qh_first, qh_rest = qhs[0], "".join(qhs[1:])
    answers.append((ls["tag"], ls["title"], ans))
    parts.append(f'''<section class="pg">
<span class="tag">{esc(ls["tag"])} · prática</span>
<h2>Explique e cards</h2>
<h3>Explique (15 min)</h3>
<p>{esc(ls["fey"])}</p>
<h3>Cards sugeridos</h3>
<table class="cards small">{cards}</table>
<p class="tiny">Estes cards já estão no arquivo .csv para importar no Noji.</p>
</section>
<section class="pg">
<span class="tag">{esc(ls["tag"])} · exercícios</span>
<p class="tiny"><b>5 exercícios, com consulta.</b> Tente primeiro; depois confira na lição. Gabarito no fim do PDF.</p>
{qh_first}{qh_rest}
</section>''')

# sábado
qh = ""
ans = []
for n, (t, o, a, why) in enumerate(sat_qs, start=1):
    h, letter = question(n, t, o, a)
    qh += h
    ans.append((n, letter, why))
answers.append(("Segunda 26/10", "Teste da semana", ans))
parts.append('''<section class="pg">
<span class="tag">Segunda 26/10 · revisão</span>
<h2>Revise e teste</h2>
<h3>Passo a passo (2h)</h3>
<ol class="small">
<li><b>Desenhe de memória</b> o navio visto de cima e de lado, com todos os nomes (20 min). Depois compare com as figuras.</li>
<li><b>Cards</b> da semana, os 45 (20 min).</li>
<li><b>Releia</b> só as lições em que se sentiu inseguro (30 min).</li>
<li><b>Teste de 10 questões</b>, sem consultar, no ritmo da prova: 2 min por questão (próxima página).</li>
<li><b>Corrija</b> pelo gabarito e anote os erros no caderno, com a causa A, B ou C (20 min).</li>
</ol>
<div class="box"><p><b>Meta:</b> 7 ou mais acertos para avançar. Menos que isso: na segunda, refaça as lições dos erros, e depois siga com a Semana 2.</p></div>
</section>
<section class="pg">
<span class="tag">Segunda · teste</span>
<h2>Teste da semana: 10 questões</h2>''' + qh + '</section>')

# gabarito
g = '<section class="pg"><span class="tag">Gabarito comentado</span><h2>Respostas</h2><p class="tiny">Só confira depois de tentar.</p>'
for tag, title, ans in answers:
    g += f'<h3>{esc(tag)}: {esc(title)}</h3><table>'
    for n, letter, why in ans:
        g += f'<tr><td style="width:12%"><b>{n}</b></td><td style="width:12%"><b>{letter.upper()}</b></td><td>{esc(why)}</td></tr>'
    g += '</table>'
g += '</section>'
parts.append(g)

doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>PSCPP – Semana 1</title>
<link rel="stylesheet" href="base.css"></head><body>{"".join(parts)}</body></html>'''
(OUT / "semana1.html").write_text(doc, encoding="utf-8")

# ---------------------------------------------------------------- CSV (Noji)
import csv
rows = list(aula0_cards)
for ls in lessons:
    rows += list(ls["cards"])
with open(OUT / "PSCPP-cartoes-Noji-semana1.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for a, b in rows:
        w.writerow([a, b])
print(len(rows), "cartões")
