
class NutritionInformation:
    calories: float # Calorias
    total_fats: float # Total de grasas
    cholesterol: float # Colesterol
    sodium: float # Sodio
    total_carbohydrates: float # Carbohidratos totales
    protein: float # Proteina
    vitamins_minerals: dict[str, float]
    servings_per_persons: float # Porciones por persona. Ej: Para 3 personas
    