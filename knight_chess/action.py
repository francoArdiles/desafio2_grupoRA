import json


class Action:

    def __init__(self, knight_id, movement):
        self._knight_id = knight_id
        self.knight_movement = movement

    def send(self):
        result = {
            "knight_id": self._knight_id,
            "knight_movement": self.knight_movement
        }
        print(json.dumps(result))

    @property
    def knight_id(self):
        return int(self._knight_id)

    def __str__(self):
        return '"knight_id": {}, knight_movement: {}'.format(
            self._knight_id, self.knight_movement)
