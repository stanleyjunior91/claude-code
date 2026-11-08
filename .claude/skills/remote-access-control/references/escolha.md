# Escolha da ferramenta

Dê **uma** recomendação principal pro cenário do usuário. Esta tabela mapeia cenário → ferramenta.

## Tabela de decisão

| Cenário | Recomendação | Por quê |
|---|---|---|
| Quero o mais simples, grátis, sem instalar quase nada | **Chrome Remote Desktop** | Roda pelo navegador/conta Google; config em minutos; multiplataforma |
| Controlar meu PC pelo celular | **Chrome Remote Desktop** ou **AnyDesk** | Apps bons em Android/iOS; baixa latência |
| Dar suporte pontual a um parente/amigo | **AnyDesk** ou **TeamViewer** | A pessoa só abre o app e passa o ID/código; sessão aprovada na hora |
| Windows Pro/Enterprise, melhor desempenho | **RDP** (Área de Trabalho Remota) | Nativo, protocolo eficiente; ideal em LAN ou sobre VPN/Tailscale |
| Só preciso de terminal / linha de comando | **SSH** | Leve, seguro, padrão da indústria |
| Acessar pela internet sem mexer no roteador | **Tailscale** (+ RDP/VNC/SSH por cima) | Cria rede privada criptografada; dispensa abrir portas |
| Linux ↔ Linux/macOS com tela | **VNC** ou **Chrome Remote Desktop** | VNC é padrão em Linux; CRD é mais fácil |
| Ambiente corporativo com política de TI | Falar com a **TI** e usar a solução deles | Evita violar política; TI pode já ter VPN/RDP/Jump host |

## Comparativo rápido

### Chrome Remote Desktop
- ✅ Grátis, simples, Windows/macOS/Linux/ChromeOS; client por navegador ou app móvel.
- ✅ Acesso desassistido com PIN; usa a conta Google (2FA herdado).
- ➖ Menos recursos (sem transferência de arquivos robusta, sem multi-monitor avançado em alguns casos).
- Melhor para: uso pessoal, acesso à própria máquina.

### AnyDesk / TeamViewer
- ✅ Rápidos, multiplataforma, transferência de arquivos, chat, multi-monitor.
- ✅ Acesso desassistido (senha fixa) e assistido (ID + aprovação na hora).
- ➖ Grátis só para uso pessoal; uso comercial é pago. TeamViewer às vezes acusa "uso comercial" por engano.
- Melhor para: suporte remoto, controle cheio de recursos.

### RDP (Área de Trabalho Remota do Windows)
- ✅ Nativo no Windows **Pro/Enterprise** (não vem no Home como host), protocolo muito eficiente.
- ✅ Ótimo em LAN; excelente desempenho.
- ➖ Expor RDP direto na internet é arriscado — use **sempre** VPN/Tailscale ou RD Gateway. Config de acesso externo é mais técnica.
- Melhor para: quem tem Windows Pro e quer desempenho, em rede local ou sobre VPN.

### VNC (RealVNC, TightVNC, TigerVNC, macOS Screen Sharing)
- ✅ Multiplataforma, padrão aberto; macOS tem "Compartilhamento de Tela" nativo (é VNC).
- ➖ Mais manual; precisa cuidar de criptografia e de como atravessar o roteador (preferir via VPN/Tailscale).
- Melhor para: Linux, macOS, ambientes mistos.

### SSH
- ✅ Leve, criptografado, padrão para terminal remoto; port forwarding e túneis.
- ➖ Só terminal (sem tela gráfica, exceto via X11 forwarding/encaminhamento, que é limitado).
- Melhor para: administração via linha de comando, servidores.

### Tailscale / WireGuard
- ✅ Monta uma rede privada criptografada entre seus dispositivos; **não precisa abrir portas** no roteador.
- ✅ Combina com RDP/VNC/SSH por cima, de forma segura, pela internet.
- ➖ É camada de rede, não um "controle de tela" por si só — você usa outra ferramenta por cima.
- Melhor para: acesso remoto pela internet com segurança, sem port forwarding.

## Princípio geral de segurança na escolha

Para **acesso pela internet**, prefira **não expor a porta diretamente**. A ordem de preferência é:
1. **Tailscale/WireGuard/VPN** e, por dentro dela, RDP/VNC/SSH.
2. Ferramenta com relay próprio e conta protegida por 2FA (Chrome Remote Desktop, AnyDesk, TeamViewer).
3. Port forwarding manual no roteador — **último recurso**, só com a porta endurecida (ver `seguranca.md`).
