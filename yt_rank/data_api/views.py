from django.core import serializers as srz
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ThreadInfoData, UpdateInfoData
import time
# Create your views here.
class UpdateInfoSerializer(serializers.Serializer):
    anydesk_id = serializers.CharField(max_length=20)
    excel_num = serializers.IntegerField(default=None,)
    host_name = serializers.CharField(max_length=50,)
    uuid = serializers.CharField(max_length=50,)
    task_type = serializers.CharField(max_length=20,)
    try_done = serializers.BooleanField(default=False)
    success = serializers.BooleanField(default=None)
    msg = serializers.CharField(max_length=300,)
    target_path = serializers.CharField(max_length=300, default=None,)
    file_name = serializers.CharField(max_length=300, default=None,)
    download_url = serializers.CharField(max_length=300, default=None,)
    line_from = serializers.IntegerField(default=None)
    line_to = serializers.IntegerField(default=None)
    absolute_path = serializers.BooleanField(default=None)
    after_run = serializers.BooleanField(default=None)
    process_name = serializers.CharField(max_length=300, default=None,)

class SetUpdateInfoFlagChange(APIView):
    def post(self, request):
        anydesk_id = request.data.get('anydesk_id', None)
        uuid = request.data.get('uuid', None)
        _type = request.data.get('type', None)

        if not UpdateInfoData.objects.filter(anydesk_id=anydesk_id,uuid=uuid).exists():
            return Response(data={'msg': 'fail', 'error': '해당 작업이 존재하지 않습니다.'})
        update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id, uuid=uuid).first()
        if _type == 'success':
            update_info_data.success = True
        elif _type == 'fail':
            update_info_data.success = False
            err_msg = request.data.get('msg', None)
            update_info_data.msg = err_msg
        elif _type == 'try':
            update_info_data.try_done = True
        update_info_data.save()
        return Response(data={'msg': 'success'})

class GetUpdateInfo(APIView):
    def get(self, request):
        anydesk_id = request.data.get('anydesk_id',None)
        host_name = request.data.get('host_name', None)
        if anydesk_id is None and host_name is None:
            return Response(data={'msg': 'fail', 'error': '애니데스크와 호스트 아이디가 모두 없습니다.'})
        update_info_data = None
        if UpdateInfoData.objects.filter(anydesk_id=anydesk_id).exists():
            update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id)
        elif UpdateInfoData.objects.filter(host_name=host_name).exists():
            update_info_data = UpdateInfoData.objects.filter(host_name=host_name)
        if update_info_data is None:
            return Response(data={'msg': 'success', 'data':None})
        # data = UpdateInfoSerializer(update_info_data)
        print(update_info_data.values())
        data = json.dumps(list(update_info_data.values()),cls=DjangoJSONEncoder)
        return Response(data={'msg': 'success', 'data':data})
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
        if len(anydesk_id_list)==0:
            return Response(data={'msg': 'fail','error':'애니데스크 아이디 0개'})
        for n,anydesk_id in enumerate(anydesk_id_list):
            update_info_data = None
            if UpdateInfoData.objects.filter(anydesk_id=anydesk_id).exists():
                update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id).first()
            if update_info_data is None:
                UpdateInfoData.objects.create(
                    anydesk_id=anydesk_id,
                    excel_num=excel_num,
                    uuid=uuid,
                    task_type=task_type,
                    target_path=target_path,
                    file_name=file_name,
                    download_url=download_url,
                    line_from=line_from_list[n],
                    line_to=line_to_list[n],
                    absolute_path=absolute_path,
                    after_run=after_run,
                    process_name=process_name,
                )
                continue
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
            update_info_data.line_from = line_from_list[n]
            update_info_data.line_to = line_to_list[n]
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
            return Response(data={'msg': 'fail','error':'애니데스크 아이디와 호스트 네임이 모두 없습니다'})
        update_info_data = None
        if UpdateInfoData.objects.filter(anydesk_id=anydesk_id).exists():
            update_info_data = UpdateInfoData.objects.filter(anydesk_id=anydesk_id).first()
        elif UpdateInfoData.objects.filter(host_name=host_name).exists():
            update_info_data = UpdateInfoData.objects.filter(host_name=host_name).first()
        if update_info_data is None:
            UpdateInfoData.objects.create(
                anydesk_id=anydesk_id,
                excel_num=excel_num,
                host_name=host_name,
                uuid=uuid,
                task_type=task_type,
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
        keyword = request.data.get('keyword',None)
        is_filter = request.data.get('is_filter',False)
        target_url = request.data.get('target_url',None)
        enter_type = request.data.get('enter_type',None)
        target_state = request.data.get('target_state',None)
        thread_infos = ThreadInfoData.objects.filter(host_name=host_name, anydesk_id=anydesk_id, thread_index=thread_index)
        if not thread_infos.exist():
            return Response(data={'msg': 'fail','error':'no_thread_infos'})
        thread = thread_infos.first()
        thread.keyword = keyword
        thread.is_filter = is_filter
        thread.target_url = target_url
        thread.enter_type = enter_type
        thread.target_state = target_state
        thread.save()
        return Response(data={'msg': 'success',})

class GetThreadInfoListFromController(APIView):
    def get(self, request):
        server_num = request.data.get('server_num',None)
        if server_num is None:
            return_data = {'thread_list': list(ThreadInfoData.objects.values().all())}
            return Response(data=return_data)
        return_data = {'thread_list':list(ThreadInfoData.objects.filter(server_num=server_num).values().first())}
        return Response(data=return_data)
class GetThreadInfoListFromClient(APIView):
    def post(self, request):
        host_name = request.data.get('host_name', None)  #
        anydesk_id = request.data.get('anydesk_id', None)  #
        hai_ip_account = request.data.get('hai_ip_account', None)  #
        total_logged_in = request.data.get('total_logged_in', None)  #
        thread_list = request.data.get('thread_list', [])  #
        for thread in thread_list:
            if not ThreadInfoData.objects.filter(host_name=host_name, anydesk_id=anydesk_id, thread_index=thread['thread_index']).exists():
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

                ThreadInfoData.objects.create(
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
                    last_connected_timestamp = int(time.time())
                )
                continue
            thread_info = ThreadInfoData.objects.filter(host_name=host_name, anydesk_id=anydesk_id, thread_index=thread['thread_index']).first()
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
            thread_info.last_connected_timestamp = int(time.time())
            thread_info.save()
        thread_info_list = ThreadInfoData.objects.filter(host_name=host_name, anydesk_id=anydesk_id).all()
        return_thread_info_list = []
        for thread in thread_info_list:
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
                target_state=thread.target_state
            )
            return_thread_info_list.append(data)
        return_data = {'thread_list':return_thread_info_list}
        return Response(data=return_data)