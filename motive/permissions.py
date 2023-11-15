from rest_framework.permissions import BasePermission


class IsAddMotive(BasePermission):
    """ add motive """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_motive' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllMotive(BasePermission):
    """ view all motive """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_motive_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewDetailMotive(BasePermission):
    """ view detail motive """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_motive_detail' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsChangeMotive(BasePermission):
    """ update motive """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'change_motive' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsDestroyMotive(BasePermission):
    """ destroy motive """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'delete_motive' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsRestoreFirm(BasePermission):
    """ restore motive """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'active_motive' in user['member']['user_permissions']:
                return True
            else:
                return False
