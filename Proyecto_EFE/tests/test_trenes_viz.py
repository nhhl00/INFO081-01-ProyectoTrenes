#!/usr/bin/env python3
"""
Test rápido para verificar que los trenes se renderizan correctamente en el canvas.
"""
import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.pestañas import Pestañas

def test_trenes_visualization():
    """Prueba la visualización de trenes."""
    root = tk.Tk()
    root.title("Test Visualización de Trenes")
    root.geometry("800x600")
    
    # Crear un frame para botones (dummy)
    frame_botones = ttk.Frame(root)
    
    # Crear pestañas
    pestanas = Pestañas(root, frame_botones)
    
    print("[TEST] Interfaz creada.")
    print(f"[TEST] Trenes cargados: {len(pestanas.trenes_list)}")
    for tren in pestanas.trenes_list:
        print(f"  - {tren.nombre_tren} ({tren.id_tren}) en {tren.estacion_actual}")
    
    print("[TEST] Canvas items antes de dibujar:", len(pestanas.canvas.find_all()))
    
    # Forzar un dibujo inicial
    pestanas.dibujar_elementos()
    
    canvas_items = pestanas.canvas.find_all()
    print("[TEST] Canvas items después de dibujar:", len(canvas_items))
    print(f"[TEST] Total items en canvas: {len(canvas_items)}")
    
    # Listar tags de cada item para verificar si están los trenes
    tren_count = 0
    for item_id in canvas_items:
        tags = pestanas.canvas.gettags(item_id)
        if any('tren_' in t for t in tags):
            tren_count += 1
            print(f"  ✓ Item {item_id}: TREN - tags={tags}")
        elif any(t in ['estacion', 'via_line', 'info', 'pasajeros', 'texto'] for t in tags):
            print(f"  Item {item_id}: {tags}")
    
    print(f"\n[RESULT] Trenes encontrados en canvas: {tren_count}")
    
    # Cerrar después de 2 segundos
    root.after(2000, root.quit)
    root.mainloop()

if __name__ == "__main__":
    test_trenes_visualization()
