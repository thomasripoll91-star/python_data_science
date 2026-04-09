from fastapi import FastAPI, Query
from pydantic import BaseModel
from enum import Enum
import pandas as pd
import joblib

app = FastAPI(title="API Telco Churn - Interface Intuitive")

# 1. Chargement
modele = joblib.load('../model.pkl')
preprocessor = joblib.load('preprocessor.pkl')


# 2. Définition des choix pour les listes déroulantes
class PaymentMethodEnum(str,Enum):
    Electronic_check = "Electronic check"
    Mailed_check = "Mailed check",
    Bank_transfer = "Bank transfer (automatic)"
    Credit_card = "Credit card (automatic)"

class OuiNon(str, Enum):
    oui = "Oui"
    non = "Non"

class ContratEnum(str, Enum):
    month = "Month-to-month"
    one_year = "One year"
    two_year = "Two year"

class InternetEnum(str, Enum):
    no = "No"
    dsl = "DSL"
    fiber = "Fiber optic"
    

# Mapping pour traduire les choix utilisateur en données IA
MAPPING_OUI_NON = {"Oui": 1, "Non": 0}

PROFIL_CACHE = {
    "gender": "Female", "SeniorCitizen": 0, "Partner": 0, "Dependents": 0,
    "MultipleLines": 0, "StreamingTV": 0, "PaperlessBilling": 1, "TotalCharges": 29.85
}

@app.post("/predict")
def predict_churn(
    tenure: int = Query(..., description="Nombre de mois"),
    PhoneService: OuiNon = Query(..., description="Service téléphone (Obligatoire)"),
    InternetService: InternetEnum = Query(..., description="Service en ligne (Obligatoire)"),
    OnlineSecurity: OuiNon = Query(..., description="Sécurité en ligne (Obligatoire)"),
    OnlineBackup: OuiNon = Query(..., description="Sauvegarde en ligne (Obligatoire)"),
    DeviceProtection: OuiNon = Query(..., description="Protection appareil (Obligatoire)"),
    TechSupport: OuiNon = Query(..., description="Support technique (Obligatoire)"),
    StreamingMovies: OuiNon = Query(..., description="Streaming Films (Obligatoire)"),
    Contract: ContratEnum = Query(..., description="Type de contrat (Obligatoire)"),
    PaymentMethod: PaymentMethodEnum = Query(..., description="Type de payement (Obligatoire)"),
    MonthlyCharges: float = Query(..., description="Montant mensuel (Obligatoire)"),
    
):
    try:
        # Conversion des choix "Oui/Non" en 1/0 pour le modèle
        input_data = {
            "tenure": tenure,
            "PhoneService": MAPPING_OUI_NON[PhoneService],
            "InternetService": InternetService.value,
            "OnlineSecurity": MAPPING_OUI_NON[OnlineSecurity],
            "OnlineBackup": MAPPING_OUI_NON[OnlineBackup],
            "DeviceProtection": MAPPING_OUI_NON[DeviceProtection],
            "TechSupport": MAPPING_OUI_NON[TechSupport],
            "StreamingMovies": MAPPING_OUI_NON[StreamingMovies],
            "Contract": Contract.value,
            "PaymentMethod": PaymentMethod.value,
            "MonthlyCharges": MonthlyCharges
        }
        
        # Fusion avec les colonnes cachées
        donnees_finales = {**PROFIL_CACHE, **input_data}
        df_client = pd.DataFrame([donnees_finales])
        
        # Alignement strict avec le preprocessor
        cols_preproc = list(preprocessor.feature_names_in_)
        df_client = df_client[cols_preproc]
        
        # Transformation et Prédiction
        X_transformed = preprocessor.transform(df_client)
        X_final = pd.DataFrame(X_transformed, columns=list(modele.feature_names_in_))
        
        prediction = modele.predict(X_final)[0]
        probabilite = modele.predict_proba(X_final)[0][1]
        
# f. La Prédiction Finale
        prediction = modele.predict(X_final)[0]
        probabilite_churn = modele.predict_proba(X_final)[0][1] # Probabilité de partir
        
        if prediction == 1:
            # Cas : Risque de départ
            resultat = "RISQUE DE départ"
            # On affiche la probabilité de partir telle quelle
            score_final = probabilite_churn 
            label_score = "Risque de départ"
        else:
            # Cas : Fidèle
            resultat = "CLIENT FIDÈLE"
            # On inverse : 1 - risque de partir = probabilité de rester
            score_final = 1 - probabilite_churn 
            label_score = "Confiance du client"

        return {
            "diagnostic": resultat,
            label_score: f"{score_final * 100:.1f}%",
            "statut": "Analyse terminée"
        }
        
    except Exception as e:
        return {"error": str(e)}