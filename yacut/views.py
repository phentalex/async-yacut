from flask import redirect, render_template

from . import app
from .forms import URLForm, UploadFileForm
from .models import URLMap
from .yandexdisk import async_upload_files_to_yandex_disk


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
        try:
            url_map = URLMap.create(
                original=form.original_link.data,
                custom_id=form.custom_id.data
            )
        except ValueError as e:
            form.custom_id.errors.append(str(e))
            return render_template('main.html', form=form)
        return render_template(
            'main.html',
            form=form,
            short_url=url_map.get_short_url()
        )
    return render_template('main.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def upload_files_view():
    """Страница для загрузки файлов."""
    form = UploadFileForm()

    if form.validate_on_submit():
        files = form.files.data
        urls = await async_upload_files_to_yandex_disk(files)
        url_maps = []
        for url in urls:
            try:
                url_map = URLMap.create(original=url)
            except ValueError:
                continue
            url_maps.append(url_map)
        return render_template(
            'upload_files.html',
            form=form,
            file_url_pairs=zip(files, url_maps)
        )
    return render_template('upload_files.html', form=form)