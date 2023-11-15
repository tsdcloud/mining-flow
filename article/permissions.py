from rest_framework.permissions import BasePermission


class IsAddCategorie(BasePermission):
    """ add categorie """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_categorie' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllCategorie(BasePermission):
    """ view all categories """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_categorie_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddArticle(BasePermission):
    """ add article """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_article' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllArticle(BasePermission):
    """ view all articles """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_article_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsDeactivate(BasePermission):
    """ suspend a url """
    def has_permission(self, request, view):
        return False


class IsActivate(BasePermission):
    """ active a url """
    def has_permission(self, request, view):
        return True
