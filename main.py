import drawSvg as draw
from flask import Response
from google.cloud import firestore

N_DIGITS = 6
DIGIT_WIDTH = 40
DIGIT_HEIGHT = 60


def get_digits(n):
    """return list of single-character strings, left-to-right the digits of n,
    zero-padded to N_DIGITS.
    Raise AssertionError if n exceeds representable digits"""

    fmtstr = f'{{:0{N_DIGITS}d}}'
    digits = list(fmtstr.format(n))
    assert len(digits) == N_DIGITS, f'Overflow trying to fit {n}' \
                                    f'into {N_DIGITS} digits'

    return digits


def draw_counter(n):
    """Given integer n, returns a drawSVG.Drawing representing n"""
    d = draw.Drawing(
        width=N_DIGITS * DIGIT_WIDTH,
        height=DIGIT_HEIGHT
    )

    g = draw.LinearGradient(0, 0, 0, DIGIT_HEIGHT)
    g.addStop(0, 'black')
    g.addStop(0.5, '#666')
    g.addStop(1, 'black')

    d.draw(draw.Rectangle(
        0,
        0,
        width=N_DIGITS * DIGIT_WIDTH,
        height=DIGIT_HEIGHT,
        fill=g
    ))

    for x in range(-1, N_DIGITS+1):
        d.draw(
            draw.Line(
                x*DIGIT_WIDTH,
                0,
                x*DIGIT_WIDTH,
                DIGIT_HEIGHT,
                stroke_width=8,
                stroke='#222'
            )
        )

    for digit, x in zip(get_digits(n), range(N_DIGITS)):
        d.draw(
            draw.Text(
                digit,
                fontSize=DIGIT_HEIGHT,
                x=(x+.5)*DIGIT_WIDTH,
                y=DIGIT_HEIGHT*.65,
                fill='white',
                font_family='courier, MONOSPACE',
                center=True
            ))

    return d


def test_counter(request):
    """GCF entrypoint: returns svg payload of counter displaying "69"."""
    return draw_counter(69).asSvg()


def get_counter(request):
    """GCF entrypoint: retrieves counter state from firestore, initializing if
    necessary.
    Increments this and persists to firestore, returning svg payload of counter
    displaying new count"""

    db = firestore.Client()
    doc_ref = db.collection(u'counter').document(u'count')
    doc = doc_ref.get()
    old_n = doc.get(u'n') if doc.exists else 0

    n = old_n + 1
    doc_ref.set({u'n': n})

    return Response(draw_counter(n).asSvg(), mimetype='image/svg+xml')
