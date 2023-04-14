import plotly.io as pio
import pytest

from nerv.callbacks import switch_template_func


@pytest.mark.parametrize(
    "switch, template1, template2",
    [(True, "plotly_dark", "simple_white"), (False, "plotly_dark", "simple_white")],
)
def test_switch_template_fuc(switch, histogram, scatter, template1, template2):
    template = template1 if switch else template2
    output = switch_template_func(switch, histogram, scatter, template1, template2)
    assert output[0]["layout"]["template"] == pio.templates[template]
    assert output[1]["layout"]["template"] == pio.templates[template]
