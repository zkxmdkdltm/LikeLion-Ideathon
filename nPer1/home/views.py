from django.shortcuts import render

# Create your views here.
def intro(request):
    # if request.user.is_authenticated:
    #     return render(request, 'host.html')
    return render(request, 'intro.html')


#.12341234