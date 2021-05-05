import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.templatetags.static import static
from django.utils.html import format_html
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
    id_name = 'reference_id'

    def get_attribute_data(self, attrs):
        """
        Get the reference id
        """
        return {
            self.id_name: attrs['data-'+self.id_name],
        }


def bibliographic_reference_decorator(props):
    """
        Draft.js ContentState to database HTML.
    """
    return DOM.create_element('span', {
        'data-reference_id': props['reference_id'],
    }, props['children'])


@hooks.register('register_rich_text_features')
def register_glossary_term(features):
    feature_name = 'glossary'
    type_ = 'TERM'

    control = {
        'type': type_,
        'label': 'TERM',
        'description': 'Glossary Term'
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['js/glossary_term.js'],
        )
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'span[data-term_id]':
                GlossaryTermEntityElementHandler(type_)},
        'to_database_format': {
            'entity_decorators': {type_: glossary_term_decorator}},
    })

    features.default_features.append(feature_name)


def glossary_term_decorator(props):
    """
        Draft.js ContentState to database HTML.
    """
    return DOM.create_element('span', {
        'data-term_id': props['term_id'],
    }, props['children'])


class GlossaryTermEntityElementHandler(InlineEntityElementHandler):
        """
            Database HTML to Draft.js ContentState.
            Converts the span tag into a REF entity, with the right data.
        """
        mutability = 'IMMUTABLE'
        id_name = 'term_id'

        def get_attribute_data(self, attrs):
            """
            Get the reference id
            """
            return {
                self.id_name: attrs['data-' + self.id_name],
            }


class TextColourDraftail:
    """
        Register Text colour inline html function, one for each colour class
    """
    feature_name = 'entry-text-colour-1'
    text_class = 'entry-colour-1'
    text_colour_style = ''
    type_prefix = 'TEXTCOLOUR'
    label = ''
    tag = 'textcolour'

    def __init__(self, feature_name, text_class, label, text_colour_style):
        self.feature_name = feature_name
        self.text_class = text_class
        self.label = label
        self.text_colour_style = text_colour_style
        self.type = self.type_prefix + '-{}'.format(self.label)

    def register_text_colour_feature(self, features):
        control = {
            'type': self.type,
            'label': self.label,
            'description': 'Text colour',
            'style': {'color': self.text_colour_style},
        }

        features.register_editor_plugin(
            'draftail', self.feature_name,
            draftail_features.InlineStyleFeature(control)
        )

        db_conversion = {
            'from_database_format': {
                'span[data-custom-style="{}"]'.format(
                    self.feature_name
                ): InlineStyleElementHandler(
                    self.type)},
            'to_database_format': {'style_map': {
                self.type: {
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
        'entry-text-colour-1', 'entry-colour-1',
        'C1', 'rgb(20, 177, 231)'
    ),
    TextColourDraftail(
        'entry-text-colour-2', 'entry-colour-2',
        'C2',
        'rgb(186, 75, 22)'),
    TextColourDraftail(
        'entry-text-colour-3', 'entry-colour-3', 'C3',
        'rgb(0, 45, 59)'),
    TextColourDraftail(
        'entry-text-colour-4', 'entry-colour-4', 'C4',
        '#3ADB76'),
    TextColourDraftail(
        'entry-text-colour-5', 'entry-colour-5', 'C5',
        '#EC5840'),
]


for hook in text_colour_hooks:
    hooks.register(
        'register_rich_text_features',
        hook.register_text_colour_feature
    )


@hooks.register('insert_editor_css')
def editor_css():
    """ Add css for text colours and other custom styles"""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/wagtail/editor.css')
    )
