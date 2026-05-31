from flask import redirect, render_template

from yacut.utils import get_unique_short_id
from yacut.yandexdisk import async_upload_files_to_yandex_disk

from . import app, db
from .forms import URLForm, UploadFileForm
from .models import URLMap


def create_url_map(original, custom_id=None):
    short_id = get_unique_short_id(custom_id=custom_id)
    if not short_id:
        return None
    url_map = URLMap(original=original, short=short_id)
    db.session.add(url_map)
    db.session.commit()
    return url_map


@app.route('/<string:short>')
def redirect_view(short):
    """Перенаправление по короткой ссылке."""
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница."""
    form = URLForm()

    if form.validate_on_submit():
        url_map = create_url_map(form.original_link.data, form.custom_id.data)
        if not url_map:
            form.custom_id.errors.append(
                'Предложенный вариант короткой ссылки уже существует.'
            )
            return render_template('main.html', form=form)
        return render_template('main.html', form=form, short_url=url_map.short)
    return render_template('main.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
async def upload_files_view():
    """Страница для загрузки файлов."""
    form = UploadFileForm()

    if form.validate_on_submit():
        files = form.file.data
        urls = await async_upload_files_to_yandex_disk(files)
        short_urls = []
        for url in urls:
            url_map = URLMap(
                original=url,
                short=get_unique_short_id()
            )
            db.session.add(url_map)
            short_urls.append(url_map.short)
        db.session.commit()
        return render_template(
            'upload_files.html',
            form=form,
            file_url_pairs=zip(files, short_urls)
        )
    return render_template('upload_files.html', form=form)