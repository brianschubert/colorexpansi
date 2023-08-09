import colorexpansi._ansi as ansi
import colorexpansi._spec as color_spec


def test_parser() -> None:
    cases = [
        (
            "r",
            ansi.ConcatenatedCS([ansi.Color16CS(ansi.StandardColor.RED)]),
        ),
        (
            "r.g",
            ansi.ConcatenatedCS(
                [
                    ansi.Color16CS(ansi.StandardColor.RED, region="foreground"),
                    ansi.Color16CS(ansi.StandardColor.GREEN, region="background"),
                ]
            ),
        ),
        (
            "r.g+i",
            ansi.ConcatenatedCS(
                [
                    ansi.Color16CS(ansi.StandardColor.RED, region="foreground"),
                    ansi.Color16CS(ansi.StandardColor.GREEN, region="background"),
                    ansi.GraphicsModeCS(ansi.GraphicsMode.ITALIC, set=True),
                ]
            ),
        ),
        (
            "r.g-u",
            ansi.ConcatenatedCS(
                [
                    ansi.Color16CS(ansi.StandardColor.RED, region="foreground"),
                    ansi.Color16CS(ansi.StandardColor.GREEN, region="background"),
                    ansi.GraphicsModeCS(ansi.GraphicsMode.UNDERLINE, set=False),
                ]
            ),
        ),
        (
            "r.g+i-u",
            ansi.ConcatenatedCS(
                [
                    ansi.Color16CS(ansi.StandardColor.RED, region="foreground"),
                    ansi.Color16CS(ansi.StandardColor.GREEN, region="background"),
                    ansi.GraphicsModeCS(ansi.GraphicsMode.ITALIC, set=True),
                    ansi.GraphicsModeCS(ansi.GraphicsMode.UNDERLINE, set=False),
                ]
            ),
        ),
    ]

    for spec, expected_seq in cases:
        actual_seq = color_spec.parse_control(spec)
        assert actual_seq == expected_seq
