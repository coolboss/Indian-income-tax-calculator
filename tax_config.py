# tax_config.py

# Financial Year Config
CURRENT_FY = "2024-25"
ASSESSMENT_YEAR = "2025-26"

# Standard Deduction
STANDARD_DEDUCTION = 75000  # New regime standard deduction

# New Regime Tax Slabs
NEW_REGIME_SLABS = [
    {"limit": 300000, "rate": 0},
    {"limit": 600000, "rate": 0.05},
    {"limit": 900000, "rate": 0.10},
    {"limit": 1200000, "rate": 0.15},
    {"limit": 1500000, "rate": 0.20},
    {"limit": float('inf'), "rate": 0.30}
]

# Old Regime Tax Slabs
OLD_REGIME_SLABS = [
    {"limit": 250000, "rate": 0},
    {"limit": 500000, "rate": 0.05},
    {"limit": 1000000, "rate": 0.20},
    {"limit": float('inf'), "rate": 0.30}
]

# Surcharge Slabs
SURCHARGE_SLABS = {
    "new_regime": [
        {"limit": 50000000, "rate": 0.25},  # > 5 crore
        {"limit": 20000000, "rate": 0.15},  # > 2 crore
        {"limit": 10000000, "rate": 0.10},  # > 1 crore
    ],
    "old_regime": [
        {"limit": 50000000, "rate": 0.37},  # > 5 crore
        {"limit": 20000000, "rate": 0.25},  # > 2 crore
        {"limit": 10000000, "rate": 0.15},  # > 1 crore
    ]
}

# Cess Rate
CESS_RATE = 0.04

# Deduction Limits
DEDUCTION_LIMITS = {
    "80C": 150000,
    "80D": {
        "senior_citizen": 50000,
        "normal": 25000
    },
    "80CCD": 50000,
}

# Important Dates
TAX_DATES = {
    "advance_tax": [
        {"date": "15 Jun 2024", "percentage": 15},
        {"date": "15 Sep 2024", "percentage": 45},
        {"date": "15 Dec 2024", "percentage": 75},
        {"date": "15 Mar 2025", "percentage": 100}
    ],
    "filing_deadline": "31 Jul 2025",
    "audit_deadline": "30 Sep 2024"
}