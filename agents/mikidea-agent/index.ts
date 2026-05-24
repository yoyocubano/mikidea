import { agent, tool } from "@21st-sdk/agent";
import { z } from "zod";

// ============================================================================
// CONFIGURATION - Externalize magic numbers and constants
// ============================================================================

const CONFIG = {
  // Pricing constants (in USD)
  PRICING: {
    BASE_HALF_TRAILA: 275,
    BASE_FULL_TRAILA: 650,
    MILEAGE_RATE: 3.85,
    FUEL_SURCHARGE: 85,
  },
  
  // Service type multipliers
  SERVICE_MULTIPLIERS: {
    junk: 1.0,
    construction: 1.0,
    roofing: 1.45,
    scrap: 0.6,
  } as const,
  
  // Supported languages for internationalization
  LANGUAGES: {
    es: {
      greeting: "¡Hola! Soy el asistente de Aguilar-Guilarte Haul & Harvest.",
      estimate_intro: "Basado en tus datos, el estimado para",
      contact_question: "¿Deseas que te ponga en contacto con un operador?",
      currency: "$",
    },
    en: {
      greeting: "Hello! I'm the Aguilar-Guilarte Haul & Harvest assistant.",
      estimate_intro: "Based on your information, the estimated cost for",
      contact_question: "Would you like me to connect you with an operator?",
      currency: "$",
    },
  },
  
  // Validation constraints
  VALIDATION: {
    MIN_MILEAGE: 0,
    MAX_MILEAGE: 500,
    MIN_VOLUME: 0.1,
    MAX_VOLUME: 3.0,
  },
};

// Type definitions
type ServiceType = keyof typeof CONFIG.SERVICE_MULTIPLIERS;
type Language = keyof typeof CONFIG.LANGUAGES;

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Detect language from user input or default to Spanish
 */
function detectLanguage(userInput?: string): Language {
  if (!userInput) return 'es';
  
  // Simple heuristic - can be enhanced with proper language detection
  const commonEnglishWords = ['the', 'and', 'is', 'are', 'have', 'has', 'want', 'need'];
  const words = userInput.toLowerCase().split(/\s+/);
  const englishWordCount = words.filter(w => commonEnglishWords.includes(w)).length;
  
  return englishWordCount > 2 ? 'en' : 'es';
}

/**
 * Validate input parameters
 */
function validateInputs(
  serviceType: string,
  mileage: number,
  volume: number
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  // Validate service type
  if (!Object.keys(CONFIG.SERVICE_MULTIPLIERS).includes(serviceType)) {
    errors.push(`Invalid service type. Must be one of: ${Object.keys(CONFIG.SERVICE_MULTIPLIERS).join(', ')}`);
  }
  
  // Validate mileage
  if (mileage < CONFIG.VALIDATION.MIN_MILEAGE) {
    errors.push(`Mileage cannot be negative (got: ${mileage})`);
  }
  if (mileage > CONFIG.VALIDATION.MAX_MILEAGE) {
    errors.push(`Mileage exceeds maximum of ${CONFIG.VALIDATION.MAX_MILEAGE} miles`);
  }
  
  // Validate volume
  if (volume < CONFIG.VALIDATION.MIN_VOLUME) {
    errors.push(`Volume must be at least ${CONFIG.VALIDATION.MIN_VOLUME} (got: ${volume})`);
  }
  if (volume > CONFIG.VALIDATION.MAX_VOLUME) {
    errors.push(`Volume exceeds maximum of ${CONFIG.VALIDATION.MAX_VOLUME} trailas`);
  }
  
  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Calculate estimate with proper separation of concerns
 */
function calculateEstimate(
  serviceType: ServiceType,
  mileage: number,
  volume: number
): number {
  const baseRate = volume <= 0.5 
    ? CONFIG.PRICING.BASE_HALF_TRAILA 
    : CONFIG.PRICING.BASE_FULL_TRAILA;
  
  const multiplier = CONFIG.SERVICE_MULTIPLIERS[serviceType] || 1.0;
  const mileageCost = mileage * CONFIG.PRICING.MILEAGE_RATE;
  
  return (baseRate * multiplier) + mileageCost + CONFIG.PRICING.FUEL_SURCHARGE;
}

/**
 * Format currency amount
 */
function formatCurrency(amount: number, language: Language): string {
  return `${CONFIG.LANGUAGES[language].currency}${amount.toFixed(2)}`;
}

// ============================================================================
// AGENT DEFINITION
// ============================================================================

export default agent({
  name: "Aguilar-Guilarte AI",
  system: `Eres el asistente inteligente de 'Aguilar-Guilarte Haul & Harvest' en Houston. 
Tu objetivo es ayudar a los clientes a despejar basura, escombros y muebles. 
Hablas en español e inglés según el idioma del cliente. Eres profesional, eficiente y conoces bien el lema: 
'Inventiva Cubana, Fuerza Americana'.

Servicios principales:
- Junk removal (basura general)
- Construction debris (escombros de construcción)
- Roofing materials (materiales de techado)
- Scrap metal (metal de chatarra)

Precios base:
- Media traila (≤0.5): $275
- Traila completa (>0.5): $650
- Millaje: $3.85/milla
- Combustible: $85 fijo

Multiplicadores por tipo:
- Roofing: 1.45x
- Scrap: 0.6x
- Otros: 1.0x`,
  
  tools: {
    calculate_estimate: tool({
      description: "Calcula un presupuesto estimado basado en el tipo de servicio, distancia y volumen de carga.",
      inputSchema: z.object({
        serviceType: z.enum(["junk", "construction", "roofing", "scrap"]).describe("Tipo de servicio"),
        mileage: z.number().describe("Millas de distancia"),
        volume: z.number().describe("Volumen (0.5 para media traila, 1.0 para full)"),
        language: z.enum(["es", "en"]).optional().describe("Idioma preferido (default: auto-detect)"),
        userInput: z.string().optional().describe("Input del usuario para detección de idioma"),
      }),
      execute: async ({ serviceType, mileage, volume, language, userInput }) => {
        // Auto-detect language if not specified
        const detectedLang = language || detectLanguage(userInput);
        
        // Validate inputs
        const validation = validateInputs(serviceType, mileage, volume);
        if (!validation.valid) {
          return {
            content: [
              {
                type: "text",
                text: `⚠️ Error en los datos proporcionados:\n\n${validation.errors.join('\n')}`,
              },
            ],
          };
        }
        
        // Calculate estimate
        const total = calculateEstimate(serviceType as ServiceType, mileage, volume);
        const formattedTotal = formatCurrency(total, detectedLang);
        
        // Get localized messages
        const messages = CONFIG.LANGUAGES[detectedLang];
        
        // Build response with breakdown
        const breakdown = [
          `${messages.estimate_intro} ${serviceType} es de ${formattedTotal}`,
          "",
          "📊 Desglose:",
          `- Tarifa base: ${formatCurrency(volume <= 0.5 ? CONFIG.PRICING.BASE_HALF_TRAILA : CONFIG.PRICING.BASE_FULL_TRAILA, detectedLang)}`,
          `- Multiplicador (${serviceType}): ${CONFIG.SERVICE_MULTIPLIERS[serviceType]}x`,
          `- Millaje (${mileage} mi × $${CONFIG.PRICING.MILEAGE_RATE}): ${formatCurrency(mileage * CONFIG.PRICING.MILEAGE_RATE, detectedLang)}`,
          `- Combustible: ${formatCurrency(CONFIG.PRICING.FUEL_SURCHARGE, detectedLang)}`,
          "",
          messages.contact_question,
        ].join('\n');
        
        return {
          content: [
            {
              type: "text",
              text: breakdown,
            },
          ],
        };
      },
    }),
    
    // New tool: Get service information
    get_service_info: tool({
      description: "Obtiene información detallada sobre los tipos de servicio disponibles",
      inputSchema: z.object({
        serviceType: z.enum(["junk", "construction", "roofing", "scrap"]).optional().describe("Tipo de servicio específico"),
        language: z.enum(["es", "en"]).optional().describe("Idioma preferido"),
      }),
      execute: async ({ serviceType, language }) => {
        const lang = language || 'es';
        const messages = CONFIG.LANGUAGES[lang];
        
        const services = {
          junk: {
            es: "Remoción de basura general: muebles viejos, electrodomésticos, cajas, etc.",
            en: "General junk removal: old furniture, appliances, boxes, etc.",
          },
          construction: {
            es: "Escombros de construcción: drywall, madera, concreto, materiales de demolición.",
            en: "Construction debris: drywall, wood, concrete, demolition materials.",
          },
          roofing: {
            es: "Materiales de techado: tejas, shingles, madera de techo. (Tarifa especial: 1.45x)",
            en: "Roofing materials: tiles, shingles, roof wood. (Special rate: 1.45x)",
          },
          scrap: {
            es: "Metal de chatarra: aluminio, cobre, acero. (Descuento: 0.6x)",
            en: "Scrap metal: aluminum, copper, steel. (Discount: 0.6x)",
          },
        };
        
        if (serviceType) {
          return {
            content: [
              {
                type: "text",
                text: `**${serviceType.toUpperCase()}**\n\n${services[serviceType][lang]}\n\nMultiplicador: ${CONFIG.SERVICE_MULTIPLIERS[serviceType]}x`,
              },
            ],
          };
        }
        
        // Return all services
        const allServices = Object.entries(services)
          .map(([key, value]) => `**${key.toUpperCase()}**: ${value[lang]}`)
          .join('\n\n');
        
        return {
          content: [
            {
              type: "text",
              text: `${messages.greeting}\n\n${allServices}`,
            },
          ],
        };
      },
    }),
  },
});
