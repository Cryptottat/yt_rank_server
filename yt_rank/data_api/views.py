from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ThreadInfoData as ThreadInfo
import time
# Create your views here.

class SetThreadInfoFromController(APIView):
    def post(self, request):
        host_name = request.data.get('host_name', None)  #
        anydesk_id = request.data.get('anydesk_id', None)  #
        thread_index = request.data.get('thread_index', None)  #
        keyword = request.data.get('keyword',None)
        is_filter = request.data.get('is_filter',False)
        target_url = request.data.get('target_url',None)
        enter_type = request.data.get('enter_type',None)
        target_state = request.data.get('target_state',None)
        thread_infos = ThreadInfo.objects.filter(host_name=host_name, anydesk_id=anydesk_id, thread_index=thread_index)
        if not thread_infos.exist():
            return {'msg': False}
        thread = thread_infos.first()
        thread.keyword = keyword
        thread.is_filter = is_filter
        thread.target_url = target_url
        thread.enter_type = enter_type
        thread.target_state = target_state
        thread.save()

class GetThreadInfoListFromController(APIView):
    def get(self, request):
        server_num = request.data.get('server_num',None)
        if server_num is None:
            return_data = {'thread_list': list(ThreadInfo.objects.values().all())}
            return Response(data=return_data)
        return_data = {'thread_list':list(ThreadInfo.objects.filter(server_num=server_num).values().first())}
        return Response(data=return_data)
class GetThreadInfoListFromClient(APIView):
    def post(self, request):
        host_name = request.data.get('host_name', None)  #
        anydesk_id = request.data.get('anydesk_id', None)  #
        hai_ip_account = request.data.get('hai_ip_account', None)  #
        total_logged_in = request.data.get('total_logged_in', None)  #
        thread_list = request.data.get('thread_list', [])  #
        for thread in thread_list:
            if not ThreadInfo.objects.filter(host_name=host_name, anydesk_id=anydesk_id, thread_index=thread['thread_index']).exists():
                ThreadInfo.objects.create(
                    host_name=host_name,
                    anydesk_id=anydesk_id,
                    hai_ip_account=hai_ip_account,
                    total_logged_in=0,
                    thread_index=thread['thread_index'],
                    server_num=thread['server_num'],
                    proxy=thread['proxy'],
                    google_id=thread['google_id'],
                    google_password=thread['google_password'],
                    google_email=thread['google_email'],
                    user_agent=thread['user_agent'],
                    google_logged_in=thread['google_logged_in'],
                    now_state=thread['now_state'],
                    is_filter=False,
                    last_connected_timestamp = int(time.time())
                )
                continue
            thread_info = ThreadInfo.objects.filter(host_name=host_name, anydesk_id=anydesk_id, thread_index=thread['thread_index']).first()
            thread_info.server_num = thread['server_num']
            thread_info.proxy = thread['proxy']
            thread_info.google_id = thread['google_id']
            thread_info.google_password = thread['google_password']
            thread_info.google_email = thread['google_email']
            thread_info.user_agent = thread['user_agent']
            thread_info.google_logged_in = thread['google_logged_in']
            thread_info.now_state = thread['now_state']
            thread_info.save()
        thread_info_list = ThreadInfo.objects.filter(host_name=host_name, anydesk_id=anydesk_id).all()
        return_thread_info_list = []
        for thread in thread_info_list:
            data = dict(
                thread_index=thread.thread_index,
                server_num=thread.server_num,
                proxy=thread.proxy,
                google_id=thread.google_id,
                google_password=thread.google_password,
                google_email=thread.google_email,
                keyword=thread.keyword,
                is_filter=thread.is_filter,
                target_url=thread.target_url,
                enter_type=thread.enter_type,
                target_state=thread.target_state
            )
            return_thread_info_list.append(data)
        return_data = {'thread_list':return_thread_info_list}
        return Response(data=return_data)