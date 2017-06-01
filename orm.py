import databases


class Field:
    NAN = "NAN"

    def __init__(self, name, typ=None, is_primary=False, default=None, auto_increment=False):
        self.name = name
        self.type = typ
        self.is_primary = is_primary
        self.default = default
        self.auto_increment = auto_increment


class ModelMetaClass(type):
    def __new__(mcs, name, bases, attributes):
        if name == "BaseModel":
            return type.__new__(mcs, name, bases, attributes)
        table_name = attributes.get('__tablename__')
        mappings = {}
        fields = []
        primary_key = None
        for key, value in attributes.items():
            if key[0:2] == '__':
                continue
            if isinstance(value, Field):
                mappings[key] = value
                if value.is_primary:
                    if not primary_key:
                        primary_key = value
                    else:
                        raise Exception("Too many primary key {}, {}".format(primary_key, value))
                else:
                    fields.append(value)
        if not primary_key:
            raise Exception("No primary found")

        for key in mappings.keys():
            attributes.pop(key)

        attributes['__fields__'] = fields  # 保存字段
        attributes['__mappings__'] = mappings  # 保存列名与字段的映射关系
        attributes['__primary_key__'] = primary_key
        attributes['__tablename__'] = table_name
        return type.__new__(mcs, name, bases, attributes)


class BaseModel(metaclass=ModelMetaClass):
    __tablename__ = None
    __primary_key__ = None
    __mappings__ = None

    async def update(self):
        keys, args = await self.get_keys_values()

        return await self.exe("UPDATE {} SET {} WHERE {} = ?".
                              format(self.__tablename__,
                                     ",".join(["{}=?".format(key) for key in keys]),
                                     self.__primary_key__.name,
                                     ),
                              [arg for arg in args] + [getattr(self, self.__primary_key__.name)])

    async def save(self):
        keys, args = await self.get_keys_values()

        return await self.exe("INSERT INTO {} ({}) VALUES({})".
                              format(self.__tablename__, ",".join([i for i in keys]), ",".join(["?"]*len(args))), args)

    async def delete(self):
        return await self.exe("DELETE FROM {} WHERE {}=?".format(self.__tablename__, self.__primary_key__.name),
                              getattr(self, self.__primary_key__.name))

    async def get_keys_values(self):
        keys = []
        values = []
        for key, field in self.__mappings__.items():
            if field.auto_increment or field.is_primary:
                continue
            keys.append(key)
            values.append(getattr(self, key, field.default))
        return keys, values

    @classmethod
    async def filter_by(cls, **kwargs):
        keys = []
        args = []
        for key, value in kwargs.items():
            keys.append(key)
            args.append(value)
        res = await databases.select("select * from {} where {}".
                                     format(cls.__tablename__, ','.join(["{}=?".format(i) for i in keys])), tuple(args))
        if len(res) == 0:
            return None
        else:
            return [cls(**i) for i in res]

    @classmethod
    async def exe(cls, sql, args=None):
        return await databases.execute(sql, args)
