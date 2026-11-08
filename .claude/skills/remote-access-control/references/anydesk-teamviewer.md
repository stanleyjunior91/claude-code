# AnyDesk e TeamViewer

Ferramentas de controle de tela com muitos recursos (transferência de arquivos, chat, multi-monitor, impressão remota). Dois modos: **assistido** (ID + alguém aprova na hora) e **desassistido** (senha fixa configurada no host). Gratuitas **para uso pessoal**; uso comercial exige licença.

## AnyDesk

### Instalar
- Baixe em `anydesk.com` nos dois dispositivos (host e client). Há app para Windows, macOS, Linux, Android, iOS.
- No **macOS**, conceda em System Settings → Privacy & Security: **Accessibility**, **Screen Recording** e **Input Monitoring** ao AnyDesk.

### Sessão assistida (alguém está no host)
1. No host, abra o AnyDesk e leia o **endereço/ID** (um número).
2. No client, digite esse ID no campo "Remote Desk" → **Connect**.
3. A pessoa no host clica em **Accept**. A sessão fica visível pra ela.

### Acesso desassistido (entrar sem aprovação na hora) — só na sua própria máquina
1. No host: Settings → **Security** → habilite **"Enable unattended access"** e defina uma **senha forte**.
2. (Opcional) Habilite **two-factor authentication** na conta AnyDesk.
3. No client, conecte pelo ID e informe a senha de acesso desassistido.
4. Mantenha o AnyDesk configurado para iniciar com o sistema, se quiser acesso contínuo.

> Faça acesso desassistido **apenas** em máquinas suas. Em máquina de outra pessoa, use o modo assistido, para que o dono veja e aprove cada sessão.

## TeamViewer

### Instalar
- Baixe em `teamviewer.com` nos dois lados. Multiplataforma.
- No macOS, conceda as mesmas permissões (Accessibility, Screen Recording, Input Monitoring).

### Sessão assistida
1. No host, abra o TeamViewer e leia **"Your ID"** e a **"Password"** (senha aleatória que muda por sessão).
2. No client, em "Control Remote Computer", digite o **Partner ID** → Connect → informe a senha.

### Acesso desassistido
1. Crie/entre numa conta TeamViewer e **associe o dispositivo** à conta (Assign device).
2. Defina uma **senha pessoal** (Personal password) ou use **Easy Access** ligado à conta.
3. Ative **2FA** na conta TeamViewer.
4. No client, conecte pelo ID usando a senha pessoal.

### Evitar o bloqueio de "uso comercial"
O TeamViewer às vezes marca uso pessoal como comercial e limita a sessão. Mitigações:
- Use sessões curtas e encerre ao terminar.
- Registre o uso pessoal no formulário do próprio TeamViewer (dentro do app, quando ele acusa).
- Se o problema persistir, **prefira o AnyDesk** ou o Chrome Remote Desktop para uso pessoal.

## Segurança (ambas)
- Senha de acesso desassistido **forte e única** + **2FA na conta**.
- Mantenha o app **atualizado** (já houve campanhas de golpe usando essas ferramentas — nunca conceda acesso a quem liga dizendo ser "suporte técnico").
- Revise a **lista de dispositivos confiáveis** e remova os que não usa.
- Ative **allowlist** de quem pode conectar, se a versão permitir.

## Problemas comuns
- **Tela preta ou sem controle no macOS**: faltam permissões de Accessibility/Screen Recording/Input Monitoring.
- **"Commercial use detected" (TeamViewer)**: ver seção acima; considere trocar de ferramenta.
- **Conexão cai em redes corporativas**: firewall bloqueando; use a versão com relay na nuvem ou fale com a TI.
- **Lentidão**: baixe a qualidade de imagem nas configurações de exibição da sessão.
