# VivaProof

**Practice. Explain. Prove.** An evidence-grounded voice examiner for project vivas.

Paste short notes, answer aloud, hear a follow-up and receive feedback linked to exact source text. The app validates every displayed evidence quote against your numbered notes. Unsupported quotes are rejected rather than shown as proof.

## Run

Python 3.9+ and Chrome/Edge. No Python packages required.

```sh
# Create .env with ASSEMBLYAI_API_KEY=your_key, or use a hosting secret.
# Never put the key in the browser or repository.
python3 server.py
```

Open http://localhost:3000. Without an API key, the explicitly labeled **Sample walkthrough** works. It is pre-written, not an AI or voice demonstration.

## AssemblyAI architecture

1. Python server mints a short-lived single-use Voice Agent API token.
2. Browser streams PCM16 24 kHz microphone audio over AssemblyAI WebSocket.
3. Per-session configuration contains numbered notes and an examiner prompt.
4. AssemblyAI handles speech recognition, managed conversational reasoning, turn detection, interruptions and speech output.
5. The agent calls `render_feedback`. The browser verifies exact quotes locally and returns its result only after `reply.done`, preventing mid-turn races. Interrupted pending results are discarded.
6. The learner reviews the card, retries and can download the session locally.

No separate LLM/TTS keys, GPU, database or paid phone service required.

## Scope and safety

- English MVP with short pasted notes (12,000 characters; first 60 nonempty lines).
- Coaching, not academic grading. A verified quote proves the quoted text exists, not that the interpretation or learner assessment is correct.
- Notes can be wrong; the coach is only grounded in what the learner provides.
- Use public or fictional notes. Notes, audio and transcripts are processed by AssemblyAI under its policies. The app does not persist them; AssemblyAI may retain session artifacts.
- API key stays server-side. Sessions capped at five minutes; default 20 token requests/hour per server process. This is a demo limit, not production abuse protection.
- A public deployed URL can consume the owner's credits. Production needs authentication, persistent quotas and provider budget controls.
- No accent/intelligence inference, no guaranteed grades, no fabricated benchmark claims.

## Tests

```sh
python3 -m py_compile server.py
node test-core.js
```

Eleven deterministic tests cover numbered notes, genuine quotes, invented IDs, fabricated/too-short quotes, mixed citations, tool configuration, key exclusion untrusted-note handling in the prompt and malformed evidence payloads. UI checks were performed locally in headless Chrome at desktop and mobile widths. Live provider connectivity is separately documented in the submission; offline checks are not evidence that speech is working.

## Deploy

The deployment packages the frontend into `server.py` so the private repository is self-contained. The development archive keeps separate frontend files for editing. `render.yaml` declares a free Python web service. Supply the AssemblyAI key as a hosting secret. Startup: `python3 server.py`; health: `/health`. Do not commit `.env`.

## Attribution

Audio capture/playback and API plumbing adapted from the official AssemblyAI Python Voice Agent starter: https://github.com/AssemblyAI/voice-agent-starter-python . VivaProof adds dynamic note context, evidence validation, feedback UI, session export and demo limits. Built with AI coding assistance. No claim that this code was written without such assistance.

Documentation:
- https://www.assemblyai.com/docs/voice-agents/voice-agent-api
- https://www.assemblyai.com/docs/voice-agents/voice-agent-api/browser-integration
- https://www.assemblyai.com/docs/voice-agents/voice-agent-api/tools/client-side-tools
