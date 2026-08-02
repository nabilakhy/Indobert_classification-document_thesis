import html


def safe_text(value):
    return html.escape(str(value))


def score_to_percent(score):
    return max(0.0, min(float(score) * 100, 100.0))
