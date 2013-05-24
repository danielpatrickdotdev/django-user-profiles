import os
from django.core.files.storage import FileSystemStorage

class OverwriteFileSystemStorage(FileSystemStorage):
    '''Custom Storage model to overwrite image if one already exists
    with that name. Note that currently it will not remove icons with
    same slug but different file extension (#TODO).
    '''
    def get_available_name(self, name):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name