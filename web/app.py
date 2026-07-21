"""App Flask: gestión visual de perfiles de empresa y generación de carruseles."""
from __future__ import annotations

from pathlib import Path

from flask import (Flask, abort, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

from agent import config, copywriter, pipeline, store

ALLOWED_LOGO = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"}

app = Flask(__name__)
app.secret_key = "social-agent-dev"  # solo para mensajes flash en local
config.ensure_dirs()


@app.route("/")
def index():
    return render_template("index.html", profiles=store.list_profiles())


@app.route("/profiles", methods=["POST"])
def create_profile():
    name = (request.form.get("name") or "").strip()
    if not name:
        flash("El nombre de la empresa es obligatorio.", "error")
        return redirect(url_for("index"))

    profile = store.create_profile(
        name=name,
        website=request.form.get("website", ""),
        sector=request.form.get("sector", ""),
        handle=request.form.get("handle", ""),
    )
    _save_logo(profile["id"], request.files.get("logo"))

    # Analiza la web + logo en el momento de crear el perfil.
    try:
        pipeline.analyze_profile(profile["id"])
        flash(f"Perfil «{name}» creado y analizado.", "ok")
    except Exception as exc:  # noqa: BLE001
        flash(f"Perfil creado, pero el análisis falló: {exc}", "warn")
    return redirect(url_for("profile", profile_id=profile["id"]))


@app.route("/profiles/<profile_id>")
def profile(profile_id):
    p = store.get_profile(profile_id)
    if not p:
        abort(404)
    return render_template(
        "profile.html", p=p, posts=pipeline.list_posts(profile_id),
        pillars=copywriter.PILLARS,
    )


@app.route("/profiles/<profile_id>/logo", methods=["POST"])
def update_logo(profile_id):
    if not store.get_profile(profile_id):
        abort(404)
    if _save_logo(profile_id, request.files.get("logo")):
        pipeline.analyze_profile(profile_id)
        flash("Logo actualizado y marca re-analizada.", "ok")
    else:
        flash("No se subió ningún logo válido.", "error")
    return redirect(url_for("profile", profile_id=profile_id))


@app.route("/profiles/<profile_id>/reanalyze", methods=["POST"])
def reanalyze(profile_id):
    if not store.get_profile(profile_id):
        abort(404)
    try:
        kit = pipeline.analyze_profile(profile_id)
        msg = "Marca re-analizada." + (f" Aviso: {kit['error']}" if kit.get("error") else "")
        flash(msg, "ok" if not kit.get("error") else "warn")
    except Exception as exc:  # noqa: BLE001
        flash(f"El análisis falló: {exc}", "error")
    return redirect(url_for("profile", profile_id=profile_id))


@app.route("/profiles/<profile_id>/generate", methods=["POST"])
def generate(profile_id):
    if not store.get_profile(profile_id):
        abort(404)
    pillar = request.form.get("pillar", "problema_solucion")
    try:
        post = pipeline.generate_carousel(profile_id, pillar)
        flash(f"Carrusel «{post['pillar_label']}» generado ({len(post['slides'])} slides).", "ok")
    except Exception as exc:  # noqa: BLE001
        flash(f"No se pudo generar el carrusel: {exc}", "error")
    return redirect(url_for("profile", profile_id=profile_id))


@app.route("/profiles/<profile_id>/delete", methods=["POST"])
def delete(profile_id):
    store.delete_profile(profile_id)
    flash("Perfil eliminado.", "ok")
    return redirect(url_for("index"))


@app.route("/media/<profile_id>/<path:filename>")
def media(profile_id, filename):
    """Sirve logos e imágenes de carruseles desde la carpeta de datos."""
    base = store.profile_dir(profile_id)
    return send_from_directory(base, filename)


def _save_logo(profile_id: str, file) -> bool:
    if not file or not file.filename:
        return False
    ext = Path(secure_filename(file.filename)).suffix.lower()
    if ext not in ALLOWED_LOGO:
        return False
    dest_name = f"logo{ext}"
    file.save(store.profile_dir(profile_id) / dest_name)
    store.update_profile(profile_id, logo=dest_name)
    return True


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
