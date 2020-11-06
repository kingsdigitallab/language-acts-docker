import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import \
    InlineEntityElementHandler
from wagtail.core import hooks


@hooks.register('register_rich_text_features')
def register_bibliographic_reference(features):
    feature_name = 'reference'
    type_ = 'REF'

    control = {
        'type': type_,
        'label': 'REF',
        'description': 'Bibliographic reference'
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['js/bibliographic_reference.js'],
        )
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'a[data-ref]': BibliographicReferenceEntityElementHandler(type_)},
        'to_database_format': {
            'entity_decorators': {type_: bibliographic_reference_decorator}},
    })

    features.default_features.append('reference')


class BibliographicReferenceEntityElementHandler(InlineEntityElementHandler):
    mutability = 'MUTABLE'

    def get_attribute_data(self, attrs):
        """
        Get the reference id (and page?)
        """
        return {
            'bibliography_entry_id': attrs['data-bibliography_entry_id'],
            'bibliography_entry_reference': attrs[
                'data-bibliography_entry_reference']
        }


def bibliographic_reference_decorator(props):
    return DOM.create_element('span', {
        'data-bibliography_entry_id': props['bibliography_entry_id'],
        'data-bibliography_entry_reference': props[
            'bibliography_entry_reference']
    })


"""

features.register_editor_plugin(
        'draftail', 'link', draftail_features.EntityFeature({
            'type': 'LINK',
            'icon': 'link',
            'description': gettext('Link'),
            # We want to enforce constraints on which links can be pasted
            into rich text.
            # Keep only the attributes Wagtail needs.
            'attributes': ['url', 'id', 'parentId'],
            'whitelist': {
                # Keep pasted links with http/https protocol, and not-pasted
                links (href = undefined).
                'href': "^(http:|https:|undefined$)",
            }
        }, js=[
            'wagtailadmin/js/page-chooser-modal.js',
        ])
    )
    features.register_converter_rule('contentstate', 'link', {
        'from_database_format': {
            'a[href]': ExternalLinkElementHandler('LINK'),
            'a[linktype="page"]': PageLinkElementHandler('LINK'),
        },
        'to_database_format': {
            'entity_decorators': {'LINK': link_entity}
        }
    })

"""
