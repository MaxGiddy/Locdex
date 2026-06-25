# Locdex
A coding agent that never touches your repo directly, tells you what a task will cost before running it, and routes routine work to Qwen3-Coder instead of burning your Claude/GPT API budget on every keystroke

Most local coding agents (Cline, Continue.dev, Aider) edit your files live and leave review entirely to you. This one doesn't — every AI-generated change is tested, linted, and AI-safety-reviewed before it becomes a pull request a human approves. Nothing reaches your repo unreviewed, ever.

## Why this exists

- **You're not choosing between "free but unreliable" and "great but expensive."** The router tries Qwen3-Coder first, and only escalates to Claude/GPT when its own confidence is low, it fails tests, or aggregate usage data says this category of task needs cloud help anyway.
- **You see the cost before you pay it.** Multi-file tasks get a cost estimate up front — like a quote — not a surprise bill.
- **Nothing ships without review.** Tests, lint, and an AI safety pass (checking for secrets, scope creep, suspicious changes) all have to pass before a PR opens. You merge it, not the AI.
- **No forced 20GB download.** Run the model locally for $0/use and full offline capability, or skip straight to a hosted endpoint for a few-MB install. Both are real, fully-supported choices — see below.

## What it is NOT

This isn't an attempt to rival Claude or GPT, and it doesn't store or redistribute anything those models generate. The "learning" here is entirely about *routing decisions* — knowing when Qwen is good enough vs. when to spend money on claude — not about closing the capability gap between them. See `BUILD_SPEC.md` for the full reasoning.

## Run it local, or skip the download — your choice

| | Download locally | Hosted endpoint |
|---|---|---|
| Install size | ~18-20GB (one-time) | A few MB |
| Per-use cost | $0 forever after download | ~$0.11-0.22 per million tokens |
| Works offline | Yes, fully | No — every call needs internet |
| Your code leaves the machine | Never, for primary-model tasks | Yes, every request goes to the hosted endpoint |

Both run the same model, Qwen3-Coder — this is purely about where it executes. Hosted mode is still far cheaper than escalating straight to Claude or GPT (full comparison table in `BUILD_SPEC.md` Section 1.4), but it's a genuinely paid, internet-dependent mode — "free" specifically describes the local-download path. You're asked which you want on first run.

## Language support (v0.1)

| | Python | TypeScript/JavaScript | Go |
|---|---|---|---|
| Code generation | ✅ | ✅ | ✅ |
| Test/lint validation | ✅ | ✅ | ✅ |
| Multi-file consistency check | ✅ Full (AST-based) | ⚠️ Approximate (grep-based) | ⚠️ Approximate (grep-based) |

Other languages: code generation and interactive chat work fine; the validated-PR pipeline isn't available yet — you'd commit/push manually, same as before this tool existed. Rust support is planned (see `BUILD_SPEC.md` Section 3.5.1).

## Quick start

```bash
# 1. Clone and install
git clone https://github.com/yourname/agenttool.git
cd agenttool
python3 -m venv venv && source venv/bin/activate
pip install -e .

# 2a. EITHER: download the model locally (~18-20GB, $0 per use, works offline)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3-coder:30b-a3b

# 2b. OR: skip the download, use the hosted endpoint instead
export OPENROUTER_API_KEY=your_openrouter_key

# 3. Set your cloud API key (used only when the router escalates)
export ANTHROPIC_API_KEY=your_key   # or OPENAI_API_KEY

# 4. Set your GitHub token (used only when you explicitly "ship" a change)
export GITHUB_TOKEN=your_github_personal_access_token

# 5. Run it
agenttool chat
```

Full setup, including troubleshooting and exact hardware requirements, is in `SETUP_GUIDE.md`.

## How a session works

```
$ agenttool chat
> add input validation to the login function in auth.py
[router: local model, attempt 1... confidence 0.81, tests pass]
✓ Here's the change: [diff shown inline]

> looks good but also handle the empty-string case
[router: local model, attempt 1... confidence 0.74, tests pass]
✓ Updated: [diff shown inline]

> ship it
[validator: tests ✓  lint ✓  AI safety review ✓]
[git: branch ✓  add ✓  commit ✓  push ✓]
✓ Opened PR #42: "Add input validation to login()"
```

Everything before `ship it` runs through the router only — no GitHub involvement. (In download mode, this is also $0 and fully offline; in hosted mode, each turn makes a small, paid API call — see the cost table above.) Only the explicit "ship it" step runs the full validation gate and opens a real pull request.

## Hardware you need

A laptop with 16GB RAM handles building this comfortably. Running the default local model (download mode) comfortably wants ~32GB RAM given its size — or skip that entirely with hosted mode, which needs no extra RAM at all. Full breakdown in `SETUP_GUIDE.md`.

## Opt-in shared learning (off by default)

You can optionally let the tool share anonymous routing outcomes (task category, success/failure, language, which provider performed best — never your code) to help improve routing decisions for everyone, including which cloud provider tends to work best for a given kind of task. Fully described, with the exact data schema, on first run and in `BUILD_SPEC.md` Section 3.10.

## License

[Choose one — MIT is the standard default for projects wanting maximum adoption: permissive, well-understood, no friction for contributors or commercial use.]

## Contributing

[Add once you've decided on a contribution flow — even a one-line "open an issue first" is enough for v0.1.]
