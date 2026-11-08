# VNC

Protocolo aberto de controle de tela, multiplataforma. Implementações comuns: **RealVNC** (fácil, com conta e relay), **TightVNC**/**TigerVNC**/**UltraVNC** (Windows/Linux), e o **Compartilhamento de Tela** nativo do macOS (que é VNC). Bom para Linux e ambientes mistos. Exige mais cuidado com criptografia e com atravessar o roteador do que as opções "com nuvem".

## macOS — Compartilhamento de Tela nativo
**No host (Mac a ser controlado):**
1. System Settings → **General → Sharing** → ative **Screen Sharing**.
2. Em "Allow access for", escolha os usuários permitidos.
3. Anote o endereço mostrado (ex.: `vnc://192.168.0.30` ou o nome `.local`).

**No client:**
- Outro Mac: Finder → **Ir → Conectar ao servidor** → `vnc://IP-do-host`.
- Qualquer SO: use um VNC viewer (ex.: RealVNC Viewer) apontando para o IP.

## Linux
**Host com GNOME:** Configurações → **Compartilhamento** → **Compartilhamento de tela remota** (usa VNC). Defina senha.
**Servidores/headless:** instale `tigervnc-standalone-server`, crie a senha com `vncpasswd` e inicie `vncserver :1` (abre o display :1 na porta 5901). Para desktop completo, configure o `~/.vnc/xstartup` com o ambiente gráfico.

**Client:** qualquer VNC viewer (RealVNC Viewer, Remmina, TigerVNC viewer) apontando para `IP:porta` (porta 5900 + número do display).

## Windows
- Instale **TightVNC**/**UltraVNC** (servidor no host) ou **RealVNC** (Server no host, Viewer no client).
- Defina **senha de acesso** forte na configuração do servidor.
- O RealVNC facilita acesso pela internet via conta/cloud; TightVNC/UltraVNC são mais LAN-first.

## Acesso pela internet com VNC — o ponto crítico
VNC puro **não é fortemente criptografado** em todas as implementações e **não deve** ser exposto direto na internet. Faça assim:

1. **Preferir Tailscale/VPN** (ver `ssh-tailscale.md`): conecte o viewer ao **IP Tailscale** do host. Simples e seguro.
2. **Ou túnel SSH**: encaminhe a porta VNC por dentro do SSH:
   ```
   ssh -L 5901:localhost:5901 usuario@host
   ```
   e aponte o viewer para `localhost:5901`. Assim o tráfego VNC viaja criptografado dentro do SSH.
3. **RealVNC com conta** faz o relay criptografado por você (mais fácil, porém depende do serviço deles).

**Evite** abrir a porta 5900/5901 no roteador sem túnel/VPN.

## Segurança
- Senha de VNC forte (algumas implementações limitam o tamanho — mais um motivo para usar túnel/VPN por cima).
- Habilite criptografia na implementação que tiver (RealVNC, UltraVNC com plugin).
- Restrinja por IP quando possível.
- Encerre a sessão do servidor VNC quando não estiver usando (`vncserver -kill :1` no Linux).

## Problemas comuns
- **Tela preta / sem sessão (Linux headless)**: o `xstartup` não subiu um ambiente gráfico; configure-o.
- **Cores/lentidão**: baixe a profundidade de cor e a qualidade no viewer.
- **Não conecta pela internet**: esperado sem túnel/VPN — monte Tailscale ou use `ssh -L`.
- **macOS pede permissão**: conceda Screen Recording ao processo, se solicitado.
