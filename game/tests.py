import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Player, Room, NPC, Item, InventoryItem, ChatMessage, Party, PartyMembership
from . import services


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
        response = self.client.post(
            '/command/',
            data=json.dumps({'command': 'look'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        output = response.json()['output']
        self.assertIn("Hub", output)
        self.assertIn("The center.", output)

    def test_movement(self):
        response = self.client.post(
            '/command/',
            data=json.dumps({'command': 'north'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.location.id, 2)
        self.assertIn("Other", response.json()['output'])

    def test_attack_npc(self):
        npc = NPC.objects.create(
            name="Drone", location=self.hub, hp=20, hp_max=20,
            attack=5, defense=2, lvl=1, money_drop=10, exp_drop=10
        )
        response = self.client.post(
            '/command/',
            data=json.dumps({'command': 'attack drone'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        npc.refresh_from_db()
        self.assertLess(npc.hp, 20)
        self.assertIn("You hit Drone", response.json()['output'])

    def test_buy_item(self):
        self.hub.shop_name = "General Store"
        self.hub.save()
        item = Item.objects.create(name="Battery", price=20, item_type="misc")

        response = self.client.post(
            '/command/',
            data=json.dumps({'command': 'buy battery'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.money, 30)
        self.assertTrue(InventoryItem.objects.filter(player=self.player, item=item).exists())

    def test_equip_item(self):
        item = Item.objects.create(name="Laser", item_type="weapon", attack_bonus=5)
        InventoryItem.objects.create(player=self.player, item=item)

        response = self.client.post(
            '/command/',
            data=json.dumps({'command': 'equip laser'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.attack, 15)

        ii = InventoryItem.objects.get(player=self.player, item=item)
        self.assertTrue(ii.equipped)

    def test_say_command(self):
        response = self.client.post(
            '/command/',
            data=json.dumps({'command': 'say hello world'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("You say: hello world", response.json()['output'])
        self.assertTrue(ChatMessage.objects.filter(message="hello world").exists())

    def test_who_command(self):
        response = self.client.post(
            '/command/',
            data=json.dumps({'command': 'who'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("neo", response.json()['output'])


class PartyTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create rooms
        self.hub = Room.objects.create(id=1, name="Hub", description="The center.")
        self.other_room = Room.objects.create(id=2, name="Other", description="Elsewhere.")
        self.hub.exits = {"north": 2}
        self.hub.save()
        self.other_room.exits = {"south": 1}
        self.other_room.save()

        # Create users and players
        self.leader_user = User.objects.create_user(username="leader", password="password")
        self.leader = Player.objects.create(
            user=self.leader_user, location=self.hub, hp=100, hp_max=100,
            attack=10, defense=5, money=50, online=True
        )

        self.member_user = User.objects.create_user(username="member", password="password")
        self.member = Player.objects.create(
            user=self.member_user, location=self.hub, hp=100, hp_max=100,
            attack=10, defense=5, money=50, online=True
        )

        self.other_user = User.objects.create_user(username="other", password="password")
        self.other = Player.objects.create(
            user=self.other_user, location=self.hub, hp=100, hp_max=100,
            attack=10, defense=5, money=50, online=True
        )

    def test_create_party(self):
        result = services.create_party(self.leader, "Test Party")
        self.assertIn("Party 'Test Party' created", result)
        self.assertTrue(Party.objects.filter(name="Test Party").exists())
        self.assertEqual(Party.objects.first().leader, self.leader)

    def test_create_party_while_in_party(self):
        services.create_party(self.leader)
        result = services.create_party(self.leader, "Another Party")
        self.assertIn("already in a party", result)

    def test_invite_to_party(self):
        services.create_party(self.leader)
        result = services.invite_to_party(self.leader, "member")
        self.assertIn("Invited member to the party", result)
        self.member.refresh_from_db()
        self.assertIsNotNone(self.member.party_invite)

    def test_invite_not_in_party(self):
        result = services.invite_to_party(self.leader, "member")
        self.assertIn("not in a party", result)

    def test_invite_not_leader(self):
        # Create party with member as leader, then try to invite with leader
        services.create_party(self.member)
        result = services.invite_to_party(self.leader, "other")
        self.assertIn("not in a party", result)

    def test_invite_target_not_online(self):
        services.create_party(self.leader)
        self.member.online = False
        self.member.save()
        result = services.invite_to_party(self.leader, "member")
        self.assertIn("not found or not online", result)

    def test_accept_party_invite(self):
        services.create_party(self.leader)
        services.invite_to_party(self.leader, "member")
        self.member.refresh_from_db()
        result = services.accept_party_invite(self.member)
        self.assertIn("joined", result)
        self.assertTrue(self.member.parties.exists())

    def test_accept_no_invite(self):
        result = services.accept_party_invite(self.member)
        self.assertIn("No pending party invitation", result)

    def test_party_max_size(self):
        services.create_party(self.leader, "Full Party")
        services.invite_to_party(self.leader, "member")
        self.member.refresh_from_db()
        services.accept_party_invite(self.member)
        self.leader.refresh_from_db()
        services.invite_to_party(self.leader, "other")
        self.other.refresh_from_db()
        services.accept_party_invite(self.other)
        # Now try to invite a 4th player (should fail - party is full)
        # Create a 4th player
        fourth_user = User.objects.create_user(username="fourth", password="password")
        fourth = Player.objects.create(
            user=fourth_user, location=self.hub, hp=100, hp_max=100,
            attack=10, defense=5, money=50, online=True
        )
        self.leader.refresh_from_db()
        result = services.invite_to_party(self.leader, "fourth")
        self.assertIn("Party is full", result)

    def test_leave_party(self):
        services.create_party(self.leader)
        services.invite_to_party(self.leader, "member")
        self.member.refresh_from_db()
        services.accept_party_invite(self.member)
        self.member.refresh_from_db()
        result = services.leave_party(self.member)
        self.assertIn("left the party", result)
        self.assertFalse(self.member.parties.exists())

    def test_leave_party_as_leader_disbands(self):
        services.create_party(self.leader)
        services.invite_to_party(self.leader, "member")
        services.accept_party_invite(self.member)
        result = services.leave_party(self.leader)
        self.assertIn("disbanded the party", result)
        self.assertFalse(Party.objects.exists())

    def test_get_party_status(self):
        services.create_party(self.leader, "Status Test")
        result = services.get_party_status(self.leader)
        self.assertIn("Status Test", result)
        self.assertIn("leader", result.lower())

    def test_get_party_status_not_in_party(self):
        result = services.get_party_status(self.leader)
        self.assertIn("not in a party", result)

    def test_party_movement(self):
        services.create_party(self.leader)
        services.invite_to_party(self.leader, "member")
        self.member.refresh_from_db()
        services.accept_party_invite(self.member)
        self.member.refresh_from_db()
        result = services.move_party_leader(self.leader, "north")
        self.assertIn("Other", result)
        self.member.refresh_from_db()
        self.assertEqual(self.member.location.id, 2)  # Member moved with leader

    def test_party_movement_not_leader(self):
        services.create_party(self.leader)
        services.invite_to_party(self.leader, "member")
        self.member.refresh_from_db()
        services.accept_party_invite(self.member)
        self.member.refresh_from_db()
        result = services.move_party_leader(self.member, "north")
        self.assertIn("Only the party leader", result)
