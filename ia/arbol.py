# ia/arbol.py
"""
Estructura mínima para un árbol de decisiones emocional.
Útil si quieres mapear combinaciones de emociones a rutas concretas.
"""

from typing import Dict, Any, Optional, List

# Ejemplo simple de nodo
class NodoDecision:
    def __init__(self, key: str, respuesta: Optional[str]=None, hijos: Optional[Dict[str, 'NodoDecision']]=None):
        self.key = key
        self.respuesta = respuesta
        self.hijos = hijos or {}

    def agregar_hijo(self, valor: str, nodo: 'NodoDecision'):
        self.hijos[valor] = nodo

    def evaluar(self, signos: List[str]) -> Optional[str]:
        """
        Recorre el árbol buscando la primera respuesta aplicable según la lista de signos/emociones.
        Implementación simple; puedes alterar la lógica (prioridad, combinación, etc).
        """
        # Si nodo tiene respuesta, devolverla
        if self.respuesta:
            return self.respuesta
        # Buscar un hijo cuya clave esté en signos
        for v, nodo in self.hijos.items():
            if v in signos:
                return nodo.evaluar(signos)
        return None
