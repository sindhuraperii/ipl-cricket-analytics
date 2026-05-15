import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle

print("=" * 80)
print("🤖 TRAINING MACHINE LEARNING MODELS")
print("=" * 80 + "\n")

# ============================================
# LOAD PREPARED DATA
# ============================================

print("📥 Loading prepared data...\n")

X_train = pd.read_csv('data/processed/X_train.csv')
X_test = pd.read_csv('data/processed/X_test.csv')
y_train = pd.read_csv('data/processed/y_train.csv').values.ravel()
y_test = pd.read_csv('data/processed/y_test.csv').values.ravel()

print(f"   Training set: {X_train.shape}")
print(f"   Testing set: {X_test.shape}\n")

# ============================================
# MODEL 1: LOGISTIC REGRESSION
# ============================================

print("⚙️ Training Model 1: Logistic Regression...\n")

lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train, y_train)

# Predictions
y_pred_lr = lr_model.predict(X_test)

# Metrics
lr_accuracy = accuracy_score(y_test, y_pred_lr)
lr_precision = precision_score(y_test, y_pred_lr)
lr_recall = recall_score(y_test, y_pred_lr)
lr_f1 = f1_score(y_test, y_pred_lr)

print(f"   ✅ Logistic Regression Results:")
print(f"      • Accuracy:  {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")
print(f"      • Precision: {lr_precision:.4f}")
print(f"      • Recall:    {lr_recall:.4f}")
print(f"      • F1-Score:  {lr_f1:.4f}\n")

# ============================================
# MODEL 2: RANDOM FOREST
# ============================================

print("⚙️ Training Model 2: Random Forest...\n")

rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# Predictions
y_pred_rf = rf_model.predict(X_test)

# Metrics
rf_accuracy = accuracy_score(y_test, y_pred_rf)
rf_precision = precision_score(y_test, y_pred_rf)
rf_recall = recall_score(y_test, y_pred_rf)
rf_f1 = f1_score(y_test, y_pred_rf)

print(f"   ✅ Random Forest Results:")
print(f"      • Accuracy:  {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
print(f"      • Precision: {rf_precision:.4f}")
print(f"      • Recall:    {rf_recall:.4f}")
print(f"      • F1-Score:  {rf_f1:.4f}\n")

# ============================================
# MODEL COMPARISON
# ============================================

print("📊 MODEL COMPARISON:\n")

models_comparison = pd.DataFrame({
    'Model': ['Logistic Regression', 'Random Forest'],
    'Accuracy': [lr_accuracy, rf_accuracy],
    'Precision': [lr_precision, rf_precision],
    'Recall': [lr_recall, rf_recall],
    'F1-Score': [lr_f1, rf_f1]
})

print(models_comparison.to_string(index=False))
print()

# Choose best model
best_model = rf_model if rf_accuracy > lr_accuracy else lr_model
best_model_name = 'Random Forest' if rf_accuracy > lr_accuracy else 'Logistic Regression'

print(f"🏆 BEST MODEL: {best_model_name}\n")

# ============================================
# SAVE MODELS
# ============================================

print("💾 Saving models...\n")

with open('models/logistic_regression_model.pkl', 'wb') as f:
    pickle.dump(lr_model, f)

with open('models/random_forest_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

with open('models/best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

print("   ✅ Models saved:")
print("      • models/logistic_regression_model.pkl")
print("      • models/random_forest_model.pkl")
print("      • models/best_model.pkl\n")

# ============================================
# FEATURE IMPORTANCE (Random Forest)
# ============================================

print("🔍 FEATURE IMPORTANCE (Random Forest):\n")

feature_importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print(feature_importance.to_string(index=False))
print()

print("=" * 80)
print("✅ MODEL TRAINING COMPLETE!")
print("=" * 80 + "\n")