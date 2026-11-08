# RDP — Área de Trabalho Remota do Windows

Protocolo nativo e eficiente da Microsoft. O **host** (quem é controlado) precisa ser **Windows Pro, Enterprise ou Education** — o Windows **Home não** pode ser host de RDP. O **client** pode ser qualquer coisa: app "Remote Desktop" da Microsoft em Windows, macOS, Android, iOS, ou clientes como FreeRDP/Remmina no Linux.

## 1. Habilitar o RDP no host (Windows Pro+)
1. Configurações → **Sistema** → **Área de Trabalho Remota** → ative **"Área de Trabalho Remota"**.
2. Anote o **nome do PC** (Configurações → Sistema → Sobre → "Nome do dispositivo").
3. Garanta que sua conta tem senha. Em "Usuários", adicione quais contas podem conectar, se necessário.
4. Deixe o PC configurado para **não suspender** quando quiser acesso (Energia → Suspender = Nunca na tomada).

## 2. Conectar na **mesma rede local** (LAN) — simples e seguro
1. Descubra o **IP local** do host: `ipconfig` no CMD (ex.: `192.168.0.42`).
2. No client, abra o app **Remote Desktop** (ou "Conexão de Área de Trabalho Remota" / `mstsc` no Windows).
3. Digite o IP (ou o nome do PC) → informe usuário e senha → conecta.

Na LAN, o RDP já é a melhor experiência. Não precisa abrir nada no roteador.

## 3. Conectar pela **internet** — fazer do jeito seguro

⚠️ **Nunca** exponha a porta RDP (3389) direto na internet via port forwarding simples. RDP aberto é alvo constante de ataques de força bruta e de exploits (BlueKeep etc.). Use uma destas camadas:

### Opção recomendada: Tailscale (ou VPN) por cima
1. Instale **Tailscale** no host e no client (ver `ssh-tailscale.md`), ambos na mesma conta.
2. No client, conecte-se ao host pelo **IP Tailscale** (100.x.y.z) no app de RDP.
3. A porta RDP nunca fica exposta à internet pública — só é alcançável dentro da rede Tailscale.

### Alternativa corporativa: RD Gateway
- Em empresa, use um **Remote Desktop Gateway** administrado pela TI. Não monte isso por conta própria em ambiente de trabalho sem a TI.

### Se realmente precisar de port forwarding (último recurso)
- Mude a porta padrão (não resolve sozinho, mas reduz ruído).
- **Restrinja por IP de origem** no firewall.
- Exija **NLA (Network Level Authentication)** — já vem ligado; mantenha.
- Senha forte + **bloqueio de conta** após tentativas.
- Mantenha o Windows **atualizado**.
- Ainda assim: prefira VPN/Tailscale. Port forwarding de RDP é desencorajado.

## 4. Ajustes úteis
- **NLA** (Network Level Authentication): mantenha ativado (exige autenticação antes de abrir a sessão).
- **Multi-monitor**: no `mstsc`, aba "Exibir" → "Usar todos os monitores".
- **Som, área de transferência, impressoras, pastas**: aba "Recursos Locais" para redirecionar.
- Encerre com **logoff** (não só fechar a janela) para liberar a sessão.

## Problemas comuns
- **"Sua edição do Windows não suporta"**: o host é Windows **Home** → RDP como host não está disponível. Use Chrome Remote Desktop/AnyDesk, ou faça upgrade para Pro.
- **Não conecta pela internet**: provavelmente certo — não deveria mesmo, sem VPN/Tailscale. Monte o Tailscale.
- **Credenciais recusadas com NLA**: use `DOMÍNIO\usuário` ou `nomedoPC\usuário`; confirme a senha; conta local precisa ter senha.
- **Firewall bloqueia**: garanta a regra "Área de Trabalho Remota" liberada no Firewall do Windows (perfil de rede correto: Privada).
- **Sessão desconecta ao suspender**: ajuste as opções de energia do host.
