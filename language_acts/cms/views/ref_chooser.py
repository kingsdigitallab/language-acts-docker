from typing import List, Union

from django.apps import apps
from django.conf import settings
from django.contrib.admin.utils import unquote
from django.db.models import Model
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.snippets.views import chooser as snippet_chooser
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
            model_name.lstrip(),
            get_snippet_model_from_url_params(app_label, model_name.lstrip())
        ]


def get_page_model() -> Model:
    if settings.REFERENCE_MODEL:
        ref_models = settings.REFERENCE_MODEL
        for ref_model in ref_models.keys():
            # NOTE: Assumes a single entry in reference
            # will need to change to allow multiples reference objects
            app_name, model_name = ref_models[ref_model].split(".")

        return apps.get_model(app_name, model_name)
    return None


def choose(request: HttpRequest, app_label: str = None, model_name: str = None,
           prop_name: str = None):
    """ Use the default snippet chooser function
    but pass through the app and model from the settings"""
    if app_label is None or model_name is None:
        app_label, model_name, model = get_reference_model()
    return snippet_chooser.choose(request, app_label, model_name)


def chosen(
    request: HttpRequest, app_label: str, model_name: str, prop_name: str,
    pk: str
):
    item = get_object_or_404(apps.get_model(app_label, model_name),
                             pk=unquote(pk))

    snippet_data = {
        prop_name: str(item.pk),
        'label': str(item),
        # 'page_id': str(p.pk),
        # 'edit_link': reverse('wagtailsnippets:edit', args=(
        #     app_label, model_name, quote(item.pk)))
    }

    return render_modal_workflow(
        request,
        None, None,
        None, json_data={'step': 'chosen', 'result': snippet_data}
    )
