# Changelog

## 2026.11.09.6

Debian package updates:

- `apt` 3.0.3 → 3.0.4
- `libapt-pkg7.0` 3.0.3 → 3.0.4
- `zlib1g` 1:1.3.dfsg+really1.3.1-1+b1 → 1:1.3.dfsg+really1.3.1-1+deb13u1

## 2026.11.03.5

- corosync-qnetd now receives the stop signal directly and shuts down cleanly. Previously `runuser` force-killed it 2 seconds after every stop, logging "Session terminated, killing shell... ...killed."

## 2026.11.03.2

- Log lines are now timestamped in the Home Assistant system timezone (e.g. `2026-11-03 07:55:16 MST`), covering add-on startup messages, sshd and corosync-qnetd output.
- Added `tzdata` to the image so the timezone Supervisor passes in is honored instead of falling back to UTC.

## 2026.11.03.1

- Initial release: corosync-qnetd on Debian trixie (aarch64) as a Proxmox QDevice arbiter on TCP 5403.
- NSS certificate database and SSH host key persist in `/data` across updates.
- Optional key-only sshd (default port 2222) for `pvecm qdevice setup`; runs only while `authorized_keys` is set.
