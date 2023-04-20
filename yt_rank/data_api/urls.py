from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('get_thread_info_list_from_client', views.GetThreadInfoListFromClient.as_view(), name='get_thread_info_list_from_client'),
    re_path('get_thread_info_list_from_controller', views.GetThreadInfoListFromController.as_view(), name='get_thread_info_list_from_controller'),
    re_path('set_thread_info_from_controller', views.SetThreadInfoFromController.as_view(), name='set_thread_info_from_controller')
    # re_path('get_data', views.GetData.as_view(), name='get_data'),
    # re_path('set_proxy', views.SetProxy.as_view(), name='set_proxy'),
    # re_path('get_proxy', views.GetProxy.as_view(), name='get_proxy'),
    # re_path('set_google_account', views.SetGoogleAccount.as_view(), name='set_google_account'),
    # re_path('get_google_account', views.GetGoogleAccount.as_view(), name='get_google_account'),
    # re_path('change_google_account', views.ChangeGoogleAccount.as_view(), name='change_google_account'),
    # re_path('change_proxy', views.ChangeProxy.as_view(), name='change_proxy'),
]