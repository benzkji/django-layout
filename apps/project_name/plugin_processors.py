from django.utils.safestring import mark_safe


def default_div(instance, placeholder, rendered_content, original_context):
    if not instance._render_meta.text_enabled\
            and not instance.plugin_type == "AccordionEntryPlugin":
        return mark_safe('<div class="plugin plugin_%s">%s</div>'
                         % (instance.plugin_type.lower(), rendered_content))
    else:
        return rendered_content
