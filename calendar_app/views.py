import calendar as cal
from collections import defaultdict
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CalendarEntryForm
from .models import CalendarEntry
from recipes.models import Recipe, Category, UserScheduleMapping


@login_required
def admin_settings(request):
    """Manage custom categories and weekly schedule mapping."""
    categories = Category.objects.filter(user=request.user)
    mappings = {m.day_of_week: m.category_id for m in UserScheduleMapping.objects.filter(user=request.user)}
    
    context = {
        'categories': categories,
        'mappings': mappings,
        'days': UserScheduleMapping.DAYS_OF_WEEK,
    }
    return render(request, 'calendar_app/admin_settings.html', context)


@login_required
def calendar_view(request):
    """Monthly calendar showing scheduled recipes."""
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Clamp month to 1-12 and adjust year
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    # Build calendar weeks
    cal_obj = cal.Calendar(firstweekday=0)  # Monday first
    month_days = cal_obj.monthdatescalendar(year, month)

    # Get entries for the visible date range
    first_day = month_days[0][0]
    last_day = month_days[-1][-1]

    entries = CalendarEntry.objects.filter(
        user=request.user,
        date__gte=first_day,
        date__lte=last_day,
    ).select_related('recipe')

    # Group entries by date
    entries_by_date = defaultdict(list)
    for entry in entries:
        entries_by_date[entry.date].append(entry)

    # Build week data for template
    weeks = []
    for week in month_days:
        week_data = []
        for day in week:
            week_data.append({
                'date': day,
                'is_today': day == today,
                'is_current_month': day.month == month,
                'entries': entries_by_date.get(day, []),
            })
        weeks.append(week_data)

    # Prev / next month
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    # User's recipes for the add dialog
    user_recipes = Recipe.objects.filter(user=request.user).order_by('title')

    context = {
        'weeks': weeks,
        'year': year,
        'month': month,
        'month_name': cal.month_name[month],
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'today': today,
        'user_recipes': user_recipes,
        'has_entries': entries.exists(),
        'day_names': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    }
    return render(request, 'calendar_app/calendar.html', context)


@login_required
def calendar_add(request):
    """Add a recipe to the calendar (POST only)."""
    if request.method != 'POST':
        return redirect('calendar_view')

    form = CalendarEntryForm(request.POST, user=request.user)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        try:
            entry.save()
            messages.success(
                request,
                f'"{entry.recipe.title}" added to {entry.date.strftime("%b %d")}!'
            )
        except IntegrityError:
            messages.warning(request, 'This recipe is already scheduled for that meal.')
    else:
        messages.error(request, 'Could not add to calendar. Please check the form.')

    # Redirect back to the appropriate month on the calendar
    target_date = form.cleaned_data.get('date', date.today())
    next_url = request.POST.get('next', '')
    if next_url:
        return redirect(next_url)
    return redirect(f'/calendar/?year={target_date.year}&month={target_date.month}')


@login_required
def calendar_delete(request, pk):
    """Remove a recipe from the calendar (POST only)."""
    if request.method != 'POST':
        return redirect('calendar_view')

    entry = get_object_or_404(CalendarEntry, pk=pk, user=request.user)
    entry_date = entry.date
    entry.delete()
    messages.success(request, 'Removed from calendar.')
    return redirect(f'/calendar/?year={entry_date.year}&month={entry_date.month}')
