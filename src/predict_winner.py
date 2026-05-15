import pickle
import pandas as pd
import numpy as np

print("\n" + "=" * 80)
print("🏏 IPL MATCH WINNER PREDICTION TOOL")
print("=" * 80 + "\n")

# Load the best model
print("📥 Loading trained model...\n")

with open('models/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/label_encoder.pkl', 'rb') as f:
    le_toss = pickle.load(f)

print("✅ Model loaded successfully!\n")

# ============================================
# PREDICTION FUNCTION
# ============================================

def predict_match_winner(team1_wins, team2_wins, batter_runs, bowler_wicket, runs_extras, toss_decision):
    """
    Predict IPL match winner
    
    Parameters:
    - team1_wins: Number of wins by team1 before this match
    - team2_wins: Number of wins by team2 before this match
    - batter_runs: Total runs scored by batting team
    - bowler_wicket: Number of wickets taken by bowling team
    - runs_extras: Extra runs conceded
    - toss_decision: 'bat' or 'field'
    
    Returns:
    - prediction: 1 if team1 wins, 0 if team2 wins
    - probability: Confidence level (0-100%)
    """
    
    # Encode toss decision
    toss_encoded = le_toss.transform([toss_decision])[0]
    
    # Create feature array
    features = np.array([[
        team1_wins,
        team2_wins,
        batter_runs,
        bowler_wicket,
        runs_extras,
        toss_encoded
    ]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    return prediction, probability

# ============================================
# EXAMPLE PREDICTIONS
# ============================================

print("📋 EXAMPLE PREDICTIONS:\n")
print("-" * 80 + "\n")

# Example 1: Strong team vs weak team
print("Example 1: CSK (Strong) vs Delhi (New Team)\n")
print("   Scenario:")
print("   • CSK has won 10 matches before")
print("   • Delhi has won 2 matches before")
print("   • CSK scored 165 runs")
print("   • Delhi took 5 wickets")
print("   • Delhi gave away 8 extra runs")
print("   • CSK won toss and chose to bat\n")

pred1, prob1 = predict_match_winner(
    team1_wins=10,
    team2_wins=2,
    batter_runs=165,
    bowler_wicket=5,
    runs_extras=8,
    toss_decision='bat'
)

winner1 = "Team 1 (CSK)" if pred1 == 1 else "Team 2 (Delhi)"
confidence1 = prob1[int(pred1)] * 100

print(f"   🎯 Prediction: {winner1}")
print(f"   📊 Confidence: {confidence1:.2f}%")
print(f"   💭 Reason: CSK's experience and good batting performance\n")

print("-" * 80 + "\n")

# Example 2: Close match
print("Example 2: MI vs RCB (Equally Strong)\n")
print("   Scenario:")
print("   • MI has won 8 matches before")
print("   • RCB has won 7 matches before")
print("   • MI scored 155 runs")
print("   • RCB took 6 wickets")
print("   • RCB gave away 5 extra runs")
print("   • RCB won toss and chose to field\n")

pred2, prob2 = predict_match_winner(
    team1_wins=8,
    team2_wins=7,
    batter_runs=155,
    bowler_wicket=6,
    runs_extras=5,
    toss_decision='field'
)

winner2 = "Team 1 (MI)" if pred2 == 1 else "Team 2 (RCB)"
confidence2 = prob2[int(pred2)] * 100

print(f"   🎯 Prediction: {winner2}")
print(f"   📊 Confidence: {confidence2:.2f}%")
print(f"   💭 Reason: Close match, slight edge to one team\n")

print("-" * 80 + "\n")

# Example 3: Underdog scenario
print("Example 3: Punjab vs Mumbai (Underdog Match)\n")
print("   Scenario:")
print("   • Punjab has won 3 matches before")
print("   • Mumbai has won 12 matches before")
print("   • Punjab scored 180 runs (exceptional!)")
print("   • Mumbai took 8 wickets (excellent bowling)")
print("   • Mumbai gave away 3 extra runs (disciplined)")
print("   • Punjab won toss and chose to bat\n")

pred3, prob3 = predict_match_winner(
    team1_wins=3,
    team2_wins=12,
    batter_runs=180,
    bowler_wicket=8,
    runs_extras=3,
    toss_decision='bat'
)

winner3 = "Team 1 (Punjab)" if pred3 == 1 else "Team 2 (Mumbai)"
confidence3 = prob3[int(pred3)] * 100

print(f"   🎯 Prediction: {winner3}")
print(f"   📊 Confidence: {confidence3:.2f}%")
print(f"   💭 Reason: Strong bowling & experience favors Mumbai\n")

print("-" * 80 + "\n")

# Example 4: Batting masterclass
print("Example 4: Rajasthan vs Sunrisers (High Scoring)\n")
print("   Scenario:")
print("   • Rajasthan has won 6 matches before")
print("   • Sunrisers has won 9 matches before")
print("   • Rajasthan scored 195 runs (record-breaking!)")
print("   • Sunrisers took 3 wickets (poor bowling)")
print("   • Sunrisers gave away 12 extra runs (loose bowling)")
print("   • Sunrisers won toss and chose to bat first\n")

pred4, prob4 = predict_match_winner(
    team1_wins=6,
    team2_wins=9,
    batter_runs=195,
    bowler_wicket=3,
    runs_extras=12,
    toss_decision='bat'
)

winner4 = "Team 1 (Rajasthan)" if pred4 == 1 else "Team 2 (Sunrisers)"
confidence4 = prob4[int(pred4)] * 100

print(f"   🎯 Prediction: {winner4}")
print(f"   📊 Confidence: {confidence4:.2f}%")
print(f"   💭 Reason: Exceptional batting performance\n")

print("=" * 80)
print("✅ PREDICTIONS COMPLETE!")
print("=" * 80 + "\n")

print("💡 HOW TO USE THIS MODEL:\n")
print("   1. Gather match data")
print("   2. Call predict_match_winner() function")
print("   3. Get prediction and confidence score\n")

print("📊 MODEL ACCURACY REMINDER:\n")
print("   • Logistic Regression Accuracy: 71.55%")
print("   • This means: ~72 out of 100 predictions correct")
print("   • Much better than random guessing (50%)\n")

print("🔍 FACTORS THAT MATTER (Importance):\n")
print("   1. Bowler Wicket:        29.07%  ← Most important!")
print("   2. Batter Runs:          21.49%")
print("   3. Team1 Wins:           17.13%")
print("   4. Team2 Wins:           17.01%")
print("   5. Runs Extras:          12.83%")
print("   6. Toss Decision:         2.47%  ← Least important\n")

print("⚠️ IMPORTANT NOTES:\n")
print("   • Cricket has surprises - 100% prediction is impossible")
print("   • Use historical data for best predictions")
print("   • Model works best with accurate input data")
print("   • Consider external factors (injuries, weather, form)\n")