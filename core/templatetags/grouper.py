from django.template import Library

register = Library()

@register.filter
def grouper(list_, n=4):
    """Group the given list into a list of lists of size n"""
    # Note that the itertools grouper recipe from https://docs.python.org/3/library/itertools.html#itertools-recipes
    # isn't viable here as it creats groups of a fixed size. Neither is zip_longest, as that returns None values; we
    # want to just reduce the number of items in the last list.
    list_groups = []
    index = 0
    while index < len(list_):
        list_groups.append(list_[index:index+n])
        index += n
    return list_groups
