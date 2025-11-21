def menu_estaciones(gestor_est):
    print("1) Agregar estación")
    print("2) Listar estaciones")
    print("3) Eliminar estación")
    op = input("Opción: ")

    if op == "1":
        nombre = input("Nombre: ")
        poblacion = int(input("Población: "))
        gestor_est.agregar(nombre, poblacion, [])
