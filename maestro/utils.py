def format_categories(categorias):
    contenedor = []
    profundidad = -1
    print(categorias)
    for c in categorias:
        print(c.nivel)
        if c.nivel == 1:
            contenedor.append([c.descripcion])
            print(contenedor)
            profundidad += 1
        else:
            contenedor[profundidad].append(c.descripcion)
    return contenedor
