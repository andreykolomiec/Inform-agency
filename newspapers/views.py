from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from newspapers.forms import (
    RedactorCreationForm,
    RedactorSearchForm,
    NewspaperForm,
    NewspaperSearchForm,
    TopicSearchForm,
)
from newspapers.models import Redactor, Newspaper, Topic


@login_required
def index(request):
    """View function for home page of the site."""

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_topics": Topic.objects.count(),
        "num_redactors": Redactor.objects.count(),
        "num_newspapers": Newspaper.objects.count(),
        "num_visits": num_visits + 1,
    }

    return render(request, "newspapers/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(initial={"name": name})
        context["search_query"] = name
        return context

    def get_queryset(self):
        queryset = Topic.objects.all().order_by("name")
        form = TopicSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspapers:topic-list")
    template_name = "newspapers/topic_form.html"


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspapers:topic-list")
    template_name = "newspapers/topic_form.html"


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("newspapers:topic-list")
    template_name = "newspapers/topic_delete.html"


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        topic = self.request.GET.get("topic", "")
        context["search_form"] = NewspaperSearchForm(initial={"topic": topic})
        context["search_query"] = topic
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.select_related("topic")
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(topic__name__icontains=form.cleaned_data["topic"])
        return queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspapers:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newspapers:newspaper-list")
    template_name = "newspapers/newspaper_confirm_delete.html"


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(initial={"username": username})
        context["search_query"] = username
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all().order_by("username")
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspapers")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    fields = ["username", "first_name", "last_name", "years_of_experience"]
    success_url = reverse_lazy("newspapers:redactor-list")
    template_name = "newspapers/redactor_form.html"

    def form_valid(self, form):
        return super().form_valid(form)


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("newspapers:redactor-list")
    template_name = "newspapers/redactor_confirm_delete.html"


class AboutUsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "newspapers/about_us.html"


class ContactsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "newspapers/contacts.html"
