# c0admin 🐧

Suggests GNU/Linux terminal commands from natural language using AI.

![c0admin Banner](c0admin-banner.png)

> [!WARNING]
> For the automatic copy to clipboard feature to work, you must have the ‘xsel’ and ‘xclip’ packages installed on your system.

[How to get personal Google Gemini API key?](https://github.com/mbrell/c0admin/blob/main/how-to-get-gemini-api-key.md)

## Installation

To install `c0admin` system-wide on GNU/Linux:

```bash
curl -s https://raw.githubusercontent.com/mbrell/c0admin/main/install.sh | bash
```
This will:

- Download and install c0admin to ~/.c0admin/
- Set up a Python virtual environment
- Install dependencies
- Make c0admin available as a global terminal command

After installation, you can start the app anytime by simply typing:

```bash
c0admin
```

## Commands

- `--help`

- `/del` — Delete the GEMINI API KEY.
- `/exit` — Exit the app safely.
- `/help` — Redirects to repository.
- `/history` — Displays the command history (history.txt).
- `/setinst <url>` — Set a custom system instruction from a given URL.
- `/resetinst` — Reset system instruction to the default one.

## Custom System Instructions

From the [system-instructions](https://github.com/mbrell/c0admin-system-instructions) repo you can see all the community-created system instructions.

We welcome your contributions on this issue.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

Built with ❤️ using Python
