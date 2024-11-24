from django.shortcuts import render
from .forms import DonorRegistration, Contact, Search
from .models import donor_Registration, sea_rch, con_tact





def home(request):
    return render(request, 'polls/base.html')


def about(request):
    return render(request, 'polls/about.html')


def donor_registration(request):
    forms = DonorRegistration()
    if request.method == 'POST':
        forms = DonorRegistration(request.POST)
        if forms.is_valid():
            forms.save()
            context = {
                'forms': forms
            }

            return render(request, 'polls/donor_list.html', context)

        print(forms.errors)

    context_form = {
        'forms': forms
    }

    return render(request, 'polls/donor_registration.html', context_form)


def search(request):
    forms = Search()
    if request.method == 'POST':
        forms = Search(request.POST)
        if forms.is_valid():
            # Get cleaned data from the form
            bloodgroup = forms.cleaned_data.get('blood_group', None)
            state = forms.cleaned_data.get('state', None)
            city = forms.cleaned_data.get('city', None)

            # Build a dynamic query using Q objects
            query = Q()
            if bloodgroup:  # Add condition if blood_group is provided
                query &= Q(blood_group__icontains=bloodgroup)
            if state:  # Add condition if state is provided
                query &= Q(state__icontains=state)
            if city:  # Add condition if city is provided
                query &= Q(city__icontains=city)

            # Filter donors based on the query
            donor_filter = donor_Registration.objects.filter(query)

            context = {
                'forms': forms,
                'donor_filter': donor_filter,  # Pass the results to the template
            }

            return render(request, 'polls/search_list.html', context)

        print(forms.errors)

    context_form = {
        'forms': forms
    }

    return render(request, 'polls/search.html', context_form)


def search_info(request, email):
    email = email
    detail = donor_Registration.objects.get(email=email)

    context = {
        'details': detail
    }

    return render(request, 'polls/search_info.html', context)


def about_us(request):
    return render(request, 'about_us.html')


def contact(request):
    forms = Contact()
    if request.method == 'POST':
        forms = Contact(request.POST)
        if forms.is_valid():
            forms.save()

    context = {
        'forms': forms
    }

    return render(request, 'polls/contact.html', context)
