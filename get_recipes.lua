local names = ""

for recipe_name, recipe in pairs(game.recipe_prototypes) do
    local match = string.match(recipe_name, "(.*)%-pyvoid%-gas")
    if match then
        fluid = game.get_filtered_fluid_prototypes({{filter = "name", name = match}})
        if recipe.ingredients[1].minimum_temperature == fluid[match].default_temperature then
            names = names .. match .. "\n"
        end
    end
end

game.write_file("recipes.gas", names)

local names = ""

for recipe_name, recipe in pairs(game.recipe_prototypes) do
    local match = string.match(recipe_name, "(.*)%-pyvoid%-fluid")
    if match then
            names = names .. match .. "\n"
    end
end

game.write_file("recipes.liquid", names)