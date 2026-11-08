# SSH e Tailscale

Dois pilares do acesso remoto seguro: **SSH** para terminal remoto, e **Tailscale** (rede estilo WireGuard) para alcançar suas máquinas pela internet **sem abrir portas** no roteador. Combinam muito bem: Tailscale leva você até a máquina; SSH/RDP/VNC fazem o trabalho por cima.

---

## SSH (terminal remoto)

### Host
- **Linux**: instale e ligue o servidor — `sudo apt install openssh-server` (Debian/Ubuntu) e `sudo systemctl enable --now ssh`.
- **macOS**: System Settings → General → Sharing → ative **Remote Login**.
- **Windows**: Configurações → Aplicativos → Recursos Opcionais → adicione **OpenSSH Server**; depois `Start-Service sshd` e `Set-Service sshd -StartupType Automatic` no PowerShell (admin).

### Client
```
ssh usuario@host_ou_ip
```

### Autenticação por chave (recomendado — mais seguro que senha)
1. No client, gere o par de chaves:
   ```
   ssh-keygen -t ed25519 -C "meu-acesso"
   ```
2. Copie a chave pública para o host:
   ```
   ssh-copy-id usuario@host        # Linux/macOS
   ```
   (No Windows, adicione a chave em `C:\Users\<user>\.ssh\authorized_keys` ou, para admin, em `C:\ProgramData\ssh\administrators_authorized_keys`.)
3. **Desabilite login por senha** no host (`/etc/ssh/sshd_config`):
   ```
   PasswordAuthentication no
   PermitRootLogin no
   ```
   e recarregue: `sudo systemctl reload ssh`.

### Túneis úteis (port forwarding)
- Levar uma porta remota pro seu client (ex.: VNC 5901):
  ```
  ssh -L 5901:localhost:5901 usuario@host
  ```
- Encaminhar RDP por dentro do SSH:
  ```
  ssh -L 3389:localhost:3389 usuario@host
  ```
  depois conecte o RDP a `localhost:3389`.

### Segurança SSH
- Use **chave ed25519** + frase de senha; evite senha pura.
- Troque a porta padrão só reduz ruído (não é segurança real).
- Use **fail2ban** (Linux) para barrar força bruta se o SSH ficar exposto.
- Melhor ainda: **não exponha o SSH** na internet — coloque-o atrás do Tailscale.

---

## Tailscale (acesso pela internet sem abrir portas)

Cria uma rede privada criptografada (malha WireGuard) entre seus dispositivos. Cada um ganha um IP estável `100.x.y.z`, alcançável de qualquer lugar, **sem port forwarding**. Grátis para uso pessoal.

### Configurar
1. Crie conta em `tailscale.com` (login por Google/Microsoft/GitHub, com 2FA).
2. Instale o Tailscale no **host** e no **client** (Windows, macOS, Linux, Android, iOS) e faça login **na mesma conta (tailnet)** nos dois.
3. Cada dispositivo aparece no painel com seu IP `100.x.y.z` e um nome MagicDNS (ex.: `meu-pc`).

### Usar por cima
- **SSH**: `ssh usuario@meu-pc` ou `ssh usuario@100.x.y.z`.
- **RDP**: no app de Área de Trabalho Remota, conecte ao IP `100.x.y.z` do host.
- **VNC**: aponte o viewer para o IP `100.x.y.z`.

Como o host só é alcançável dentro do seu tailnet autenticado, **nenhuma porta fica exposta na internet pública** — é a forma mais simples e segura de acesso remoto externo para uso pessoal.

### Recursos extras
- **Tailscale SSH**: deixa o próprio Tailscale gerenciar o acesso SSH com as ACLs da conta (dispensa gerenciar chaves manualmente).
- **ACLs**: no painel, limite quais dispositivos podem falar com quais.
- **Exit nodes / subnet router**: avançado; só se precisar rotear uma rede inteira.

### Alternativas equivalentes
- **WireGuard puro** (mais manual), **ZeroTier** (semelhante ao Tailscale), ou a **VPN do seu roteador** (muitos roteadores têm servidor WireGuard/OpenVPN embutido).

## Problemas comuns
- **Não conecta via Tailscale**: confirme que os dois estão **online** e logados no mesmo tailnet; cheque o status no painel; em redes restritas, o Tailscale usa relays DERP automaticamente.
- **SSH recusa a chave**: permissões do `~/.ssh` (700) e `authorized_keys` (600); no Windows, caminho do `administrators_authorized_keys`.
- **Windows OpenSSH não inicia**: verifique o serviço `sshd` e a regra de firewall da porta 22.
