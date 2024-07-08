from pydantic import BaseModel, ConfigDict, Field
from prediction.constants import ActivityFactor, Gender, Objectives

# Weight se medira en kg y height en cm.

class UserData(BaseModel):
    gender: Gender = Field(description="Puede ser FEMENINO o MASCULINO")
    weight: float = Field(description="En kilogramos")
    height: float = Field(description="En centimetros")
    age: int
    objective: Objectives = Field("Puede ser PERDER_PESO, GANAR_MASA_MUSCULAR, MANTENER_PESO")
    activity_factor: ActivityFactor = Field(description="Puede ser MUY_LIGERA, LIGERA, MODERADA, INTENSA, MUY_INTENSA")
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        populate_by_name=True,
        json_schema_extra = {
            "example": {
                "gender": "M",
                "weight": 70.0,
                "height": 180.0,
                "age": 30,
                "objective": "GANAR_MASA_MUSCULAR",
                "activity_factor": "MODERADA"
            }
        },
    )
    #Indice de masa muscular
    def calculate_IMC(self):
        height_m = self.height / 100
        return self.weight / (height_m ** 2)
    
    def calculate_TMB(self):
        TMB = (10 * self.weight) + (6.25 * self.height) - (5 * self.age)
        if self.gender.value == "M":
            TMB += 5
        else:
            TMB -= - 161  
        if self.objective.value is not 0:
            cal_per_objective_min = float(self.objective.value) * float(0.5)
            cal_per_objective_max = float(self.objective.value)
            cal_per_objective = (cal_per_objective_max - cal_per_objective_min) / 2
        else:
            cal_per_objective = 0

        if self.objective.name == Objectives.GANAR_MASA_MUSCULAR:
            return (float(TMB) * float(self.activity_factor.value)) + float(cal_per_objective) 

        return (float(TMB) * float(self.activity_factor.value)) - float(cal_per_objective)

    # Envia la cantidad de proteinas, grasas y carbohidratos de un alimento y devuelve un boolean si la ingesta de macronutrientes
    # es adecuada.
    def calculate_calories_by_macronutrients(self, proteins: float, fats: float, carbs: float):
        expected_proteins, expected_carbs, expected_fats = self._get_expected_macronutrients_percentage()
        cal_proteins = proteins * 4
        cal_carbs = carbs * 4
        cal_fats = fats * 9
        total_cals = cal_proteins + cal_fats + cal_carbs

        per_proteins = cal_proteins / total_cals
        per_carbs = cal_carbs / total_cals
        per_fats = cal_fats / total_cals
        
        return (per_proteins / 3 <= expected_proteins 
                                        and per_carbs / 3 <= expected_carbs 
                                        and per_fats / 3 <= expected_fats)

    # Envia el porcentaje de proteinas, grasas y carbohidratos de un alimento por dia
    def _get_expected_macronutrients_percentage(self):
        objective = self.objective.name
        if objective is Objectives.MANTENER_PESO:
            #proteins, carbs and fats
            return 0.15, 0.6, 0.3 
        elif objective is Objectives.GANAR_MASA_MUSCULAR:
            return 0.24, 0.48, 0.28
        else:
            return 0.35, 0.45, 0.35
        
def get_user_data(
    gender: Gender,
    weight_kg: float,
    height_cm: float,
    age: int,
    objective: Objectives,
    activity_factor: ActivityFactor
) -> UserData:
    return UserData(
        gender=gender,
        weight=weight_kg,
        height=height_cm,
        age=age,
        objective=objective,
        activity_factor=activity_factor
    )