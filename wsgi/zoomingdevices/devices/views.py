# # core
import json

# # Third Party
import django_filters
from django_redis import get_redis_connection

# # REST Framework
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

# # project
from zoomingdevices.lib.helpers import RedisConverter

# # App
from . import models, serializers


try:
    rConn = get_redis_connection('default')
    rConn.ping()
    redis_alive = True
except:
    redis_alive = False

hashName = 'devices:master'


class DeviceFilter(django_filters.FilterSet):

    class Meta:
        model = models.Device
        fields = {
            'device_name': ['exact'],
            'magnification': ['exact', 'lte', 'lt', 'gte', 'gt'],
            'field_of_view': ['exact', 'lte', 'lt', 'gte', 'gt'],
            'view_range': ['exact', 'lte', 'lt', 'gte', 'gt'],
            }


class DeviceList(generics.ListCreateAPIView):
    """List all devices or create a new one."""

    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    permission_classes = (IsAdminUser,)
    paginate_by = 10
    filter_class = DeviceFilter
    search_fields = ('device_name', )

    def get(self, request, *args, **kwargs):
        qp = request.QUERY_PARAMS.copy()
        qp.pop('page', None)
        if redis_alive and not len(qp):     # no redis any other query param is passed
            pageNo = int(request.QUERY_PARAMS.get('page', 1)) or 1
            start = ((pageNo-1)*self.paginate_by)
            limit = start+self.paginate_by
            allKeys = rConn.hkeys(hashName)
            count = len(allKeys)
            if allKeys:
                if start > count:
                    return Response({
                            "detail": "Invalid page \"{0}\": "
                                "That page contains no results."
                                .format(pageNo)}, status=404)

                keys = allKeys[start:limit]
                vals = rConn.hmget(hashName, keys)
                vals = vals if vals else []
                pageLinkIncomplete = ("{0}{1}/devices/?page="
                        .format("http://", request.get_host()))
                prevP = (pageLinkIncomplete+"{0}"
                            .format(pageNo-1)
                        if pageNo > 1 else None)
                nextP = (pageLinkIncomplete+"{0}"
                            .format(pageNo+1)
                        if limit < count else None)
                retDict = {
                    'count': count,
                    'prev': prevP,
                    'next': nextP,
                    'results': [json.loads(RedisConverter.decode(i))
                        for i in vals]
                }
                return Response(retDict, status=200)

        res = self.list(request, *args, **kwargs)
        if redis_alive and not len(qp) and res.data['results']:   # Should we do this here? Not advised in prod
            # get all models
            objs = models.Device.objects.all()
            pipe = rConn.pipeline()     # either redis is fully updated or not at all
            for i in objs:
                ser = serializers.DeviceSerializer(i).data
                jsonStr = json.dumps(ser)
                pipe.hset(hashName, i.pk, jsonStr)
            pipe.execute()
        return res

    def perform_create(self, serializer):
        dObj = serializer.save()
        dObjSerialized = serializers.DeviceSerializer(dObj).data
        rConn.hset(hashName, dObj.pk, json.dumps(dObjSerialized))


class DeviceUpdate(generics.RetrieveUpdateDestroyAPIView):
    """Get a particular device and/or update/delete it."""

    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        device = rConn.hget(hashName, kwargs['pk'])
        if device:
            device = RedisConverter.decode(device)
            return Response(json.loads(device), status=200)
        res = self.retrieve(request, *args, **kwargs)
        rConn.hset(hashName, kwargs['pk'], json.dumps(res.data))
        return res

    def perform_update(self, serializer):
        dObj = serializer.save()
        dObjSerialized = serializers.DeviceSerializer(dObj).data
        rConn.hset(hashName, dObj.pk, json.dumps(dObjSerialized))

    def perform_destroy(self, instance):
        dId = instance.pk
        instance.delete()
        rConn.hdel(hashName, dId)
