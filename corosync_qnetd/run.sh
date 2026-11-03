#!/bin/bash
set -euo pipefail

# Prefix every line from this script, sshd and qnetd with a local timestamp.
# Supervisor sets TZ to the HA system timezone; tzdata in the image honors it.
exec > >(while IFS= read -r line; do
    printf '%(%Y-%m-%d %H:%M:%S %Z)T %s\n' -1 "$line"
done) 2>&1

OPTS=/data/options.json
SSH_PORT=$(jq -r '.ssh_port' "$OPTS")

# --- Persist the qnetd NSS database across rebuilds/updates ---
mkdir -p /data/qnetd /data/ssh
if [ ! -L /etc/corosync/qnetd ]; then
    rm -rf /etc/corosync/qnetd
    ln -s /data/qnetd /etc/corosync/qnetd
fi
if [ ! -d /data/qnetd/nssdb ]; then
    echo "[qnetd] Initializing NSS database"
    corosync-qnetd-certutil -i
fi
# pvecm signs certs over SSH as root; hand ownership back to the daemon user
chown -R coroqnetd:coroqnetd /data/qnetd

# Runtime dir for the local control socket (systemd's RuntimeDirectory= normally does this)
mkdir -p /run/corosync-qnetd
chown coroqnetd:coroqnetd /run/corosync-qnetd

# --- Optional sshd for `pvecm qdevice setup` (key-only, runs only if keys are set) ---
[ -f /data/ssh/ssh_host_ed25519_key ] || \
    ssh-keygen -q -t ed25519 -N '' -f /data/ssh/ssh_host_ed25519_key
mkdir -p /root/.ssh && chmod 700 /root/.ssh
jq -r '.authorized_keys[]' "$OPTS" > /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

if [ -s /root/.ssh/authorized_keys ]; then
    echo "[qnetd] Starting sshd on port ${SSH_PORT}"
    /usr/sbin/sshd -p "$SSH_PORT" \
        -h /data/ssh/ssh_host_ed25519_key \
        -o PermitRootLogin=prohibit-password \
        -o PasswordAuthentication=no \
        -o KbdInteractiveAuthentication=no \
        -o UsePAM=no
else
    echo "[qnetd] No authorized_keys set; sshd disabled"
fi

echo "[qnetd] Starting corosync-qnetd on TCP 5403"
# setpriv drops privileges and execs in place, so qnetd itself receives
# Supervisor's SIGTERM and shuts down cleanly (runuser would SIGKILL it after 2s).
exec setpriv --reuid=coroqnetd --regid=coroqnetd --init-groups -- corosync-qnetd -f
