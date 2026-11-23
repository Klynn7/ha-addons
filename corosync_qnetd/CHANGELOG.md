# Changelog

## 2026.11.23.1

Debian package updates:

- `base-files` 13.8+deb13u7 → 13.8+deb13u8
- `libc-bin` 2.41-12+deb13u4 → 2.41-12+deb13u5
- `libc6` 2.41-12+deb13u4 → 2.41-12+deb13u5
- `libgssapi-krb5-2` 1.21.3-5+deb13u1 → 1.21.3-5+deb13u2
- `libk5crypto3` 1.21.3-5+deb13u1 → 1.21.3-5+deb13u2
- `libkrb5-3` 1.21.3-5+deb13u1 → 1.21.3-5+deb13u2
- `libkrb5support0` 1.21.3-5+deb13u1 → 1.21.3-5+deb13u2
- `libssl3t64` 3.5.7-1~deb13u3 → 3.5.9-1~deb13u1
- `openssl-provider-legacy` 3.5.7-1~deb13u3 → 3.5.9-1~deb13u1

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
