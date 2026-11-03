# Home Assistant add-ons

## Corosync QNetd (`corosync_qnetd`)

Proxmox QDevice arbiter (`corosync-qnetd`) for an even-node Proxmox cluster, running on the Home Assistant host.

- qnetd listens on TCP 5403 (host network).
- The NSS cert database and SSH host key persist in `/data`, so updates don't break the QDevice.
- sshd only runs while `authorized_keys` is non-empty (key auth only, default port 2222). It's needed only for `pvecm qdevice setup`.

### Updates

`.github/workflows/build.yaml` runs weekly. It builds a probe image and compares its full package list (plus add-on sources) against `corosync_qnetd/build-manifest.txt`. If anything changed, it pushes new per-arch images to GHCR, then bumps `version` in `config.yaml`. Turn on **Auto update** for the add-on in Home Assistant to pick these up.

Run the workflow manually with **force** to publish without changes.

### Proxmox setup

```
# every node
apt install corosync-qdevice

# setup node: /root/.ssh/config
Host <HA IP>
    Port 2222
    User root

# add the setup node's /root/.ssh/id_rsa.pub to the add-on's authorized_keys, start it, then:
pvecm qdevice setup <HA IP>
pvecm status
```

Afterwards: restart the add-on, then clear `authorized_keys` and restart again to turn sshd off.
