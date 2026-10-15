from datetime import date, time
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Log, Plan, Slot
from .stats import day_stats


class PlannerTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user('a', password='p')
        self.client.login(username='a', password='p')
        self.plan = Plan.objects.create(user=self.u, start_date=date.today())
        self.slot = Slot.objects.create(plan=self.plan, weekday=date.today().weekday(),
                                        subject='Maths', start_time=time(18), end_time=time(20))

    def test_percent_partial_and_full(self):
        self.assertEqual(day_stats(self.plan, date.today())['percent'], 0)
        self.client.post(reverse('log_minutes', args=[self.slot.id]), {'minutes': 60})
        self.assertEqual(day_stats(self.plan, date.today())['percent'], 50)
        self.client.post(reverse('log_minutes', args=[self.slot.id]), {'full': 1})
        self.assertEqual(day_stats(self.plan, date.today())['percent'], 100)

    def test_pages_load(self):
        for n in ('dashboard', 'plan', 'report'):
            self.assertEqual(self.client.get(reverse(n)).status_code, 200)

    def test_cannot_log_other_users_slot(self):
        User.objects.create_user('b', password='p')
        self.client.login(username='b', password='p')
        r = self.client.post(reverse('log_minutes', args=[self.slot.id]), {'minutes': 10})
        self.assertEqual(r.status_code, 404)
