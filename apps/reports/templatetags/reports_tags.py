import re

from django import template
from django.template.defaultfilters import title
from django.urls import reverse

from apps.reports.urls import urlpatterns


register = template.Library()


@register.simple_tag
def report_links():
    abbreviations = re.compile(
        r"(mi|eod|cb1|obiee)",
        flags=re.IGNORECASE,
    )

    def replace_abbreviations(full_name):
        words = full_name.split()

        words = [
            abbreviations.sub(
                lambda match: match.group(1).upper(),
                word,
            )
            for word in words
        ]

        return " ".join(words)

    reports = []

    for url_pattern in urlpatterns:
        # Ignore unnamed URLs and the Reports landing page.
        if not url_pattern.name or url_pattern.name == "index":
            continue

        display_name = title(url_pattern.name.replace("_", " "))

        reports.append(
            {
                "name": replace_abbreviations(display_name),
                "url": reverse(f"reports:{url_pattern.name}"),
            }
        )

    return reports
