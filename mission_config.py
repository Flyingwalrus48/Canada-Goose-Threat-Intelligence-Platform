# mission_config.py

# --- MISSION OVERVIEW ---
TARGET_DESTINATION = "Mexico City, Mexico"
MISSION_TIMEFRAME = "November 15-20, 2025"
PRINCIPAL = "EVP of North American Operations"
OVERALL_RISK_LEVEL = "HIGH"

# --- KEY INTELLIGENCE FINDINGS (Manually Researched for Demo) ---
KEY_FINDINGS = [
    {
        'threat_level': 'HIGH',
        'source': 'Local Crime Analytics',
        'finding': 'High risk of opportunistic street crime (theft, robbery) in Polanco and Condesa districts, targeting individuals with luxury watches or electronics.'
    },
    {
        'threat_level': 'MEDIUM',
        'source': 'OSINT - News Analysis',
        'finding': 'Recent protests by teachers\' unions have caused significant, unannounced traffic disruptions in the city center near the Zócalo.'
    },
    {
        'threat_level': 'MEDIUM',
        'source': 'Gov. of Canada Advisory',
        'finding': 'Official advisory warns of express kidnapping risk and recommends avoiding unofficial taxis. Use of app-based services (Uber, DiDi) or vetted car services is essential.'
    }
]

# --- RECOMMENDED MITIGATION STRATEGIES ---
MITIGATION_STRATEGIES = {
    'Personal Security': [
        'Maintain a low profile; avoid wearing expensive jewelry or watches publicly.',
        'Do not use your mobile phone while walking on the street; step into a shop if needed.',
        'Vary routines and travel times to avoid establishing a predictable pattern.'
    ],
    'Transportation': [
        'Exclusively use pre-booked, vetted car services for all movements.',
        'Confirm driver and vehicle details (license plate) before entering.',
        'Share your live location with the security team during all transits.'
    ],
    'Contingency': [
        'In case of a robbery, comply with demands. Do not resist.',
        'The primary designated safe haven is the Canadian Embassy in Mexico City.',
        'Immediate medical support is available at the recommended hospitals listed below.'
    ]
}

# --- DESTINATION FACTSHEET ---
DESTINATION_FACTSHEET = {
    'Vetted Hospitals': [
        {'name': 'ABC Medical Center, Santa Fe Campus', 'address': 'Av. Carlos Graef Fernández 154, Santa Fe, Cuajimalpa', 'notes': 'Top-tier private hospital with bilingual staff.'},
        {'name': 'Hospital Español', 'address': 'Av. Ejército Nacional Mexicano 613, Polanco', 'notes': 'Well-regarded hospital in a central upscale district.'}
    ],
    'Cultural & Legal Considerations': [
        'Business etiquette is formal. Punctuality is respected but not always strictly observed.',
        'It is illegal to drink alcohol in public spaces.',
        'Carry a copy of your passport and visa; keep the original in a hotel safe.'
    ],
    'Visa & Immigration': [
        'Canadian citizens do not require a visa for tourist or business stays up to 180 days.',
        'A valid passport and a completed Multiple Migratory Form (FMM) are required upon entry.'
    ]
}
# mission_config.py

QUANTITATIVE_ALERTS = [
    {'source': 'Aviation Data Feed', 'alert': 'Detected a 35% spike in flight cancellations at MEX airport in the last 48 hours.'},
    {'source': 'Currency Monitor', 'alert': 'CAD/MXN exchange rate shows high volatility, increasing 3%.'}
]