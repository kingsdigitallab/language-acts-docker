from typing import List, Union

from django.conf import settings
from django.contrib.admin.utils import unquote
from django.db.models import Model
from django.shortcuts import get_object_or_404
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.snippets.views.snippets import get_snippet_model_from_url_params

"""
Bibliographic reference snippet chooser views
Adapted from the wagtail snippet chooser views
https://github.com/wagtail/wagtail/blob
/1f2b6fb449781fba0bcd313cca0158812a9bb1e6/wagtail/snippets/views/chooser.py

"""


def get_reference_model() -> List[Union[str, str, Model]]:
    if settings.REFERENCE_MODEL:
        ref_models = settings.REFERENCE_MODEL
        app_label = ''
        model_name = ''
        for model in ref_models.keys():
            # Right now we're assuming one entry
            # could be refactored to allow an initial step of choosing
            # ref type
            app_label, model_name = model.split(",")

        return [
            app_label,
            model_name,
            get_snippet_model_from_url_params(app_label, model_name.lstrip())
        ]


def chosen(request, pk):
    app_label, model_name, model = get_reference_model()
    item = get_object_or_404(model, pk=unquote(pk))
    p = item.get_usage()[0]
    # bibliography_url = p.url+'#entry-{}'.format(p.pk)
    # If a slug has been specified, use that
    # if len(settings.REFERENCE_MODEL[model]) > 0:
    #     app_name, model_name = settings.REFERENCE_MODEL[
    #         model].split(",")
    #     page_model = apps.get_model(app_name, model_name.lstrip())
    #     page = Page.objects.get(slug=settings.REFERENCE_MODEL[model])
    # else:
    #     items = model.objects.all()

    snippet_data = {
        'reference_id': str(item.pk),
        'page_id': str(p.pk),
        # 'edit_link': reverse('wagtailsnippets:edit', args=(
        #     app_label, model_name, quote(item.pk)))
    }

    return render_modal_workflow(
        request,
        None, None,
        None, json_data={'step': 'chosen', 'result': snippet_data}
    )
