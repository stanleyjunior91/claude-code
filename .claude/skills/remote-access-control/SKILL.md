---
name: remote-access-control
description: Guia prático para configurar, usar e solucionar problemas de ferramentas legítimas de acesso e controle remoto (controlar um PC de longe, área de trabalho remota, shell remoto) nos equipamentos do próprio usuário ou em máquinas que ele está autorizado a administrar. Cobre Chrome Remote Desktop, AnyDesk, TeamViewer, RDP (Área de Trabalho Remota do Windows), VNC, SSH e Tailscale, com foco em segurança. Use quando o usuário quiser controlar/acessar um computador remotamente, montar área de trabalho remota, acessar a máquina de casa/trabalho pelo celular ou por outro PC, escolher entre as ferramentas, configurar acesso desassistido, ou resolver falhas de conexão. NÃO use para obter acesso a máquinas de terceiros sem autorização, para esconder a conexão do dono do equipamento, nem para contornar controles de segurança.
---

# Acesso e controle remoto

Esta skill ajuda o usuário a montar e operar acesso remoto **legítimo** às próprias máquinas (ou a máquinas que ele administra com autorização): controlar a área de trabalho de longe, abrir um shell remoto, acessar o PC de casa pelo celular etc.

Responda em português quando o usuário falar português. Mantenha em inglês os termos técnicos das ferramentas (host, client, unattended access, port forwarding).

## Regra de escopo — leia antes de ajudar

Ajude apenas quando a conexão for a um equipamento que o usuário **possui ou tem autorização clara para administrar**. Sinais de que está tudo certo: ele quer acessar "meu PC", "minha máquina de casa", "o notebook do trabalho que eu administro".

**Recuse e explique**, sem dar o passo a passo, se o pedido for para:
- acessar uma máquina de terceiro sem o consentimento do dono;
- instalar acesso remoto de forma **oculta**, que o dono/usuário do equipamento não veja (backdoor, "modo invisível", sem ícone na bandeja, sem aviso de sessão);
- **contornar** senha de login, bloqueio de tela, antivírus, EDR ou política de TI;
- manter acesso de forma persistente a um equipamento que deixou de ser do usuário (ex.: PC de um emprego anterior).

Na dúvida sobre a autorização, **pergunte de quem é a máquina** antes de prosseguir. Acesso remoto consentido e visível é legítimo; acesso oculto ou sem permissão não é — a diferença não está na ferramenta, está em quem autorizou e em quem consegue ver a sessão.

## O que esta sessão do Claude NÃO faz

Deixe isto claro quando for relevante: **o Claude (esta sessão) não assume o controle da tela/mouse do computador do usuário.** Esta skill é um **guia de configuração** das ferramentas de acesso remoto, que são softwares independentes (Chrome Remote Desktop, AnyDesk etc.). Quem controla a máquina é o próprio usuário, a partir de outro dispositivo, usando essas ferramentas.

(O recurso *Remote Control* do Claude Code conecta uma sessão a **uma pasta** autorizada para tarefas de código — isso é outra coisa, não é controle da área de trabalho. Se for o caso, oriente pelo app de desktop: Settings → Claude Code → Remote Control.)

## Como conduzir

1. **Descubra o cenário** com 2–3 perguntas rápidas, se ainda não souber:
   - Sistema da máquina a controlar (o *host*): Windows, macOS ou Linux?
   - De onde vai acessar (o *client*): celular (Android/iOS), outro PC, navegador?
   - Tela gráfica ou só terminal/linha de comando?
   - Mesma rede (Wi-Fi/LAN) ou pela internet?
   - Precisa de **acesso desassistido** (entrar sem alguém aprovar do outro lado) ou alguém estará na máquina para aceitar?

2. **Recomende uma ferramenta** usando `references/escolha.md`. Dê **uma** recomendação principal e o porquê, não um catálogo.

3. **Dê o passo a passo** do arquivo de referência correspondente, adaptado ao SO e ao dispositivo do usuário.

4. **Feche com segurança**: aplique o checklist de `references/seguranca.md` (senha/PIN forte, 2FA, atualizar, limitar acesso, encerrar sessão).

## Arquivos de referência

| Arquivo | Quando ler |
|---|---|
| `references/escolha.md` | Sempre, para recomendar a ferramenta certa ao cenário (tabela de decisão + prós/contras) |
| `references/chrome-remote-desktop.md` | Opção mais simples e grátis, multiplataforma, pelo navegador |
| `references/anydesk-teamviewer.md` | Controle de tela com mais recursos; acesso desassistido; suporte a terceiros |
| `references/windows-rdp.md` | Área de Trabalho Remota nativa do Windows Pro/Enterprise (melhor desempenho em rede/VPN) |
| `references/vnc.md` | VNC (RealVNC, TightVNC, macOS Screen Sharing); multiplataforma, mais manual |
| `references/ssh-tailscale.md` | Terminal remoto (SSH) e rede privada segura (Tailscale/WireGuard) para acesso pela internet sem abrir portas |
| `references/seguranca.md` | Sempre no fim: checklist de segurança e endurecimento; o que nunca fazer |

## Recomendações rápidas (atalho)

- **"Só quero algo simples e grátis, pelo navegador"** → Chrome Remote Desktop.
- **"Quero controlar meu PC pelo celular, fácil"** → Chrome Remote Desktop ou AnyDesk.
- **"Dar suporte ao PC de um parente"** → AnyDesk ou TeamViewer (com a pessoa presente para aprovar).
- **"Tenho Windows Pro e quero o melhor desempenho"** → RDP, de preferência sobre uma VPN ou Tailscale.
- **"Só preciso de terminal/linha de comando"** → SSH.
- **"Acessar pela internet sem abrir portas no roteador"** → Tailscale (e por cima dele: RDP, VNC ou SSH).
