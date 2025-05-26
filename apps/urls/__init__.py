from apps.urls.account import urlpatterns as account
from apps.urls.market import urlpatterns as market
from apps.urls.profile import urlpatterns as profile
from apps.urls.register_login import urlpatterns as reg_log
from apps.urls.search import urlpatterns as search
from apps.urls.operator import urlpatterns as operator

urlpatterns=[
    *market,
    *reg_log,
    *profile,
    *account,
    *search,
    *operator,
]
