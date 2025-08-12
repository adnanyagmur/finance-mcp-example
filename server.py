# Basit FastMCP sunucusu: Truncgil 'today.json' verisini araçlar olarak sunar
# Not: Küçük ve hedefe yönelik yorumlar eklendi (neden'leri vurgular)
from __future__ import annotations

from typing import Any, Dict

import httpx
from fastmcp import Context, FastMCP


mcp = FastMCP("Finance MCP")  # Sunucu adı: IDE/istemcide görünecek kimlik


async def _fetch_truncgil_today(ctx: Context | None = None) -> Dict[str, Any]:
    """Truncgil 'today.json' verisini ham haliyle döndürür (yardımcı).

    Doğru uç‑nokta: https://finans.truncgil.com/today.json
    """

    url = "https://finans.truncgil.com/today.json"
    timeout_seconds = 10.0  # Ağ çağrısı için makul zaman aşımı

    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.get(url)
            response.raise_for_status()
    except httpx.RequestError as exc:
        # Ağ/DNS/bağlantı hatalarını kullanıcıya okunur şekilde ilet
        if ctx is not None:
            await ctx.error(f"Truncgil isteği başarısız: {exc}")
        return {
            "source": "truncgil",
            "error": "request_error",
            "message": str(exc),
        }
    except httpx.HTTPStatusError as exc:
        # 4xx/5xx durumlarını açık bir hata yapısı ile döndür
        if ctx is not None:
            await ctx.error(f"Truncgil HTTP hatası: {exc}")
        return {
            "source": "truncgil",
            "error": "http_status_error",
            "status_code": exc.response.status_code if exc.response is not None else None,
            "message": str(exc),
        }

    try:
        payload = response.json()
    except ValueError as exc:  # JSON decode error
        # Beklenmeyen/bozuk JSON’a karşı koruma
        if ctx is not None:
            await ctx.error(f"Truncgil JSON ayrıştırma hatası: {exc}")
        return {
            "source": "truncgil",
            "error": "invalid_json",
            "message": str(exc),
        }

    return payload


@mcp.tool
async def finance_truncgil_get_today(ctx: Context | None = None) -> Dict[str, Any]:
    """Truncgil Finance 'today.json' verisinin tamamını döndürür (parametresiz)."""
    payload = await _fetch_truncgil_today(ctx)

    if isinstance(payload, dict) and payload.get("error"):
        # Hata nesnesini doğrudan döndür
        return payload

    # Alan adları kaynakta farklı yazılabildiği için alternatifleri kontrol et
    update_date = payload.get("Update_Date") or payload.get("update_date") or payload.get("last_update")

    return {
        "source": "truncgil",
        "update_date": update_date,
        "data": payload,
    }


@mcp.tool
async def finance_truncgil_get_symbol(symbol: str, ctx: Context | None = None) -> Dict[str, Any]:
    """Tek bir sembol veya üst seviye anahtar için Truncgil verisini döndürür.

    Örn: symbol="USD" veya belgedeki başka bir üst seviye alan.
    """

    # Neden doğrudan helper çağrısı? Başka tool’u çağırmak (FunctionTool) yerine
    # ham veriyi alıp tek anahtarı seçmek, istemci/sunucu akışını sadeleştirir.
    payload = await _fetch_truncgil_today(ctx)

    if isinstance(payload, dict) and payload.get("error"):
        return payload

    # Tarih alanı çeşitli isimlerle gelebilir
    update_date = payload.get("Update_Date") or payload.get("update_date") or payload.get("last_update")
    value = payload.get(symbol)

    if value is None:
        # Sembol yoksa açık bir durum bilgisi ver
        if ctx is not None:
            await ctx.info(f"İstenen sembol bulunamadı: {symbol}")
        return {
            "source": "truncgil",
            "symbol": symbol,
            "error": "not_found",
            "message": f"Sembol bulunamadı: {symbol}",
        }

    return {
        "source": "truncgil",
        "symbol": symbol,
        "update_date": update_date,
        "value": value,
    }


if __name__ == "__main__":
    mcp.run()


