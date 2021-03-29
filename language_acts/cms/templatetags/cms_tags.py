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
from language_acts.cms.models.snippets import GlossaryTerm, BibliographyEntry
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


def add_glossary_terms(value: str) -> str:
    # add glossary links
    for term in GlossaryTerm.objects.all():
        if term.term in str(value):
            value = value.replace(
                term.term,
                '<a title="{}" href="{}">{}</a>'.format(
                    term.description, "#", term.term
                ),
            )
    return value


@register.filter
def remove_paragraph(text: str) -> str:
    return text.replace('</p>', '').replace('<p>', '')


def create_ref_link(ref, page) -> str:
    """
    Create a foundation dropdown that contains the full reference
    and a link to the bibliography page
    """

    menu_id = "reference-dropdown-{}".format(page.pk)
    # strip out pointless paragraph tags
    clean_citation = remove_paragraph(ref.reference)
    ref_link = (
        '<a class="ref_toggle" data-toggle="{}">{}</a>'.format(
            menu_id, clean_citation
        )
    )
    return ref_link


def add_dropdowns(ref, page) -> str:
    bibliography_url = page.url + "#reference-{}".format(page.pk)
    menu_id = "reference-dropdown-{}".format(page.pk)
    dropdown_text = '<a href="{}">{}</a>'.format(bibliography_url,
                                                 ref.full_citation)
    return '<div class="dropdown-pane" id="{}" \
        data-position="top" data-alignment="center" data-dropdown \
        data-hover="true" data-hover-pane="true">{}</div>'.format(
        menu_id, dropdown_text
    )


def add_bibliography_references(value: str, dropdown=False) -> str:
    ref_path = re.compile(r'<span data-reference_id="(\d+)">([^<]*)</span>')
    while True:
        if type(value) == RichText:
            value = value.source
        result = ref_path.search(value)
        if result:
            ref_id = int(result.group(1))
            if ref_id > 0:
                try:
                    ref = BibliographyEntry.objects.get(pk=ref_id)
                    page = None
                    for usage in ref.get_usage():
                        # make sure we've got the right
                        # linked object
                        if type(usage.specific) == get_page_model():
                            page = usage
                    if ref and page:
                        # create a link to the bibliography page
                        # that jumps to our ref
                        if not dropdown:
                            value = value.replace(
                                result.group(0), create_ref_link(ref, page)
                            )
                        elif dropdown:
                            value = add_dropdowns(ref, page)
                    else:
                        print("WARNING: Ref called without page {}".format(
                            ref_id))
                        if ref:
                            value = value.replace(result.group(0),
                                                  ref.reference)

                except ObjectDoesNotExist:
                    print(" ref not found ")
        else:
            break

    return value


@register.filter
def add_references(block):
    """Add links from glossary terms and bibliography
    May be split to only add one type later if necessary"""
    # if type(block) ==
    value_str = ""
    if type(block) == wagtail_blocks.stream_block.StreamValue.StreamChild:
        if "html" in block.value:
            value_str = block.value["html"]
    elif type(block) == RichText:
        value_str = block.source
    elif type(block) == str:
        value_str = block
    # bibliography refs
    value_str = add_bibliography_references(value_str)
    return RichText(value_str)


@register.filter
def add_reference_dropdowns(block):
    # bibliography refs
    value_str = add_bibliography_references(block, True)
    return RichText(value_str)
