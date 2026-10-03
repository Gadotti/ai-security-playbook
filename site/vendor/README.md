# Vendored libraries

Pinned copies of the third-party scripts the explorer needs, served from this repo instead of a CDN so the site works offline and can't silently change under us (see [LLM04: Supply Chain](../../docs/owasp-llm/LLM04.md)). Each file keeps its upstream license header.

*Downloaded 2026-09-27.*

| File | Library | Version | License | Source | SHA-256 |
|---|---|---|---|---|---|
| `marked.min.js` | marked | 12.0.2 | MIT | https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js | `15fabce5b65898b32b03f5ed25e9f891a729ad4c0d6d877110a7744aa847a894` |
| `purify.min.js` | DOMPurify | 3.1.6 | Apache-2.0 / MPL-2.0 | https://cdn.jsdelivr.net/npm/dompurify@3.1.6/dist/purify.min.js | `c0845096a7c4a6741f362ac506c94c1c7d27dc603bcc1bf64a587f76f2dbe3a1` |
| `highlight.min.js` | highlight.js (common languages) | 11.9.0 | BSD-3-Clause | https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js | `837a6fa5b0c736b52bbde2b2b6190f305da3fc9ed41681db5321507057b5c846` |
| `hljs-dockerfile.min.js` | highlight.js Dockerfile grammar | 11.9.0 | BSD-3-Clause | https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/dockerfile.min.js | `436757dd11b42ca83c2092e33bd05280344c1f716991289c843f9587d601ee4d` |
| `js-yaml.min.js` | js-yaml | 4.1.0 | MIT | https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js | `45dc3dd03dc07a06705a2c2989b8c7f709013f04bd5386e3279d4e447f07ebd7` |

Not vendored (too large, about 10 MB): **Pyodide v0.26.4**, loaded from `https://cdn.jsdelivr.net/pyodide/v0.26.4/full/` only when a lab's **Run** button is pressed. The version is pinned in `PYODIDE_URL` in [`../assets/app.js`](../assets/app.js).

Verify the files match the table:

```bash
cd site/vendor && sha256sum *.js
```
