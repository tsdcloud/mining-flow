from rest_framework.permissions import BasePermission


class IsAddStockageAera(BasePermission):
    """ add stockage aera """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_stockageaera' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllStockageAera(BasePermission):
    """ view all stockageAera """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_stockageaera_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddStockagePartner(BasePermission):
    """ add stockage partner """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_stockagepartner' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllStockagePartner(BasePermission):
    """ view all stockage partner """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_stockagepartner_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddCareer(BasePermission):
    """ add career """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_career' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllCareer(BasePermission):
    """ view all career """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_career_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddCareerLv(BasePermission):
    """ add career lv """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_careerlv' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllCareerLv(BasePermission):
    """ view all careerlv """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_careerlv_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddStockageAeraLv(BasePermission):
    """ add stokcage aera lv """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_stockageaeralv' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllStockageAeraLv(BasePermission):
    """ view all stockageaeralv """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_stockageaeralv_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsApproveStockageAeraLv(BasePermission):
    """ approve stockageaeralv """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'approve_stockageaeralv' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddCareerArticle(BasePermission):
    """ associate career and article """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_career_article' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllCareerArticle(BasePermission):
    """ view all careerarticle """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_careerarticle_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsApproveCareerLv(BasePermission):
    """ approve careerlv """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'approve_careerlv' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddDepot(BasePermission):
    """ add a new depot """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_depot' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllDepot(BasePermission):
    """ view all depot """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_depot_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddHubPartner(BasePermission):
    """ add a new hub partner """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_hubpartner' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllHubPartner(BasePermission):
    """ view all hubpartner """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_hubpartner_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddTransfer(BasePermission):
    """ add a new transfer """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_transfer' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllTransfer(BasePermission):
    """ view all transfer """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_transfer_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsReceiveTransfer(BasePermission):
    """ receive a transfer """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'receive_transfer' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsReceiveSaleTransfer(BasePermission):
    """ receive a transfer plus sale """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'receive_sale_transfer' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddStockagePartnerArticle(BasePermission):
    """ add a new assiation depot vente article """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_stockage_partner_article' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllStockagePartnerArticle(BasePermission):
    """ view all stockage partner article """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_stockage_partner_article_all' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsAddSale(BasePermission):
    """ add a new sale """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_sale' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllSale(BasePermission):
    """ view all sales """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_all_sale' in user['member']['user_permissions']:
                return True
            else:
                return False
