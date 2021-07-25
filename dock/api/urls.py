from django.urls import path

from dock.api.views import (
    AccountCreate,
    AccountDeposit,
    AccountDetails,
    AccountWithdraw,
    AccountDeactivate,
    AccountActivate,
    AccountTransactions,
)

urlpatterns = [
    path('accounts/', AccountCreate.as_view()),
    path('accounts/<int:account_id>/', AccountDetails.as_view()),
    path('accounts/<int:account_id>/deposit/', AccountDeposit.as_view()),
    path('accounts/<int:account_id>/withdraw/', AccountWithdraw.as_view()),
    path('accounts/<int:account_id>/deactivate/', AccountDeactivate.as_view()),
    path('accounts/<int:account_id>/activate/', AccountActivate.as_view()),
    path('accounts/<int:account_id>/transactions/', AccountTransactions.as_view()),
]
