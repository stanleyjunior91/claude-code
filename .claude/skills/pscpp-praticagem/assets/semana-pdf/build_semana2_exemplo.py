#!/usr/bin/env python3
"""Semana 2: Flutuar e não virar. Gera semana2.html e o CSV de cartões (Noji)."""
import csv, html, pathlib

OUT = pathlib.Path(__file__).parent
L = "abcde"

def esc(s): return html.escape(s, quote=False)

def question(n, text, opts, ans):
    o = "".join(f'<p class="o">({L[i]}) {esc(t)}</p>' for i, t in enumerate(opts))
    return f'<div class="q"><p class="t">{n}. {esc(text)}</p>{o}</div>', L[ans]

# ------------------------------------------------------------------ figuras
SVG_ARQ = '''<svg viewBox="0 0 200 130" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">
<path d="M50,36 L50,85 Q50,100 66,100 L134,100 Q150,100 150,85 L150,36 Z" fill="#dbe7f3" stroke="#12355b" stroke-width="2.5"/>
<rect x="0" y="70" width="200" height="60" fill="#5aa9dd" opacity="0.4"/>
<line x1="0" y1="70" x2="200" y2="70" stroke="#1d6fa5" stroke-width="1.2" stroke-dasharray="5 3"/>
<line x1="90" y1="62" x2="90" y2="104" stroke="#b91c1c" stroke-width="2.2"/><path d="M85,98 L90,108 L95,98 Z" fill="#b91c1c"/>
<line x1="110" y1="106" x2="110" y2="42" stroke="#15803d" stroke-width="2.2"/><path d="M105,50 L110,38 L115,50 Z" fill="#15803d"/>
<circle cx="90" cy="62" r="3" fill="#b91c1c"/><circle cx="110" cy="85" r="3" fill="#15803d"/>
<text x="84" y="55" font-size="9" text-anchor="end" fill="#b91c1c" font-weight="bold">peso</text>
<text x="84" y="65" font-size="8" text-anchor="end" fill="#b91c1c">(em G)</text>
<text x="116" y="108" font-size="9" fill="#15803d" font-weight="bold">empuxo</text>
<text x="116" y="118" font-size="8" fill="#15803d">(em B)</text>
<text x="2" y="66" font-size="7.5" fill="#1d6fa5">linha d'água</text>
<text x="100" y="14" font-size="9.5" text-anchor="middle" fill="#12355b" font-weight="bold">peso do navio = empuxo → flutua</text>
</svg>'''

SVG_GM = '''<svg viewBox="28 22 144 136" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">
<defs><marker id="ah" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L6,3 L0,6 z" fill="#12355b"/></marker></defs>
<g transform="rotate(25 100 80)">
<path d="M60,40 L60,110 Q60,125 78,125 L122,125 Q140,125 140,110 L140,40 Z" fill="#dbe7f3" stroke="#12355b" stroke-width="2.5"/>
<line x1="100" y1="40" x2="100" y2="125" stroke="#12355b" stroke-width="0.9" stroke-dasharray="4 3"/>
</g>
<rect x="0" y="91" width="200" height="69" fill="#5aa9dd" opacity="0.4"/>
<line x1="0" y1="91" x2="200" y2="91" stroke="#1d6fa5" stroke-width="1" stroke-dasharray="5 3"/>
<line x1="91.55" y1="98" x2="91.55" y2="140" stroke="#b91c1c" stroke-width="2"/>
<line x1="100" y1="105.4" x2="100" y2="64" stroke="#15803d" stroke-width="2"/>
<path d="M96.5,72 L100,62 L103.5,72 Z" fill="#15803d"/>
<line x1="91.55" y1="148" x2="100" y2="148" stroke="#12355b" stroke-width="1" marker-start="url(#ah)" marker-end="url(#ah)"/>
<line x1="100" y1="106" x2="100" y2="152" stroke="#12355b" stroke-width="0.5" stroke-dasharray="2 2"/>
<line x1="91.55" y1="140" x2="91.55" y2="152" stroke="#12355b" stroke-width="0.5" stroke-dasharray="2 2"/>
<circle cx="100" cy="80" r="2.8" fill="#12355b"/><text x="105" y="79" font-size="11" font-weight="bold" fill="#12355b">M</text>
<circle cx="91.55" cy="98.1" r="2.8" fill="#b91c1c"/><text x="85" y="97" font-size="11" font-weight="bold" text-anchor="end" fill="#b91c1c">G</text>
<circle cx="100" cy="105.4" r="2.8" fill="#15803d"/><text x="106" y="113" font-size="11" font-weight="bold" fill="#15803d">B</text>
<text x="104" y="68" font-size="8" fill="#15803d">empuxo</text>
<text x="86" y="138" font-size="8" text-anchor="end" fill="#b91c1c">peso</text>
<text x="104" y="150" font-size="10" font-weight="bold" fill="#12355b">GZ</text>
<text x="170" y="32" font-size="7" text-anchor="end" fill="#4a5a6a">inclinação exagerada</text>
</svg>'''

SVG_FSE = '''<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, sans-serif">
<defs><clipPath id="tk"><rect x="60" y="30" width="80" height="60" transform="rotate(15 100 60)"/></clipPath>
<marker id="a2" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#12355b"/></marker></defs>
<rect x="0" y="62" width="200" height="40" fill="#5aa9dd" opacity="0.55" clip-path="url(#tk)"/>
<rect x="60" y="30" width="80" height="60" transform="rotate(15 100 60)" fill="none" stroke="#12355b" stroke-width="2.5"/>
<line x1="56" y1="62" x2="190" y2="62" stroke="#1d6fa5" stroke-width="1.2" stroke-dasharray="5 3"/>
<text x="100" y="14" font-size="9" text-anchor="middle" font-weight="bold" fill="#12355b">tanque parcialmente cheio, com banda</text>
<text x="2" y="52" font-size="7.5" fill="#1d6fa5">superfície</text>
<text x="2" y="60" font-size="7.5" fill="#1d6fa5">livre</text>
<text x="2" y="68" font-size="7" fill="#1d6fa5">(horizontal)</text>
<line x1="128" y1="86" x2="150" y2="94" stroke="#12355b" stroke-width="1.4" marker-end="url(#a2)"/>
<text x="196" y="108" font-size="8" text-anchor="end" fill="#12355b">o líquido corre para o lado da banda</text>
<text x="100" y="118" font-size="8" text-anchor="middle" fill="#b91c1c" font-weight="bold">G efetivo sobe, GM efetivo diminui</text>
</svg>'''

# ------------------------------------------------------------------ lições
lessons = []

lessons.append(dict(
    key="D1", tag="Dia 1", title="Peso, empuxo e deslocamento",
    meta="Programa: II.15 e II.16.8 · Livro: Arte Naval V1 cap. 2 · Vídeo, busque: “princípio de Arquimedes navio flutua” ou “archimedes principle ship floating explained”",
    idea="Um navio flutua porque a água o empurra para cima com uma força igual ao peso dele.",
    pre=[("Um navio de aço pesa milhares de toneladas e flutua. Por quê?", "desloca água de peso igual ao dele"),
         ("Um metro cúbico de água salgada pesa mais ou menos que um de água doce?", "mais (1,025 contra 1,000 t)")],
    body='''<ul>
<li><b>Princípio de Arquimedes:</b> um corpo na água recebe um <b>empuxo</b>, de baixo para cima, igual ao <b>peso da água que ele desloca</b>.</li>
<li>O navio flutua quando o <b>peso dele = empuxo</b>.</li>
<li><b>Deslocamento (Δ):</b> o peso da água que o navio desloca, em toneladas. É igual ao peso do navio, com tudo a bordo.</li>
<li><b>Δ = ρ × ∇</b>: ρ é a densidade da água (<b>salgada ≈ 1,025 t/m³</b>; <b>doce = 1,000 t/m³</b>) e ∇ é o volume submerso (m³).</li>
<li><b>Deslocamento leve:</b> o navio vazio, sem carga, combustível, água e provisões. <b>Deslocamento carregado:</b> no calado máximo.</li>
<li><b>Porte bruto (DWT)</b> = deslocamento carregado − deslocamento leve. É o quanto o navio pode carregar.</li>
</ul>
<div class="box"><p><b>Exemplo resolvido:</b> volume submerso ∇ = 42 000 m³ (o mesmo da Semana 1).<br>
No mar: Δ = 1,025 × 42 000 = <b>43 050 t</b>.<br>
No rio, o peso é o mesmo, então ∇ = 43 050 ÷ 1,000 = <b>43 050 m³</b>: o navio afunda mais. É por isso que o calado cresce em água doce.</p></div>''',
    fig=SVG_ARQ, figh=36,
    memo="Pesa 43 050 t, desloca 43 050 t de água. Peso = empuxo.",
    tab="",
    aord="O deslocamento é a “massa” que o prático precisa mover e parar. Quanto maior, maior a inércia e mais longe o navio vai antes de parar. Por isso ele normalmente consta nas informações de manobra do navio.",
    fey="Explique a um amigo por que um navio de 40 000 toneladas flutua, usando a palavra empuxo.",
    cards=[("Empuxo", "Força de baixo para cima que a água exerce sobre o navio. Igual ao peso da água deslocada."),
           ("Princípio de Arquimedes", "O empuxo é igual ao peso do líquido deslocado pelo corpo."),
           ("Deslocamento (Δ)", "Peso da água deslocada pelo navio, em toneladas. Igual ao peso do navio."),
           ("Fórmula do deslocamento", "Δ = ρ × ∇ (densidade da água × volume submerso)."),
           ("Densidade da água salgada e da doce", "Salgada ≈ 1,025 t/m³; doce = 1,000 t/m³."),
           ("Deslocamento leve", "Peso do navio vazio, sem carga, combustível, água e provisões."),
           ("Deslocamento carregado", "Peso do navio no calado máximo."),
           ("Porte bruto (DWT)", "Deslocamento carregado menos deslocamento leve: o quanto o navio pode carregar.")],
    qs=[("Segundo o princípio de Arquimedes, o empuxo sobre um navio flutuando é igual ao:", ["volume do casco", "peso do líquido que ele desloca", "peso da carga", "calado multiplicado pela boca", "peso do lastro"], 1, "Empuxo = peso do líquido deslocado."),
        ("Volume submerso de 30 000 m³ em água salgada (1,025 t/m³). O deslocamento é:", ["29 268 t", "30 000 t", "30 750 t", "31 250 t", "33 000 t"], 2, "30 000 × 1,025 = 30 750 t."),
        ("O mesmo navio (30 750 t) entra num rio de água doce (1,000 t/m³). O volume submerso passa a ser:", ["29 268 m³", "30 000 m³", "31 500 m³", "30 750 m³", "41 000 m³"], 3, "30 750 ÷ 1,000 = 30 750 m³: mais volume submerso, calado maior."),
        ("Deslocamento carregado de 50 000 t e deslocamento leve de 8 000 t. O porte bruto é:", ["8 000 t", "42 000 t", "50 000 t", "58 000 t", "6,25 t"], 1, "50 000 − 8 000 = 42 000 t."),
        ("Marque a INCORRETA:", ["O deslocamento é medido em toneladas.", "O navio flutua quando seu peso é igual ao empuxo.", "A água doce é mais densa que a água salgada.", "Deslocamento = densidade da água × volume submerso.", "O porte bruto é o deslocamento carregado menos o leve."], 2, "A água SALGADA é mais densa (1,025 contra 1,000).")],
))

lessons.append(dict(
    key="D2", tag="Dia 2", title="Tonelagem: três coisas diferentes",
    meta="Programa: II.15 e II.16.8 (e III.18) · Livro: Arte Naval V1 cap. 2 · Vídeo, busque: “arqueação bruta gross tonnage explained”",
    idea="“Tonelagem” pode ser peso ou volume. Quem confunde erra a prova.",
    pre=[("Arqueação bruta é um peso ou um volume?", "volume"),
         ("A partir de que arqueação bruta a praticagem é obrigatória, em regra?", "acima de 500")],
    body='''<ul>
<li><b>Arqueação bruta (AB; em inglês GT)</b> mede o <b>volume de todos os espaços fechados</b> do navio. É um número <b>sem unidade</b>. Apesar do nome, <b>não é peso</b>.</li>
<li><b>Arqueação líquida (AL; NT)</b> está ligada ao volume dos espaços de carga.</li>
<li>Pela Convenção Internacional de Arqueação (1969): <b>AB = K1 × V</b>, em que V é o volume dos espaços fechados (m³) e <b>K1 = 0,2 + 0,02 × log₁₀(V)</b>.</li>
<li>A AB serve para taxas e regras. Por exemplo, a Lei 14.813/2024 (art. 13, § 6º) torna a praticagem obrigatória em todas as ZP para navios com <b>AB superior a 500</b>, salvo as exceções.</li>
</ul>
<div class="box"><p><b>Exemplo resolvido:</b> V = 100 000 m³.<br>
log₁₀(100 000) = 5, então K1 = 0,2 + 0,02 × 5 = 0,3.<br>
AB = 0,3 × 100 000 = <b>30 000</b>.</p></div>''',
    fig="",
    memo="Peso: deslocamento e porte bruto (toneladas). Volume: arqueação (sem unidade).",
    tab='''<table><tr><th>Grandeza</th><th>O que é</th><th>Unidade</th></tr>
<tr><td>Deslocamento</td><td>quanto o navio pesa agora</td><td>toneladas</td></tr>
<tr><td>Porte bruto</td><td>quanto pode carregar</td><td>toneladas</td></tr>
<tr><td>Arqueação bruta</td><td>quão grande é por dentro (volume)</td><td>sem unidade</td></tr></table>''',
    aord="A AB é um dos dados do navio que dizem se a praticagem é obrigatória (acima de 500, em regra). Já o porte bruto mostra quanto o navio carrega, e o deslocamento, quanto ele pesa no momento.",
    fey="Explique a um amigo a diferença entre deslocamento, porte bruto e arqueação bruta, com um exemplo.",
    cards=[("Arqueação bruta (AB, GT)", "Medida do volume de todos os espaços fechados do navio. Sem unidade. Não é peso."),
           ("Arqueação líquida (AL, NT)", "Medida ligada ao volume dos espaços de carga."),
           ("Fórmula da AB (Convenção de 1969)", "AB = K1 × V, com K1 = 0,2 + 0,02 × log10(V). V é o volume dos espaços fechados em m³."),
           ("Praticagem obrigatória (Lei 14.813, art. 13, § 6º)", "Navios com AB superior a 500, salvo as exceções."),
           ("Quais grandezas são peso?", "Deslocamento e porte bruto, em toneladas."),
           ("Qual grandeza é volume?", "Arqueação (bruta e líquida), sem unidade.")],
    qs=[("A arqueação bruta (AB) é uma medida de:", ["peso do navio em toneladas", "volume dos espaços fechados do navio, sem unidade", "carga máxima transportável", "calado máximo", "área da linha d'água"], 1, "Volume dos espaços fechados, sem unidade."),
        ("Com AB = K1 × V, K1 = 0,2 + 0,02 × log₁₀(V) e V = 100 000 m³, a AB vale:", ["20 000", "25 000", "30 000", "40 000", "100 000"], 2, "log₁₀(100 000) = 5; K1 = 0,3; AB = 30 000."),
        ("Pela Lei 14.813/2024 (art. 13, § 6º), a praticagem é obrigatória, em regra, para navios com arqueação bruta:", ["acima de 100", "acima de 300", "acima de 1 000", "superior a 500", "acima de 10 000"], 3, "Superior a 500, salvo as exceções."),
        ("Qual destas grandezas é um peso, medido em toneladas?", ["arqueação bruta", "deslocamento", "arqueação líquida", "coeficiente de bloco", "boca"], 1, "Deslocamento."),
        ("Marque a INCORRETA:", ["Arqueação bruta é uma medida de volume.", "O porte bruto indica quanto o navio pode carregar.", "O deslocamento é o peso do navio em dado momento.", "A arqueação bruta é o peso do navio em toneladas.", "O porte bruto é medido em toneladas."], 3, "A AB é volume, não peso.")],
))

lessons.append(dict(
    key="D3", tag="Dia 3", title="Flutuabilidade e imersão: quanto afunda ao carregar",
    meta="Programa: II.15 e II.16.8 · Livro: Arte Naval V1 cap. 2 · Vídeo, busque: “reserva de flutuabilidade TPC toneladas por centímetro”",
    idea="Cada tonelada a mais faz o navio afundar um pouco. O TPC diz quanto.",
    pre=[("Se você descarrega o navio, o calado aumenta ou diminui?", "diminui"),
         ("Quando aumenta a borda-livre, a segurança contra afundar aumenta ou diminui?", "aumenta")],
    body='''<ul>
<li><b>Flutuabilidade:</b> a capacidade do navio de flutuar.</li>
<li><b>Reserva de flutuabilidade:</b> o volume <b>estanque</b> do casco <b>acima</b> da linha d'água. Quanto maior a borda-livre, maior a reserva.</li>
<li>A <b>marca de borda-livre</b> (disco de Plimsoll) fica pintada no costado e indica o <b>limite de carregamento</b>.</li>
<li>Carregar o navio aumenta o calado, até que a água deslocada pese o mesmo que o novo peso.</li>
<li><b>TPC</b> (toneladas por centímetro de imersão): o peso que faz o calado variar 1 cm.<br>
<b>TPC = ρ × Aw ÷ 100</b>, em que Aw é a área do plano da linha d'água (m²).</li>
<li>É uma conta aproximada, que supõe o costado reto junto à linha d'água.</li>
</ul>
<div class="box"><p><b>Exemplo resolvido:</b> Aw = 6 000 m², água salgada.<br>
TPC = 1,025 × 6 000 ÷ 100 = <b>61,5 t/cm</b>.<br>
Carregar 615 t aumenta o calado em 615 ÷ 61,5 = <b>10 cm</b>.</p></div>''',
    fig="",
    memo="Mais peso, mais calado. Quantos centímetros? Peso ÷ TPC.",
    tab='''<div class="box key"><p><b>Ligação com a Semana 1:</b> em água doce o calado cresce cerca de 2,5%. A lógica é a mesma: o peso não muda, mas a água é menos densa, então o navio desloca mais volume.</p></div>''',
    aord="O calado muda durante a operação: com a carga, o combustível consumido e a densidade da água. O Comandante informa o calado ao prático (NORMAM-311, art. 2.30.2), que precisa dele para saber quanta água sobra sob a quilha na barra.",
    fey="Explique a um amigo por que um navio com mais carga afunda mais e como se calcula quanto.",
    cards=[("Flutuabilidade", "Capacidade do navio de flutuar."),
           ("Reserva de flutuabilidade", "Volume estanque do casco acima da linha d'água."),
           ("Marca de borda-livre (Plimsoll)", "Marca pintada no costado: limite de carregamento."),
           ("TPC", "Toneladas por centímetro de imersão: peso que muda o calado em 1 cm."),
           ("Fórmula do TPC", "TPC = ρ × Aw ÷ 100 (Aw = área da linha d'água em m²)."),
           ("Quanto o calado muda ao carregar?", "Peso carregado ÷ TPC, em centímetros (aproximado).")],
    qs=[("A reserva de flutuabilidade é:", ["o volume submerso do casco", "o volume estanque do casco acima da linha d'água", "a carga máxima", "o peso do lastro", "o calado médio"], 1, "Volume estanque acima da linha d'água."),
        ("Aw = 5 000 m², em água salgada (1,025 t/m³). O TPC vale:", ["5,1 t/cm", "51,25 t/cm", "512,5 t/cm", "50 t/cm", "5 125 t/cm"], 1, "1,025 × 5 000 ÷ 100 = 51,25 t/cm."),
        ("Um navio com TPC de 51,25 t/cm carrega 512,5 t. O calado aumenta, aproximadamente:", ["1 cm", "5 cm", "10 cm", "50 cm", "100 cm"], 2, "512,5 ÷ 51,25 = 10 cm."),
        ("Para AUMENTAR a reserva de flutuabilidade (mais borda-livre), o navio deve:", ["receber carga", "descarregar peso", "entrar em água doce", "tomar lastro", "aumentar o calado"], 1, "Menos peso, menos calado, mais borda-livre."),
        ("Marque a INCORRETA:", ["Carregar o navio aumenta o calado.", "TPC é o peso que muda o calado em 1 cm.", "Quanto maior a borda-livre, maior a reserva de flutuabilidade.", "A marca de borda-livre indica o limite de carregamento.", "Quanto maior a borda-livre, menor a reserva de flutuabilidade."], 4, "Mais borda-livre, MAIS reserva.")],
))

lessons.append(dict(
    key="D4", tag="Dia 4", title="Estabilidade: G, B, M e GM",
    meta="Programa: II.32 · Livro: Hensen e van der Laan, Estabilidade dos rebocadores, cap. 2 (Drive) · Vídeo, busque: “ship stability GM explained”",
    idea="Para não virar, o peso e o empuxo precisam formar um par de forças que endireite o navio.",
    pre=[("O peso do navio age no centro de gravidade ou no de carena?", "gravidade (G)"),
         ("Inclinado, o navio estável tende a voltar ou a virar?", "voltar")],
    body='''<ul>
<li><b>G</b>: centro de gravidade; o <b>peso</b> age para baixo em G. <b>K</b> é a quilha (referência das alturas).</li>
<li><b>B</b>: centro de carena (o livro diz “centro de flutuação, COB”), o centro do volume submerso; o <b>empuxo</b> age para cima em B.</li>
<li>Com <b>banda</b>, <b>B vai para o lado que afunda</b>: peso e empuxo ficam em linhas verticais diferentes e formam um par. O braço do par é o <b>GZ</b> (braço de endireitamento), que tende a trazer o navio ao <b>adriçado</b> (vertical).</li>
<li><b>M</b>: metacentro (inicial), onde a vertical do empuxo cruza a linha de centro. Para pequenos ângulos é considerado fixo.</li>
<li><b>GM</b> (altura metacêntrica): distância de G a M. <b>M acima de G (GM &gt; 0): estável</b>; GM maior, mais estabilidade; GM negativo: instável.</li>
<li>Pequenos ângulos: <b>GZ ≈ GM × sen(banda)</b>. Alturas a partir da quilha: <b>GM = KM − KG</b>.</li>
</ul>''',
    fig=SVG_GM, figh=36,
    tab='''<div class="box"><p><b>Exemplo:</b> KM = 9,5 m e KG = 8,2 m: GM = <b>1,3 m</b>. Com banda de 10°, GZ ≈ 1,3 × 0,174 ≈ <b>0,23 m</b>.</p></div>''',
    memo="G puxa para baixo, B empurra para cima, GZ endireita. GM positivo = estável. GM grande: balanço brusco; GM pequeno: balanço lento. Só vale para pequenos ângulos (banda grande: curva de estabilidade e ângulo de alagamento).",
    aord="O prático não calcula o GM, mas percebe: navio que balança devagar e demora a voltar da banda pode ter GM baixo. Vale avisar o comandante.",
    fey="Explique a um amigo, com um desenho, por que um navio estável volta à posição vertical depois de inclinar.",
    cards=[("G (centro de gravidade)", "Ponto onde o peso do navio age, para baixo."),
           ("B (centro de carena, COB)", "Centro do volume submerso; ponto onde o empuxo age, para cima."),
           ("M (metacentro inicial)", "Ponto onde a vertical do empuxo cruza a linha de centro (pequenos ângulos)."),
           ("GM (altura metacêntrica)", "Distância de G a M. GM positivo: estável. Maior GM, mais estabilidade."),
           ("GM = ?", "GM = KM − KG (K = quilha, referência das alturas)."),
           ("GZ (braço de endireitamento)", "Braço do par peso-empuxo. GZ ≈ GM × sen(banda), para pequenos ângulos."),
           ("GM grande x GM pequeno (balanço)", "GM grande: balanço curto e brusco. GM pequeno: balanço lento, ângulos grandes."),
           ("Ângulo de alagamento", "Banda em que a água passa a entrar por aberturas do casco.")],
    qs=[("O ponto G é o:", ["centro de carena", "centro de gravidade, onde atua o peso", "metacentro", "centro da linha d'água", "ponto da quilha"], 1, "G = centro de gravidade."),
        ("O centro de carena (B, ou COB) é o centro do:", ["peso do navio", "convés", "volume submerso, onde atua o empuxo", "tanque de lastro", "casco emerso"], 2, "Centro do volume submerso."),
        ("Para pequenos ângulos, o navio é estável quando:", ["G está acima de M", "GM é negativo", "GM é zero", "GM é positivo (M acima de G)", "B está acima de M"], 3, "GM positivo."),
        ("KM = 9,5 m e KG = 8,2 m. A altura metacêntrica GM vale:", ["0,8 m", "1,3 m", "1,7 m", "8,2 m", "17,7 m"], 1, "9,5 − 8,2 = 1,3 m."),
        ("Marque a INCORRETA:", ["GZ é o braço de endireitamento.", "Para pequenos ângulos, GZ ≈ GM × sen(banda).", "GM maior significa mais estabilidade inicial.", "Se G está acima de M, o navio volta sozinho à posição vertical.", "O GM só vale para pequenos ângulos de inclinação."], 3, "Com G acima de M (GM negativo) o navio é instável: não volta.")],
))

lessons.append(dict(
    key="D5", tag="Dia 5", title="O que mexe na estabilidade: carga, superfície livre e banda",
    meta="Programa: II.32 · Livro: Hensen e van der Laan, Estabilidade dos rebocadores, cap. 2 (arquivo no Drive) · Vídeo, busque: “free surface effect ship stability” ou “efeito de superfície livre”",
    idea="O GM muda a cada carregamento. Quem sobe o G perde estabilidade.",
    pre=[("Colocar carga pesada no convés sobe ou desce o G?", "sobe"),
         ("Num tanque só meio cheio, o líquido fica parado quando o navio inclina?", "não, corre para o lado da banda")],
    body='''<ul>
<li><b>G sobe, GM diminui:</b> carga pesada ou água no convés, gelo, tanques vazios no fundo. O GM pode até ficar negativo. <b>G desce, GM aumenta:</b> lastro baixo, carga pesada no porão inferior.</li>
<li><b>Superfície livre:</b> líquido num tanque <b>parcialmente cheio</b> corre para o lado da banda. O efeito é como subir o G: o <b>GM efetivo diminui</b>.</li>
<li>Tanque <b>cheio</b> ou <b>vazio</b> não tem superfície livre. O efeito cresce com o cubo da largura do tanque, por isso se evitam tanques parcialmente cheios.</li>
<li><b>Banda temporária:</b> vento de través, guinada (o navio inclina para fora da curva), força do cabo de reboque. Some quando a causa some.</li>
<li><b>Banda permanente:</b> carga ou tanques mal distribuídos. Não some sozinha.</li>
</ul>''',
    fig=SVG_FSE,
    memo="G sobe = GM cai. Superfície livre = G “virtual” sobe, sem a carga mudar de lugar. Temporária some; permanente fica.",
    tab="",
    aord="Um rebocador puxado de través pelo cabo, com força alta, pode ser virado (emborcamento, ou girting): a força transversal no cabo aumenta a banda e muda a estabilidade a cada instante. O tema volta quando estudarmos rebocadores.",
    fey="Explique a um amigo por que um tanque meio cheio é mais perigoso que um tanque cheio.",
    cards=[("G sobe: o que acontece ao GM?", "O GM diminui (menos estabilidade)."),
           ("O que faz o G subir?", "Carga pesada ou água no convés, gelo, tanques vazios no fundo."),
           ("O que faz o G descer?", "Lastro baixo, carga pesada no porão inferior."),
           ("Efeito de superfície livre", "Líquido em tanque parcialmente cheio corre para o lado da banda e reduz o GM efetivo."),
           ("Tanque sem efeito de superfície livre", "Tanque totalmente cheio ou totalmente vazio."),
           ("Banda temporária x permanente", "Temporária: vento, guinada, cabo; some com a causa. Permanente: carga ou tanques mal distribuídos."),
           ("Emborcamento (girting) de rebocador", "Risco de virar por força transversal alta no cabo de reboque.")],
    qs=[("O líquido num tanque parcialmente cheio (superfície livre) faz o GM efetivo:", ["aumentar", "diminuir", "não mudar", "dobrar", "ficar sempre negativo"], 1, "Reduz o GM efetivo."),
        ("Passar carga pesada do porão para o convés faz o G:", ["descer e o GM aumentar", "subir e o GM diminuir", "ficar igual", "subir e o GM aumentar", "descer e o GM diminuir"], 1, "G sobe, GM diminui."),
        ("Qual tanque NÃO tem efeito de superfície livre?", ["parcialmente cheio e largo", "parcialmente cheio e estreito", "totalmente cheio", "com 50% de nível", "com 30% de nível"], 2, "Tanque totalmente cheio (ou vazio)."),
        ("Banda causada por vento de través, que some quando o vento cessa, é banda:", ["permanente", "negativa", "de lastro", "temporária", "de superfície livre"], 3, "Temporária."),
        ("Marque a INCORRETA:", ["Quanto mais largo o tanque parcial, maior o efeito de superfície livre.", "Lastro baixo diminui o G e aumenta o GM.", "Na guinada, o navio inclina para fora da curva.", "Banda permanente pode vir de carga mal distribuída.", "Mais tanques parcialmente cheios aumentam a estabilidade."], 4, "Tanques parciais REDUZEM a estabilidade.")],
))

# ------------------------------------------------------------------ teste
test_qs = [
 ("“O empuxo é igual ao peso do líquido deslocado.” Esse é o princípio de:", ["Bernoulli", "Arquimedes", "Froude", "Plimsoll", "Nomoto"], 1, "Arquimedes."),
 ("Volume submerso de 40 000 m³ em água salgada (1,025 t/m³). O deslocamento é:", ["39 024 t", "40 000 t", "41 000 t", "42 000 t", "45 000 t"], 2, "40 000 × 1,025 = 41 000 t."),
 ("Deslocamento carregado de 90 000 t e deslocamento leve de 15 000 t. O porte bruto é:", ["15 000 t", "75 000 t", "90 000 t", "105 000 t", "6 t"], 1, "90 000 − 15 000 = 75 000 t."),
 ("A arqueação bruta mede:", ["o peso do navio", "a carga transportável", "o calado máximo", "o volume dos espaços fechados", "a densidade da água"], 3, "Volume dos espaços fechados."),
 ("V = 10 000 m³; AB = K1 × V com K1 = 0,2 + 0,02 × log₁₀(V). A AB vale:", ["2 000", "2 800", "3 000", "4 000", "10 000"], 1, "log₁₀ = 4; K1 = 0,28; AB = 2 800."),
 ("Aw = 6 000 m² em água salgada (1,025 t/m³). O TPC vale:", ["6,15 t/cm", "30,75 t/cm", "61,5 t/cm", "615 t/cm", "6 150 t/cm"], 2, "1,025 × 6 000 ÷ 100 = 61,5 t/cm."),
 ("O centro de carena (B) é o ponto de aplicação do:", ["peso", "empuxo", "TPC", "deslocamento leve", "GM"], 1, "Empuxo (centro do volume submerso)."),
 ("KM = 10,1 m e KG = 9,0 m. O GM vale:", ["0,9 m", "1,1 m", "1,9 m", "9,0 m", "19,1 m"], 1, "10,1 − 9,0 = 1,1 m."),
 ("O efeito de superfície livre:", ["aumenta o GM efetivo", "só ocorre em tanques cheios", "não altera a estabilidade", "diminui o GM efetivo", "só ocorre em água doce"], 3, "Diminui o GM efetivo."),
 ("Marque a INCORRETA:", ["GM positivo indica estabilidade inicial.", "Arqueação bruta é medida de volume.", "O porte bruto é o peso do navio vazio.", "Carregar o navio aumenta o calado.", "Lastro baixo aumenta o GM."], 2, "O porte bruto é a capacidade de carga; o peso do navio vazio é o deslocamento leve."),
]

# ------------------------------------------------------------------ HTML
parts = []
parts.append('''<section class="first cover">
<span class="tag">Semana 2</span>
<h1>Flutuar<br>e não virar</h1>
<p class="big">Deslocamento, tonelagem e estabilidade</p>
<div class="box key"><p><b>Como usar:</b> uma lição por dia, na ordem. Gabarito no fim.</p>
<p><b>Calendário:</b> S2 = 27/10 a 02/11. Se começou depois, siga a sequência e mantenha o domingo livre.</p></div>
<h3>Roteiro</h3>
<p class="small">Dia 1 peso, empuxo e deslocamento · Dia 2 tonelagem · Dia 3 flutuabilidade e TPC · Dia 4 estabilidade (G, B, M, GM) · Dia 5 o que mexe na estabilidade · Revisão e teste · Gabarito</p>
<p class="tiny">Cartões da semana: arquivo .csv (Noji). Exercícios: 5 por dia, com consulta.</p>
</section>''')

parts.append('''<section class="pg">
<span class="tag">Antes de começar · 5 min</span>
<h2>Revisão rápida da Semana 1</h2>
<p class="small">Responda de memória. Se travar, volte ao PDF da Semana 1 ou aos cards.</p>
<ol class="small">
<li>Qual é a cor da luz de bombordo?</li>
<li>O que é o calado? E a borda-livre?</li>
<li>Como se calcula o coeficiente de bloco?</li>
<li>Qual é a rotação em torno do eixo vertical?</li>
<li>Em água doce, o calado aumenta ou diminui? Por quê?</li>
</ol>
<div class="box key"><p>Respostas: vermelha; calado = linha d'água até a quilha, borda-livre = linha d'água até o convés; Cb = volume submerso ÷ (Lpp × B × T); guinada (yaw); aumenta, porque a água doce é menos densa e o navio desloca mais volume.</p></div>
<h3>O que esta semana resolve</h3>
<p class="small">Na Semana 1 você aprendeu <b>onde</b> o navio está na água. Agora aprende <b>por que</b> ele flutua e <b>por que não vira</b>. Essas duas ideias voltam em manobrabilidade, rebocadores e fundeio.</p>
</section>''')

answers = []
for ls in lessons:
    pre = " ".join(f'<b>{i}.</b> {esc(q)} <span class="tiny">(resposta: {esc(a)})</span>' for i, (q, a) in enumerate(ls["pre"], start=1))
    fig = ('<div>' + ls["fig"].replace('<svg ', f'<svg style="max-height:{ls.get("figh", 44)}mm" ', 1) + '</div>') if ls["fig"] else ""
    parts.append(f'''<section class="pg">
<span class="tag">{esc(ls["tag"])}</span>
<h2>{esc(ls["title"])}</h2>
<p class="meta">{esc(ls["meta"])}</p>
<div class="box key"><p><b>Ideia do dia:</b> {esc(ls["idea"])}</p></div>
<p class="small"><b>Antes de ler (chute):</b> {pre}</p>
<h3>A lição</h3>
{ls["body"]}
{fig}
{ls["tab"]}
<div class="box"><p><b>Lembre assim:</b> {esc(ls["memo"])}</p></div>
<div class="box warn"><p><b>A bordo:</b> {esc(ls["aord"])}</p></div>
</section>''')
    cards = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in ls["cards"])
    qhs, ans = [], []
    for n, (t, o, a, why) in enumerate(ls["qs"], start=1):
        h, letter = question(n, t, o, a)
        qhs.append(h); ans.append((n, letter, why))
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
{"".join(qhs)}
</section>''')

qh, ans = "", []
for n, (t, o, a, why) in enumerate(test_qs, start=1):
    h, letter = question(n, t, o, a)
    qh += h; ans.append((n, letter, why))
answers.append(("Revisão e teste", "Teste da semana", ans))
parts.append('''<section class="pg">
<span class="tag">Revisão · segunda</span>
<h2>Revise e teste</h2>
<h3>Passo a passo (2h)</h3>
<ol class="small">
<li><b>Desenhe de memória</b> o navio flutuando (peso em G, empuxo em B) e o navio inclinado, com G, B, M e GZ (20 min). Compare com as figuras.</li>
<li><b>Cards</b> das Semanas 1 e 2 (20 min).</li>
<li><b>Releia</b> só as lições em que se sentiu inseguro (30 min).</li>
<li><b>Teste de 10 questões</b>, sem consultar, no ritmo da prova: 2 min por questão (próxima página).</li>
<li><b>Corrija</b> pelo gabarito e anote os erros no caderno, com a causa A, B ou C (20 min).</li>
</ol>
<div class="box"><p><b>Meta:</b> 7 ou mais acertos para avançar à Semana 3. Menos que isso: refaça as lições dos erros antes da nova.</p></div>
</section>
<section class="pg">
<span class="tag">Revisão · teste</span>
<h2>Teste da semana: 10 questões</h2>''' + qh + '</section>')

g = '<section class="pg"><span class="tag">Gabarito comentado</span><h2>Respostas</h2><p class="tiny">Só confira depois de tentar.</p>'
for tag, title, ans in answers:
    g += f'<h3>{esc(tag)}: {esc(title)}</h3><table>'
    for n, letter, why in ans:
        g += f'<tr><td style="width:12%"><b>{n}</b></td><td style="width:12%"><b>{letter.upper()}</b></td><td>{esc(why)}</td></tr>'
    g += '</table>'
g += '</section>'
parts.append(g)

doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>PSCPP – Semana 2</title>
<link rel="stylesheet" href="base.css"><link rel="stylesheet" href="s2.css"></head><body>{"".join(parts)}</body></html>'''
(OUT / "semana2.html").write_text(doc, encoding="utf-8")

rows = []
for ls in lessons:
    rows += list(ls["cards"])
with open(OUT / "PSCPP-cartoes-Noji-semana2.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for a, b in rows:
        w.writerow([a, b])
print(len(rows), "cartões;", sum(len(l["qs"]) for l in lessons) + len(test_qs), "questões")
