
def validar_horizonte(horizonte: int) -> int:
    """Valida que el horizonte esté entre 1 y 16 días."""
    if not 1 <= horizonte <= 16:
        raise ValueError("El horizonte debe estar entre 1 y 16 días.")

    return horizonte
