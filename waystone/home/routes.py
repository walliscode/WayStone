from . import bp


@bp.route("/")
def home():
    return "Muthafucka!"
