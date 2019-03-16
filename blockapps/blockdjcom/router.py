class DbRouter:
    DB_MAP = {
                'fcoin':
                {
                 'market_trade_order': ('market_trade_order_ro', 'market_trade_order'),
                },
            }

    def _getRoDB(self, mapinfo, model=None):
        kwargs = {}
        if model.__name__.startswith('Db'):
            kwargs['dbnum'] = model.__name__[2:4]
        if kwargs:
            dbalias = mapinfo[0] % kwargs
        else:
            dbalias = mapinfo[0]
        return dbalias

    def _getRwDB(self, mapinfo, model=None):
        kwargs = {}
        if model.__name__.startswith('Db'):
            kwargs['dbnum'] = model.__name__[2:4]
        if kwargs:
            dbalias = mapinfo[1] % kwargs
        else:
            dbalias = mapinfo[1]
        return dbalias

    def db_for_read(self, model, **hints):
        app_db_map = DbRouter.DB_MAP.get(model._meta.app_label, {})
        mapinfo = app_db_map.get(model._meta.db_table, None)
        if not mapinfo: return None
        return self._getRoDB(mapinfo, model)

    def db_for_write(self, model, **hints):
        app_db_map = DbRouter.DB_MAP.get(model._meta.app_label, {})
        mapinfo = app_db_map.get(model._meta.db_table, None)
        if not mapinfo: return None
        return self._getRwDB(mapinfo, model)

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label not in DbRouter.DB_MAP:
            return None
        app_db_map = DbRouter.DB_MAP[app_label]
        for model_name0, dbs in app_db_map.items():
            if type(dbs) in (tuple, list):
# rwdb
                if dbs[1] == db:
                    return True
            else:
                for modelcls, mapinfo in dbs.items():
                    if mapinfo[1] == db:
                        return True
        return None
