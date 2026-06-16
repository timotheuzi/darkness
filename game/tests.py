from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Player, Room, NPC, Item, InventoryItem, ChatMessage

class GameLogicTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create rooms
        self.hub = Room.objects.create(id=1, name="Hub", description="The center.")
        self.other_room = Room.objects.create(id=2, name="Other", description="Elsewhere.")
        self.hub.exits = {"north": 2}
        self.hub.save()
        self.other_room.exits = {"south": 1}
        self.other_room.save()

        # Create user and player
        self.user = User.objects.create_user(username="neo", password="password")
        self.player = Player.objects.create(
            user=self.user, location=self.hub, hp=100, hp_max=100,
            attack=10, defense=5, money=50, online=True
        )
        self.client.login(username="neo", password="password")

    def test_look_command(self):
        response = self.client.post('/command/', data={'command': 'look'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        output = response.json()['output']
        self.assertIn("Hub", output)
        self.assertIn("The center.", output)

    def test_movement(self):
        response = self.client.post('/command/', data={'command': 'north'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.location.id, 2)
        self.assertIn("Other", response.json()['output'])

    def test_attack_npc(self):
        npc = NPC.objects.create(
            name="Drone", location=self.hub, hp=20, hp_max=20,
            attack=5, defense=2, lvl=1, money_drop=10, exp_drop=10
        )
        response = self.client.post('/command/', data={'command': 'attack drone'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        npc.refresh_from_db()
        self.assertLess(npc.hp, 20)
        self.assertIn("You hit Drone", response.json()['output'])

    def test_buy_item(self):
        self.hub.shop_name = "General Store"
        self.hub.save()
        item = Item.objects.create(name="Battery", price=20, item_type="misc")
        
        response = self.client.post('/command/', data={'command': 'buy battery'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.money, 30)
        self.assertTrue(InventoryItem.objects.filter(player=self.player, item=item).exists())

    def test_equip_item(self):
        item = Item.objects.create(name="Laser", item_type="weapon", attack_bonus=5)
        InventoryItem.objects.create(player=self.player, item=item)
        
        response = self.client.post('/command/', data={'command': 'equip laser'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.attack, 15)
        
        ii = InventoryItem.objects.get(player=self.player, item=item)
        self.assertTrue(ii.equipped)

    def test_say_command(self):
        response = self.client.post('/command/', data={'command': 'say hello world'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("You broadcast: hello world", response.json()['output'])
        self.assertTrue(ChatMessage.objects.filter(message="hello world").exists())

    def test_who_command(self):
        response = self.client.post('/command/', data={'command': 'who'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("neo", response.json()['output'])
