from datetime import date

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SlotForm
from .models import Log, Plan, Slot
from .stats import day_stats, fmt, week_stats


def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        return redirect('plan')
    return render(request, 'registration/signup.html', {'form': form})


def current_plan(user):
    return user.plans.first()


@login_required
def dashboard(request):
    plan = current_plan(request.user)
    if not plan:
        messages.info(request, 'Create your weekly timetable first.')
        return redirect('plan')
    today = date.today()
    in_week = plan.start_date <= today <= plan.end_date
    data = day_stats(plan, today) if in_week else None
    day_no = (today - plan.start_date).days + 1
    return render(request, 'dashboard.html', {
        'plan': plan, 'in_week': in_week, 'today': data, 'day_no': day_no,
        'planned_txt': fmt(data['planned']) if data else '',
        'studied_txt': fmt(data['studied']) if data else '',
    })


@login_required
@require_POST
def log_minutes(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id, plan__user=request.user)
    today = date.today()
    if not (slot.plan.start_date <= today <= slot.plan.end_date) or slot.weekday != today.weekday():
        messages.error(request, 'This slot is not for today.')
        return redirect('dashboard')
    log, _ = Log.objects.get_or_create(slot=slot, date=today)
    if 'full' in request.POST:
        log.minutes = slot.planned_minutes
    else:
        try:
            log.minutes += max(0, int(request.POST.get('minutes', 0)))
        except ValueError:
            pass
    log.save()
    return redirect('dashboard')


@login_required
def plan_view(request):
    plan = current_plan(request.user)
    if not plan:
        plan = Plan.objects.create(user=request.user)
    form = SlotForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        slot = form.save(commit=False)
        slot.plan = plan
        slot.save()
        return redirect('plan')
    by_day = [(name, [s for s in plan.slots.all() if s.weekday == i]) for i, name in
              [(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
               (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]]
    return render(request, 'plan.html', {'plan': plan, 'form': form, 'by_day': by_day})


@login_required
@require_POST
def delete_slot(request, slot_id):
    get_object_or_404(Slot, id=slot_id, plan__user=request.user).delete()
    return redirect('plan')


@login_required
@require_POST
def new_week(request):
    """Start a fresh 7-day cycle from today, copying the previous slots."""
    old = current_plan(request.user)
    plan = Plan.objects.create(user=request.user, start_date=date.today())
    if old and request.POST.get('copy'):
        Slot.objects.bulk_create([
            Slot(plan=plan, weekday=s.weekday, subject=s.subject,
                 start_time=s.start_time, end_time=s.end_time) for s in old.slots.all()])
    return redirect('plan')


@login_required
def report(request):
    plan = current_plan(request.user)
    if not plan:
        return redirect('plan')
    days, overall = week_stats(plan)
    for d in days:
        d['planned_txt'], d['studied_txt'] = fmt(d['planned']), fmt(d['studied'])
    chart = {
        'labels': [d['date'].strftime('%a %d') for d in days],
        'planned': [d['planned'] for d in days],
        'studied': [d['studied'] for d in days],
    }
    return render(request, 'report.html', {
        'plan': plan, 'days': days, 'overall': overall, 'chart': chart,
        'total_studied': fmt(sum(d['studied'] for d in days)),
        'total_planned': fmt(sum(d['planned'] for d in days)),
    })
