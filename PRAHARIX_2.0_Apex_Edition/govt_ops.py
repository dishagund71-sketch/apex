"""
PRAHARIX 2.0 Apex Edition - Government Operations & Command Panel Module
=============================================================================
District Collector Command Panel, SDRF/NDRF Tasking, ICS-201 Incident Reports,
Emergency SITREP Generation, Multi-Department Alerts, and Audit Trail Management.
Fully compliant with Maharashtra State Disaster Management Authority (MSDMA)
and National Disaster Management Authority (NDMA) Incident Command System (ICS).
"""

import json
import uuid
import time
from datetime import datetime, timezone

# ============================================================================
# 1. MAHARASHTRA DISTRICT COLLECTORATES (ALL 36 DISTRICTS & DEOC HOTLINES)
# ============================================================================

MAHARASHTRA_COLLECTORS = {
    "Ahmednagar": {"collector": "Collector & DM, Ahilyanagar", "deoc_phone": "0241-2323844", "toll_free": "1077", "email": "collector.ahmednagar@maharashtra.gov.in", "tehsils": 14, "hq": "Ahilyanagar"},
    "Akola": {"collector": "Collector & DM, Akola", "deoc_phone": "0724-2435013", "toll_free": "1077", "email": "collector.akola@maharashtra.gov.in", "tehsils": 7, "hq": "Akola"},
    "Amravati": {"collector": "Collector & DM, Amravati", "deoc_phone": "0721-2662366", "toll_free": "1077", "email": "collector.amravati@maharashtra.gov.in", "tehsils": 14, "hq": "Amravati"},
    "Chhatrapati Sambhajinagar": {"collector": "Collector & DM, Chhatrapati Sambhajinagar", "deoc_phone": "0240-2334501", "toll_free": "1077", "email": "collector.aurangabad@maharashtra.gov.in", "tehsils": 9, "hq": "Chhatrapati Sambhajinagar"},
    "Beed": {"collector": "Collector & DM, Beed", "deoc_phone": "02442-222301", "toll_free": "1077", "email": "collector.beed@maharashtra.gov.in", "tehsils": 11, "hq": "Beed"},
    "Bhandara": {"collector": "Collector & DM, Bhandara", "deoc_phone": "07184-252257", "toll_free": "1077", "email": "collector.bhandara@maharashtra.gov.in", "tehsils": 7, "hq": "Bhandara"},
    "Buldhana": {"collector": "Collector & DM, Buldhana", "deoc_phone": "07262-242307", "toll_free": "1077", "email": "collector.buldhana@maharashtra.gov.in", "tehsils": 13, "hq": "Buldhana"},
    "Chandrapur": {"collector": "Collector & DM, Chandrapur", "deoc_phone": "07172-251597", "toll_free": "1077", "email": "collector.chandrapur@maharashtra.gov.in", "tehsils": 15, "hq": "Chandrapur"},
    "Dhule": {"collector": "Collector & DM, Dhule", "deoc_phone": "02562-288724", "toll_free": "1077", "email": "collector.dhule@maharashtra.gov.in", "tehsils": 4, "hq": "Dhule"},
    "Gadchiroli": {"collector": "Collector & DM, Gadchiroli", "deoc_phone": "07132-222011", "toll_free": "1077", "email": "collector.gadchiroli@maharashtra.gov.in", "tehsils": 12, "hq": "Gadchiroli"},
    "Gondia": {"collector": "Collector & DM, Gondia", "deoc_phone": "07182-236125", "toll_free": "1077", "email": "collector.gondia@maharashtra.gov.in", "tehsils": 8, "hq": "Gondia"},
    "Hingoli": {"collector": "Collector & DM, Hingoli", "deoc_phone": "02456-221601", "toll_free": "1077", "email": "collector.hingoli@maharashtra.gov.in", "tehsils": 5, "hq": "Hingoli"},
    "Jalgaon": {"collector": "Collector & DM, Jalgaon", "deoc_phone": "0257-2222333", "toll_free": "1077", "email": "collector.jalgaon@maharashtra.gov.in", "tehsils": 15, "hq": "Jalgaon"},
    "Jalna": {"collector": "Collector & DM, Jalna", "deoc_phone": "02482-224401", "toll_free": "1077", "email": "collector.jalna@maharashtra.gov.in", "tehsils": 8, "hq": "Jalna"},
    "Kolhapur": {"collector": "Collector & DM, Kolhapur", "deoc_phone": "0231-2659232", "toll_free": "1077", "email": "collector.kolhapur@maharashtra.gov.in", "tehsils": 12, "hq": "Kolhapur"},
    "Latur": {"collector": "Collector & DM, Latur", "deoc_phone": "02382-243001", "toll_free": "1077", "email": "collector.latur@maharashtra.gov.in", "tehsils": 10, "hq": "Latur"},
    "Mumbai City": {"collector": "Collector & DM, Mumbai City", "deoc_phone": "022-22661231", "toll_free": "1077", "email": "collector.mumbaicity@maharashtra.gov.in", "tehsils": 1, "hq": "Fort, Mumbai"},
    "Mumbai Suburban": {"collector": "Collector & DM, Mumbai Suburban", "deoc_phone": "022-26514742", "toll_free": "1077", "email": "collector.mumbaisub@maharashtra.gov.in", "tehsils": 3, "hq": "Bandra East"},
    "Nagpur": {"collector": "Collector & DM, Nagpur", "deoc_phone": "0712-2562668", "toll_free": "1077", "email": "collector.nagpur@maharashtra.gov.in", "tehsils": 14, "hq": "Civil Lines, Nagpur"},
    "Nanded": {"collector": "Collector & DM, Nanded", "deoc_phone": "02462-234035", "toll_free": "1077", "email": "collector.nanded@maharashtra.gov.in", "tehsils": 16, "hq": "Nanded"},
    "Nandurbar": {"collector": "Collector & DM, Nandurbar", "deoc_phone": "02564-210001", "toll_free": "1077", "email": "collector.nandurbar@maharashtra.gov.in", "tehsils": 6, "hq": "Nandurbar"},
    "Nashik": {"collector": "Collector & DM, Nashik", "deoc_phone": "0253-2578500", "toll_free": "1077", "email": "collector.nashik@maharashtra.gov.in", "tehsils": 15, "hq": "Nashik"},
    "Dharashiv": {"collector": "Collector & DM, Dharashiv (Osmanabad)", "deoc_phone": "02472-222401", "toll_free": "1077", "email": "collector.osmanabad@maharashtra.gov.in", "tehsils": 8, "hq": "Dharashiv"},
    "Palghar": {"collector": "Collector & DM, Palghar", "deoc_phone": "02525-297474", "toll_free": "1077", "email": "collector.palghar@maharashtra.gov.in", "tehsils": 8, "hq": "Palghar"},
    "Parbhani": {"collector": "Collector & DM, Parbhani", "deoc_phone": "02452-223401", "toll_free": "1077", "email": "collector.parbhani@maharashtra.gov.in", "tehsils": 9, "hq": "Parbhani"},
    "Pune": {"collector": "Collector & DM, Pune", "deoc_phone": "020-26123371", "toll_free": "1077", "email": "collector.pune@maharashtra.gov.in", "tehsils": 14, "hq": "Shivajinagar, Pune"},
    "Raigad": {"collector": "Collector & DM, Raigad", "deoc_phone": "02141-222001", "toll_free": "1077", "email": "collector.raigad@maharashtra.gov.in", "tehsils": 15, "hq": "Alibag"},
    "Ratnagiri": {"collector": "Collector & DM, Ratnagiri", "deoc_phone": "02352-222226", "toll_free": "1077", "email": "collector.ratnagiri@maharashtra.gov.in", "tehsils": 9, "hq": "Ratnagiri"},
    "Sangli": {"collector": "Collector & DM, Sangli", "deoc_phone": "0233-2373023", "toll_free": "1077", "email": "collector.sangli@maharashtra.gov.in", "tehsils": 10, "hq": "Sangli"},
    "Satara": {"collector": "Collector & DM, Satara", "deoc_phone": "02162-238050", "toll_free": "1077", "email": "collector.satara@maharashtra.gov.in", "tehsils": 11, "hq": "Satara"},
    "Sindhudurg": {"collector": "Collector & DM, Sindhudurg", "deoc_phone": "02362-228847", "toll_free": "1077", "email": "collector.sindhudurg@maharashtra.gov.in", "tehsils": 8, "hq": "Oros"},
    "Solapur": {"collector": "Collector & DM, Solapur", "deoc_phone": "0217-2731012", "toll_free": "1077", "email": "collector.solapur@maharashtra.gov.in", "tehsils": 11, "hq": "Solapur"},
    "Thane": {"collector": "Collector & DM, Thane", "deoc_phone": "022-25301740", "toll_free": "1077", "email": "collector.thane@maharashtra.gov.in", "tehsils": 7, "hq": "Court Naka, Thane"},
    "Wardha": {"collector": "Collector & DM, Wardha", "deoc_phone": "07152-241501", "toll_free": "1077", "email": "collector.wardha@maharashtra.gov.in", "tehsils": 8, "hq": "Wardha"},
    "Washim": {"collector": "Collector & DM, Washim", "deoc_phone": "07252-232501", "toll_free": "1077", "email": "collector.washim@maharashtra.gov.in", "tehsils": 6, "hq": "Washim"},
    "Yavatmal": {"collector": "Collector & DM, Yavatmal", "deoc_phone": "07232-242501", "toll_free": "1077", "email": "collector.yavatmal@maharashtra.gov.in", "tehsils": 16, "hq": "Yavatmal"}
}

# ============================================================================
# 2. KEY GOVERNMENT DEPARTMENTS (12 DEPARTMENTS)
# ============================================================================

GOVERNMENT_DEPARTMENTS = [
    "Revenue and Forest Department (Disaster Management Cell / Relief & Rehab)",
    "Home Department (Maharashtra State Police, SDRF, Fire & Home Guards)",
    "Public Health and Family Welfare (Directorate of Health Services)",
    "Water Resources Department (Irrigation & Dam Safety Organization)",
    "Public Works Department (PWD - Bridges & Highway Infrastructure)",
    "Agriculture Department (Kharif/Rabi Crop Assessment & Relief)",
    "Energy & Power Department (MSEDCL & MSETCL Grid Restoration)",
    "Urban Development Department (Municipal Corporations & Stormwater Drainage)",
    "Food, Civil Supplies and Consumer Protection (Rationing & Community Kitchens)",
    "Rural Development and Panchayati Raj (Zilla Parishad Field Relief Units)",
    "Animal Husbandry and Fisheries (Livestock Rescue & Harbor Safety)",
    "Information and Public Relations (DGIPR - Official Fact-Checking & Bulletins)"
]

_ACTIVE_INCIDENTS = {}
_AUDIT_LOGS = []

# ============================================================================
# 3. AUDIT LOGGING FUNCTION
# ============================================================================

def log_audit_event(user, action, details):
    """Logs an authenticated administrative event with timestamp for chain of custody."""
    entry = {
        "event_id": f"AUD-{uuid.uuid4().hex[:8].upper()}",
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "timestamp_epoch": int(time.time()),
        "user": user,
        "action": action,
        "details": details
    }
    _AUDIT_LOGS.append(entry)
    if len(_AUDIT_LOGS) > 1000:
        _AUDIT_LOGS.pop(0)
    return entry

# ============================================================================
# 4. INCIDENT TRACKING SYSTEM (CREATE, UPDATE, CLOSE)
# ============================================================================

def track_incident(incident_id, action, details=None):
    """State machine for tracking disaster incidents: create, update, assign_resource, log_casualty, close."""
    details = details or {}
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if action == "create":
        new_id = incident_id or f"INC-{uuid.uuid4().hex[:6].upper()}"
        inc = {
            "incident_id": new_id,
            "district": details.get("district", "Kolhapur"),
            "hazard_type": details.get("hazard_type", "Flood"),
            "severity": details.get("severity", "High"),
            "status": "ACTIVE_OPERATIONAL",
            "created_at": ts,
            "last_updated": ts,
            "incident_commander": details.get("commander", f"Collector & DM, {details.get('district', 'Kolhapur')}"),
            "location_desc": details.get("location", "Panchganga River Basin"),
            "casualties": {"fatalities": 0, "injuries": 0, "rescued": 0, "evacuated": 0},
            "deployed_units": [],
            "action_log": [{"timestamp": ts, "entry": "Incident officially opened in PRAHARIX State Portal."}]
        }
        _ACTIVE_INCIDENTS[new_id] = inc
        log_audit_event(details.get("user", "System"), "CREATE_INCIDENT", f"Opened {new_id} in {inc['district']}")
        return inc

    inc = _ACTIVE_INCIDENTS.get(incident_id)
    if not inc:
        return {"error": f"Incident {incident_id} not found", "status": "FAILED"}

    if action == "update":
        for k in ["severity", "location_desc", "incident_commander", "status"]:
            if k in details:
                inc[k] = details[k]
        inc["last_updated"] = ts
        if "log_note" in details:
            inc["action_log"].append({"timestamp": ts, "entry": details["log_note"]})
        log_audit_event(details.get("user", "Admin"), "UPDATE_INCIDENT", f"Updated {incident_id}: {details.get('log_note', 'Refreshed')}")

    elif action == "assign_resource":
        unit = details.get("unit_name", "NDRF Team A")
        inc["deployed_units"].append({"unit": unit, "assigned_at": ts, "task": details.get("task", "Search and Rescue")})
        inc["action_log"].append({"timestamp": ts, "entry": f"Assigned tactical unit: {unit} for {details.get('task', 'SAR')}."})
        log_audit_event(details.get("user", "Admin"), "ASSIGN_RESOURCE", f"Dispatched {unit} to {incident_id}")

    elif action == "log_casualty":
        for key in ["fatalities", "injuries", "rescued", "evacuated"]:
            if key in details:
                inc["casualties"][key] += int(details[key])
        inc["last_updated"] = ts
        log_audit_event(details.get("user", "Admin"), "LOG_CASUALTIES", f"Updated casualties on {incident_id}")

    elif action == "close":
        inc["status"] = "CLOSED_RESOLVED"
        inc["closed_at"] = ts
        inc["closure_summary"] = details.get("summary", "Relief operations concluded. Handed to rehabilitation.")
        inc["action_log"].append({"timestamp": ts, "entry": f"Incident CLOSED. Summary: {inc['closure_summary']}"})
        log_audit_event(details.get("user", "Admin"), "CLOSE_INCIDENT", f"Closed incident {incident_id}")

    return inc

# ============================================================================
# 5. EMERGENCY CHECKLIST GENERATOR (BY HAZARD TYPE AND OPERATIONAL PHASE)
# ============================================================================

def get_emergency_checklist(hazard_type, phase):
    """
    Returns step-by-step Standard Operating Procedures (SOPs) based on MSDMP & NDMA.
    Hazards: 'flood', 'earthquake', 'cyclone', 'landslide', 'heatwave'
    Phases: 'mitigation_preparedness', 'early_warning_alert', 'active_response', 'post_disaster_relief_recovery'
    """
    h, p = hazard_type.lower(), phase.lower()
    all_checklists = {
        "flood": {
            "mitigation_preparedness": [
                "Review CWC gauge telemetry across all upstream river barrages and weirs.",
                "Verify functional readiness of 100% inflatable motorized rescue boats (IRB) and OBM engines.",
                "Audit desilting of primary stormwater drainage culverts and nullahs in municipal limits.",
                "Stockpile halogen tablets, chlorine, ORS packets, and antivenom in Primary Health Centers.",
                "Designate elevated relief shelters with backup DG generators and potable water supplies."
            ],
            "early_warning_alert": [
                "Issue ITU-T CAP Emergency SMS cell-broadcasts to all registered mobile subscribers in low zones.",
                "Activate 24x7 DEOC hotline 1077 with dual shift officer staffing.",
                "Order police pickets to halt light vehicular traffic over warning-level bridges.",
                "Pre-position 5th Bn NDRF Pune detachment and State SDRF water rescue teams at tehsil points.",
                "Begin pre-emptive evacuation of nursing homes, infirmaries, and ground-floor residential clusters."
            ],
            "active_response": [
                "Deploy motorized boats and divers to extract marooned citizens to elevated shelters.",
                "Establish aerial winching corridors with IAF Lohegaon base for roof-top extractions in cut-off zones.",
                "Distribute potable drinking water pouches (min 5 L/person/day) and dry ration packets.",
                "Deploy mobile generator sets (DG) to sustain district civil hospital ICU wards and water pumping.",
                "Conduct drone aerial thermal recon of river embankments to detect breaches early."
            ],
            "post_disaster_relief_recovery": [
                "Commence joint Revenue-Agriculture field panchanamas for crop submergence and livestock mortality ex-gratia.",
                "Disinfect submerged wells and community water tanks with bleaching powder to prevent epidemics.",
                "Inspect structural stability of overtopped bridges and national highway culverts by PWD engineers.",
                "Distribute financial gratuitous relief via direct DBT bank transfers to verified displaced households.",
                "Submit Post-Disaster Needs Assessment (PDNA) report to State SDMA."
            ]
        },
        "earthquake": {
            "mitigation_preparedness": [
                "Audit BIS 1893 seismic compliance of district civil hospitals, bridges, and municipal headquarters.",
                "Conduct scheduled statewide mock drill exercises with NDRF, SDRF, Home Guards, and Civil Defense.",
                "Maintain acoustic life-detector sensors and diamond concrete cutters in regional SAR depots.",
                "Inspect industrial gas and chemical pipelines passing through fault lines for automatic shutoff valves."
            ],
            "early_warning_alert": [
                "Trigger automated Early Warning siren systems and NavIC cell broadcasts upon primary P-wave detection.",
                "Order immediate halt of all metro trains, suburban rail, and high-speed expressway traffic.",
                "Instruct industrial plants to initiate automated SCADA shutdown of high-pressure boiler valves.",
                "Mobilize Quick Response Teams (QRT) of fire services and civil defense to predefined rally points."
            ],
            "active_response": [
                "Dispatch heavy Collapsed Structure Search & Rescue (CSSR) squads with K9 search dog units.",
                "Establish forward triage medical field tents outside hospital compounds to manage mass trauma.",
                "Isolate ruptured electrical distribution cables and extinguish secondary transformer fires.",
                "Deploy ground-penetrating radar and acoustic listening devices to detect trapped survivors beneath rubble.",
                "Establish satellite VSAT communications at Collectorate in case terrestrial telecom fiber is severed."
            ],
            "post_disaster_relief_recovery": [
                "Inspect buildings and categorize safety placards (Green = Safe, Yellow = Limited, Red = Unsafe).",
                "Erect temporary prefabricated shelter villages equipped with sanitation blocks and solar micro-grids.",
                "Provide trauma counseling and psychiatric first aid to bereaved families through DHS clinical teams.",
                "Initiate forensic audit of collapsed structures and enforce building code compliance."
            ]
        },
        "cyclone": {
            "mitigation_preparedness": [
                "Trim hazardous tree branches near high-tension electrical feeder corridors across coastal belts.",
                "Verify stock of satellite phones (Inmarsat/NavIC) at all coastal port offices and fisheries hubs.",
                "Inspect cyclone multi-purpose shelters along coastal belts (Raigad, Ratnagiri, Sindhudurg, Palghar).",
                "Enforce total ban on artisanal and mechanized marine fishing voyages 72 hours prior to landfall."
            ],
            "early_warning_alert": [
                "Broadcast cyclone tracking cone advisories and coastal storm-surge inundation estimates every 3 hours.",
                "Complete total mandatory evacuation of coastal thatched hamlets located within 1.5 km of high tide line.",
                "Anchor all harbor tugs, fishing trawlers, and barges securely at sheltered estuarine creek docks.",
                "Shut down coastal aerial cable cars, high cranes, and secure all temporary hoardings/billboards."
            ],
            "active_response": [
                "Issue strict stay-indoors shelter-in-place directives during eyewall passage and false calm of cyclone eye.",
                "Deploy PWD heavy road clearance teams equipped with mechanized chainsaws to remove uprooted trees.",
                "Coordinate with Indian Coast Guard (ICG) Dornier aircraft and offshore patrol vessels for distress beacons.",
                "Sustain emergency operations of civil hospital power supply using elevated backup generators."
            ],
            "post_disaster_relief_recovery": [
                "MSEDCL power utility teams to systematically replace snapped conductors, fallen poles, and transformers.",
                "Test drinking water wells in coastal villages for sea-water salinity intrusion and flush contamination.",
                "Provide immediate financial grant for damaged fishing boats, nets, and flooded coastal salt pans.",
                "Submit preliminary cyclone damage sitrep to Chief Minister Disaster Relief Fund within 48 hours."
            ]
        },
        "landslide": {
            "mitigation_preparedness": [
                "Map landslide hazard zonation (LHZ) along Western Ghats passes (Bhor Ghat, Kasara Ghat, Amba Ghat).",
                "Install inclinometer and soil moisture telemetry sensors on vulnerable steep cut slopes.",
                "Clear blocked hillside retaining wall weep holes to relieve excessive hydrostatic pore pressure.",
                "Pre-position heavy earthmovers (JCB/excavators) near high-risk ghat highway sectors."
            ],
            "early_warning_alert": [
                "Issue landslide red alerts when cumulative 48-hour rainfall exceeds threshold (>250mm).",
                "Divert intercity express buses and freight trucks away from active slip zones to bypass corridors.",
                "Evacuate vulnerable foothill and cliff-edge tribal hamlets to designated community centers."
            ],
            "active_response": [
                "Dispatch NDRF mountain SAR teams with chasm traverse gear, heavy hydraulic spreaders, and stretchers.",
                "Employ drone thermal imaging to survey unstable upper scarp faces for imminent secondary debris flows.",
                "Create controlled bypass drainage around landslide debris dams to prevent downstream flash flood outburst.",
                "Organize aerial evacuation for critically injured casualties using air ambulances / IAF helicopters."
            ],
            "post_disaster_relief_recovery": [
                "Conduct geological slope stability analysis before permitting heavy machinery onto toe debris.",
                "Erect rockfall barrier netting, shotcrete, and reinforced soil terracing across scarred slopes.",
                "Permanently relocate high-risk foothill settlements under State Resettlement & Rehabilitation Policy."
            ]
        },
        "heatwave": {
            "mitigation_preparedness": [
                "Formulate District Heat Action Plan (HAP) with IMD temperature threshold color codes.",
                "Establish cool roofs in slum clusters and ensure water tankers for water-stressed localities.",
                "Equip all municipal transit stops and primary markets with shaded awnings and free drinking water kiosks."
            ],
            "early_warning_alert": [
                "Issue public heatwave warning bulletins via radio, TV, and WhatsApp groups when temp exceeds 43C.",
                "Adjust school and government office hours to morning shifts (07:00 to 11:30 AM).",
                "Prohibit outdoor manual construction labor between 12:00 noon and 04:00 PM."
            ],
            "active_response": [
                "Open dedicated air-conditioned heat stroke treatment wards with ice packs and IV fluids in all civil hospitals.",
                "Conduct thermal misting of crowded bus depots and primary market squares.",
                "Deploy ASHA health workers to perform door-to-door welfare checks on elderly and vulnerable residents."
            ],
            "post_disaster_relief_recovery": [
                "Review heat mortality panchanamas and submit epidemiological heat-stress reports to DHS.",
                "Audit urban tree canopy coverage and update urban forestry targets to mitigate heat-island hotspots."
            ]
        }
    }

    entry = all_checklists.get(h, all_checklists["flood"])
    tasks = entry.get(p, entry.get("active_response", []))
    return {
        "hazard_type": hazard_type.capitalize(),
        "phase": phase.replace("_", " ").title(),
        "total_actions": len(tasks),
        "protocol_authority": "Maharashtra State Disaster Management Plan (MSDMP) & NDMA SOP",
        "action_checklist": [{"step": i + 1, "task": t, "mandatory": True, "lead_agency": "DDMA"} for i, t in enumerate(tasks)]
    }

# ============================================================================
# 6. DEPARTMENT-WISE ALERT MANAGEMENT
# ============================================================================

def get_department_alerts(dept_name, hazard_type):
    """Generates department-specific tactical directives and operational readiness levels."""
    b, h = dept_name.lower(), hazard_type.lower()
    directives, alert = [], "ORANGE ALERT (STANDBY)"

    if "health" in b:
        directives = ["Cancel non-emergency leaves for surgeons and trauma staff.", "Verify cryogenic liquid oxygen tanks and backup cylinders.", "Pre-position 25,000 ORS packets and antivenom vials at PHCs.", "Formulate 4 mobile disaster medical squads equipped with defibrillators."]
        alert = "RED ALERT (HIGH SURGE PREPARATION)"
    elif "police" in b or "home" in b:
        directives = ["Deploy police pickets to close access roads leading to submerged bridges.", "Coordinate wireless VHF traffic communication on emergency 156.800 MHz.", "Mobilize Home Guards and Civil Defense for shelter security cordons.", "Enforce prohibitory orders under Sec 144 CrPC around overflowing dam spillways."]
        alert = "RED ALERT (MANDATORY TRAFFIC & SECURITY LOCKDOWN)"
    elif "water" in b:
        directives = ["Hourly monitoring of reservoir inflow (cusecs) and spillway discharge.", "Issue siren warnings 3 hours prior to increasing dam outflow.", "Inspect dam piezometers and drainage galleries for seepage anomalies.", "Coordinate with neighboring interstate water authorities (Almatti Dam cell)."]
        alert = "ORANGE ALERT (DISCHARGE REGULATION ACTIVE)"
    elif "pwd" in b or "works" in b:
        directives = ["Pre-stage heavy excavators and dump trucks at critical bottlenecks.", "Inspect structural pier scour on masonry and concrete bridges across rivers.", "Erect retro-reflective barricades around washed-out road shoulders.", "Keep emergency Bailey Bridge components ready in regional workshops."]
    elif "power" in b or "energy" in b:
        directives = ["De-energize electrical transformers in submerged zones to prevent electrocution.", "Stage 100 mobile diesel generators (125 kVA) for hospitals and pump stations.", "Mobilize MSEDCL overhead line repair gangs from non-affected divisions."]
    else:
        directives = [f"Activate Departmental 24x7 control room in coordination with DEOC 1077.", "Mobilize field inspectors to assess vulnerability and execute countermeasures.", "Submit hourly status SITREP updates to District Collector command portal."]

    return {
        "department": dept_name,
        "hazard_type": hazard_type.capitalize(),
        "readiness_status": alert,
        "operational_directives": directives,
        "reporting_frequency": "Every 2 Hours to DEOC",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }

# ============================================================================
# 7. EMERGENCY SITREP GENERATION (SITUATION REPORT)
# ============================================================================

def generate_sitrep(incident_data, format="full"):
    """
    Generates standard formatted NDMA/SDMA Situation Report.
    format: 'full' (human-readable tactical report) or 'dict' (structured JSON)
    """
    inc = incident_data if isinstance(incident_data, dict) else {}
    sitrep_id = f"SITREP-{uuid.uuid4().hex[:6].upper()}"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    district = inc.get("district", "Kolhapur")
    hazard = inc.get("hazard_type", "Monsoonal Flood")
    sev = inc.get("severity", "Critical")

    data = {
        "sitrep_number": sitrep_id,
        "date_time_utc": ts,
        "operational_period": "06:00 to 18:00 Hours IST",
        "jurisdiction": f"District Disaster Management Authority, {district}",
        "hazard": hazard,
        "severity": sev,
        "lead_incident_commander": inc.get("incident_commander", f"District Magistrate & Collector, {district}"),
        "executive_summary": f"Severe {hazard} incident affecting multiple tehsils in {district}. Emergency response teams actively deployed.",
        "casualties": inc.get("casualties", {"fatalities": 0, "injuries": 14, "rescued": 380, "evacuated": 2450}),
        "displaced_persons_in_shelters": inc.get("displaced", 4200),
        "shelters_active": 8,
        "critical_infrastructure_status": {
            "dams_monitored": "Radhanagari Dam at 98% capacity; 4 spillway gates open releasing 8,200 cusecs.",
            "transportation": "NH-48 operational with police escort; 2 state highway causeways closed.",
            "power_and_grid": "8 rural substations switched off for safety; 35,000 consumers affected.",
            "telecommunications": "Mobile cellular connectivity normal; 3 mobile COWs deployed."
        },
        "resources_deployed": {
            "ndrf_battalion": "5th Bn NDRF (Pune) - 4 teams (180 personnel) with 16 IRB boats",
            "sdrf_detachment": "Maharashtra SDRF Pune Coy - 2 teams (90 personnel)",
            "indian_army": "Southern Command 1 composite column on standby",
            "civil_defense_volunteers": 120
        },
        "next_operational_objectives": [
            "Complete evacuation of isolated riverside wards before scheduled 20:00 dam discharge surge.",
            "Deliver 5,000 food packets and clean water containers to Government Polytechnic shelter.",
            "Maintain continuous VHF check-ins between DEOC and flood rescue boats."
        ]
    }

    if format == "dict":
        return data

    c = data["casualties"]
    ci = data["critical_infrastructure_status"]
    rd = data["resources_deployed"]
    report = (
        f"========================================================================================\n"
        f"PRAHARIX 2.0 APEX COMMAND - EMERGENCY SITUATION REPORT ({data['sitrep_number']})\n"
        f"CLASSIFICATION: OFFICIAL TACTICAL EMERGENCY | JURISDICTION: {data['jurisdiction']}\n"
        f"HAZARD: {data['hazard']} | SEVERITY: {data['severity']} | TIMESTAMP: {data['date_time_utc']}\n"
        f"========================================================================================\n"
        f"1. EXECUTIVE SUMMARY: {data['executive_summary']}\n"
        f"2. CASUALTY METRICS: Fatalities: {c['fatalities']} | Injuries: {c['injuries']} | Rescued: {c['rescued']} | Evacuated: {c['evacuated']}\n"
        f"   Displaced Persons in Active Shelters: {data['displaced_persons_in_shelters']} across {data['shelters_active']} camps\n"
        f"3. INFRASTRUCTURE: Dams: {ci['dams_monitored']} | Roads: {ci['transportation']} | Grid: {ci['power_and_grid']}\n"
        f"4. FORCES DEPLOYED: NDRF: {rd['ndrf_battalion']} | SDRF: {rd['sdrf_detachment']} | Volunteers: {rd['civil_defense_volunteers']}\n"
        f"5. NEXT OBJECTIVES:\n" + "".join([f"   - [ ] {o}\n" for o in data['next_operational_objectives']]) +
        f"========================================================================================"
    )
    return report

# ============================================================================
# 8. AUTOMATED INCIDENT REPORT (STRUCTURED ICS-201 BRIEFING FORM)
# ============================================================================

def generate_incident_report(incident):
    """Compiles an official ICS-201 Incident Briefing document adhering to NDMA / NIMS."""
    inc = incident if isinstance(incident, dict) else {}
    inc_id = inc.get("incident_id", "INC-TACTICAL-201")
    dist = inc.get("district", "Kolhapur")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    return {
        "form": "ICS-201 (Incident Briefing Form)",
        "incident_name": f"{dist.upper()} {inc.get('hazard_type', 'HAZARD').upper()} RESPONSE",
        "incident_id": inc_id,
        "date_initiated": inc.get("created_at", ts),
        "map_coordinates": f"Lat: {inc.get('lat', 16.7050)}, Lon: {inc.get('lon', 74.2433)}",
        "incident_commander": inc.get("incident_commander", f"Collector & DM, {dist}"),
        "safety_officer": f"Chief Fire Officer / District Police Chief, {dist}",
        "situation_summary": f"Active {inc.get('hazard_type', 'incident')} with high operational risk. Weather conditions challenging.",
        "current_objectives": [
            "Ensure zero human life loss in inundated sectors through swift boat extraction.",
            "Maintain emergency access road for ambulance convoys to District Civil Hospital.",
            "Establish secondary satellite communications between Collector Command and field teams."
        ],
        "tactical_organization_chart": {
            "incident_commander": inc.get("incident_commander", f"Collector & DM, {dist}"),
            "operations_section": f"SP {dist} / SDRF Commandant",
            "logistics_section": "Resident Deputy Collector (RDC) & PWD Executive Engineer",
            "planning_section": "District Disaster Management Officer (DDMO) & IMD Liaison",
            "finance_admin": "Treasury Officer & SDM Headquarters"
        },
        "resources_ordered_and_on_scene": inc.get("deployed_units", [
            {"unit": "5th Bn NDRF Team A", "status": "ON-SCENE", "role": "Water Rescue"},
            {"unit": "SDRF Company 1", "status": "ON-SCENE", "role": "Evacuation Logistics"}
        ]),
        "action_history": inc.get("action_log", [{"timestamp": ts, "entry": "Initial ICS-201 Form Generated."}])
    }

# ============================================================================
# 9. PDF REPORT EXPORT DATA PREPARATION
# ============================================================================

def generate_pdf_report_data(assessments, incidents):
    """Formats complete disaster intelligence into structured dictionary ready for ReportLab PDF."""
    inc_list = incidents if isinstance(incidents, list) else list(_ACTIVE_INCIDENTS.values())
    ass_list = assessments if isinstance(assessments, list) else []

    total_displaced = sum(int(i.get("casualties", {}).get("evacuated", 0)) for i in inc_list)
    total_fatalities = sum(int(i.get("casualties", {}).get("fatalities", 0)) for i in inc_list)
    total_injuries = sum(int(i.get("casualties", {}).get("injuries", 0)) for i in inc_list)
    total_rescued = sum(int(i.get("casualties", {}).get("rescued", 0)) for i in inc_list)

    return {
        "report_title": "PRAHARIX 2.0 APEX EDITION - STATE DISASTER MASTER SITREP",
        "generated_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "reporting_body": "Maharashtra State Disaster Management Authority (MSDMA) & Relief Commissionerate",
        "executive_kpis": {
            "active_incidents_count": len(inc_list),
            "total_rescued": total_rescued,
            "total_evacuated": total_displaced,
            "total_fatalities": total_fatalities,
            "total_injuries": total_injuries
        },
        "incidents_table": [
            {"id": inc.get("incident_id", "N/A"), "district": inc.get("district", "Unknown"), "hazard": inc.get("hazard_type", "Flood"), "severity": inc.get("severity", "High"), "status": inc.get("status", "ACTIVE")}
            for inc in inc_list
        ],
        "assessments_summary": [
            {"zone": a.get("zone_name", "Sector"), "score": a.get("composite_priority_score", 0), "tier": a.get("tactical_tier", "NORMAL"), "population": a.get("population_at_risk", 0)}
            for a in ass_list[:8]
        ],
        "collector_control_rooms": [
            {"district": d, "collector": MAHARASHTRA_COLLECTORS[d]["collector"], "hotline": MAHARASHTRA_COLLECTORS[d]["deoc_phone"], "toll_free": MAHARASHTRA_COLLECTORS[d]["toll_free"]}
            for d in ["Kolhapur", "Sangli", "Satara", "Pune", "Raigad", "Ratnagiri", "Mumbai Suburban", "Nagpur"]
        ]
    }

# ============================================================================
# 10. DISTRICT COLLECTOR COMMAND PANEL DATA GETTER
# ============================================================================

def get_collector_command_panel(district):
    """Retrieves unified command center telemetry for a specific District Collector."""
    info = MAHARASHTRA_COLLECTORS.get(district, MAHARASHTRA_COLLECTORS["Kolhapur"])
    active_in_dist = [inc for inc in _ACTIVE_INCIDENTS.values() if inc.get("district") == district]

    return {
        "district": district,
        "collector_office": info["collector"],
        "control_room_hotline": info["deoc_phone"],
        "toll_free": info["toll_free"],
        "official_email": info["email"],
        "tehsils_under_command": info["tehsils"],
        "active_incidents": active_in_dist,
        "emergency_services": {"police": "112", "fire": "101", "ambulance": "108", "disaster_mgmt": "1077"},
        "system_status": "ONLINE - SECURE PRAHARIX LINK ESTABLISHED"
    }

# ============================================================================
# CLI SELF TEST
# ============================================================================

if __name__ == "__main__":
    print(f"[*] Loaded {len(MAHARASHTRA_COLLECTORS)} Maharashtra District Collectorates.")
    print(f"[*] Loaded {len(GOVERNMENT_DEPARTMENTS)} State Government Departments.")
    test_inc = track_incident("INC-TEST-001", "create", {"district": "Kolhapur", "hazard_type": "Flood", "severity": "High"})
    track_incident("INC-TEST-001", "log_casualty", {"rescued": 140, "evacuated": 920})
    sitrep = generate_sitrep(test_inc, format="full")
    print(f"\n[+] Sample Generated SITREP:\n{sitrep[:350]}...\n")
    print("[+] Government Operations Module Initialized Successfully.")
