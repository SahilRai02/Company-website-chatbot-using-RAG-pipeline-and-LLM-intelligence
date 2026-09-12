from backend.rag.persona_loader import PersonaLoader

persona = PersonaLoader.load()

print("=" * 80)
print(persona)
print("=" * 80)