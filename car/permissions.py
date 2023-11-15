from rest_framework.permissions import BasePermission


class IsAddTractor(BasePermission):
    """ add tractor """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_tractor' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewTractor(BasePermission):
    """ view tractor """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_tractor_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddTrailer(BasePermission):
    """ add trailer """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_trailer' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewTrailer(BasePermission):
    """ view trailer """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_trailer_all' in user['member']['user_permissions']:
                return True
            else:
                return False
