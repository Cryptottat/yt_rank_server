from django.urls import path, re_path
from . import views

urlpatterns = [
    path('get_thread_info_list_from_client', views.GetThreadInfoListFromClient.as_view(), name='get_thread_info_list_from_client'),
    path('get_thread_info_list_from_controller', views.GetThreadInfoListFromController.as_view(), name='get_thread_info_list_from_controller'),
    path('set_thread_info_from_controller', views.SetThreadInfoFromController.as_view(), name='set_thread_info_from_controller'),

    path('get_update_info', views.GetUpdateInfo.as_view(), name='get_update_info'),
    path('set_update_info_by_anydesk_id_list', views.SetUpdateInfoByAnydeskIDList.as_view(), name='set_update_info_by_anydesk_id_list'),
    path('set_update_info_by_anydesk_id', views.SetUpdateInfoByAnydeskId.as_view(), name='set_update_info_by_anydesk_id'),
    path('set_update_info_flag_change', views.SetUpdateInfoFlagChange.as_view(), name='set_update_info_flag_change'),

    # re_path('get_data', views.GetData.as_view(), name='get_data'),
    # re_path('set_proxy', views.SetProxy.as_view(), name='set_proxy'),
    # re_path('get_proxy', views.GetProxy.as_view(), name='get_proxy'),
    # re_path('set_google_account', views.SetGoogleAccount.as_view(), name='set_google_account'),
    # re_path('get_google_account', views.GetGoogleAccount.as_view(), name='get_google_account'),
    # re_path('change_google_account', views.ChangeGoogleAccount.as_view(), name='change_google_account'),
    # re_path('change_proxy', views.ChangeProxy.as_view(), name='change_proxy'),
]