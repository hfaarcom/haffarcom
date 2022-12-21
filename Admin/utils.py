from datetime import datetime


def getDataByDate(model, type, query):
    if type == 'monthly':
        dic = {}
        year = datetime.today().year
        if query == 'date':
            for i in range(1, 13):
                data = model.objects.filter(date__year=year, date__month=i).count()
                dic[i] = data
            return dic
        elif query == 'date_joined':       
            for i in range(1, 13):
                data = model.objects.filter(date_joined__year=year, date_joined__month=i).count()
                dic[i] = data
            return dic
