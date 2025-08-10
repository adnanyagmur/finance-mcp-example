## Finance MCP — FastMCP + Truncgil Örneği

Basit bir MCP sunucusu. `fastmcp` ile çalışır, Truncgil `today.json` uç‑noktasından veri çeker ve iki tool sağlar:

- `finance_truncgil_get_today(keys: Optional[list[str]])`
- `finance_truncgil_get_symbol(symbol: str)`

Veri kaynağı (doğru uç‑nokta): `https://finans.truncgil.com/today.json`

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
Varsayılan transport: STDIO. MCP uyumlu istemciler bu süreçle konuşarak araçları çağırabilir.

### Hızlı test (demo istemci)
```bash
python demo_client.py
```
Bu script, yerel MCP sunucusuna bağlanır ve iki tool’u çağırır.

### Cursor entegrasyonu (opsiyonel)
`.cursor/mcp.json` yerine ayarlardan eklemek önerilir. Örnek yapılandırma:
```json
{
  "mcpServers": {
    "finance": {
      "command": "/Users/<your-username>/Desktop/projects/mcp-example/.venv/bin/python",
      "args": ["/Users/<your-username>/Desktop/projects/mcp-example/server.py"]
    }
  }
}
```
Ardından Cursor'a reload atınız. Chat’te ayarlar Agent mod ve Auto modda ilken "Bana usd try paritesini ver" gibi bir komutla çalıştırabilirsiniz.

### Örnek çağrılar
- `finance_truncgil_get_today` girdi örneği: `{ "keys": ["USD", "EUR"] }`
- `finance_truncgil_get_symbol` girdi örneği: `{ "symbol": "USD" }`

### Notlar
- IDE import uyarıları için yorumlayıcıyı `.venv/bin/python` olarak seçin. Pyright için `pyrightconfig.json` eklenmiştir.
- `.cursor/` klasörü `.gitignore`’dadır; public repo’ya yerel MCP ayarlarını koymayın.

### Kaynaklar
- FastMCP: [GitHub — jlowin/fastmcp](https://github.com/jlowin/fastmcp?tab=readme-ov-file&source=post_page-----6c7c1ce5b996---------------------------------------)
- Truncgil Docs: [finance.truncgil.com/docs#/](https://finance.truncgil.com/docs#/)

