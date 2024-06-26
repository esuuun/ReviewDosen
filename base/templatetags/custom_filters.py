from django import template

register = template.Library()

@register.filter
def get_grade_count(grade_counts, grade_name):
    try:
        return grade_counts.get(grade_name, 0)
    except AttributeError:
        return 0
