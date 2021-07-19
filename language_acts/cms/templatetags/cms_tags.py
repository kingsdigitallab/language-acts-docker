import re
from datetime import date

import wagtail.core.blocks as wagtail_blocks
from django import template
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from wagtail.core.models import Page, Site
from wagtail.core.rich_text import RichText

from language_acts.cms.models.pages import (
    BlogPost,
    Event,
    NewsPost,
    HomePage,
    BlogIndexPage,
    NewsIndexPage,
    EventIndexPage,
)
from language_acts.cms.models.snippets import BibliographyEntry, GlossaryTerm
from language_acts.cms.views.ref_chooser import get_page_model

register = template.Library()


@register.filter
def get_section(current_page):
    homepage = HomePage.objects.first()
    current_section = (
        Page.objects.ancestor_of(current_page, inclusive=True)
            .child_of(homepage)
            .first()
    )
    return current_section


@register.filter
def order_by(queryset, field):
    return queryset.order_by(field)


@register.simple_tag
def are_comments_allowed():
    """Returns True if commenting on the site is allowed, False otherwise."""
    return getattr(settings, "ALLOW_COMMENTS", False)


@register.inclusion_tag("cms/tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context, root, current_page):
    """Returns the pages that are part of the breadcrumb trail of the current
    page, up to the root page."""
    pages = (
        current_page.get_ancestors(inclusive=True).descendant_of(root).filter(
            live=True)
    )

    return {
        "request": context["request"],
        "root": root,
        "current_page": current_page,
        "pages": pages,
    }


@register.simple_tag
def get_homepage_events():
    """Returns 3 latest news posts"""
    today = date.today()
    events = Event.objects.live().filter(date_from__gte=today).order_by(
        "date_from")
    if events.count() < 4:
        return events
    else:
        return events[:4]


@register.filter
def lines(val):
    if "\r\n" in val:
        return val.split("\r\n")
    else:
        return val.split("\n")


@register.filter
def related_words(page):
    return page.get_siblings(inclusive=False).live()


@register.simple_tag
def get_news_preview():
    """Returns 3 latest news posts"""
    today = date.today()
    pages = NewsPost.objects.live().filter(date__lte=today).order_by("-date")
    if pages.count() < 3:
        return pages
    else:
        return pages[:3]


@register.simple_tag
def get_blog_posts_preview():
    """Returns 3 latest blog posts"""
    today = date.today()
    pages = BlogPost.objects.live().filter(date__lte=today).order_by("-date")
    if pages.count() < 4:
        return pages
    else:
        return pages[:4]


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Returns the site root Page, not the implementation-specific model used.
    Object-comparison to self will return false as objects would differ.

    :rtype: `wagtail.core.models.Page`
    """
    if "request" in context and hasattr(context["request"], "site"):
        return Site.find_for_request(context["request"]).root_page
    else:
        return None


@register.simple_tag(takes_context=False)
def get_ga_id():
    return getattr(settings, 'GA_ID')


@register.simple_tag(takes_context=False)
def get_twitter_name():
    return getattr(settings, "TWITTER_NAME")


@register.simple_tag(takes_context=False)
def get_twitter_url():
    return getattr(settings, "TWITTER_URL")


@register.simple_tag(takes_context=False)
def get_twitter_widget_id():
    return getattr(settings, "TWITTER_WIDGET_ID")


@register.simple_tag
def has_view_restrictions(page):
    """Returns True if the page has view restrictions set up, False
    otherwise."""
    return page.view_restrictions.count() > 0


@register.inclusion_tag("cms/tags/show_children_in_menu.html",
                        takes_context=False)
def show_children_in_menu(page):
    """ Force certain page types to never show children in menu"""
    show_children = True
    children = None
    if (
        type(page.specific) == BlogIndexPage
        or type(page.specific) == NewsIndexPage
        or type(page.specific) == EventIndexPage
    ):
        show_children = False
    if show_children:
        children = page.get_children().live().in_menu().specific()
    return {"page": page, "show_children": show_children, "children": children}


@register.inclusion_tag("cms/tags/main_menu.html", takes_context=True)
def main_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    # Added for wagtail 2.11
    if "request" in context:
        request = context["request"]
    else:
        request = None
    if request is not None and root is None:
        root = Site.find_for_request(context["request"]).root_page
    if root is None:
        root = current_page
    try:
        menu_pages = root.get_children().live().in_menu()
        root.active = current_page.url == root.url if current_page else False
        for page in menu_pages:
            page.active = (
                current_page.url.startswith(
                    page.url) if current_page else False
            )
    except AttributeError:
        print("Error in root: {}:{}".format(root, current_page))
        menu_pages = []

    return {
        "request": request,
        "root": root,
        "current_page": current_page,
        "menu_pages": menu_pages,
    }


@register.inclusion_tag("cms/tags/footer_menu.html", takes_context=True)
def footer_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    root.active = current_page.url == root.url if current_page else False

    for page in menu_pages:
        page.active = current_page.url.startswith(
            page.url) if current_page else False

    return {
        "request": context["request"],
        "root": root,
        "current_page": current_page,
        "menu_pages": menu_pages,
    }


@register.filter
def querify(req):
    if "?q=" in req:
        return req
    else:
        return "{}?q=".format(req)


@register.simple_tag(takes_context=True)
def get_request_parameters(context, exclude=None):
    """Returns a string with all the request parameters except the exclude
    parameter."""
    params = ""
    request = context["request"]

    for key, value in request.GET.items():
        if key != exclude:
            params += "&{key}={value}".format(key=key, value=value)

    return params


@register.simple_tag
def page_in_submenu(page: Page = None, parent: Page = None) -> bool:
    """Return true if page parent is in page's children
    (for sidebar menus)"""
    if page and parent:
        for sub in parent.get_children().live().in_menu():
            if sub.pk == page.pk:
                return True
    return False


@register.simple_tag(takes_context=True)
def get_toggler_status(context, page):
    """Return open if menu in href, closed otherwise """
    request = context["request"]
    if request and "toggler_open" in request.GET:
        try:
            # Assumes only one open at a time
            page_id = int(request.GET["toggler_open"])
            if page.pk == page_id:
                return True
        except TypeError:
            pass
    return False


@register.filter
def remove_paragraph(text: str) -> str:
    return text.replace('</p>', '').replace('<p>', '')


def create_ref_link(ref, content_prefix: str = '',
                    content_suffix: str = '',
                    selection_text: str = None) -> str:
    """
    Create a foundation dropdown that contains the full reference
    and a link to the bibliography page
    """
    menu_id = "reference-dropdown-{}-{}".format(
        str(ref.__class__.__name__).lower(),
        ref.pk
    )
    if ref.__class__.__name__ == 'BibliographyEntry':
        # strip out pointless paragraph tags
        clean_citation = remove_paragraph(ref.reference)
    elif ref.__class__.__name__ == 'GlossaryTerm':
        if selection_text:
            clean_citation = remove_paragraph(selection_text)
        else:
            clean_citation = remove_paragraph(ref.term)
    else:
        clean_citation = ''
    ref_link = (
        '<a class="ref_toggle ' + ref.__class__.__name__
        + '" data-toggle="{}">{}</a>'.format(
            menu_id, content_prefix + clean_citation + content_suffix
        )
    )
    return ref_link


def add_dropdowns(ref, page) -> str:
    url = ''
    link_text = 'Go to Bibliography'
    if ref.__class__.__name__ == 'BibliographyEntry':
        # strip out pointless paragraph tags
        dropdown_text = '{}'.format(ref.full_citation)
        if page:
            url = page.url + "#reference-{}".format(ref.pk)
    elif ref.__class__.__name__ == 'GlossaryTerm':
        dropdown_text = '{}'.format(ref.description)
        if page:
            url = page.url + "#term-{}".format(ref.pk)
            link_text = 'Go to Glossary'
    else:
        dropdown_text = ''
    menu_id = "reference-dropdown-{}-{}".format(
        str(ref.__class__.__name__).lower(),
        ref.pk
    )
    if page:
        dropdown_text += ' <a href="{}">{}</a>'.format(
            url, link_text
        )
    return '<div class="dropdown-pane" id="{}" \
        data-position="top" data-alignment="center" data-dropdown \
        data-hover="true" data-hover-pane="true">{}</div>'.format(
        menu_id, dropdown_text
    )


def get_prefix_suffix(result):
    suffix = ''
    if len(result.groups()) >= 2 and len(
        result.group(2)
    ) > 0:
        # content before [ref_1]
        prefix = ' ' + result.group(2) + ' '
    else:
        prefix = ''
    if len(result.groups()) >= 3 and len(
        result.group(4)
    ) > 0:
        # content after [ref_1]
        suffix = ' ' + result.group(4) + ' '
    if (
        len(result.groups()) >= 4
        and result.group(5) and len(result.group(5)) > 0
    ):
        # edge case when there are two </span> tags
        suffix = suffix + result.group(5)
    return prefix, suffix


def add_glossary_terms(value: str) -> str:
    # <span data-term_id="1">[term_1_second-sentence]</span>
    ref_path = re.compile(
        r'\[term_(\d+)_*(.*?)\]'
    )
    if type(value) == RichText:
        value = value.source
    while True:
        result = ref_path.search(value)
        if result:
            ref_id = int(result.group(1))
            if ref_id > 0:
                try:
                    ref = GlossaryTerm.objects.get(pk=ref_id)
                    if ref:
                        # create a link to the glossary
                        # that jumps to our ref

                        # prefix, suffix = get_prefix_suffix(result)
                        selection_text = ''
                        if result.group(2):
                            selection_text = result.group(2).replace('-', ' ')
                        value = value.replace(
                            result.group(0),
                            create_ref_link(
                                ref, '', '', selection_text
                            )
                        )
                    else:
                        print("WARNING: No Ref found: {}".format(
                            ref_id))

                except ObjectDoesNotExist:
                    print(" ref not found ")
        else:
            break
    return value


def add_bibliography_references(value: str) -> str:
    # ref_path = re.compile(
    #     r'<span data-reference_id="(\d+)">(.*?)(\[ref_\d+\])(.*?)</span>('
    #     r'</span>)*'
    # )
    ref_path = re.compile(
        r'\[ref_(\d+)\]'
    )
    if type(value) == RichText:
        value = value.source
    while True:
        result = ref_path.search(value)
        if result:
            ref_id = int(result.group(1))
            if ref_id > 0:
                try:
                    ref = BibliographyEntry.objects.get(pk=ref_id)
                    if ref:
                        # create a link to the bibliography page
                        # that jumps to our ref
                        # prefix, suffix = get_prefix_suffix(result)
                        value = value.replace(
                            result.group(0),
                            # create_ref_link(ref, prefix, suffix)
                            create_ref_link(ref, '', '')
                        )
                    else:
                        print("WARNING: No Ref found: {}".format(
                            ref_id))
                        break

                except ObjectDoesNotExist:
                    print(" ref not found ")
                    value = value.replace(
                        result.group(0), ''
                    )
        else:
            break

    return value


def get_value_string(block):
    value_str = ""
    if type(block) == wagtail_blocks.stream_block.StreamValue.StreamChild:
        if "html" in block.value:
            value_str = block.value["html"]
    elif type(block) == RichText:
        value_str = block.source
    elif type(block) == str:
        value_str = block
    return value_str


@register.filter
def add_references(block):
    """Add short form dropdown hover links (e.g. citation)
    """
    # if type(block) ==
    value_str = get_value_string(block)
    value_str = add_bibliography_references(value_str)
    value_str = add_glossary_terms(value_str)
    return RichText(value_str)


@register.filter
def add_reference_dropdowns(block):
    """ Create the dropdown content for both bibliography references
    and glossary terms
    could be refactored to be a bit more nimble
    [ref_4] [term_2]
    """
    value_str = get_value_string(block)
    dropdown_text = ''
    ref_path = re.compile(r'\[(\w+)_(\d+)_*(.*?)\]')
    while True:
        result = ref_path.search(value_str)
        if result:
            ref_id = int(result.group(2))
            reference_key = result.group(1)
            if ref_id > 0:
                try:

                    if reference_key == 'ref':
                        ref = BibliographyEntry.objects.get(pk=ref_id)
                    elif reference_key == 'term':
                        ref = GlossaryTerm.objects.get(pk=ref_id)
                    else:
                        ref = None

                    if ref:
                        page = None
                        for usage in ref.get_usage():
                            # make sure we've got the right
                            # linked object
                            if type(usage.specific) == get_page_model(ref):
                                page = usage
                        # create a link to the page
                        # that jumps to our ref if present
                        value_str = value_str.replace(
                            result.group(0), create_ref_link(ref)
                        )
                        dropdown_text = dropdown_text + add_dropdowns(ref,
                                                                      page)

                except ObjectDoesNotExist:
                    print(" ref not found ")
                    value_str = value_str.replace(
                        result.group(0), ''
                    )
        else:
            break
    return RichText(dropdown_text)
