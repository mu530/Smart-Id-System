from django import template

register = template.Library()


@register.filter(name="user_role")
def has_user_role(user, role):
    """
    Checks if the given user has the specified role.
    Usage: {{ request.user|has_user_role:"is_cafe_staff" }}
    """

    return user.role == role
