from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from compile import settings
from django.http.response import JsonResponse


def index(request):
    return render(request, 'front/index.html')


@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        fileName = file.name
        # print(fileName)
        import os
        filePath = os.path.join(settings.BASE_DIR, 'media', 'file', fileName)
        with open(filePath, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
            f.close()
        return HttpResponse("ok")


@csrf_exempt
def lexical(request):
    if request.method == 'POST':
        fileName = request.POST.get('fileName')
        print(fileName)
        import os
        filePath = os.path.join(settings.BASE_DIR, 'media', 'file', fileName)
        from ablan.lexical_scanner import getToken
        result = []
        result = getToken(filePath)
        res = {'result': result}
        # return HttpResponse(res, content_type="application/json")
        return JsonResponse(res)


@csrf_exempt
def syntax(request):
    if request.method == 'POST':
        import os
        from compile import settings
        filePath = os.path.join(settings.BASE_DIR, 'lex_to_syntax.json')
        from ablan.syntax_scanner import getTree
        result = []
        result, flag = getTree(filePath)
        res = {'result' : result}
        return JsonResponse(res)
