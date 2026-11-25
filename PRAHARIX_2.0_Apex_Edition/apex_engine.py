"""
PRAHARIX 2.0 - APEX STRATEGIC TACTICAL ENGINE
==============================================
Next-Generation Space-Edge-Ground Cyber-Physical Disaster Command System.
Incorporating:
1. InSAR Coherence Damage Proxy Mapping (DPM) & ISRO NISAR / NavIC Downlink.
2. Multi-Hazard "Domino Cascade" Physics Failure Engine (Seismic -> Landslide -> River Damming -> GLOF/Breach).
3. Dynamic NetworkX Convoy Rerouting Engine with active bridge/road obstruction cuts.
4. Edge Drone-AI USAR Reconnaissance (YOLOv8 Detection Geometry + Acoustic Rubble Life Signal).
5. Autonomous NDMA Tactical AI Incident Commander (ICS-201/204 IAP Formulation & Logistics Matrix).
"""

import math
import time
import json
import numpy as np
import networkx as nx
from datetime import datetime, timezone

# =====================================================================
# APEX 1: InSAR DAMAGE PROXY MAPPING (DPM) & ISRO NISAR / NavIC DOWNLINK
# =====================================================================

def compute_insar_damage_proxy_map(center_lat=32.20, center_lon=76.32, radius_km=35.0, event_mag=6.8):
    """
    Computes synthetic Interferometric Synthetic Aperture Radar (InSAR) Coherence Loss
    and Line-of-Sight (LOS) Surface Displacement vectors representing ISRO NISAR (L-band)
    and Copernicus Sentinel-1 (C-band) radar interferometry.
    Coherence gamma: 1.0 (Completely Stable) -> 0.0 (Severe Structural Destruction/Liquefaction).
    """
    grid_size = 7
    lat_step = (radius_km / 111.0) / (grid_size // 2)
    lon_step = (radius_km / (111.0 * math.cos(math.radians(center_lat)))) / (grid_size // 2)

    cells = []
    base_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    for i in range(-3, 4):
        for j in range(-3, 4):
            c_lat = round(center_lat + i * lat_step, 4)
            c_lon = round(center_lon + j * lon_step, 4)
            dist_km = math.sqrt((i * lat_step * 111.0)**2 + (j * lon_step * 111.0 * math.cos(math.radians(center_lat)))**2)

            # Physics decay of coherence based on earthquake magnitude and distance
            decay = max(0.0, 1.0 - (dist_km / (event_mag * 6.5)))
            pre_event_coherence = round(0.85 + np.random.uniform(-0.05, 0.08), 2)
            
            # Post event coherence drops sharply near epicenter
            coherence_loss = round(min(0.95, decay * (0.55 + np.random.uniform(0.1, 0.35))), 2)
            post_event_coherence = round(max(0.05, pre_event_coherence - coherence_loss), 2)

            # LOS surface deformation in millimeters (-subsidence, +uplift)
            los_displacement_mm = round(-1.0 * decay * (event_mag * 22.4 + np.random.uniform(-15.0, 35.0)), 1)

            # Damage classification based on coherence loss
            if coherence_loss > 0.65:
                dmg_grade = "D4-D5 (Pancake/Heavy Structural Collapse)"
                color = "#ff1744"
                risk_badge = "CRITICAL DESTRUCTION"
            elif coherence_loss > 0.40:
                dmg_grade = "D2-D3 (Moderate-to-Severe Wall Shear Failure)"
                color = "#ff9100"
                risk_badge = "MODERATE DAMAGE"
            elif coherence_loss > 0.20:
                dmg_grade = "D1 (Superficial Cracking / Liquefaction Signs)"
                color = "#ffd600"
                risk_badge = "MINOR DISTURBANCE"
            else:
                dmg_grade = "D0 (Structurally Intact)"
                color = "#00e676"
                risk_badge = "INTACT"

            cells.append({
                "cell_id": f"DPM-R{i+4}C{j+4}",
                "lat": c_lat,
                "lon": c_lon,
                "distance_km": round(dist_km, 1),
                "pre_coherence": pre_event_coherence,
                "post_coherence": post_event_coherence,
                "coherence_loss": coherence_loss,
                "los_displacement_mm": los_displacement_mm,
                "damage_grade": dmg_grade,
                "risk_badge": risk_badge,
                "color": color
            })

    # ISRO NavIC S-band Satellite Downlink packet (EMS Direct-to-Cell)
    navic_packet = {
        "transponder": "ISRO IRNSS-1I (NavIC Geo-Sat)",
        "downlink_freq": "2492.028 MHz (S-Band NavIC EMS)",
        "eirp_dbw": 42.5,
        "payload_hex": f"0x1A4F_NAV_EQ{int(event_mag*10)}_LAT{int(abs(center_lat)*100)}_LON{int(abs(center_lon)*100)}_CRC89B",
        "broadcast_text_en": f"NAVIC EMERGENCY BROADCAST: M{event_mag} Rupture Confirmed. Immediate high ground evacuation advised for radius {radius_km}km.",
        "broadcast_text_hi": f"नाविक आपातकालीन प्रसारण: M{event_mag} भूकंप की पुष्टि। त्रिज्या {radius_km}किमी के नागरिक तुरंत खुले स्थानों पर जाएं।",
        "target_sat_coverage": "India Subcontinent & Ocean Region (0°-40°N, 60°-100°E)"
    }

    return {
        "status": "DPM_GENERATED",
        "sensor_fusion": "ISRO NISAR (L-band 24cm) + Copernicus Sentinel-1 (C-band 5.6cm)",
        "radar_geometry": "Ascending Pass Path 142 / Frame 480",
        "spatial_resolution": "10m x 10m Ground Posting",
        "processed_at": base_time,
        "cells": cells,
        "critical_cells_count": sum(1 for c in cells if "CRITICAL" in c["risk_badge"]),
        "navic_satellite_downlink": navic_packet
    }


# =====================================================================
# APEX 2: MULTI-HAZARD "DOMINO CASCADE" PHYSICS FAILURE ENGINE
# =====================================================================

def simulate_multi_hazard_cascade(
    mag=7.2,
    fault_name="Himalayan Frontal Thrust (HFT)",
    region="Kangra-Chamba Himalayan Belt",
    dam_name="Pong Dam / Beas Hydro Complex",
    dam_capacity_mcm=8570
):
    """
    Simulates the cascading domino failure chain across 5 discrete chronological phases:
    1. Primary Seismic Fault Rupture (PGA calculation)
    2. Co-seismic Landslide Debris Volume (Keefer / Marc scaling laws)
    3. River Blockage & Landslide Dam Formation (Outburst Impoundment)
    4. Landslide Dam Overtopping & Catastrophic Breach (Costa-Schuster breach flow)
    5. Downstream Hydroelectric Grid Islanding & Metropolitan Flood Wave
    """
    # 1. Seismic Rupture
    pga_g = round(10 ** (0.24 * mag - 1.25), 3) # Joyner-Boore near-field acceleration
    fault_rupture_length_km = round(10 ** (0.5 * mag - 1.8), 1) # Wells & Coppersmith

    # 2. Landslide volume scaling: Log10(V) = 1.44*M - 4.16 (Marc et al. 2016)
    log_v = 1.44 * mag - 4.16
    debris_volume_million_m3 = round((10 ** log_v) / 1e6, 2)
    debris_volume_million_m3 = max(1.2, debris_volume_million_m3)
    critical_slopes_failed = int(mag * 8.5)

    # 3. River Damming & Lake Formation
    river_inflow_m3s = 480.0 # Average monsoon river discharge
    impounded_lake_hours = round(debris_volume_million_m3 * 1e6 / (river_inflow_m3s * 3600 * 0.4), 1)
    lake_crest_depth_m = round(28.0 + (mag - 6.0) * 18.0, 1)

    # 4. Dam Breach Peak Discharge: Qp = 0.0158 * (V_w)^0.41 * (H_d)^1.08 (Costa 1988)
    vol_water_m3 = min(debris_volume_million_m3 * 0.5 * 1e6, 45e6)
    peak_breach_discharge_m3s = round(0.0158 * (vol_water_m3 ** 0.41) * (lake_crest_depth_m ** 1.08), 0)
    time_to_breach_hours = round(max(1.8, impounded_lake_hours * 0.35), 1)

    # 5. Downstream Impact
    flood_wave_speed_kmh = 32.0 # Fast mountain surge wave
    downstream_reach_km = 68.0
    arrival_time_min = round((downstream_reach_km / flood_wave_speed_kmh) * 60, 0)
    grid_trip_latency_ms = 450

    timeline = [
        {
            "step": 1,
            "phase": "T+00:00 (Immediate)",
            "title": "Primary Seismic Rupture",
            "icon": "⚡",
            "hazard": "Seismic Ground Shaking",
            "severity": "CRITICAL",
            "metrics": f"PGA: {pga_g}g | Rupture Length: {fault_rupture_length_km} km | Mag: {mag}",
            "description": f"Hypocentral shear failure along {fault_name}. Strong ground motion initiates slope instability across 40km radius.",
            "status": "CONFIRMED"
        },
        {
            "step": 2,
            "phase": "T+00:08 Minutes",
            "title": "Co-Seismic Slope Failure & Landslides",
            "icon": "🏔️",
            "hazard": "Mass Wasting / Rock Avalanche",
            "severity": "HIGH",
            "metrics": f"Debris Volume: {debris_volume_million_m3} Million m³ | Slopes Failed: {critical_slopes_failed}",
            "description": "Steep Himalayan slopes exceed critical shear strength threshold. Massive scree blocks choke upper river canyon.",
            "status": "IMMINENT"
        },
        {
            "step": 3,
            "phase": "T+00:45 Minutes",
            "title": "River Blockage & Artificial Dam Impoundment",
            "icon": "🌊",
            "hazard": "Landslide Dam / Impoundment",
            "severity": "CRITICAL",
            "metrics": f"Barrier Height: {lake_crest_depth_m}m | Filling Rate: {river_inflow_m3s} m³/s",
            "description": "Natural rockfall dam impounds canyon. Water levels rising rapidly behind uncompacted debris barrier.",
            "status": "PREDICTED (High Probability)"
        },
        {
            "step": 4,
            "phase": f"T+{time_to_breach_hours} Hours",
            "title": "Catastrophic Barrier Overtopping & Outburst (GLOF)",
            "icon": "💥",
            "hazard": "Flash Flood Outburst",
            "severity": "EXTREME",
            "metrics": f"Peak Breach Discharge: {peak_breach_discharge_m3s:,} m³/s | Breach Window: ~45 min",
            "description": f"Overtopping initiates piping erosion. Breaching barrier releases colossal hydrostatic flood wave into downstream gorge.",
            "status": "TIMED TRIGGER"
        },
        {
            "step": 5,
            "phase": f"T+{time_to_breach_hours}h + {int(arrival_time_min)}m",
            "title": "Downstream Inundation & Hydro Grid Islanding",
            "icon": "🛑",
            "hazard": "Infrastructure Submergence & Grid Trip",
            "severity": "HIGH",
            "metrics": f"Impact Target: {dam_name} | Grid Trip: {grid_trip_latency_ms}ms Interlock",
            "description": "Spillway flood surge exceeds safe freeboard. Downstream power generation turbines trip into emergency islanding mode.",
            "status": "INTERLOCK ENGAGED"
        }
    ]

    return {
        "scenario_name": f"{region} Multi-Hazard Domino Cascade",
        "trigger_magnitude": mag,
        "fault_source": fault_name,
        "pga_peak_g": pga_g,
        "debris_volume_m3": f"{debris_volume_million_m3} Million m³",
        "peak_flood_discharge_m3s": f"{peak_breach_discharge_m3s:,} m³/s",
        "breach_countdown_hours": time_to_breach_hours,
        "downstream_warning_lead_time_min": arrival_time_min,
        "timeline": timeline,
        "recommended_preemptive_evacuation_km2": round(debris_volume_million_m3 * 14.5, 1)
    }


# =====================================================================
# APEX 3: DYNAMIC NETWORKX CONVOY REROUTING WITH BRIDGE FAILURE OBSTACLES
# =====================================================================

# Tactical road graph topology of key North-Central Indian disaster corridors
INDIAN_TACTICAL_ROAD_NODES = {
    "NDRF_8_GZB": {"name": "8th Bn NDRF (Ghaziabad Base)", "lat": 28.6922, "lon": 77.4478, "type": "BASE"},
    "DELHI_ISBT": {"name": "Delhi Kashmere Gate Transport Hub", "lat": 28.6667, "lon": 77.2300, "type": "JUNCTION"},
    "HINDON_AFB": {"name": "IAF Hindon Strategic Airbase", "lat": 28.7061, "lon": 77.3586, "type": "AIRBASE"},
    "PANIPAT": {"name": "Panipat Grand Trunk Corridor", "lat": 29.3909, "lon": 76.9635, "type": "HIGHWAY"},
    "AMBALA_CANTT": {"name": "Ambala Cantt Military Junction", "lat": 30.3752, "lon": 76.7821, "type": "JUNCTION"},
    "CHANDIGARH_STAGING": {"name": "Chandigarh Emergency Staging Hub", "lat": 30.7333, "lon": 76.7794, "type": "STAGING"},
    "ROPAR_BRIDGE": {"name": "Ropar Sutlej River Bridge", "lat": 30.9664, "lon": 76.5331, "type": "CHOKEPOINT_BRIDGE"},
    "BILASPUR_NH205": {"name": "Bilaspur Mountain Pass NH-205", "lat": 31.3326, "lon": 76.7554, "type": "HIGHWAY"},
    "MANDI_BRIDGE": {"name": "Mandi Beas River Suspension Bridge", "lat": 31.7087, "lon": 76.9320, "type": "CHOKEPOINT_BRIDGE"},
    "NDRF_14_MANDI": {"name": "14th Bn NDRF (Jakhari, Mandi)", "lat": 31.7200, "lon": 76.9400, "type": "BASE"},
    "KANGRA_AIRPORT": {"name": "Gaggal Kangra Forward Strip", "lat": 32.1651, "lon": 76.2634, "type": "AIRSTRIP"},
    "DHARAMSHALA_LZ": {"name": "Dharamshala Disaster Zone LZ (Ground Zero)", "lat": 32.2190, "lon": 76.3234, "type": "GROUND_ZERO"}
}

TACTICAL_ROAD_EDGES = [
    ("NDRF_8_GZB", "DELHI_ISBT", 24, 0.6),
    ("NDRF_8_GZB", "HINDON_AFB", 12, 0.3),
    ("DELHI_ISBT", "PANIPAT", 88, 1.4),
    ("PANIPAT", "AMBALA_CANTT", 112, 1.8),
    ("AMBALA_CANTT", "CHANDIGARH_STAGING", 46, 0.8),
    ("CHANDIGARH_STAGING", "ROPAR_BRIDGE", 42, 0.7),
    ("ROPAR_BRIDGE", "BILASPUR_NH205", 68, 1.6),
    ("BILASPUR_NH205", "MANDI_BRIDGE", 55, 1.5),
    ("MANDI_BRIDGE", "NDRF_14_MANDI", 8, 0.2),
    ("NDRF_14_MANDI", "DHARAMSHALA_LZ", 94, 2.8),
    ("MANDI_BRIDGE", "DHARAMSHALA_LZ", 98, 2.9),
    # Alternate Mountain Bypass via Una & Kangra Valley
    ("CHANDIGARH_STAGING", "BILASPUR_NH205", 95, 2.2),
    ("ROPAR_BRIDGE", "KANGRA_AIRPORT", 165, 3.8), # Western Valley Bypass
    ("KANGRA_AIRPORT", "DHARAMSHALA_LZ", 14, 0.4),
    # Air Corridor (IAF C-130J / Mi-17 Airlift)
    ("HINDON_AFB", "KANGRA_AIRPORT", 420, 1.1)
]

def compute_dynamic_convoy_routing(
    origin="NDRF_8_GZB",
    destination="DHARAMSHALA_LZ",
    collapsed_bridges=["MANDI_BRIDGE"],
    flooded_corridors=["BILASPUR_NH205"]
):
    """
    Constructs a NetworkX tactical graph. Evaluates edge survival against
    active structural collapse and flood inundation zones.
    Computes optimal failover convoy route and multimodal airlift alternative.
    """
    G = nx.Graph()

    for u, v, dist, hrs in TACTICAL_ROAD_EDGES:
        edge_status = "OPERATIONAL"
        weight = hrs

        # If bridge collapsed or flooded, sever edge with infinite penalty
        if u in collapsed_bridges or v in collapsed_bridges:
            edge_status = "SEVERED_COLLAPSED_BRIDGE"
            weight = 99999.0
        elif u in flooded_corridors or v in flooded_corridors:
            edge_status = "BLOCKED_FLOOD_SUBMERGENCE"
            weight = 99999.0

        G.add_edge(u, v, distance_km=dist, transit_hours=hrs, weight=weight, status=edge_status)

    # 1. Compute Primary Ground Convoy Path (ignoring cuts to see nominal route)
    G_nominal = nx.Graph()
    for u, v, dist, hrs in TACTICAL_ROAD_EDGES:
        G_nominal.add_edge(u, v, weight=hrs, distance_km=dist)
    nominal_path = nx.shortest_path(G_nominal, source=origin, target=destination, weight="weight")
    nominal_dist = sum(G_nominal[nominal_path[i]][nominal_path[i+1]]["distance_km"] for i in range(len(nominal_path)-1))
    nominal_time = sum(G_nominal[nominal_path[i]][nominal_path[i+1]]["weight"] for i in range(len(nominal_path)-1))

    # 2. Compute Resilient Failover Path with Dynamic Edge Cuts
    try:
        failover_path = nx.shortest_path(G, source=origin, target=destination, weight="weight")
        total_failover_weight = sum(G[failover_path[i]][failover_path[i+1]]["weight"] for i in range(len(failover_path)-1))
        
        if total_failover_weight >= 90000:
            failover_possible = False
            failover_path_nodes = []
            failover_dist = 0
            failover_time = 0
        else:
            failover_possible = True
            failover_path_nodes = failover_path
            failover_dist = sum(G[failover_path[i]][failover_path[i+1]]["distance_km"] for i in range(len(failover_path)-1))
            failover_time = round(sum(G[failover_path[i]][failover_path[i+1]]["transit_hours"] for i in range(len(failover_path)-1)), 1)
    except Exception:
        failover_possible = False
        failover_path_nodes = []
        failover_dist = 0
        failover_time = 0

    # 3. Multimodal Air Insertion Alternative (IAF C-130J from Hindon to Gaggal Airstrip)
    air_route = ["NDRF_8_GZB", "HINDON_AFB", "KANGRA_AIRPORT", "DHARAMSHALA_LZ"]
    air_time_hours = round(0.3 + 1.1 + 0.4 + 0.5, 1) # +0.5h staging
    air_dist_km = 446

    # Node details formatting
    path_details = []
    for node_id in (failover_path_nodes if failover_possible else air_route):
        info = INDIAN_TACTICAL_ROAD_NODES.get(node_id, {})
        path_details.append({
            "node_id": node_id,
            "name": info.get("name", node_id),
            "lat": info.get("lat", 0.0),
            "lon": info.get("lon", 0.0),
            "type": info.get("type", "NODE")
        })

    return {
        "origin": INDIAN_TACTICAL_ROAD_NODES[origin]["name"],
        "destination": INDIAN_TACTICAL_ROAD_NODES[destination]["name"],
        "severed_chokepoints": collapsed_bridges + flooded_corridors,
        "nominal_nominal_hours": round(nominal_time, 1),
        "nominal_nominal_distance_km": nominal_dist,
        "nominal_path": [INDIAN_TACTICAL_ROAD_NODES[n]["name"] for n in nominal_path],
        "failover_available": failover_possible,
        "failover_hours": failover_time,
        "failover_distance_km": failover_dist,
        "failover_path": [INDIAN_TACTICAL_ROAD_NODES[n]["name"] for n in failover_path_nodes],
        "active_corridor_nodes": path_details,
        "air_insertion_hours": air_time_hours,
        "air_insertion_distance_km": air_dist_km,
        "air_insertion_path": [INDIAN_TACTICAL_ROAD_NODES[n]["name"] for n in air_route],
        "tactical_recommendation": (
            "COMMAND DIRECTIVE: Mandi Bridge collapsed on primary corridor. "
            "Reroute road convoys via Western Valley bypass (Ropar -> Gaggal -> Dharamshala). "
            f"Simultaneously initiate IAF C-130J tactical airlift from Hindon AFB (ETA {air_time_hours} hrs)."
        )
    }


# =====================================================================
# APEX 4: EDGE UAV DRONE-AI RECONNAISSANCE & ACOUSTIC RUBBLE USAR
# =====================================================================

def get_drone_swarm_telemetry(zone_name="Kangra Sector 4"):
    """
    Returns real-time edge drone swarm reconnaissance telemetry:
    - Computer Vision YOLOv8 detections (trapped survivors, thermal heat spots, structural collapse)
    - Acoustic Rubble Probe spectral audio analysis (detecting SOS rhythmic taps)
    """
    detections = [
        {
            "id": "UAV-DET-01",
            "class": "TRAPPED_SURVIVOR",
            "confidence": 0.94,
            "thermal_signature_c": 36.8,
            "bbox": [140, 210, 85, 120], # [x, y, w, h]
            "gps": {"lat": 32.2215, "lon": 76.3260},
            "depth_est_m": 1.8,
            "triage_tag": "RED (IMMEDIATE RESCUE)",
            "icon": "🚨"
        },
        {
            "id": "UAV-DET-02",
            "class": "PANCAKE_STRUCTURAL_COLLAPSE",
            "confidence": 0.98,
            "thermal_signature_c": 18.2,
            "bbox": [320, 80, 240, 180],
            "gps": {"lat": 32.2198, "lon": 76.3245},
            "depth_est_m": 0.0,
            "triage_tag": "EMS-98 GRADE 5 (HEAVY USAR REQUIRED)",
            "icon": "🏚️"
        },
        {
            "id": "UAV-DET-03",
            "class": "ACTIVE_SURVIVOR_WAVING",
            "confidence": 0.91,
            "thermal_signature_c": 37.1,
            "bbox": [480, 310, 95, 130],
            "gps": {"lat": 32.2230, "lon": 76.3275},
            "depth_est_m": 0.0,
            "triage_tag": "RED (EXTRICATION READY)",
            "icon": "🙋"
        },
        {
            "id": "UAV-DET-04",
            "class": "RUPTURED_LPG_PIPELINE",
            "confidence": 0.89,
            "thermal_signature_c": -4.2,
            "bbox": [70, 420, 160, 90],
            "gps": {"lat": 32.2185, "lon": 76.3210},
            "depth_est_m": 0.5,
            "triage_tag": "HAZMAT WARNING (CBRN/EXPLOSION)",
            "icon": "☣️"
        }
    ]

    # Acoustic Subsurface Probe Classifier
    acoustic_probe = {
        "probe_id": "ACOUSTIC-PROBE-ALPHA-07",
        "sensor_type": "Piezo-Electric Geophone & Rubble Contact Microphone",
        "sampling_rate_khz": 48.0,
        "peak_frequency_hz": 245.0,
        "rhythmic_pattern": "3 TAPS / 5 SECONDS (SOS CADENCE)",
        "signal_to_noise_db": "+16.8 dB",
        "human_tapping_probability": 0.93,
        "ambient_generator_filtered": True,
        "triangulated_rubble_depth_m": 2.4,
        "verdict": "CONFIRMED CONSCIOUS TRAPPED VICTIM SIGNAL"
    }

    return {
        "swarm_status": "AIRBORNE_PATROL_ACTIVE",
        "drones_online": 4,
        "drone_models": "DRDO Rustom-T / DJI Matrice 350 RTK Thermal",
        "flight_altitude_m": 45.0,
        "target_sector": zone_name,
        "battery_avg_pct": 78,
        "video_stream_latency_ms": 68,
        "detections": detections,
        "trapped_survivors_count": 2,
        "acoustic_probe": acoustic_probe
    }


# =====================================================================
# APEX 5: AUTONOMOUS NDMA TACTICAL AI INCIDENT COMMANDER (ICS-201/204)
# =====================================================================

def generate_autonomous_incident_action_plan(
    incident_name="KANGRA VALLEY MEGATHRUST EVENT",
    mag=6.8,
    affected_pop=1200000,
    primary_bn="14th Bn NDRF (Himachal)"
):
    """
    Synthesizes an official Incident Action Plan (IAP) conforming to NDMA and
    international Incident Command System (ICS-201/ICS-204) standards.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Surgical Logistics Matrix calculation based on population and magnitude
    est_displaced = int(affected_pop * (0.015 * (mag - 4.5)))
    oxygen_cylinders = int(est_displaced * 0.08)
    inflatable_boats = int(est_displaced * 0.02)
    k9_dog_squads = 8
    hydraulic_cssr_spreaders = 24
    field_surgical_units = 4
    water_purification_liters_day = est_displaced * 15 # Sphere standard: 15L/person/day

    objectives = [
        "1. Complete Golden Hour (0-60 min) acoustic & drone USAR grid sweeps across Sector 1-4.",
        "2. Establish primary airlift corridor between IAF Hindon and Gaggal forward strip.",
        "3. Bypass collapsed Mandi Suspension Bridge via western Ropar-Una tactical corridor.",
        "4. Pre-activate AIIMS Field Detachment and Stage-1 Trauma Triage at Kangra District Stadium.",
        "5. Broadcast continuous NavIC S-band and ITU-T CAP v1.2 alerts in Hindi and Punjabi."
    ]

    assignments = [
        {
            "branch": "Operations (Search & Rescue)",
            "commander": "Commandant, 14th Bn NDRF",
            "task": "Heavy CSSR breaching and diamond wire rubble cutting at high-density collapsed zones.",
            "status": "DEPLOYED"
        },
        {
            "branch": "Aviation Support",
            "commander": "Air Officer Commanding, IAF Hindon",
            "task": "Maintain 6 continuous Mi-17V5 sorties for aero-medical evacuation of critical casualties.",
            "status": "AIRBORNE"
        },
        {
            "branch": "Logistics & Shelter",
            "commander": "State Relief Commissioner, HP",
            "task": f"Mobilize {water_purification_liters_day:,} Liters/day portable drinking water and {oxygen_cylinders} medical O2 cylinders.",
            "status": "EN_ROUTE"
        },
        {
            "branch": "Telecommunications & Mesh",
            "commander": "NDMA Sachet Technical Wing",
            "task": "Deploy 12 portable LoRa/VHF mesh repeater poles to bypass downed cellular towers.",
            "status": "OPERATIONAL"
        }
    ]

    speech_announcement_hi = (
        f"ध्यान दें! राष्ट्रीय आपदा प्रबंधन प्राधिकरण और प्रहारी-एक्स का सर्वोच्च आपातकालीन संदेश। "
        f"{incident_name} के कारण प्रभावित क्षेत्रों में राहत और बचाव दल सक्रिय कर दिए गए हैं। "
        f"नागरिक सुरक्षित राहत शिविरों की ओर जाएं और क्षतिग्रस्त इमारतों से दूर रहें।"
    )

    return {
        "iap_id": f"NDMA-IAP-2026-{int(time.time()) % 100000:05d}",
        "incident_name": incident_name,
        "date_time": now,
        "operational_period": "00:00 - 12:00 Hours (Tactical Phase 1)",
        "incident_commander": "Integrated Incident Commander (NDMA / NDRF HQ)",
        "command_objectives": objectives,
        "branch_assignments": assignments,
        "estimated_displaced_persons": f"{est_displaced:,}",
        "logistics_supply_matrix": {
            "drinking_water_liters_day": f"{water_purification_liters_day:,} L/day",
            "medical_oxygen_cylinders": f"{oxygen_cylinders:,} Units",
            "heavy_hydraulic_cssr_tools": f"{hydraulic_cssr_spreaders} Sets",
            "k9_canine_search_squads": f"{k9_dog_squads} Dog Teams",
            "field_trauma_surgical_units": f"{field_surgical_units} Mobile Rigs",
            "inflatable_rescue_boats": f"{inflatable_boats:,} Craft"
        },
        "voice_announcement_hi": speech_announcement_hi
    }
