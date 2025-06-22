from . import clean_html, div_wrapped_html

available_converters = {
    "Чистый HTML (без div)": clean_html,
    "HTML с обёртками div": div_wrapped_html,
}
