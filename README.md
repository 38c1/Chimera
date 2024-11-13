# Chimera Scratch API

**Chimera** lets you sign into your Scratch account through your `session_id` and read/write Cloud Variables.

**Chimera** is lightweight and neatly fits into one Python file.

<img src="media/Chimera.svg" alt="Description of Image" width="50%" />

![GitHub license](https://badgen.net/github/license/38c1/Chimera)
![Stable release](https://badgen.net/github/release/38c1/Chimera/stable)

## Quick Start

To get started, you can load Chimera directly by executing this Python code:

```python
import requests
exec(requests.get("https://raw.githubusercontent.com/38c1/Chimera/refs/heads/main/chimera.py").text)
