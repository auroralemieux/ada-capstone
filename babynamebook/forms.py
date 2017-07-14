
from django.core.exceptions import ValidationError
from django import forms

from .models import Book

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'tree_upload',)

    def clean_tree_upload(self):
        file = self.cleaned_data['tree_upload']
        try:
            if file:
                file_type = file.content_type.split('/')[1]
                print(file_type)
                print(file.name)

                if len(file.name.split('.')) == 1:
                    raise forms.ValidationError(_('File type is not supported'))

                if file_type not in settings.TASK_UPLOAD_FILE_TYPES:
                    raise forms.ValidationError(_('File type is not supported'))
        except:
            pass

        return file
    # def clean_file(self):
    #     yourfile = self.cleaned_data.get("tree_upload", False)
    #     filetype = magic.from_buffer(yourfile.read())
    #     if not "application/ged" in filetype:
    #         raise ValidationError("File is not GED.")
    #     return yourfile

    # def clean_tree(self):
    #     file = self.cleaned_data.get('tree_upload')
    #     mime = magic.from_buffer(file.read(), mime=True)
    #     print(mime)
    #     if not mime == 'application/ged':
    #         raise forms.ValidationError('File must be a GED document')
    #     else:
    #         return file
