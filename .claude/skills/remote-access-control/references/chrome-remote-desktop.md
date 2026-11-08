# Chrome Remote Desktop (CRD)

Opção mais simples e grátis. Funciona por conta Google; client via navegador (qualquer SO) ou app móvel (Android/iOS). Dois modos: **acesso remoto** (à própria máquina, desassistido com PIN) e **suporte remoto** (compartilhar com outra pessoa via código único).

Site: `remotedesktop.google.com`

## Pré-requisitos
- Conta Google (de preferência com **2FA** ativado).
- No **host** (máquina a ser controlada): navegador Google Chrome (ou Edge/Chromium) instalado.

## Configurar acesso à própria máquina (desassistido)

**No host (a máquina que você vai controlar):**
1. Abra o Chrome e vá em `remotedesktop.google.com/access`.
2. Em **"Configurar acesso remoto"**, clique no ícone de download para instalar o complemento **Chrome Remote Desktop Host**.
3. Dê um **nome** à máquina.
4. Defina um **PIN de 6+ dígitos** (não óbvio; ver `seguranca.md`).
5. Autorize as permissões do SO:
   - **macOS**: System Settings → Privacy & Security → Accessibility e Screen Recording → habilite o Chrome Remote Desktop.
   - **Windows**: aprove o UAC durante a instalação.
   - **Linux**: pode exigir configurar uma sessão de desktop virtual (ver "Notas Linux" abaixo).
6. Deixe a máquina **ligada** e **sem suspender** enquanto quiser acessá-la (ver dica de energia no fim).

**No client (de onde você acessa):**
1. Acesse `remotedesktop.google.com/access` logado **na mesma conta Google**, ou abra o app **Chrome Remote Desktop** (Android/iOS).
2. Selecione a máquina na lista → digite o **PIN** → conecta.

## Suporte remoto (ajudar outra pessoa, com ela presente)

**Na máquina de quem recebe ajuda:**
1. Vá em `remotedesktop.google.com/support`.
2. Em **"Receber suporte"**, gere um **código de acesso** (válido por poucos minutos) e passe para quem vai ajudar.

**Na máquina de quem ajuda:**
1. Em `remotedesktop.google.com/support`, aba **"Dar suporte"**, digite o código.
2. A pessoa do outro lado precisa **clicar em compartilhar/aprovar**. A sessão fica visível pra ela o tempo todo.

## Notas por SO

- **Windows**: funciona no Home e no Pro. Em multi-monitor, use o seletor de telas na barra do CRD.
- **macOS**: é obrigatório conceder **Acessibilidade** e **Gravação de Tela** ao Chrome Remote Desktop, senão a tela aparece preta ou o controle não funciona.
- **Linux**: o suporte é mais sensível; costuma exigir configurar uma sessão (`~/.chrome-remote-desktop-session`) e pacotes do ambiente gráfico. Em algumas distros é preciso criar uma sessão virtual separada. Se der trabalho, prefira VNC + Tailscale no Linux.

## Dicas de energia (para acesso desassistido)
- Windows: Configurações → Sistema → Energia → "Suspender" = Nunca (ao menos quando conectado à tomada).
- macOS: System Settings → Energy/Battery → impeça o sleep automático quando na tomada ("Prevent automatic sleeping when the display is off").
- Se a máquina suspender, o CRD cai até ela voltar.

## Problemas comuns
- **Tela preta (macOS)**: faltou permissão de Gravação de Tela. Conceda e reinicie o Chrome.
- **Máquina não aparece na lista**: confira se está logado na **mesma** conta Google nos dois lados e se o host está ligado/online.
- **"Autorização expirada" / desconecta sozinho**: reautentique no host; verifique se o Chrome do host está atualizado e rodando.
- **Entrada de teclado/atalhos não passa**: use o teclado virtual do app móvel, ou o menu do CRD para enviar Ctrl+Alt+Del.
