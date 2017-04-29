from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from core.templatetags.pagination import pagina
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.template import RequestContext
from core.decorators import only_post

from core.models import Issue, Watch
from core.services import watch_services
from core.services.mail_services import notify_admin


def feedback(request):
    _issues = Issue.objects.filter(is_feedback=True).order_by('-creationDate')
    issues = pagina(request, _issues)
    return render(request, 'core2/feedback.html', {'issues': issues})


@login_required
@only_post
def addFeedback(request):
    dict = request.POST
    issue_title = dict['title']
    issue_description = dict['description']
    if not issue_title or not issue_description:
        raise BaseException(_('title and description are required'))
    issue = Issue.newIssueFeedback(issue_title, issue_description, request.user)
    issue.save()
    watch_services.watch_issue(request.user, issue.id, Watch.CREATED)
    notify_admin(_('new Feedback: %s') % issue_title, issue_description)
    return redirect('feedback')
