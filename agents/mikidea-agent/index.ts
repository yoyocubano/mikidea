import { agent, tool } from "@21st-sdk/agent";
import { z } from "zod";

export default agent({
  name: "Aguilar-Guilarte AI",
  system: "Eres el asistente inteligente de 'Aguilar-Guilarte Haul & Harvest' en Houston. Tu objetivo es ayudar a los clientes a despejar basura, escombros y muebles. Hablas en español e inglés. Eres profesional, eficiente y conoces bien el lema: 'Inventiva Cubana, Fuerza Americana'.",
  tools: {
    calculate_estimate: tool({
      description: "Calcula un presupuesto estimado basado en el tipo de servicio, distancia y volumen de carga.",
      inputSchema: z.object({
        serviceType: z.enum(["junk", "construction", "roofing", "scrap"]).describe("Tipo de servicio"),
        mileage: z.number().describe("Millas de distancia"),
        volume: z.number().describe("Volumen (0.5 para media traila, 1.0 para full)"),
      }),
      execute: async ({ serviceType, mileage, volume }) => {
        let base = volume === 0.5 ? 275 : 650;
        let multiplier = serviceType === "roofing" ? 1.45 : (serviceType === "scrap" ? 0.6 : 1.0);
        const total = (base * multiplier) + (mileage * 3.85) + 85;
        
        return {
          content: [
            { 
              type: "text", 
              text: `Basado en tus datos, el estimado para ${serviceType} es de $${total.toFixed(2)}. ¿Deseas que te ponga en contacto con un operador?` 
            }
          ],
        };
      },
    }),
  },
});
