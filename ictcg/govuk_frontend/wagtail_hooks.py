from wagtail.core import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
import wagtail.admin.rich_text.editors.draftail.features as draftail_features


@hooks.register('register_rich_text_features')
def register_help_text_feature(features):
    """
    Registering the `inset-text` feature, which uses the `govuk-inset-text` class
    Stored as HTML with a `<div class="govuk-inset-text">` tag.
    """
    feature_name = 'govuk-inset-text'
    type_ = 'govuk-inset-text'

    control = {
        'type': type_,
        'label': 'Q',
        'description': 'GOVUK inset text',
        'element': 'div',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'div[class=govuk-inset-text]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'div', 'props': {'class': 'govuk-inset-text'}}}},
    })
