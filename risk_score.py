def calculate_risk_score(breaches, platforms):
    """
    Calculates a digital risk score from 0 to 100 based on the findings.
    - 0 means no digital footprint/risk found.
    - 100 means extremely high risk (many breaches, lots of leaked sensitive info).
    """
    score = 0
    
    # 1. Evaluate Breaches (Heavy weight)
    # Base penalty for each data breach found
    for breach in breaches:
        score += 20 
        
        # Additional penalty for highly sensitive data classes leaked
        sensitive_classes = ['Passwords', 'Credit cards', 'Social Security Numbers', 'Health data', 'Bank account numbers']
        classes = breach.get('DataClasses', [])
        for data_class in classes:
            if data_class in sensitive_classes:
                score += 10
                
    # 2. Evaluate Platforms (Light weight footprint tracking)
    # A large public footprint inherently increases your attack surface
    score += len(platforms) * 5
    
    # Cap the score strictly between 0 and 100
    if score > 100:
        score = 100
        
    # Determine risk category text for the UI
    category = "Low"
    if score >= 75:
        category = "Critical"
    elif score >= 50:
        category = "High"
    elif score >= 25:
        category = "Moderate"
        
    return {
        "score": score,
        "category": category
    }

# For testing this script independently
if __name__ == "__main__":
    mock_breaches = [{"Name": "Test", "DataClasses": ["Passwords", "Email addresses"]}]
    mock_platforms = [{"platform": "GitHub"}, {"platform": "Twitter"}]
    print(calculate_risk_score(mock_breaches, mock_platforms))
