from .permissions import GroupAOnly, GroupBOnly
from rest_framework.views import APIView
from rest_framework.response import Response


class File:

    def __init__(self, path):
        self.path = path

    def get_data(self):
        with open(self.path) as file:
            data_list = file.read().split('|')
            list_of_data_lists = [data_list[i:i+4] for i in range(0, len(data_list), 4)]
        return list_of_data_lists

    def get_keys(self):
        keys = [self.get_data()[i][2] for i in range(0, len(self.get_data()))]
        return keys

    def save_changes(self, data_list):
        with open(self.path, 'w') as file:
            file.write('|'.join([value for data in data_list for value in data]))


file = File('static/binfile')


class Create(APIView):

    permission_classes = (GroupBOnly,)

    def post(self, request):
        post_data = request.data.get('data', ' ')
        data_list = file.get_data()
        try:
            for key in post_data[0]:
                if key in file.get_keys():
                    return Response(f'{key} already exists')
                list_ = [key, post_data[0][key]]
                size = [str(len(list_[0].encode('utf-8'))), str(len(list_[1].encode('utf-8')))]
                final = size + list_
                data_list.append(final)
            file.save_changes(data_list)
            return Response('Done')
        except TypeError:
            return Response('Wrong JSON')


class Read(APIView):

    permission_classes = (GroupAOnly, )

    def get(self, request):
        return Response(file.get_keys())


class Update(APIView):

    permission_classes = (GroupBOnly, )

    def post(self, request): #NOT READY
        post_data = request.data.get('data', ' ')
        data_list = file.get_data()
        try:
            for key in post_data[0]:
                for data in data_list:
                    if key == data[2]:
                        data[3] = post_data[0][key]
                        data[1] = str(len(post_data[0][key].encode('utf-8')))
                        break
            file.save_changes(data_list)
            return Response('Done')
        except TypeError:
            return Response('Wrong JSON')


class Delete(APIView):

    permission_classes = (GroupBOnly,)

    def post(self, request):
        post_keys = request.data.get('keys', ' ')
        data_list = file.get_data()
        try:
            for key in post_keys:
                for data in enumerate(data_list):
                    if key == data[1][2]:
                        data_list.pop(data[0])
                        break
            file.save_changes(data_list)
            return Response('Done')
        except TypeError:
            return Response('Wrong JSON')


class Search(APIView):

    permission_classes = (GroupAOnly, GroupBOnly)

    def get(self, request):
        query = request.GET.get('query', ' ')
        data_list = file.get_data()
        result = []
        for data in data_list:
            if query in data[3]:
                result.append(data[2])
        return Response(result)


# admin|admin
# user_1|=*UY&/j6YEG4kajY|Group_A
# user_2|=*UY&/j6YEG4kajY|Group_A, Group_B
# Формат для post запросов - {"data": [{"key1":"value1", "key2":"value2"}]}