import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Step 1: Load your trained models
make_model = joblib.load("MVL_make_ML_MDL.joblib")
model_model = joblib.load("MVL_model_ML_MDL.joblib")
variant_model = joblib.load("MVL_Variant_ML_MDL.joblib")
type_model = joblib.load("MVL_Type_ML_MDL.joblib")
bodystyle_model = joblib.load("MVL_Bodystyle_ML_MDL.joblib")
engine_model = joblib.load("MVL_Engine_ML_MDL.joblib")

# Step 2: Load your dataset
df = pd.read_excel("train sheet.xlsx")

# Assuming columns are: 'combined details', 'Engine'
X = df["combined details"]
y = df["Engine"]

# Step 3: Generate predictions from base models
base_predictions = pd.DataFrame({
    'make_pred': make_model.predict(X),
    'model_pred': model_model.predict(X),
    'variant_pred': variant_model.predict(X),
    'type_pred': type_model.predict(X),
    'bodystyle_pred': bodystyle_model.predict(X),
    'engine_pred': engine_model.predict(X)
})

# Step 4: Split stacked data
X_train, X_test, y_train, y_test = train_test_split(base_predictions, y, test_size=0.2, random_state=42)

# Step 5: Define a meta-model (you can change this)
meta_model = RandomForestClassifier(n_estimators=200, random_state=42)
# or try: meta_model = LogisticRegression(max_iter=1000)

# Step 6: Train meta-model on base predictions
meta_model.fit(X_train, y_train)

# Step 7: Evaluate
y_pred = meta_model.predict(X_test)
print("Meta-model Accuracy:", accuracy_score(y_test, y_pred))

# Step 8: Save stacked model
joblib.dump(meta_model, "MVL_Stacked_ML_Model.joblib")
print("✅ Stacked model saved successfully!")
