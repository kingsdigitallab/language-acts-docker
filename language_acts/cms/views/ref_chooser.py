from typing import List, Union

from django.conf import settings
from django.contrib.admin.utils import unquote
from django.core.paginator import Paginator
from django.db.models import Model
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.search.backends import get_search_backend
from wagtail.search.index import class_is_indexed
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


def choose(request):
    app_label, model_name, model = get_reference_model()
    if model:
        items = model.objects.all()
        # Preserve the snippet's model-level ordering if specified,
        # but fall back on PK if not
        # (to ensure pagination is consistent)
        if not items.ordered:
            items = items.order_by('pk')

        # Search
        is_searchable = class_is_indexed(model)
        is_searching = False
        search_query = None
        if is_searchable and 'q' in request.GET:
            search_form = SearchForm(
                request.GET, placeholder=_(
                    "Search %(snippet_type_name)s"
                ) % {
                    'snippet_type_name': model._meta.verbose_name
                }
            )

            if search_form.is_valid():
                search_query = search_form.cleaned_data['q']

                search_backend = get_search_backend()
                items = search_backend.search(search_query, items)
                is_searching = True

        else:
            search_form = SearchForm(
                placeholder=_("Search %(snippet_type_name)s") % {
                    'snippet_type_name': model._meta.verbose_name
                })

        # Pagination
        paginator = Paginator(items, per_page=25)
        paginated_items = paginator.get_page(request.GET.get('p'))

        # If paginating or searching, render "results.html"
        if request.GET.get('results', None) == 'true':
            return TemplateResponse(request,
                                    "wagtailsnippets/chooser/results.html",
                                    {
                                        'model_opts': model._meta,
                                        'items': paginated_items,
                                        'query_string': search_query,
                                        'is_searching': is_searching,
                                    })

        return render_modal_workflow(
            request,
            'wagtailsnippets/chooser/choose.html', None,
            {
                'model_opts': model._meta,
                'items': paginated_items,
                'is_searchable': is_searchable,
                'search_form': search_form,
                'query_string': search_query,
                'is_searching': is_searching,
            }, json_data={'step': 'choose'}
        )


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
