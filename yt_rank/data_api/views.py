from django.core import serializers as srz
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import ThreadInfoData, UpdateInfoData
import time


# Create your views here.
class UpdateInfoSerializer(serializers.Serializer):
    anydesk_id = serializers.CharField(max_length=20)
    excel_num = serializers.IntegerField(default=None, )
    host_name = serializers.CharField(max_length=50, )
    uuid = serializers.CharField(max_length=50, )
    task_type = serializers.CharField(max_length=20, )
    try_done = serializers.BooleanField(default=False)
    success = serializers.BooleanField(default=None)
    msg = serializers.CharField(max_length=300, )
    target_path = serializers.CharField(max_length=300, default=None, )
    file_name = serializers.CharField(max_length=300, default=None, )
    download_url = serializers.CharField(max_length=300, default=None, )
    line_from = serializers.IntegerField(default=None)
    line_to = serializers.IntegerField(default=None)
    absolute_path = serializers.BooleanField(default=None)
    after_run = serializers.BooleanField(default=None)
    process_name = serializers.CharField(max_length=300, default=None, )


class SetUpdateInfoFlagChange(APIView):
    def post(self, request):
        anydesk_id = request.data.get('anydesk_id', None)
        uuid = request.data.get('uuid', None)
        _type = request.data.get('type', None)
        err_msg = request.data.get('msg', None)
        if not UpdateInfoData.objects.filter(anydesk_id=anydesk_id, uuid=uuid).exists():
            return Response(data={'msg': 'fail', 'error': '해당 작업이 존재하지 않습니다.'})
        update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id, uuid=uuid).first()
        if _type == 'success':
            update_info_data.success = True
            update_info_data.msg = err_msg
        elif _type == 'fail':
            update_info_data.success = False
            update_info_data.msg = err_msg
        elif _type == 'try':
            update_info_data.try_done = True
            update_info_data.msg = err_msg
        update_info_data.save()
        return Response(data={'msg': 'success'})


class GetUpdateInfo(APIView):
    def get(self, request):
        anydesk_id = request.data.get('anydesk_id', None)
        host_name = request.data.get('host_name', None)
        if anydesk_id is None and host_name is None:
            return Response(data={'msg': 'fail', 'error': '애니데스크와 호스트 아이디가 모두 없습니다.'})
        update_info_data = None
        if UpdateInfoData.objects.filter(anydesk_id=anydesk_id).exists():
            update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id)
        # elif UpdateInfoData.objects.filter(host_name=host_name).exists():
        #     update_info_data = UpdateInfoData.objects.filter(host_name=host_name)
        if update_info_data is None:
            return Response(data={'msg': 'success', 'data': None})
        # data = UpdateInfoSerializer(update_info_data)
        data = json.dumps(list(update_info_data.values()), cls=DjangoJSONEncoder)
        return Response(data={'msg': 'success', 'data': data})


class SetUpdateInfoByAnydeskIDList(APIView):
    """
    anydesk_id_list : 필수
    excel_num
    uuid
    task_type
    target_path
    file_name
    download_url
    line_from: List = SetUpdateInfoByAnydeskIDList 에서는 리스트 형태로 받아야 함. 애니데스크의 리스트 넘버에 있는것 추출해 값으로 사용
    line_to: List = SetUpdateInfoByAnydeskIDList 에서는 리스트 형태로 받아야 함. 애니데스크의 리스트 넘버에 있는것 추출해 값으로 사용
    absolute_path
    after_run
    process_name
    """

    def post(self, request):
        anydesk_id_list = request.data.get('anydesk_id_list', [])
        excel_num = request.data.get('excel_num', None)
        uuid = request.data.get('uuid', None)
        task_type = request.data.get('task_type', None)
        target_path = request.data.get('target_path', None)
        file_name = request.data.get('file_name', None)
        download_url = request.data.get('download_url', None)
        line_from_list = request.data.get('line_from_list', [])
        line_to_list = request.data.get('line_to_list', [])
        absolute_path = request.data.get('absolute_path', None)
        after_run = request.data.get('after_run', None)
        process_name = request.data.get('process_name', None)
        if len(anydesk_id_list) == 0:
            return Response(data={'msg': 'fail', 'error': '애니데스크 아이디 0개'})
        for n, anydesk_id in enumerate(anydesk_id_list):
            update_info_data = None
            if UpdateInfoData.objects.filter(anydesk_id=anydesk_id).exists():
                update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id).first()
                # update_info_data.delete()
            if update_info_data is None:
                line_from = None
                line_to = None
                if task_type == 'download_extract_replace':
                    line_from = line_from_list[n]
                    line_to = line_to_list[n]
                UpdateInfoData.objects.create(
                    anydesk_id=anydesk_id,
                    excel_num=excel_num,
                    uuid=uuid,
                    task_type=task_type,
                    try_done=False,
                    success=None,
                    msg=None,
                    target_path=target_path,
                    file_name=file_name,
                    download_url=download_url,
                    line_from=line_from,
                    line_to=line_to,
                    absolute_path=absolute_path,
                    after_run=after_run,
                    process_name=process_name,
                )
                continue
            update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id).first()
            line_from = None
            line_to = None
            if task_type == 'download_extract_replace':
                line_from = line_from_list[n]
                line_to = line_to_list[n]
            update_info_data.anydesk_id = anydesk_id
            update_info_data.excel_num = excel_num
            update_info_data.uuid = uuid
            update_info_data.task_type = task_type
            update_info_data.try_done = False
            update_info_data.success = None
            update_info_data.msg = None
            update_info_data.target_path = target_path
            update_info_data.file_name = file_name
            update_info_data.download_url = download_url
            update_info_data.line_from = line_from
            update_info_data.line_to = line_to
            update_info_data.absolute_path = absolute_path
            update_info_data.after_run = after_run
            update_info_data.process_name = process_name
            update_info_data.save()
        return Response(data={'msg': 'success'})


class SetUpdateInfoByAnydeskId(APIView):
    """
    anydesk_id : 필수
    excel_num
    host_name
    uuid
    task_type
    target_path
    file_name
    download_url
    line_from: int
    line_to: int
    absolute_path
    after_run
    process_name
    """

    def post(self, request):
        anydesk_id = request.data.get('anydesk_id', None)
        excel_num = request.data.get('excel_num', None)
        host_name = request.data.get('host_name', None)
        uuid = request.data.get('uuid', None)
        task_type = request.data.get('task_type', None)
        target_path = request.data.get('target_path', None)
        file_name = request.data.get('file_name', None)
        download_url = request.data.get('download_url', None)
        line_from = request.data.get('line_from', None)
        line_to = request.data.get('line_to', None)
        absolute_path = request.data.get('absolute_path', None)
        after_run = request.data.get('after_run', None)
        process_name = request.data.get('process_name', None)
        if anydesk_id is None and host_name is None:
            return Response(data={'msg': 'fail', 'error': '애니데스크 아이디와 호스트 네임이 모두 없습니다'})
        update_info_data = None
        if UpdateInfoData.objects.filter(anydesk_id=anydesk_id).exists():
            update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id).first()
            # update_info_data.delete()
        #     update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id).first()
        # elif UpdateInfoData.objects.filter(host_name=host_name).exists():
        #     update_info_data = UpdateInfoData.objects.filter(host_name=host_name).first()
        if update_info_data is None:
            UpdateInfoData.objects.create(
                anydesk_id=anydesk_id,
                excel_num=excel_num,
                host_name=host_name,
                uuid=uuid,
                task_type=task_type,
                try_done=False,
                success=None,
                msg=None,
                target_path=target_path,
                file_name=file_name,
                download_url=download_url,
                line_from=line_from,
                line_to=line_to,
                absolute_path=absolute_path,
                after_run=after_run,
                process_name=process_name,
            )
            return Response(data={'msg': 'success'})
        update_info_data.anydesk_id = anydesk_id
        update_info_data.excel_num = excel_num
        update_info_data.host_name = host_name
        update_info_data.uuid = uuid
        update_info_data.task_type = task_type
        update_info_data.try_done = False
        update_info_data.success = None
        update_info_data.msg = None
        update_info_data.target_path = target_path
        update_info_data.file_name = file_name
        update_info_data.download_url = download_url
        update_info_data.line_from = line_from
        update_info_data.line_to = line_to
        update_info_data.absolute_path = absolute_path
        update_info_data.after_run = after_run
        update_info_data.process_name = process_name
        update_info_data.save()
        return Response(data={'msg': 'success'})


class SetThreadInfoFromController(APIView):
    def post(self, request):
        host_name = request.data.get('host_name', None)  #
        anydesk_id = request.data.get('anydesk_id', None)  #
        thread_index = request.data.get('thread_index', None)  #
        keyword = request.data.get('keyword', 'null')
        is_filter = request.data.get('is_filter', 'null')
        target_url = request.data.get('target_url', 'null')
        enter_type = request.data.get('enter_type', 'null')
        target_state = request.data.get('target_state', 'null')
        state_for_main = request.data.get('target_state', 'null')
        thread_infos = ThreadInfoData.objects.filter(anydesk_id=anydesk_id, thread_index=thread_index)
        if not thread_infos.exist():
            return Response(data={'msg': 'fail', 'error': 'no_thread_infos'})
        thread = thread_infos.first()
        if keyword != 'null':
            thread.keyword = keyword
        if is_filter != 'null':
            thread.is_filter = is_filter
        if target_url != 'null':
            thread.target_url = target_url
        if enter_type != 'null':
            thread.enter_type = enter_type
        if target_state != 'null':
            thread.target_state = target_state
        if state_for_main != 'null':
            thread.state_for_main = state_for_main
        thread.save()
        return Response(data={'msg': 'success', })


class GetThreadInfoListFromController(APIView):
    def get(self, request):
        server_num = request.data.get('server_num', None)
        if server_num is None:
            return_data = {'thread_list': list(ThreadInfoData.objects.values().all())}
            return Response(data=return_data)
        return_data = {'thread_list': list(ThreadInfoData.objects.filter(server_num=server_num).values().first())}
        return Response(data=return_data)


class SetThreadInfoFromClient(APIView):
    def post(self, request):
        excel_num = request.data.get('excel_num', None)
        host_name = request.data.get('host_name', None)
        anydesk_id = request.data.get('anydesk_id', None)
        hai_ip_account = request.data.get('hai_ip_account', 'null')
        total_logged_in = request.data.get('total_logged_in', 'null')
        thread_index = request.data.get('thread_index', 'null')
        chrome = request.data.get('chrome', 'null')
        server_num = request.data.get('server_num', 'null')
        proxy = request.data.get('proxy', 'null')
        google_id = request.data.get('google_id', 'null')
        google_password = request.data.get('google_password', 'null')
        google_email = request.data.get('google_email', 'null')
        user_agent = request.data.get('user_agent', 'null')
        google_logged_in = request.data.get('google_logged_in', 'null')
        rank = request.data.get('rank', 'null')
        keyword = request.data.get('keyword', 'null')
        is_filter = request.data.get('is_filter', 'null')
        target_url = request.data.get('target_url', 'null')
        enter_type = request.data.get('enter_type', 'null')
        now_state = request.data.get('now_state', 'null')
        target_state = request.data.get('target_state', 'null')
        state_for_main = request.data.get('state_for_main', 'null')

        print(request.data)
        print('goo lg:',google_logged_in)
        if anydesk_id is None:
            return Response(data={'msg': 'fail'})
        thread_infos = ThreadInfoData.objects.filter(anydesk_id=anydesk_id, thread_index=thread_index)
        if not thread_infos.exists():
            return Response(data={'msg': 'fail', 'error': 'no_matched_thread_info'})
        thread = thread_infos.first()
        if hai_ip_account != 'null':
            thread.hai_ip_account = hai_ip_account
        if total_logged_in != 'null':
            thread.total_logged_in = total_logged_in
        if thread_index != 'null':
            thread.thread_index = thread_index
        if chrome != 'null':
            thread.chrome = chrome
        if server_num != 'null':
            thread.server_num = server_num
        if proxy != 'null':
            thread.proxy = proxy
        if google_id != 'null':
            thread.google_id = google_id
        if google_password != 'null':
            thread.google_password = google_password
        if google_email != 'null':
            thread.google_email = google_email
        if user_agent != 'null':
            thread.user_agent = user_agent
        if google_logged_in != 'null':
            thread.google_logged_in = google_logged_in
        if rank != 'null':
            thread.rank = rank
        if keyword != 'null':
            thread.keyword = keyword
        if is_filter != 'null':
            thread.is_filter = is_filter
        if target_url != 'null':
            thread.target_url = target_url
        if enter_type != 'null':
            thread.enter_type = enter_type
        if now_state != 'null':
            thread.now_state = now_state
        if target_state != 'null':
            thread.target_state = target_state
        if state_for_main != 'null':
            thread.state_for_main = state_for_main
        thread.last_connected_timestamp = str(int(time.time()))
        thread.save()
        return Response(data={'msg': 'success'})


class ThreadInfoDataSerializer(serializers.Serializer):
    excel_num = serializers.IntegerField(default=None, )
    host_name = serializers.CharField(max_length=20, )
    anydesk_id = serializers.CharField(max_length=20, )
    hai_ip_account = serializers.CharField(max_length=20, )
    total_logged_in = serializers.IntegerField(default=0, )
    thread_index = serializers.IntegerField()
    chrome = serializers.BooleanField()
    server_num = serializers.IntegerField(default=None, )
    proxy = serializers.CharField(max_length=20, default=None, )
    google_id = serializers.CharField(max_length=50, default=None, )
    google_password = serializers.CharField(max_length=50, default=None, )
    google_email = serializers.CharField(max_length=50, default=None, )
    user_agent = serializers.CharField(max_length=200, default=None, )
    google_logged_in = serializers.BooleanField(default=False, )
    rank = serializers.IntegerField(default=999, )
    keyword = serializers.CharField(max_length=100, default=None, )
    is_filter = serializers.BooleanField(default=False, )
    target_url = serializers.CharField(max_length=200, default=None, )
    enter_type = serializers.CharField(max_length=20, default=None, )
    now_state = serializers.CharField(max_length=20, default=None, )
    target_state = serializers.CharField(max_length=20, default=None, )
    last_connected_timestamp = serializers.CharField(max_length=25, default=0, )
    state_for_main = serializers.CharField(max_length=25, default=None)


class GetThreadInfoListFromClient(APIView):
    def get(self, request):
        anydesk_id = request.data.get('anydesk_id', None)  #
        if anydesk_id is None:
            return Response(data={'msg': 'fail'})

        server_thread_infos_by_anydesk_id = ThreadInfoData.objects.filter(anydesk_id=anydesk_id).all()
        list_for_return=[]
        for thread in server_thread_infos_by_anydesk_id:
            data = dict(
                thread_index=thread.thread_index,
                # excel_num=thread.excel_num,
                # hai_ip_account=thread.hai_ip_account,
                # server_num=thread.server_num,
                # for check //  proxy, google_id, google_password, google_email, user_agent, google_logged_in, rank 의 경우 추후에 필요시 추가할것
                keyword=thread.keyword,
                is_filter=thread.is_filter,
                target_url=thread.target_url,
                enter_type=thread.enter_type,
                # now_state=thread.now_state,
                target_state=thread.target_state,
                state_for_main=thread.state_for_main,
            )
            list_for_return.append(data)
        return Response(data={'thread_list': list_for_return})

class SetThreadInfoListFromClient(APIView):  # -> 최초 1회만 수행되는거로 하자
    def post(self, request):
        host_name = request.data.get('host_name', None)  #
        anydesk_id = request.data.get('anydesk_id', None)  #
        hai_ip_account = request.data.get('hai_ip_account', None)  #
        total_logged_in = request.data.get('total_logged_in', None)  #
        thread_list = request.data.get('thread_list', [])  #
        if host_name is None and anydesk_id is None:
            return Response(data={'thread_list': []})
        # 서버에 해당 애니데스크 정보
        thread_info_data_all_by_anydesk_id = ThreadInfoData.objects.filter(anydesk_id=anydesk_id).all()
        list_for_response = []

        # 라이브 아닌 스레드 삭제
        now_live_thread = []
        for t in thread_list:
            now_live_thread.append(t['thread_index'])
        copied_server_threads = thread_info_data_all_by_anydesk_id
        server_threads_changed = False
        for server_thread in copied_server_threads:
            if not server_thread.thread_index in now_live_thread:
                thread_index = server_thread.thread_index
                server_threads_changed = True
                ThreadInfoData.objects.filter(anydesk_id=anydesk_id, thread_index=thread_index).first().delete()
        if server_threads_changed:
            thread_info_data_all_by_anydesk_id = ThreadInfoData.objects.filter(anydesk_id=anydesk_id).all()

        # 원래 검사 하려던것 진행
        for thread in thread_list:
            thread_info_data = thread_info_data_all_by_anydesk_id.filter(thread_index=thread['thread_index']).first()
            if thread_info_data is None:
                google_id = None
                google_password = None
                google_email = None
                user_agent = None
                if 'google_id' in thread:
                    google_id = thread['google_id']
                if 'google_password' in thread:
                    google_password = thread['google_password']
                if 'google_email' in thread:
                    google_email = thread['google_email']
                if 'user_agent' in thread:
                    user_agent = thread['user_agent']

                a = ThreadInfoData.objects.create(
                    host_name=host_name,
                    anydesk_id=anydesk_id,
                    hai_ip_account=hai_ip_account,
                    total_logged_in=0,
                    thread_index=thread['thread_index'],
                    server_num=thread['server_num'],
                    proxy=thread['proxy'],
                    google_id=google_id,
                    google_password=google_password,
                    google_email=google_email,
                    user_agent=user_agent,
                    google_logged_in=thread['google_logged_in'],
                    rank=thread['rank'],
                    now_state=thread['now_state'],
                    is_filter=False,
                    last_connected_timestamp=str(int(time.time()))
                )
                list_for_response.append(a)
                continue
            thread_info = thread_info_data
            thread_info.server_num = thread['server_num']
            thread_info.proxy = thread['proxy']
            if 'google_id' in thread:
                thread_info.google_id = thread['google_id']
            if 'google_password' in thread:
                thread_info.google_password = thread['google_password']
            if 'google_email' in thread:
                thread_info.google_email = thread['google_email']
            if 'user_agent' in thread:
                thread_info.user_agent = thread['user_agent']
            thread_info.google_logged_in = thread['google_logged_in']
            thread_info.now_state = thread['now_state']
            thread_info.last_connected_timestamp = str(int(time.time()))
            thread_info.save()
            list_for_response.append(thread_info)
        return_thread_info_list = []
        for thread in list_for_response:
            data = dict(
                thread_index=thread.thread_index,
                server_num=thread.server_num,
                proxy=thread.proxy,
                google_logged_in=thread.google_logged_in,
                google_id=thread.google_id,
                google_password=thread.google_password,
                google_email=thread.google_email,
                keyword=thread.keyword,
                is_filter=thread.is_filter,
                target_url=thread.target_url,
                enter_type=thread.enter_type,
                target_state=thread.target_state,
                state_for_main=thread.state_for_main,
            )
            return_thread_info_list.append(data)
        return_data = {'thread_list': return_thread_info_list}
        return Response(data=return_data)
