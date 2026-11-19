
import pytest

from retail_forecasting.config.validation import validar_horizonte


@pytest.mark.parametrize("horizonte", [1, 8, 16])
def test_horizonte_valido(horizonte: int) -> None:
    assert validar_horizonte(horizonte) == horizonte


@pytest.mark.parametrize("horizonte", [0, -1, 17, 30])
def test_horizonte_invalido(horizonte: int) -> None:
    with pytest.raises(ValueError, match="entre 1 y 16 días"):
        validar_horizonte(horizonte)
