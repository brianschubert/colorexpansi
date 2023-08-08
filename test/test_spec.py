import colorexpansi._ansi as ansi
import colorexpansi._spec as color_spec


def test_parser() -> None:
    cases = [
        (
            "r",
            ansi.ConcatenatedSequence(
                [ansi.Color16ControlSequence(ansi.StandardColor.RED)]
            ),
        ),
        (
            "r.g",
            ansi.ConcatenatedSequence(
                [
                    ansi.Color16ControlSequence(
                        ansi.StandardColor.RED, region="foreground"
                    ),
                    ansi.Color16ControlSequence(
                        ansi.StandardColor.GREEN, region="background"
                    ),
                ]
            ),
        ),
        (
            "r.g+i",
            ansi.ConcatenatedSequence(
                [
                    ansi.Color16ControlSequence(
                        ansi.StandardColor.RED, region="foreground"
                    ),
                    ansi.Color16ControlSequence(
                        ansi.StandardColor.GREEN, region="background"
                    ),
                    ansi.GraphicsModeControlSequence(
                        ansi.GraphicsMode.ITALIC, set=True
                    ),
                ]
            ),
        ),
        (
            "r.g-u",
            ansi.ConcatenatedSequence(
                [
                    ansi.Color16ControlSequence(
                        ansi.StandardColor.RED, region="foreground"
                    ),
                    ansi.Color16ControlSequence(
                        ansi.StandardColor.GREEN, region="background"
                    ),
                    ansi.GraphicsModeControlSequence(
                        ansi.GraphicsMode.UNDERLINE, set=False
                    ),
                ]
            ),
        ),
        (
            "r.g+i-u",
            ansi.ConcatenatedSequence(
                [
                    ansi.Color16ControlSequence(
                        ansi.StandardColor.RED, region="foreground"
                    ),
                    ansi.Color16ControlSequence(
                        ansi.StandardColor.GREEN, region="background"
                    ),
                    ansi.GraphicsModeControlSequence(
                        ansi.GraphicsMode.ITALIC, set=True
                    ),
                    ansi.GraphicsModeControlSequence(
                        ansi.GraphicsMode.UNDERLINE, set=False
                    ),
                ]
            ),
        ),
    ]

    for spec, expected_seq in cases:
        actual_seq = color_spec.parse_control(spec)
        assert actual_seq == expected_seq
