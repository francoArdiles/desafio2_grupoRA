import json


class Action:

    def __init__(self, knight_id, movement):
        self.knight_id = knight_id
        self.knight_movement = movement

    def send(self):
        result = {
            "knight_id": self.knight_id,
            "knight_movement": self.knight_movement
        }
        print(json.dumps(result))

    def __str__(self):
        return '"knight_id": {}, knight_movement: {}'.format(
            self.knight_id, self.knight_movement)
