import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineEntityElementHandler,

)
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler
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


class TextColourDraftail:
    """
        Register Text colour inline html function, one for each colour class
    """
    feature_name = 'entry-text-colour-1'
    text_class = 'entry-colour-1'
    type_ = 'TEXTCOLOUR'
    label = ''
    tag = 'textcolour'

    def __init__(self, feature_name, text_class, label):
        self.feature_name = feature_name
        self.text_class = text_class
        self.label = label
        # self.type_ = type

    def register_text_colour_feature(self, features):
        control = {
            'type': self.type_,
            'label': self.label,
            'description': 'Text colour',
            'style': {'color': '$bright-blue;'},
        }

        features.register_editor_plugin(
            'draftail', self.feature_name,
            draftail_features.InlineStyleFeature(control)
        )

        db_conversion = {
            'from_database_format': {
                'span[data-custom-style]': InlineStyleElementHandler(self.type_)},
            'to_database_format': {'style_map': {
                self.type_: {
                    'element': 'span',
                    'props': {
                        'class': self.text_class,
                        'data-custom-style': self.feature_name
                    }
                }
            }
            },
        }

        features.register_converter_rule('contentstate', self.feature_name,
                                         db_conversion)

        features.default_features.append(self.feature_name)


text_colour_hooks = [

    TextColourDraftail(
        'entry-text-colour-1', 'entry-colour-1', 'C1',
    ),
    # TextColourDraftail(
    #     'entry-text-colour-2', 'entry-colour-2', 'C2',
    #     'text-colour-2'),
    # TextColourDraftail(
    #     'entry-text-colour-3', 'entry-colour-3', 'C3',
    #     'text-colour-3'),
    # TextColourDraftail(
    #     'entry-text-colour-4', 'entry-colour-4', 'C4',
    #     'text-colour-4'),
    # TextColourDraftail(
    #     'entry-text-colour-5', 'entry-colour-5', 'C5',
    #     'text-colour-5'),
]

for hook in text_colour_hooks:
    hooks.register(
        'register_rich_text_features',
        hook.register_text_colour_feature
    )
