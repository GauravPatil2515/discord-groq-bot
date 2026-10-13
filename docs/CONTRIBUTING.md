# Contributing Guidelines

Thank you for contributing to the **SkillUp Discord AI Agent**! We welcome bug reports, feature suggestions, documentation enhancements, and pull requests.

---

## Code of Conduct

Please be respectful, collaborative, and constructive when opening issues or participating in discussions.

---

## Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/discord-groq-bot.git
   cd discord-groq-bot
   ```

2. **Set up the virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install pytest pytest-asyncio ruff
   ```

3. **Configure local environment**:
   ```bash
   cp .env.example .env
   # Add your test bot token, groq key, and test server ID
   ```

---

## Code Style & Standards

We enforce strict formatting and linting rules using **`ruff`**:

- Run lint check:
  ```bash
  ruff check .
  ```
- Automatically fix linter issues:
  ```bash
  ruff check --fix .
  ```
- Format code:
  ```bash
  ruff format .
  ```

---

## Testing

Run unit tests before submitting a PR:
```bash
pytest
```

If you add new utility functions, configuration parsers, or command handlers, please include corresponding unit tests in the `tests/` directory.

---

## Pull Request Checklist

- [ ] Code adheres to Ruff style guidelines.
- [ ] No secrets, `.env` files, or API keys are committed.
- [ ] All unit tests pass.
- [ ] Documentation updated if commands, arguments, or environment variables changed.
- [ ] Conventional Commit messages (e.g. `feat: add model switching option`, `fix: handle edge case in message chunking`).
