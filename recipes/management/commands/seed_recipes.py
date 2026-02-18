from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from recipes.models import Recipe, RecipeIngredient, Category

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with 25 public recipes'

    def handle(self, *args, **options):
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
            self.stdout.write(self.style.SUCCESS(f'Created superuser: admin'))

        categories_data = ['Meat', 'Beans', 'Fish', 'Chicken', 'Pasta']
        categories = {}
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name), 'user': user}
            )
            categories[cat_name] = cat

        recipes_data = {
            'Meat': [
                ('Beef Stew', 'Classic hearty stew', ['Beef|500g|Meat', 'Potatoes|3|Produce', 'Carrots|2|Produce']),
                ('Pork Chops', 'Grilled pork chops', ['Pork|2|Meat', 'Garlic|1 clove|Produce']),
                ('Steak Frites', 'Pan-seared steak', ['Steak|1|Meat', 'Potatoes|2|Produce']),
                ('Lamb Curry', 'Spicy lamb curry', ['Lamb|400g|Meat', 'Curry Paste|2 tbsp|Pantry']),
                ('Bacon & Eggs', 'Simple breakfast', ['Bacon|4 strips|Meat', 'Eggs|2|Dairy']),
            ],
            'Beans': [
                ('Black Bean Soup', 'Spiced bean soup', ['Black Beans|1 can|Canned', 'Onion|1|Produce']),
                ('Chickpea Salad', 'Fresh summer salad', ['Chickpeas|1 can|Canned', 'Cucumber|1|Produce']),
                ('Lentil Dahl', 'Traditional lentils', ['Lentils|200g|Pantry', 'Turmeric|1 tsp|Spices']),
                ('Baked Beans', 'Homemade on toast', ['Navy Beans|1 can|Canned', 'Tomato Sauce|100ml|Pantry']),
                ('Chili Sin Carne', 'Veggie chili', ['Kidney Beans|1 can|Canned', 'Peppers|2|Produce']),
            ],
            'Fish': [
                ('Grilled Salmon', 'Lemon garlic salmon', ['Salmon|1 fillet|Fish', 'Lemon|1|Produce']),
                ('Fish & Chips', 'Crispy battered cod', ['Cod|200g|Fish', 'Potatoes|2|Produce']),
                ('Tuna Melt', 'Classic tuna sandwich', ['Tuna|1 can|Canned', 'Bread|2 slices|Bakery']),
                ('Shrimp Scampi', 'Garlic butter shrimp', ['Shrimp|200g|Fish', 'Pasta|100g|Pasta']),
                ('Seafood Paella', 'Spanish rice dish', ['Mixed Seafood|300g|Fish', 'Rice|100g|Pantry']),
            ],
            'Chicken': [
                ('Roast Chicken', 'Whole roast chicken', ['Chicken|1 whole|Meat', 'Herbs|1 bunch|Produce']),
                ('Chicken Curry', 'Creamy mild curry', ['Chicken Breast|200g|Meat', 'Coconut Milk|200ml|Canned']),
                ('Chicken Wings', 'Spicy buffalo wings', ['Wings|10|Meat', 'Hot Sauce|2 tbsp|Pantry']),
                ('Stir Fry Chicken', 'Quick veggie mix', ['Chicken|150g|Meat', 'Broccoli|1|Produce']),
                ('Chicken Caesar', 'Classic salad', ['Chicken|100g|Meat', 'Lettuce|1|Produce']),
            ],
            'Pasta': [
                ('Spaghetti Carbonara', 'Egg and bacon pasta', ['Spaghetti|100g|Pasta', 'Bacon|50g|Meat', 'Eggs|2|Dairy']),
                ('Penne Arrabbiata', 'Spicy tomato sauce', ['Penne|100g|Pasta', 'Chillies|2|Produce']),
                ('Lasagna', 'Layers of beef and cheese', ['Pasta Sheets|6|Pasta', 'Minced Beef|200g|Meat']),
                ('Mac & Cheese', 'Ultra cheesy pasta', ['Macaroni|100g|Pasta', 'Cheese|100g|Dairy']),
                ('Pesto Pasta', 'Basil and pine nuts', ['Fusilli|100g|Pasta', 'Pesto|2 tbsp|Pantry']),
            ]
        }

        for cat_name, recipes in recipes_data.items():
            category = categories[cat_name]
            for title, desc, ingredients in recipes:
                recipe, created = Recipe.objects.get_or_create(
                    title=title,
                    user=user,
                    defaults={'description': desc, 'instructions': '1. Prep\n2. Cook\n3. Eat', 'public': True}
                )
                recipe.categories.add(category)
                
                # Add ingredients
                for idx, ing_str in enumerate(ingredients):
                    name, qty, aisle = ing_str.split('|')
                    RecipeIngredient.objects.get_or_create(
                        recipe=recipe,
                        name=name,
                        defaults={'quantity': qty, 'aisle': aisle, 'order': idx}
                    )
                self.stdout.write(f'Added recipe: {title}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded 25 recipes.'))
