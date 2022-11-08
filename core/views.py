from django.http import HttpResponse

def home(request):
   text = """<h1>nossa página inicial alucinante</h1>"""
   return HttpResponse(text)