import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineEntityElementHandler,
    BlockElementHandler
)
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
            'span[data-reference_id]':
                BibliographicReferenceEntityElementHandler(type_)},
        'to_database_format': {
            'entity_decorators': {type_: bibliographic_reference_decorator}},
    })

    features.default_features.append('reference')


class BibliographicReferenceEntityElementHandler(InlineEntityElementHandler):
    """
        Database HTML to Draft.js ContentState.
        Converts the span tag into a REF entity, with the right data.
    """
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        """
        Get the reference id
        """
        return {
            'reference_id': attrs['data-reference_id'],
        }


def bibliographic_reference_decorator(props):
    """
        Draft.js ContentState to database HTML.
    """
    return DOM.create_element('span', {
        'data-reference_id': props['reference_id'],
    }, props['children'])


@hooks.register('register_rich_text_features')
def text_colour_feature_1(features):
    """
    Text colour selection function
    """
    feature_name = 'entry-text-colour-1'
    type_ = 'text-colour'
    text_class = 'entry-colour-1'

    control = {
        'type': type_,
        'label': 'C1',
        'description': 'Text colour',
        'element': 'span',
    }

    features.register_editor_plugin(
        'draftail', feature_name,
        draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'span[class={}]'.format(text_class): BlockElementHandler(type_)},
        'to_database_format': {'block_map': {
            type_: {'element': 'span', 'props': {
                'class': '{}'.format(text_class)}}
        }
        },
    })

    features.default_features.append('entry-text-colour-1')


@hooks.register('register_rich_text_features')
def text_colour_feature_2(features):
    """
    Text colour selection function
    """
    feature_name = 'entry-text-colour-2'
    type_ = 'text-colour'
    text_class = 'entry-colour-2'

    control = {
        'type': type_,
        'label': 'C2',
        'description': 'Text colour',
        'element': 'span',
    }

    features.register_editor_plugin(
        'draftail', feature_name,
        draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'span[class={}]'.format(text_class): BlockElementHandler(type_)},
        'to_database_format': {'block_map': {
            type_: {'element': 'span', 'props': {
                'class': '{}'.format(text_class)}}
        }
        },
    })

    features.default_features.append('entry-text-colour-2')


@hooks.register('register_rich_text_features')
def text_colour_feature_3(features):
    """
    Text colour selection function
    """
    feature_name = 'entry-text-colour-3'
    type_ = 'text-colour'
    text_class = 'entry-colour-3'

    control = {
        'type': type_,
        'label': 'C3',
        'description': 'Text colour',
        'element': 'span',
    }

    features.register_editor_plugin(
        'draftail', feature_name,
        draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'span[class={}]'.format(text_class): BlockElementHandler(type_)},
        'to_database_format': {'block_map': {
            type_: {'element': 'span', 'props': {
                'class': '{}'.format(text_class)}}
        }
        },
    })

    features.default_features.append('entry-text-colour-3')
