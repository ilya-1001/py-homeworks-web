from flask import Flask, jsonify, request
from flask.views import  MethodView

from models import Ad, Session
from sqlalchemy.exc import IntegrityError
from errors import HttpError

app = Flask("ad")


@app.errorhandler(HttpError)
def http_handler(err: HttpError):
    http_responce = jsonify({"error": err.message})
    http_responce.status_code = err.status_code
    return http_responce


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


def get_ad(ad_id: int):
    ad = request.session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, "ad not found")
    return ad


def add_ad(ad: Ad):
    request.session.add(ad)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "ad already exists")


class AdView(MethodView):
    def get(self, ad_id: int):
        ad = get_ad(ad_id)
        return jsonify(ad.id_dict)

    def post(self):
        data = request.json
        ad = Ad(title=data["title"], description=data["description"],
                owner=data["owner"])
        add_ad(ad)
        return jsonify(ad.id_dict)

    def patch(self, ad_id: int):
        data = request.json
        ad = get_ad(ad_id)

        if data.get("title"):
            ad.title = data["title"]
        if data.get("description"):
            ad.description = data["description"]
        if data.get("owner"):
            ad.owner = data["owner"]

        add_ad(ad)
        return jsonify(ad.id_dict)

    def delete(self, ad_id: int):
        ad = get_ad(ad_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify({"message": "ad deleted"})


ad_view = AdView.as_view("ad_view")


app.add_url_rule("/api/v1/ads/<int:ad_id>", view_func=ad_view,
                 methods=["GET", "PATCH", "DELETE"])
app.add_url_rule("/api/v1/ads", view_func=ad_view,
                 methods=["POST"])

app.run()
