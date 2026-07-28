[README.md](https://github.com/user-attachments/files/30476651/README.md)
# Universal Linux Live ISO Creator

**Create a bootable Live ISO of your installed Linux system, through a simple graphical interface.**

Universal Linux Live ISO Creator is an open-source Python application that lets you turn your currently installed Linux system into a bootable Live ISO. Unlike traditional remastering tools, it automatically detects your distribution, prepares the environment, installs any missing dependencies, and walks you through the process with a multilingual graphical interface — no command-line expertise required.

It's built for anyone who wants to:

- Back up their operating system exactly as it's configured
- Clone a customized Linux installation
- Produce a portable Live ISO to run from USB
- Deploy identical systems across multiple computers

---

## Features

- 🖥️ Graphical interface (Tkinter) — no manual command-line steps needed
- 🔍 Automatic Linux distribution detection
- 📦 Automatic dependency installation
- 🥚 Automatic Penguins-Eggs installation
- 🌐 Multilingual interface (15+ languages)
- 📊 Real-time progress tracking with elapsed/remaining time
- 🦜 Parrot OS compatibility mode
- 📋 Copyable terminal log, for easy troubleshooting

## Supported Distributions

| Family | Distributions |
|---|---|
| Debian-based | Debian, Ubuntu, Linux Mint, Devuan, Parrot OS |
| Arch-based | Arch Linux, Manjaro, EndeavourOS |
| Fedora/RHEL-based | Fedora, RHEL, Rocky Linux, AlmaLinux |
| Other | openSUSE, Alpine Linux |

## Requirements

- Linux system with a desktop environment (a display server is required — this is a GUI application)
- Python 3 with Tkinter (`python3-tk` or equivalent for your distribution)
- `sudo` privileges
- An active internet connection (used to install dependencies and Penguins-Eggs)

## Installation & Usage

```bash
git clone https://github.com/cybertoxin3/Linux-System-ISO-Cloner.git
cd Linux-System-ISO-Cloner
python3 iso_creator.py
```

1. Choose your interface language (or let it auto-detect from your system locale)
2. Click **Clone System to ISO**
3. Choose where to save the resulting `.iso` file and give it a name
4. Enter your `sudo` password when prompted
5. Wait for the process to complete — progress and estimated remaining time are shown live

## How It Works

1. Detects your Linux distribution family from `/etc/os-release`
2. Installs required build tools and dependencies via your distro's package manager
3. Installs [Penguins-Eggs](https://github.com/pieroproietti/penguins-eggs) if it isn't already present
4. Applies a compatibility fix for Parrot OS (temporarily reports itself as Debian, since Penguins-Eggs doesn't have a dedicated Parrot profile)
5. Runs the remastering process to produce the ISO
6. Moves the finished ISO to the location you chose

## Technologies

- Python
- Tkinter
- `subprocess` / `threading`
- [Penguins-Eggs](https://github.com/pieroproietti/penguins-eggs)
- Native Linux package managers (`apt`, `pacman`, `dnf`, `zypper`, `apk`)

## Project Structure

```text
Linux-System-ISO-Cloner/
├── iso_creator.py
├── README.md
└── LICENSE
```

## Contributing

Issues and pull requests are welcome. If you run into a problem, please include your distribution, the terminal log from the app (use the **Copy Log** button), and the steps that led to the error.

## License

Add your chosen license here (e.g., MIT, GPL-3.0) and include the corresponding `LICENSE` file in the repository.

---

### Suggested repository settings (GitHub "About" section — not part of this README)

**Description:**
> Universal graphical Linux ISO creator with automatic dependency installation, multilingual support, and Penguins-Eggs integration.

**Topics:**
`linux` `iso` `livecd` `penguins-eggs` `python` `tkinter` `backup` `cloning` `remaster` `linux-tools` `desktop-application`
