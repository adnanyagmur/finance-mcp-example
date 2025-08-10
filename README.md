## Finance MCP — FastMCP + Truncgil Örneği

Basit bir MCP sunucusu. `fastmcp` ile çalışır, `finance.truncgil.com` üzerindeki `v4/today.json` uç‑noktasından veri çeker ve iki tool sağlar:

- `finance_truncgil_get_today(keys: Optional[list[str]])`
- `finance_truncgil_get_symbol(symbol: str)`

### Kurulum
1) Python 3.10+ gereklidir.
2) Sanal ortam (önerilir):
```bash
python -m venv .venv && source .venv/bin/activate
```
3) Bağımlılıklar:
```bash
pip install -r requirements.txt
```

### Çalıştırma
```bash
python server.py
```
Varsayılan olarak STDIO transport ile başlar. Bir MCP istemcisi (IDE veya CLI) üzerinden araçlar çağrılabilir.

### İstemci (örnek)
`fastmcp.Client` ile test etmek için `demo_client.py` scriptini kullanabilirsiniz.

```bash
python demo_client.py
```

### Kaynaklar
- FastMCP: [GitHub — jlowin/fastmcp](https://github.com/jlowin/fastmcp?tab=readme-ov-file&source=post_page-----6c7c1ce5b996---------------------------------------)
- Truncgil Finance API: [finance.truncgil.com/docs#/](https://finance.truncgil.com/docs#/)


