// ============================================================
// CGAO SKILLS - CONTENT & DATA STORE
// ============================================================

// Global Data Object
// Estructura de datos estática para evitar problemas de CORS en local file://
// y cumplir con la regla Offline-First.

const CGAO_DATA = {
    results: [
        {
            "name": "María Paula V.",
            "program": "Sistemas",
            "technical_score": 98,
            "innovation_score": 97,
            "total_score": 97.5,
            "rank": "ORO",
            "rank_icon": "fas fa-trophy",
            "rank_class": "bg-amber-gold/10 text-amber-gold border-amber-gold/30",
            "bar_color": "bg-neon-green",
            "bar_width": "tbl-w-98",
            "text_color": "text-neon-green",
            "highlight_color": "from-amber-gold to-yellow-200"
        },
        {
            "name": "Juan Camilo R.",
            "program": "Gestión Agroempresarial",
            "technical_score": 94,
            "innovation_score": 95,
            "total_score": 94.5,
            "rank": "PLATA",
            "rank_icon": "fas fa-medal",
            "rank_class": "bg-gray-400/10 text-gray-400 border-gray-400/30",
            "bar_color": "bg-blue-400",
            "bar_width": "tbl-w-94",
            "text_color": "text-blue-400",
            "highlight_color": "from-gray-300 to-gray-500"
        },
        {
            "name": "Andrés Felipe D.",
            "program": "Escuelas de Música",
            "technical_score": 89,
            "innovation_score": 95,
            "total_score": 92.0,
            "rank": "BRONCE",
            "rank_icon": "fas fa-medal",
            "rank_class": "bg-orange-700/10 text-orange-400 border-orange-700/30",
            "bar_color": "bg-purple-400",
            "bar_width": "tbl-w-89",
            "text_color": "text-purple-400",
            "highlight_color": "from-orange-400 to-orange-600"
        }
    ]
};
