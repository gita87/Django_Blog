from django import forms
from django.utils.safestring import mark_safe


class TrixEditorWidget(forms.Widget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.legend_text = attrs.pop('legend_text', None) if attrs else None

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs, {'id': attrs['id'] if attrs and 'id' in attrs else None})
        if value is None:
            value = ''

        trix_editor = f'<trix-editor input="{final_attrs["id"]}" class="trix-content" role="textbox" trix-id="1" id="myTrixEditor">{value}</trix-editor>'

        return mark_safe(trix_editor)
