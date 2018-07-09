class NavMixin(object):
    """
    View mixin which provides sorting for ListView.
    """
    nav_main = None
    nav_name = None

    def get_context_data(self, *args, **kwargs):
        context = super(NavMixin, self).get_context_data(*args, **kwargs)
        context.update({
            'nav_main': self.nav_main,
            'nav_name': self.nav_name,
        })
        return context
