# Protocolo Global de Arquitectura: AntiGravity Core

Este documento establece el estándar obligatorio para todos los proyectos bajo el ecosistema AntiGravity.

## 1. Mandato de Arquitectura (Screaming Architecture)
Cualquier proyecto nuevo o existente DEBE reflejar su propósito de negocio en su estructura de carpetas de primer nivel.

Standard Directory Mapping:
- `src/domains/<domain-name>`: Lógica de negocio pura y casos de uso.
- `src/infrastructure/`: Implementaciones técnicas (DB, Servidores, UI libs).
- `src/shared/`: Utilidades, tipos y herramientas transversales.
- `docs/`: Todo archivo Markdown o PDF organizados por categoría (manuals, architecture, plans).
- `scripts/`: Solo scripts de automatización de entorno o ejecución rápida.

## 2. Reglas para Agentes de IA
1. **Root Limpio**: No se permiten archivos sueltos en el directorio raíz excepto configuraciones esenciales (.env, package.json, tsconfig.json).
2. **Nomenclatura Semántica**: Los nombres de los dominios deben ser verbos o sustantivos que representen la función del negocio (e.g., `lead-generation`, `intelligence`).
3. **Persistencia**: Este protocolo debe ser inyectado en los archivos `.cursorrules` de cada repositorio secundario.

## 3. Estándar de Documentación
- Cada dominio debe tener un `README.md` local si su complejidad lo requiere.
- El `README.md` raíz debe servir como mapa de los dominios.

---
*Aprobado por el Sistema AntiGravity - 2026*
