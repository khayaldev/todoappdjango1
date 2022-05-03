from django.shortcuts import render

def handle_not_found(request,exception):
  return render(request, 'notfound.html')
def handle_server(request):
  return render(request, 'serverror.html')