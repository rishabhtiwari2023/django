from django.urls import path
from . import views

urlpatterns = [
    path('transfer/<int:from_account_id>/<int:to_account_id>/<str:amount>/', views.transfer_funds, name='transfer_funds'),
    path('deposit/<int:account_id>/<str:amount>/', views.deposit_funds, name='deposit_funds'),
    path('account/<int:account_id>/', views.view_account, name='view_account'),
    path('accounts/', views.view_all_accounts, name='view_all_accounts'),
    path('account/<int:account_id>/transactions/', views.view_transaction_history, name='view_transaction_history'),
    path('account/<int:account_id>/withdraw/<str:amount>/', views.withdraw_funds, name='withdraw_funds'),
    path('create_account/', views.create_account, name='create_account'),
    path('update_account/<int:account_id>/', views.update_account, name='update_account'),
    path('delete_account/<int:account_id>/', views.delete_account, name='delete_account'),
    path('list_transactions/', views.list_transactions, name='list_transactions'),
]


