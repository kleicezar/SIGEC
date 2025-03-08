from django import template

register = template.Library()

@register.filter(name="has_perm")
def has_perm(user, perm_name):
    """Verifica se o usuário tem uma permissão específica."""
    return user.has_perm(perm_name)

    #FIXME - Esse filtro (pipe) verifica através da própria API do Django se o usuário tem uma permissão específica.
    #FIXME - O Django possui um sistema de permissões e grupos de usuários.
