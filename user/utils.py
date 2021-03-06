from django.core.serializers.python import Serializer


class LazyAccountEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'id': str(obj.id)})
        dump_object.update({'username': str(obj.user.username)})
        return dump_object