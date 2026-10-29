# linkvertise bypass

> a fast, proxy-aware bypasser for linkvertise access pages. built around the real graphql task flow.

**written by [cheapai.gay](https://cheapai.gay/) / deepthroat ai.**

---

## what it does

- takes a `linkvertise.com/access/<user>/<slug>` url
- replays the real `getContent` / `completeTask` graphql flow
- handles `WaitTask` and `AdTask` steps automatically
- returns the final destination url or paste

> [!WARNING]
> linkvertise will quickly patch this bypass if they are smart enough. the flow above is exactly what their own frontend does, so all it takes is a server-side check on `completion_token` timing or a new task type. treat this as a snapshot, not a permanent solution.

---

## how it works

```mermaid
flowchart TD
    A[getContent] --> B{task type}
    B -->|WaitTask| C[completeTask]
    B -->|AdTask| D[read completion_token + session_id]
    D --> C
    C --> A
    A -->|DetailPageTargetData| E[return url / paste]
```

| step | operation | notes |
|------|-----------|-------|
| 1 | `getContent` | fetch current task set |
| 2 | `completeTask` | wait task, no token |
| 3 | `getContent` | now returns ad tasks |
| 4 | `completeTask` | needs `completion_token` + taboola `session_id` |
| 5 | `getContent` | repeats until target data |

---

## stack

- `fastapi` for the http layer
- `curl_cffi` with `chrome150` tls fingerprint
- optional proxy rotation from `data/proxies.txt`

---

## layout

```text
.
├── data/
│   ├── config.json
│   └── proxies.txt
├── src/
│   ├── config.py
│   ├── link/
│   │   ├── parser.py
│   │   └── queries.py
│   ├── session/
│   │   ├── client.py
│   │   └── proxies.py
│   ├── tasks/
│   │   └── flow.py
│   └── web/
│       └── api.py
└── entry.py
```

---

## install

```bash
pip install fastapi uvicorn curl_cffi
```

---

## run

```bash
python entry.py
```

---

## usage

### request

```bash
curl -X POST http://127.0.0.1:8000/bypass \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://linkvertise.com/access/4768145/AE0PTnbpMtju\"}"
```

### response

```json
{
  "ok": true,
  "result": {
    "type": "URL",
    "destination": "https://www.mediafire.com/file/.../file",
    "raw": {
      "url": "https://www.mediafire.com/file/.../file",
      "paste": null
    }
  }
}
```

---

## config

`data/config.json`:

```json
{
  "tls": {
    "impersonate": "chrome150",
    "timeout": 30
  },
  "proxies": {
    "enabled": true,
    "file": "data/proxies.txt",
    "rotation": "roundrobin",
    "scheme": "http"
  },
  "http": {
    "graphql": "https://publisher.linkvertise.com/graphql",
    "pageTemplate": "https://linkvertise.com/access/{userId}/{slug}",
    "origin": "https://linkvertise.com",
    "referer": "https://linkvertise.com/"
  },
  "flow": {
    "maxSteps": 30,
    "pollInterval": 1,
    "maxWaitSeconds": 120,
    "fallbackUserId": "fallbackUserId"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "endpoint": "/bypass"
  }
}
```

---

## proxies

`data/proxies.txt`, one per line:

```text
# http://user:pass@host:port
127.0.0.1:8080
http://user:pass@1.2.3.4:3128
```

scheme is auto-added if missing. blank lines and `#` comments ignored.

---

## limitations

- ad tasks may require a real countdown on some links
- taboola session ids expire fast
- captcha-gated links are not handled
- **linkvertise will quickly patch this bypass if they are smart enough**

---

## credits

written by **[cheapai.gay](https://cheapai.gay/)** / **deepthroat ai**.