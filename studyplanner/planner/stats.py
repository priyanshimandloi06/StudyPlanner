from datetime import date

from .models import Log


def day_stats(plan, d):
    """Planned vs studied for one date of a plan."""
    today = date.today()
    slots = [s for s in plan.slots.all() if s.weekday == d.weekday()]
    logs = {l.slot_id: l.minutes for l in
            Log.objects.filter(slot__in=slots, date=d)}
    rows, planned, studied, credited = [], 0, 0, 0
    for s in slots:
        m = logs.get(s.id, 0)
        p = s.planned_minutes
        if m >= p:
            status = 'done'
        elif m > 0:
            status = 'partial'
        else:
            status = 'missed' if d < today else 'pending'
        rows.append({'slot': s, 'minutes': m, 'status': status})
        planned += p
        studied += m
        credited += min(m, p)
    percent = round(credited / planned * 100) if planned else 0
    return {'date': d, 'rows': rows, 'planned': planned, 'studied': studied, 'percent': percent}


def week_stats(plan):
    days = [day_stats(plan, d) for d in plan.dates()]
    planned = sum(x['planned'] for x in days)
    credited = sum(round(x['percent'] * x['planned'] / 100) for x in days)
    overall = round(credited / planned * 100) if planned else 0
    return days, overall


def fmt(minutes):
    h, m = divmod(minutes, 60)
    return f'{h}h {m}m' if h else f'{m}m'
