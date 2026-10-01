# VivaProof

**Practice. Explain. Prove.** An evidence-grounded voice examiner for project vivas.

Paste short notes, answer aloud, hear a follow-up and receive feedback linked to exact source text. The app validates every displayed evidence quote against your numbered notes. Unsupported quotes are rejected rather than shown as proof.

## Run

Python 3.10+ and Chrome/Edge. Backend: FastAPI and Uvicorn. Frontend: vanilla JavaScript.

```sh
# Create .env with ASSEMBLYAI_API_KEY=your_key, or use a hosting secret.
# Never put the key in the browser or repository.
pip install -r requirements.txt
python3 server.py
```

Open http://localhost:3000. Without an API key, the explicitly labeled **Sample walkthrough** works. It is pre-written, not an AI or voice demonstration.

## AssemblyAI architecture

1. FastAPI mints a short-lived single-use Voice Agent API token server-side.
2. Browser streams PCM16 24 kHz microphone audio through the FastAPI `/voice` WebSocket proxy to AssemblyAI. Speech-to-text, spoken replies and feedback events return through the same proxy. The provider key and token never reach the browser.
3. Per-session configuration contains numbered notes and an examiner prompt.
4. AssemblyAI handles speech recognition, managed conversational reasoning, turn detection, interruptions and speech output.
5. The agent calls `save_answer`. A simple text payload carries Strength, Gap, Retry and an exact source quote. The browser parses these labels, verifies full source-note text locally and returns its result only after `reply.done`, preventing mid-turn races. Interrupted pending results are discarded.
6. The learner reviews the card, retries and can download the session locally.

No separate LLM/TTS keys, GPU, database or paid phone service required. FastAPI relays audio in memory only; it does not store notes, audio or transcripts. Same-origin checks, a per-hour session cap and a five-minute provider session cap limit access.

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

Fourteen deterministic tests cover numbered notes, genuine quotes, invented IDs, fabricated/too-short quotes, mixed citations, tool configuration, key exclusion untrusted-note handling in the prompt and malformed evidence/coaching payloads. UI checks were performed locally in headless Chrome at desktop and mobile widths. Live provider connectivity is documented in the Live validation section below; offline checks are not evidence that speech is working.

## Deploy

The deployment packages the frontend into `server.py` so the repository is self-contained. The development archive keeps separate frontend files for editing. `render.yaml` declares a free Python web service. Supply the AssemblyAI key as a hosting secret. Startup: `pip install -r requirements.txt
python3 server.py`; health: `/health`. Do not commit `.env`.

## Attribution

Audio capture/playback and API plumbing adapted from the official AssemblyAI Python Voice Agent starter: https://github.com/AssemblyAI/voice-agent-starter-python . VivaProof adds dynamic note context, evidence validation, feedback UI, session export and demo limits. Built with AI coding assistance. No claim that this code was written without such assistance.

Documentation:
- https://www.assemblyai.com/docs/voice-agents/voice-agent-api
- https://www.assemblyai.com/docs/voice-agents/voice-agent-api/browser-integration
- https://www.assemblyai.com/docs/voice-agents/voice-agent-api/tools/client-side-tools

## Live validation

Live demo: https://vivaproof.onrender.com/ . A deployed desktop Chrome test on September 30, 2026 verified actual examiner audio, one complete synthetic-student answer, a client tool call, a displayed coaching card with an exact verified N3 note quote, spoken follow-up and clean teardown. No JavaScript errors. This is one synthetic-microphone turn, not a full browser or device matrix. Adaptive turn detection replaced explicit silence thresholds after initial tests split sentences. The simple text tool replaced a richer schema that produced empty replies or raw tool text. Some spoken coaching remains longer than desired. Unsupported or unstructured coaching is rejected instead of displayed as evidence.

## Answer timer and session history

Select an answer time before starting: Off, 10, 15 (default), 30 or 60 seconds.
The timer starts when student speech begins, not while the examiner is talking.
At the limit the browser replaces further microphone frames with silence. The examiner
uses the notes to give a model answer and a Strength / Gap / Retry coaching card.
The microphone opens again after the coaching audio finishes. Normal pause detection
and interruptions remain provider-managed outside a timeout.

History saves session text, feedback, source notes and date in localStorage on this
browser. No audio is recorded. Review, download or delete a session from the history
list. The list keeps the most recent 50 sessions. Private browsing, cleared site data
or storage errors can remove or prevent history; download important sessions.
The FastAPI server still relays data in memory and does not store recordings or notes.

Code map: `core.js` has `answerTimer`, `timeoutInstructions` and `historyStore`.
The `ASSETS` in `server.py` contain the UI and `app.js` audio/history wiring.
`test-features.js` tests deadlines, Off mode, local saves, reloads and storage failures.
Run `node test-core.js && node test-features.js && python3 test_backend.py`.

## Study notes, PDF import and visible model answers

Notes accept up to 48,000 characters and 300 numbered source chunks. This replaces
12,000 characters in the textarea and the old silent 60-line cut-off. Long paragraphs
are split into 1,000-character source chunks; no accepted text is silently dropped.
The backend bounds system prompts at 64,000 characters, including note IDs and coaching
instructions. Audio frames remain capped at 1 MiB. Hourly and five-minute session caps
are unchanged. Bigger notes may be slower; choose relevant chapters for each session.

Import a text PDF up to 10 MB and 100 pages. PDF.js 5.5.207 runs in the browser and
loads on demand from jsDelivr. The PDF itself is not sent to this app's server or the
CDN. Extracted text replaces the notes only after extraction succeeds and you confirm
replacement. Check the text before starting; columns and tables may read out of order.
Scanned/image-only PDFs need OCR first. Password-protected files need an unlocked copy.
This is text extraction, not OCR. Starting a viva still sends extracted notes, audio
and transcripts to AssemblyAI under its policies, just like pasted notes.

A timed-out answer appears in a separate Model answer block. It shows the examiner's
spoken model-answer text and is labeled AI-generated; check it against your notes.
Visible model answers are saved with local history and downloads. Exact-quote feedback
cards remain a separate strict check. Neither notes nor PDFs are stored on the server.

Code map: `prepareNotes`, `pdfFileCheck`, `pdfPageText`, and `modelAnswerText` in
`core.js`; `showModelAnswer` and the PDF file-input handler in embedded `app.js`;
`validate_browser_message` in `server.py` checks the maximum study context.
