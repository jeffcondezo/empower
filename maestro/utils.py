def format_categories(categorias):
    contenedor = []
    profundidad = -1
    for c in categorias:
        if c.nivel == 1:
            contenedor.append([c.descripcion])
            profundidad += 1
        else:
            contenedor[profundidad].append(c.descripcion)
    return contenedor
