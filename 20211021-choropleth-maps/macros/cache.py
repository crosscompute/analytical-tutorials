import json
from os import getenv
from os.path import expanduser, join, relpath
from tempfile import mkstemp
from urllib.request import urlretrieve

from .disk import make_folder


def cache_download(uri):
    folder = getenv('CACHE_FOLDER', join(
        expanduser('~'), '.cache', 'invisibleroads-macros'))
    return URICache(folder).get_or_set(uri, urlretrieve)


class URICache:

    def __init__(self, folder):
        self.folder = make_folder(folder)

    @property
    def _index_path(self):
        return join(self.folder, 'index.json')

    def _load_relative_path_by_uri(self):
        source_path = self._index_path
        try:
            relative_path_by_uri = json.load(open(source_path, 'rt'))
        except OSError:
            raise
        return relative_path_by_uri

    def _save_relative_path_by_uri(self, relative_path_by_uri):
        target_path = self._index_path
        json.dump(relative_path_by_uri, open(target_path, 'wt'))
        return target_path

    def get(self, uri):
        try:
            relative_path_by_uri = self._load_relative_path_by_uri()
        except OSError:
            return
        if uri not in relative_path_by_uri:
            return
        relative_path = relative_path_by_uri[uri]
        return join(self.folder, relative_path)

    def set(self, uri, download):
        try:
            relative_path_by_uri = self._load_relative_path_by_uri()
        except OSError:
            relative_path_by_uri = {}
        path = mkstemp(dir=self.folder, prefix='')[1]
        download(uri, path)
        relative_path_by_uri[uri] = relpath(path, self.folder)
        self._save_relative_path_by_uri(relative_path_by_uri)
        return path

    def get_or_set(self, uri, download):
        path = self.get(uri)
        if not path:
            path = self.set(uri, download)
        return path

    def clear(self, uri=None):
        try:
            relative_path_by_uri = self._load_relative_path_by_uri()
        except OSError:
            return
        if uri:
            try:
                relative_path_by_uri.pop(uri)
            except KeyError:
                return
        else:
            relative_path_by_uri = {}
        json.dump(relative_path_by_uri, open(self._index_path, 'wt'))