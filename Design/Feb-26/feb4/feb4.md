1. Recipes page 
1.1 The ingredients have two empty bullet points
1.2 The ingredients have two decimal points, remove them from view recipe and edit recipe page 
1.5 Recipe page: The photo is too big and cropped. I prefer to see the whole picture and much smaller so I can see photo, ingredients and method without scrolling on my laptop screen

2 Ingredients 
2.1 Ingredients should be maintained in the database as they are entered in different recipes by the user
2.1 When I create a new recipe and I enter an ingredient, I want it to help me populate the ingredient name (either from a fixed list of ingredients, or better yet my historical data. This is similar functionality of what excel does). The reason I need that, is because I want the system to understand that if I say "onion" and "onions" for example, that I mean the same thing, so it adds the ingredients correctly. 

3 My recipes page
3.1 recipes should be sorted by alphabetical order 
3.2 Add another way to view the recipes. Currently the default way is thumbails, add list way where only linked title is shown 

4 New Recipes page 
4.1 Add three tabs at this page to offer three options to the user to create new recipes. 
    - Create from text 
    - Form 
    - Create from link 
4.2 Tab Form will have the fields of `/recipes/new/` 
4.3 Tab create from text will just provide a text area to the user to write the ingredients and then the steps (1, 2, 3) and press button generate recipe. System should then create the recipe. 
4.4 Tab create from link: User will enter a URL link and click generate recipe. System will use the library recipe-scrapers (already installed) to scrape the ingredients and the instructions. 
Sample code: 
from recipe_scrapers import scrape_me

# Give it any recipe URL
scraper = scrape_me('https://www.allrecipes.com/recipe/15896/baked-ziti-ii/')

print(scraper.ingredients())
print(scraper.instructions())