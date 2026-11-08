# Segurança e endurecimento

Acesso remoto é uma porta de entrada para a máquina. Leia este checklist com o usuário **ao final** de qualquer configuração. A diferença entre acesso remoto legítimo e um backdoor não está na ferramenta — está em **autorização, visibilidade e proteção**.

## Princípios

1. **Só nas suas máquinas (ou com autorização explícita).** Configure acesso remoto apenas onde você é dono ou administrador autorizado.
2. **Visível para o dono.** O usuário/dono do equipamento deve conseguir saber que o acesso remoto existe e quando há uma sessão ativa. Nada de modo oculto para enganar o dono.
3. **Mínimo necessário.** Habilite só a ferramenta, as contas e as portas que você realmente usa. Desligue o resto.
4. **Não exponha portas cruas na internet.** Prefira VPN/Tailscale ou o relay autenticado da ferramenta.

## Checklist de endurecimento

- [ ] **Senha/PIN forte e único** para o acesso remoto (não reutilize a senha de outra coisa).
- [ ] **2FA/MFA** ativado na conta que controla o acesso (Google p/ CRD, conta AnyDesk/TeamViewer/Tailscale).
- [ ] **Atualizações em dia** no SO e na ferramenta de acesso remoto (correções de segurança).
- [ ] **Acesso pela internet via VPN/Tailscale**, não por port forwarding direto. Se for RDP/VNC/SSH externo, túnel obrigatório.
- [ ] **NLA ligado** (RDP) e **login por chave** (SSH, com `PasswordAuthentication no`).
- [ ] **Bloqueio após tentativas** de senha / fail2ban onde aplicável.
- [ ] **Allowlist de dispositivos/IPs** quando a ferramenta permitir.
- [ ] **Revisar dispositivos confiáveis** e remover os que não usa mais.
- [ ] **Encerrar a sessão** (logoff, não só fechar a janela) ao terminar.
- [ ] **Bloqueio de tela** no host, para a sessão não ficar aberta se alguém fisicamente acessar a máquina.
- [ ] **Antivírus/EDR ativos** — acesso remoto não é motivo para desligá-los.
- [ ] **Firewall** liberando só o necessário, no perfil de rede certo.

## Golpes com acesso remoto — alerte o usuário
Fraudadores pedem para a vítima instalar AnyDesk/TeamViewer e passar o ID/senha, fingindo ser "suporte técnico", "banco" ou "Microsoft". **Nunca** conceda acesso remoto a quem entrou em contato de surpresa. Só dê acesso a alguém que **você** procurou e confia.

## O que NÃO fazer / não ajudar a fazer
- Instalar acesso remoto **oculto** para que o dono/usuário não perceba.
- **Contornar** senha de login, bloqueio de tela, antivírus, EDR ou política de TI.
- Manter acesso a um equipamento que **deixou de ser seu** (ex.: PC de ex-emprego).
- Acessar máquina de terceiro **sem consentimento**.
- Desabilitar logs/avisos de sessão para esconder o acesso.

Se o pedido cair em qualquer um desses pontos, pare e explique o porquê, em vez de dar o passo a passo. Em ambiente de trabalho, o caminho certo é falar com a **TI** e usar a solução oficial (VPN/RDP Gateway/jump host).

## Desligar/remover o acesso (quando não quiser mais)
- **Chrome Remote Desktop**: `remotedesktop.google.com/access` → remova o host; desinstale o complemento.
- **AnyDesk/TeamViewer**: remova o dispositivo da conta, desligue o acesso desassistido e desinstale.
- **RDP**: Configurações → Área de Trabalho Remota → desligar.
- **VNC/SSH**: pare e desabilite o serviço (`systemctl disable --now ...`), remova chaves em `authorized_keys`.
- **Tailscale**: remova o dispositivo no painel e desinstale.
