<div align="center">

# Hi, I'm Adarsh Pillai 👋

### `aaadarsh1337` · `jackthereaper1337` · `Hasher2009`

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=18&pause=1000&color=7DCFFF&center=true&vCenter=true&width=600&lines=Offensive+security+%C2%B7+Reverse+engineering+%C2%B7+CTF;Web+exploitation+%C2%B7+Pwn+%C2%B7+Binary+exploitation; populates+leaderboards%2C+not+just+reads+them)](https://git.io/typing-svg)

**I break things to learn how they work — then I document everything.**

[![Portfolio](https://img.shields.io/badge/Portfolio-aaadarsh1337.github.io-7DCFFF?style=for-the-badge&logo=google-chrome&logoColor=16161E)](https://aaadarsh1337.github.io/)
[![Writeups](https://img.shields.io/badge/CTF_Writeups-22+-BB9AF7?style=for-the-badge&logo=bookstack&logoColor=16161E)](https://aaadarsh1337.github.io/writeups/)
[![Flagship](https://img.shields.io/badge/FLAGSHIP-Threat_Harbour-F7768E?style=for-the-badge&logo=honeygain&logoColor=16161E)](https://github.com/aaadarsh1337/threat-harbour)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-Top_2%25-9ECE6A?style=for-the-badge&logo=tryhackme&logoColor=16161E)](https://tryhackme.com/p/aaadarsh1337)

</div>

---

## 🚩 Flagship — [Threat Harbour](https://github.com/aaadarsh1337/threat-harbour)

> ### What credentials are attackers trying *right now*? Ask this box.
>
> A **Cowrie SSH honeypot on Oracle Cloud Free Tier** that publishes a **fresh leaderboard of real attacker credentials every 24 hours** — the usernames, passwords, and commands bots actually try against SSH servers in the wild.

Every exposed SSH port gets knocked on thousands of times a day by bots working through credential lists. Most people still pick passwords from exactly the pool those bots try first. This repo closes that gap with **live evidence**: if a password is in the table below, bots are already trying it against your servers too.

### 📡 Live sensor data — refreshed every 24h

| Total events | Unique IPs | Sessions | Fake logins | Commands | Downloads (+uploads) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **174,927** | **2,112** | **28,501** | **18,343** | **16,931** | **101 (+12)** |

| # | 🔑 Top username | 🔒 Top password | 💻 Top command |
|:-:|---|---|---|
| 1 | `root` (9,801) | `123456` (960) | `uname -s -v -n -r -m` (12,396) |
| 2 | `admin` (761) | `1234` (470) | `hostname` (722) |
| 3 | `user` (446) | `123` (465) | `uname -a` (356) |
| 4 | `ubuntu` (415) | `12345678` (271) | `/bin/./uname -s -v -n -r -m` (336) |
| 5 | `deploy` (248) | `admin` (259) | `whoami` (315) |

**Key findings:**

- ⏱️ Median session **2.3s** (71% under 10s) — automated scanning, not humans
- 🔍 **93%** of commands are discovery / fingerprinting (`uname`, `hostname`, `whoami`)
- 🔑 Repeated persistence probes writing toward `authorized_keys` (hash redacted, content withheld)
- 📍 Busiest /16 by volume: `109.160.0.0/16` (62,784 events) — volume only, never attribution

### ⚙️ How it stays fresh

A **GitHub Actions job runs every 24 hours**: SSHes into the sensor as a restricted read-only user, parses Cowrie logs **on the box**, and commits updated tables + charts back. **Only aggregates ever leave the sensor** — raw logs, source IPs, and payloads stay on it.

<details>
<summary><b>🏗️ Architecture — click to expand</b></summary>
<br>

Internet → OCI edge → NSG → Sensor VM (Cowrie + localhost-bound monitor stack) → analyst via SSH tunnel. Grafana/Loki never public; raw logs stay on sensor.

![Architecture](https://raw.githubusercontent.com/aaadarsh1337/threat-harbour/main/diagrams/architecture.png)
![Data pipeline](https://raw.githubusercontent.com/aaadarsh1337/threat-harbour/main/diagrams/data-pipeline.png)

One Free Tier VM (`VM.Standard.E2.1.Micro`, Ubuntu 24.04, `ap-hyderabad-1`): SSH-only Cowrie `3.0.13` + Grafana + Loki + Promtail over Docker, all localhost-bound. Deliberately small instead of a full multi-service setup like T-Pot — one port, tight scope, rebuildable.

</details>

<details>
<summary><b>📊 Activity — click to expand</b></summary>
<br>

![Session funnel](https://raw.githubusercontent.com/aaadarsh1337/threat-harbour/main/diagrams/session-funnel.png)
![Activity timeline](https://raw.githubusercontent.com/aaadarsh1337/threat-harbour/main/diagrams/activity-timeline.png)
![Dashboard](https://raw.githubusercontent.com/aaadarsh1337/threat-harbour/main/dashboard/dashboard.png)

</details>

**Use it to:** sanity-check password choices · justify MFA with real numbers · teach brute-force with a live specimen · feed blue-team blocklists and detection ideas.

**Links:** [🔴 Live leaderboard](https://github.com/aaadarsh1337/threat-harbour#collected-data--refreshed-every-24-hours-last-run-08-09-2026-utc) · [📄 Full tables](https://github.com/aaadarsh1337/threat-harbour/blob/main/analysis/summary.md) · [🤖 Machine-readable](https://raw.githubusercontent.com/aaadarsh1337/threat-harbour/main/analysis/metrics.json) · [📚 Docs](https://github.com/aaadarsh1337/threat-harbour/tree/main/docs)

`Cowrie 3.x` · `Oracle Cloud` · `Grafana + Loki` · `GitHub Actions` · `Python`

> ⚠️ One VM, one IP, one region — this is what hit *this* sensor, not the whole internet. A source IP never identifies the operator. Defensive research and education only.

---

## 🎯 Focus

- 💥 **Offensive security** — CTFs, labs, vulnerability research
- 🔬 **Reverse engineering + binary exploitation** — currently grinding assembly for RE
- 🛠️ **Security tooling** — custom utilities, from quick CTF scripts to structured automation
- 📝 **Documenting everything** — writeups, lab notes, methodology

## 🧰 Toolbox

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnu-bash&logoColor=white)
![C](https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=flat-square&logo=burpsuite&logoColor=white)
![Ghidra](https://img.shields.io/badge/Ghidra-FF0000?style=flat-square&logo=reverse-engineering&logoColor=white)
![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=flat-square&logo=wireshark&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)

| Domain | Arsenal |
|---|---|
| **Offensive** | Web Exploitation · Network Security · Reverse Engineering · Binary Exploitation · OSINT |
| **Web** | Burp Suite · FFUF · Nikto |
| **Network** | nmap · Wireshark |
| **Binary** | Ghidra · Binary Ninja · pwntools · pwndbg |
| **Forensics** | Autopsy · Binwalk |
| **Currently learning** | Forensics · Blockchain · Cloud · Assembly for RE |

---

## 🏆 CTF & Highlights

| Event | Team | Result | Proof |
|:---|:---|:---|:---|
| **TFC CTF 2026** | 404squad | #23 Human · #172 Overall | [Diploma](https://github.com/aaadarsh1337/cybersecurity-achievements/tree/main/TFCCTF) |
| **z0d1ak CTF 2026** | 404squad | #13 Human · #75 Overall | [Certificate](https://github.com/aaadarsh1337/cybersecurity-achievements/tree/main/z0d1ak-ctf) |
| **TryHackMe** | — | **Top 2%** global · **100+** rooms | [Profile](https://tryhackme.com/p/aaadarsh1337) |

[![TryHackMe](https://tryhackme-badges.s3.amazonaws.com/aaadarsh1337.png)](https://tryhackme.com/p/aaadarsh1337)

> 📝 **22+ writeups** and counting — [pwnable.kr](https://aaadarsh1337.github.io/writeups/) (`fd`, `collision`, `bof`, `passcode`) · TryHackMe (`Binary Heaven`) · picoCTF · 15-room HackerHolidays series. Every writeup shows each command and its output, step by step.

---

## 📚 Featured Repos

[![Threat Harbour](https://github-readme-stats.vercel.app/api/pin/?username=aaadarsh1337&repo=threat-harbour&theme=tokyonight)](https://github.com/aaadarsh1337/threat-harbour)
[![CTF Writeups](https://github-readme-stats.vercel.app/api/pin/?username=aaadarsh1337&repo=ctf-writeups&theme=tokyonight)](https://github.com/aaadarsh1337/ctf-writeups)
[![Security Automation Toolkit](https://github-readme-stats.vercel.app/api/pin/?username=aaadarsh1337&repo=security-automation-toolkit&theme=tokyonight)](https://github.com/aaadarsh1337/security-automation-toolkit)
[![Achievements](https://github-readme-stats.vercel.app/api/pin/?username=aaadarsh1337&repo=cybersecurity-achievements&theme=tokyonight)](https://github.com/aaadarsh1337/cybersecurity-achievements)

Plus lab-note archives: [`picoctf-lab-notes`](https://github.com/aaadarsh1337/picoctf-lab-notes) · [`tryhackme-lab-notes`](https://github.com/aaadarsh1337/tryhackme-lab-notes) · [`practical-ethical-hacking-notes`](https://github.com/aaadarsh1337/practical-ethical-hacking-notes) · [`ctf-learning-archive`](https://github.com/aaadarsh1337/ctf-learning-archive)

---

## 📊 Stats

<div align="center">

![Stats](https://github-readme-stats.vercel.app/api?username=aaadarsh1337&show_icons=true&theme=tokyonight&hide_border=true&count_private=true)
![Streak](https://github-readme-streak-stats.herokuapp.com/?user=aaadarsh1337&theme=tokyonight&hide_border=true)
![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=aaadarsh1337&layout=compact&theme=tokyonight&hide_border=true)

![Activity](https://github-readme-activity-graph.vercel.app/graph?username=aaadarsh1337&theme=tokyo-night&hide_border=true)

</div>

---

## 🎓 Certificates

- 🏅 **TFC CTF 2026**
- 🏅 **z0d1ak CTF 2026**
- 🎄 **TryHackMe Hacker Holidays**
- 🎄 **TryHackMe Advent of Cyber 3** (2021)
- 🔐 **TCM Practical Ethical Hacking**

Full library with verification links → [portfolio certificates](https://aaadarsh1337.github.io/#certificates) · [archive repo](https://github.com/aaadarsh1337/cybersecurity-achievements)

---

## 🤝 Connect

[![GitHub](https://img.shields.io/badge/GitHub-@aaadarsh1337-181717?style=for-the-badge&logo=github)](https://github.com/aaadarsh1337)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Adarsh_Pillai-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/aaadarsh1337)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-aaadarsh1337-CC0000?style=for-the-badge&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/aaadarsh1337)
[![CTFtime](https://img.shields.io/badge/CTFtime-265799-7DCFFF?style=for-the-badge&logo=flag&logoColor=16161E)](https://ctftime.org/user/265799)
[![X](https://img.shields.io/badge/X-@aaadarsh1337-000000?style=for-the-badge&logo=x)](https://x.com/aaadarsh1337)
[![Email](https://img.shields.io/badge/Email-adarshpillai1337@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:adarshpillai1337@gmail.com)
[![Discord](https://img.shields.io/badge/Discord-Hit_Me_Up-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/users/15248404499301847090)
[![pwn.college](https://img.shields.io/badge/pwn.college-hacker-9ECE6A?style=for-the-badge&logo=terminal&logoColor=16161E)](https://pwn.college/hacker/192643)
[![PicoCTF](https://img.shields.io/badge/PicoCTF-jackthereaper1337-BB9AF7?style=for-the-badge&logo=flag&logoColor=16161E)](https://learn.cylabacademy.org/users/jackthereaper1337)

---

<div align="center">

![Views](https://komarev.com/ghpvc/?username=aaadarsh1337&color=7DCFFF&style=flat-square&label=profile+views)

*Cybersecurity student, not a full-time web developer — parts of my sites and tooling were built with AI assistance so I could ship fast. Content, writeups, methodology, and sensor work are my own. I care more about the work behind the links than hand-rolling every CSS rule.*

**`pwn for life`** ⚔️

</div>
