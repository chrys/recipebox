import calendar as cal
from collections import defaultdict
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from django.utils.text import slugify
from django.views.decorators.http import require_POST

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
@require_POST
def add_category(request):
    name = request.POST.get('name', '').strip()
    if name:
        slug = slugify(name)
        # Ensure slug is unique for this user
        if not Category.objects.filter(user=request.user, slug=slug).exists():
            Category.objects.create(user=request.user, name=name, slug=slug)
            messages.success(request, f'Category "{name}" added.')
        else:
            messages.warning(request, f'Category with similar name already exists.')
    return redirect('admin_settings')


@login_required
@require_POST
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    category.delete()
    messages.success(request, 'Category removed.')
    return redirect('admin_settings')


@login_required
@require_POST
def update_schedule(request):
    day = request.POST.get('day')
    category_id = request.POST.get('category')
    
    if day is not None:
        category = None
        if category_id:
            category = get_object_or_404(Category, pk=category_id, user=request.user)
        
        UserScheduleMapping.objects.update_or_create(
            user=request.user,
            day_of_week=int(day),
            defaults={'category': category}
        )
        messages.success(request, 'Schedule updated.')
    
    return redirect('admin_settings')


import random

@login_required
@require_POST
def schedule_current_week(request):
    """Automatically schedule recipes for the current week based on user settings."""
    today = date.today()
    # Monday is 0 in python's weekday(), Sunday is 6
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    
    # Check if any entries exist for this week
    existing_entries = CalendarEntry.objects.filter(
        user=request.user,
        date__gte=monday,
        date__lte=sunday
    ).exists()
    
    if existing_entries:
        messages.warning(request, "Current week is not empty. Auto-scheduling skipped.")
        return redirect('calendar_view')
    
    # Get user mappings
    mappings = {m.day_of_week: m.category for m in UserScheduleMapping.objects.filter(user=request.user)}
    
    scheduled_count = 0
    for i in range(7):
        # UserScheduleMapping uses 0=Sunday, 1=Monday...
        # range(7) with i=0 is Monday in our date loop, but let's align.
        current_date = monday + timedelta(days=i)
        # weekday() 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
        # mappings uses 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat
        mapping_day = (i + 1) % 7
        
        category = mappings.get(mapping_day)
        if category:
            # Pick a random recipe for this category
            recipes = Recipe.objects.filter(categories=category, user=request.user)
            if recipes.exists():
                recipe = random.choice(list(recipes))
                CalendarEntry.objects.create(
                    user=request.user,
                    date=current_date,
                    recipe=recipe,
                    meal_type='dinner'
                )
                scheduled_count += 1
    
    if scheduled_count > 0:
        messages.success(request, f"Scheduled {scheduled_count} recipes for the week!")
    else:
        messages.info(request, "No recipes scheduled. Check your Admin settings and category assignments.")
        
    return redirect('calendar_view')


@login_required
@require_POST
def replace_calendar_recipe(request, pk):
    """Replace a scheduled recipe with another random recipe from the same category."""
    entry = get_object_or_404(CalendarEntry, pk=pk, user=request.user)
    
    # Get categories of the current recipe
    categories = entry.recipe.categories.all()
    if not categories.exists():
        messages.warning(request, "This recipe has no categories. Cannot find a replacement.")
        return redirect(f'/calendar/?year={entry.date.year}&month={entry.date.month}')
    
    # Find other recipes in the same categories
    # Use first category for replacement logic
    category = categories.first()
    other_recipes = Recipe.objects.filter(categories=category, user=request.user).exclude(pk=entry.recipe.pk)
    
    if other_recipes.exists():
        new_recipe = random.choice(list(other_recipes))
        entry.recipe = new_recipe
        entry.save(update_fields=['recipe'])
        messages.success(request, f'Replaced with "{new_recipe.title}".')
    else:
        messages.info(request, f'No other recipes found in category "{category.name}".')
        
    return redirect(f'/calendar/?year={entry.date.year}&month={entry.date.month}')


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

    # Check if the current week is empty for the auto-schedule button
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    has_week_entries = CalendarEntry.objects.filter(
        user=request.user,
        date__gte=monday,
        date__lte=sunday
    ).exists()

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
        'has_week_entries': has_week_entries,
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
