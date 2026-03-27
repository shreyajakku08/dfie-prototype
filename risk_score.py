def calculate_risk_score(breaches, platforms):
    """
    Calculates the Digital Footprint Exposure Index (Risk Score). 
    Backed by the Mathematical Weighted Risk Aggregate:
    
        R = min(100, \\sum_{i=1}^{n} (w_i * p_i) + C)
        
    Where:
        - w_i: The threat weight of the vulnerability (Platform impact)
        - p_i: The presence of the data point (Number of platforms)
        - C: The Critical modifier for historically severe breaches
    """
    
    # Base accumulation for formula \\sum (w_i * p_i)
    sigma_wp = 0
    # Base critical decay modifier (C)
    critical_mod_C = 0
    
    # 1. Evaluate Breaches (Critical Modifier C calculation)
    # The 'C' variable aggregates explicit structural vulnerabilities
    for breach in breaches:
        # Each known breach adds a baseline critical weight of +20
        critical_mod_C += 20 
        
        # Deep telemetry scanning for high-severity payloads
        sensitive_classes = ['Passwords', 'Credit cards', 'Social Security Numbers', 'Health data', 'Bank account numbers']
        classes = breach.get('DataClasses', [])
        for data_class in classes:
            if data_class in sensitive_classes:
                critical_mod_C += 10
                
    # 2. Evaluate Platforms (w_i * p_i calculation)
    # p_i = number of platforms, w_i = standard expansion weight 5
    p_i = len(platforms)
    w_i = 5
    sigma_wp += (w_i * p_i)
    
    # Solve final Risk Aggr algorithm R
    R = sigma_wp + critical_mod_C
    
    # Cap the final score natively at 100 max
    final_score = min(100, R)
        
    # Determine algorithmic risk category boundary for the UI
    category = "LOW RISK"
    if final_score >= 75:
        category = "CRITICAL THREAT"
    elif final_score >= 50:
        category = "ELEVATED RISK"
    elif final_score >= 25:
        category = "MODERATE RISK"
        
    return {
        "score": final_score,
        "category": category
    }

# For testing this script independently
if __name__ == "__main__":
    mock_breaches = [{"Name": "Test", "DataClasses": ["Passwords", "Email addresses"]}]
    mock_platforms = [{"platform": "GitHub"}, {"platform": "Twitter"}]
    print(calculate_risk_score(mock_breaches, mock_platforms))
