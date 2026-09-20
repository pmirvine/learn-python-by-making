class Watched:
    def __init__(self, default):
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        old = self.__get__(instance)
        instance.__dict__[self.name] = value
        watcher = getattr(instance, f"watch_{self.name}", None)
        if watcher and value != old:
            watcher(old, value)


class Television:
    channel = Watched(1)

    def watch_channel(self, old, new):
        print(f"Retuning from {old} to {new}")


television = Television()
television.channel = 4
print(television.channel, vars(television), Television.channel)
