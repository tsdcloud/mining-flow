ENDPOINT_USER = "bfc.api.user.zukulufeg.com"

ENDPOINT_ENTITY = "bfc.api.entity.zukulufeg.com"

H_OPERATION_CHOICE = [
    (1, 'CREATE'),
    (2, 'UPDATE'),
    (3, 'DELETE'),
    (4, 'RESTORE'),
    (5, 'PERMISSION'),
    (6, 'STATUS_USED'),
    (7, 'FOLLOWING_TRANSFER_CHANGED'),
    (8, 'RECEPTION_TRANSFER')
]

BOOLEAN_CHOICES = [(1, 'TRUE'), (2, 'FALSE')]

BALANCE_OPERATION_CHOICE = [
    (1, 'DEPOT - CAREER'),
    (2, 'CAREER - HUB MINIER'),
    (3, 'HUB MINIER - HUB PARTNER'),
    (4, 'HUB MINIER'),
    (5, 'HUB PARTNER')
]

STATUS_TRANSFER_CHOICE = [
    (1, 'ENCOURS'),
    (2, 'RECEPTIONER'),
    (3, 'PARTIELLEMENT APPURE'),
    (4, 'APPURER'),
]

STATUS_SALE_CHOICE = [
    (1, 'WAITING'),
    (2, 'RECEVED'),
    (3, 'OTHER'),
]

SALE_CHOICE = [
    (1, 'HUB MINIER - AIRE DE VENTE'),
    (2, 'HUB MINIER - AUTRE'),
    (3, 'AIRE DE VENTE - AUTRE'),
]
