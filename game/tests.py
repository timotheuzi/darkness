import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Player, Room, NPC, Item, InventoryItem, ChatMessage, Party
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
            user=self.user,
            location=self.hub,
            hp=100,
            hp_max=100,
            attack=10,
            defense=5,
            money=50,
            online=True,
        )
        self.client.login(username="neo", password="password")

    def test_look_command(self):
        response = self.client.post(
            "/command/", data=json.dumps({"command": "look"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        output = response.json()["output"]
        self.assertIn("Hub", output)
        self.assertIn("The center.", output)

    def test_movement(self):
        response = self.client.post(
            "/command/", data=json.dumps({"command": "north"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.location.id, 2)
        self.assertIn("Other", response.json()["output"])

    def test_attack_npc(self):
        npc = NPC.objects.create(
            name="Drone",
            location=self.hub,
            hp=20,
            hp_max=20,
            attack=5,
            defense=2,
            lvl=1,
            money_drop=10,
            exp_drop=10,
        )
        response = self.client.post(
            "/command/",
            data=json.dumps({"command": "attack drone"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        npc.refresh_from_db()
        self.assertLess(npc.hp, 20)
        self.assertIn("You hit Drone", response.json()["output"])

    def test_buy_item(self):
        self.hub.shop_name = "General Store"
        self.hub.save()
        item = Item.objects.create(name="Battery", price=20, item_type="misc")

        response = self.client.post(
            "/command/",
            data=json.dumps({"command": "buy battery"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.money, 30)
        self.assertTrue(InventoryItem.objects.filter(player=self.player, item=item).exists())

    def test_equip_item(self):
        item = Item.objects.create(name="Laser", item_type="weapon", attack_bonus=5)
        InventoryItem.objects.create(player=self.player, item=item)

        response = self.client.post(
            "/command/",
            data=json.dumps({"command": "equip laser"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.attack, 15)

        ii = InventoryItem.objects.get(player=self.player, item=item)
        self.assertTrue(ii.equipped)

    def test_say_command(self):
        response = self.client.post(
            "/command/",
            data=json.dumps({"command": "say hello world"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("You say: hello world", response.json()["output"])
        self.assertTrue(ChatMessage.objects.filter(message="hello world").exists())

    def test_who_command(self):
        response = self.client.post(
            "/command/", data=json.dumps({"command": "who"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("neo", response.json()["output"])


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
            user=self.leader_user,
            location=self.hub,
            hp=100,
            hp_max=100,
            attack=10,
            defense=5,
            money=50,
            online=True,
        )

        self.member_user = User.objects.create_user(username="member", password="password")
        self.member = Player.objects.create(
            user=self.member_user,
            location=self.hub,
            hp=100,
            hp_max=100,
            attack=10,
            defense=5,
            money=50,
            online=True,
        )

        self.other_user = User.objects.create_user(username="other", password="password")
        self.other = Player.objects.create(
            user=self.other_user,
            location=self.hub,
            hp=100,
            hp_max=100,
            attack=10,
            defense=5,
            money=50,
            online=True,
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
        _fourth = Player.objects.create(
            user=fourth_user,
            location=self.hub,
            hp=100,
            hp_max=100,
            attack=10,
            defense=5,
            money=50,
            online=True,
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


class BotAITests(TestCase):
    def setUp(self):
        # Create rooms
        self.hub = Room.objects.create(
            id=1, name="Hub", description="The center.", safe_zone=True, zone="hub"
        )
        self.combat_room = Room.objects.create(
            id=2, name="Combat Zone", description="Dangerous.", safe_zone=False, zone="slums"
        )
        self.hub.exits = {"north": 2}
        self.hub.save()
        self.combat_room.exits = {"south": 1}
        self.combat_room.save()

        # Create bot player
        self.bot_user = User.objects.create_user(username="TestBot", password="password")
        self.bot = Player.objects.create(
            user=self.bot_user,
            location=self.combat_room,
            hp=100,
            hp_max=100,
            attack=15,
            defense=5,
            money=50,
            online=True,
            is_bot=True,
            bot_aggression=70,
            bot_social=50,
            karma=-50,
            lvl=5,
        )

        # Create NPC
        self.npc = NPC.objects.create(
            name="Test NPC",
            location=self.combat_room,
            hp=30,
            hp_max=30,
            attack=5,
            defense=2,
            lvl=2,
            money_drop=10,
            exp_drop=20,
            aggressive=True,
        )

    def test_bot_attacks_npc(self):
        """Test that bots can attack NPCs and gain EXP."""
        # Set last_bot_action to the past to ensure bot acts immediately
        from django.utils import timezone
        import datetime

        self.bot.last_bot_action = timezone.now() - datetime.timedelta(seconds=30)
        self.bot.save(update_fields=["last_bot_action"])

        # Check that NPC exists in room
        npcs = NPC.objects.filter(location=self.combat_room, hp__gt=0)
        self.assertTrue(npcs.exists(), "NPC should exist in combat room")

        # Bot should be able to attack NPC
        result = services.process_bot_ai(self.bot)

        # Debug output
        self.bot.refresh_from_db()
        self.npc.refresh_from_db()

        # Check if bot attacked (either killed NPC or started combat)
        # The NPC has exp_drop=20, so bot should have gained 10 (50% rate) if killed
        # Or bot should be in combat if NPC survived
        self.assertTrue(
            self.bot.exp > 0 or self.bot.last_combat_npc is not None,
            f"Bot should have EXP or be in combat. EXP={self.bot.exp}, last_combat_npc={self.bot.last_combat_npc}, NPC HP={self.npc.hp}, result={result}",
        )

    def test_bot_combat_tick_in_combat(self):
        """Test that bots in combat get their combat ticks processed."""
        # Create a fresh NPC with more HP to survive the first attack
        npc = NPC.objects.create(
            name="Durable NPC",
            location=self.combat_room,
            hp=100,
            hp_max=100,
            attack=5,
            defense=2,
            lvl=2,
            money_drop=10,
            exp_drop=20,
        )

        # Start combat
        services.attack_target(self.bot, "Durable NPC", auto=True)
        self.bot.refresh_from_db()

        # Set last_combat_tick to the past to simulate time passing
        from django.utils import timezone
        import datetime

        self.bot.last_combat_tick = timezone.now() - datetime.timedelta(seconds=5)
        self.bot.save(update_fields=["last_combat_tick"])

        # Process combat tick
        result = services.process_combat_tick(self.bot)

        # Should have combat output
        self.assertTrue(len(result) > 0)
        self.assertIn("hit", result.lower())

    def test_bot_exp_gain_slower_than_human(self):
        """Test that bots gain EXP at 50% rate compared to humans."""
        # Create a human player for comparison
        human_user = User.objects.create_user(username="HumanPlayer", password="password")
        human = Player.objects.create(
            user=human_user,
            location=self.combat_room,
            hp=100,
            hp_max=100,
            attack=15,
            defense=5,
            money=50,
            online=True,
            is_bot=False,
            lvl=5,
        )

        # Create fresh NPC for each
        npc1 = NPC.objects.create(
            name="NPC1",
            location=self.combat_room,
            hp=1,
            hp_max=1,
            attack=5,
            defense=2,
            lvl=2,
            money_drop=10,
            exp_drop=100,
        )
        npc2 = NPC.objects.create(
            name="NPC2",
            location=self.combat_room,
            hp=1,
            hp_max=1,
            attack=5,
            defense=2,
            lvl=2,
            money_drop=10,
            exp_drop=100,
        )

        # Human kills NPC
        services.attack_target(human, "NPC1", auto=True)
        human_exp = human.exp

        # Bot kills NPC
        services.attack_target(self.bot, "NPC2", auto=True)
        bot_exp = self.bot.exp

        # Bot should have gained 50% of the EXP (50 instead of 100)
        self.assertEqual(bot_exp, 50)
        self.assertEqual(human_exp, 100)
