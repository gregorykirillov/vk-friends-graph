class PersonTypes():
    def __init__(self):
        self.deleted_or_banned_person = 0
        self.private_person = 0
        self.normal_person = 0
        self.error_fetched = 0

    def inc_private(self):
        self.private_person += 1

    def inc_deleted(self):
        self.deleted_or_banned_person += 1

    def inc_normal(self):
        self.normal_person += 1

    def inc_error(self):
        self.normal_person += 1

    def get_private(self):
        return self.private_person

    def get_deleted(self):
        return self.deleted_or_banned_person

    def get_normal(self):
        return self.normal_person

    def get_error(self):
        return self.normal_person
