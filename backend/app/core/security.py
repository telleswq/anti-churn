import secrets


def generate_api_key() -> str:
    """
    Gera uma API Key segura para autenticação de tenants.
    Formato `sk_` facilita identificação nos logs e em scanners de secrets.
    token_urlsafe(32) → 43 caracteres base64url → ~256 bits de entropia.
    """
    return f"sk_{secrets.token_urlsafe(32)}"
