from .models import AsignacionGrupo, PresentacionxProducto


def format_categories(categorias):
    contenedor = []
    profundidad = -1
    for c in categorias:
        if c.nivel == 1:
            contenedor.append([c.descripcion])
            profundidad += 1
        else:
            contenedor[profundidad].append(c.descripcion)
    print(contenedor)
    return contenedor


def empresa_list(user):
    asig_grupo = AsignacionGrupo.objects.get(usuario=user)
    sucursales = asig_grupo.sucursal.all()
    empresas = []
    for s in sucursales:
        empresas.append(s.empresa_id)
    return empresas


def set_presentacion_precio_compra(catalogoxproducto):
    for c in catalogoxproducto:
        presentacionxproducto = PresentacionxProducto.objects.filter(producto=c.producto).order_by('cantidad').reverse()[:1]
        if len(presentacionxproducto) > 0:
            c.presentacionxproducto_desc = presentacionxproducto[0].presentacion.descripcion
            c.precio_compra = presentacionxproducto[0].precio_compra
        else:
            c.presentacionxproducto_desc = 'NO DEFINIDO'
            c.precio_compra = 0.00
    return catalogoxproducto
