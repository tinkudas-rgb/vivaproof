# Third-party attribution

Audio capture/playback and Voice Agent API plumbing were adapted from
AssemblyAI's official Python starter:
https://github.com/AssemblyAI/voice-agent-starter-python

The source was inspected on September 30, 2026. Its root and README did not
include an explicit license declaration. No upstream MIT license is claimed
or invented here. VivaProof's MIT license covers original VivaProof
contributions only; rights in third-party material remain with its owner.

The starter is linked from AssemblyAI's Voice Agent API documentation:
https://www.assemblyai.com/docs/voice-agents/voice-agent-api

## PDF.js

Browser PDF text extraction uses Mozilla PDF.js (pdfjs-dist 5.5.207), Apache-2.0,
loaded on demand from jsDelivr. Source: https://github.com/mozilla/pdf.js
License: https://github.com/mozilla/pdf.js/blob/master/LICENSE
The PDF bytes remain in the browser; the CDN serves only the parser code.
