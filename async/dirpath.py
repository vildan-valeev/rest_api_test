import shutil
import tempfile


def setup_dir(app):
    dirpath = tempfile.mkdtemp(prefix='aiohttp-session-')

    def remove_dir(app):
        shutil.rmtree(dirpath)

    app.on_cleanup.append(remove_dir)
    return dirpath