/**
 * PRAHARIX 3.0 - i18n Translation Engine
 * Item #17: Hindi, Marathi, English support
 */

const PRAHARIX_I18N = {
  en: {
    dashboard: 'Command Dashboard',
    alerts: 'Live Alerts',
    earthquakes: 'Seismic Events',
    weather: 'Weather',
    risk_level: 'Risk Level',
    critical: 'CRITICAL',
    high: 'HIGH',
    medium: 'MEDIUM',
    low: 'LOW',
    district: 'District',
    severity: 'Severity',
    status: 'Status',
    description: 'Description',
    submit: 'Submit Report',
    evacuation: 'Evacuation Routes',
    shelters: 'Shelter Locations',
    resources: 'Emergency Resources',
    sitrep: 'Situation Report',
    loading: 'Loading...',
    error: 'Error loading data',
    last_updated: 'Last updated',
    total_events: 'Total Events',
    ndrf_status: 'NDRF Status',
    early_warning: 'Early Warning',
    report_incident: 'Report Incident'
  },
  hi: {
    dashboard: 'कमान डैशबोर्ड',
    alerts: 'सक्रिय अलर्ट',
    earthquakes: 'भूकंपीय घटनाएं',
    weather: 'मौसम',
    risk_level: 'जोखिम स्तर',
    critical: 'अत्यंत गंभीर',
    high: 'उच्च',
    medium: 'मध्यम',
    low: 'कम',
    district: 'जिला',
    severity: 'गंभीरता',
    status: 'स्थिति',
    description: 'विवरण',
    submit: 'रिपोर्ट जमा करें',
    evacuation: 'निकासी मार्ग',
    shelters: 'आश्रय स्थान',
    resources: 'आपातकालीन संसाधन',
    sitrep: 'स्थिति रिपोर्ट',
    loading: 'लोड हो रहा है...',
    error: 'डेटा लोड करने में त्रुटि',
    last_updated: 'अंतिम अपडेट',
    total_events: 'कुल घटनाएं',
    ndrf_status: 'एनडीआरएफ स्थिति',
    early_warning: 'प्रारंभिक चेतावनी',
    report_incident: 'घटना रिपोर्ट करें'
  },
  mr: {
    dashboard: 'कमांड डॅशबोर्ड',
    alerts: 'सक्रिय सूचना',
    earthquakes: 'भूकंप घटना',
    weather: 'हवामान',
    risk_level: 'धोका पातळी',
    critical: 'अतिगंभीर',
    high: 'उच्च',
    medium: 'मध्यम',
    low: 'कमी',
    district: 'जिल्हा',
    severity: 'तीव्रता',
    status: 'स्थिती',
    description: 'वर्णन',
    submit: 'अहवाल सादर करा',
    evacuation: 'निर्वासन मार्ग',
    shelters: 'निवारा स्थळे',
    resources: 'आपत्कालीन साधने',
    sitrep: 'परिस्थिती अहवाल',
    loading: 'लोड होत आहे...',
    error: 'डेटा लोड करण्यात त्रुटी',
    last_updated: 'शेवटचे अपडेट',
    total_events: 'एकूण घटना',
    ndrf_status: 'एनडीआरएफ स्थिती',
    early_warning: 'प्रारंभिक इशारा',
    report_incident: 'घटना नोंदवा'
  }
};

window.praharixT = function(key, lang) {
  const l = lang || localStorage.getItem('praharix-lang') || 'en';
  return (PRAHARIX_I18N[l] && PRAHARIX_I18N[l][key]) || PRAHARIX_I18N['en'][key] || key;
};

// Auto-translate elements with data-i18n attribute
function applyTranslations(lang) {
  document.querySelectorAll('[data-i18n]').forEach(function(el) {
    const key = el.getAttribute('data-i18n');
    el.textContent = window.praharixT(key, lang);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el) {
    const key = el.getAttribute('data-i18n-placeholder');
    el.placeholder = window.praharixT(key, lang);
  });
  document.querySelectorAll('[data-i18n-aria]').forEach(function(el) {
    const key = el.getAttribute('data-i18n-aria');
    el.setAttribute('aria-label', window.praharixT(key, lang));
  });
}

document.addEventListener('DOMContentLoaded', function() {
  const lang = localStorage.getItem('praharix-lang') || 'en';
  applyTranslations(lang);
});

window.praharixApplyLang = applyTranslations;
