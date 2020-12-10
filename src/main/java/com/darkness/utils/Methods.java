package com.darkness.utils;

import java.io.StringWriter;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Random;
import java.util.Set;

import com.darkness.db.UserRepo;
import com.darkness.db.ItemsDB;
import com.darkness.db.ItemsRepo;
import com.darkness.db.MapDB;
import com.darkness.db.MapRepo;
import com.darkness.db.NpcDB;
import com.darkness.db.NpcRepo;
import com.darkness.db.UserDB;
import com.darkness.db.CacheRepo;
import com.darkness.db.CacheDB;

import com.darkness.run.*;

import org.json.JSONException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.ui.Model;

public class Methods {

	@Autowired
	UserRepo userRepos;

	@Autowired
	MapRepo mapRepos;

	@Autowired
	ItemsRepo itemsRepos;

	@Autowired
	NpcRepo npcRepos;

	@Autowired
	CacheRepo cacheRepos;

	@Autowired
	TemplateController templateController;

	// public Integer mapCount = 0;
	// private Integer npcCount = 0;
	// private Integer itemCount = 0;
	// private Integer items, npcs, users, attack, defense;
	// private String name, description;

	private String map_0 = "An empty bar";
	private String map_1 = "A dark street corner";
	private String map_2 = "A dark alley";

	private String npc_0 = "Burly Bartender";
	private String npc_1 = "Vagrant";

	private String item_1 = "sterling";

	public void initializeMapValues() {
		Integer mapCount = CountMaps();
		MapDB mapDB = new MapDB();
		mapDB.setMapName("map_" + (CountMaps() + 1));
		if (CountMaps() == 0) {
			mapDB.setDescription(map_0);
		} else if ((CountMaps() & 1) == 0) {
			mapDB.setDescription(map_1);
		} else {
			mapDB.setDescription(map_2);
		}
		mapDB.setItems(0);
		mapDB.setNpcs(0);
		mapDB.setUsers(0);
		mapRepos.save(mapDB);
		// mapCount++;
	}

	public void initializeItemValues() {
		Integer itemCount = 0;
		Double attack = Math.random() * ((10 - 1) + 1);
		Double defense = Math.random() * ((5 - 1) + 1);
		ItemsDB itemsDB = new ItemsDB();
		itemsDB.setName("gun	_" + itemCount.toString());
		itemsDB.setDescription(item_1);
		itemsDB.setAttack(attack.intValue());
		itemsDB.setDefense(defense.intValue());
		// itemsDB.location(0);
		itemsRepos.save(itemsDB);
		itemCount++;
	}

	public void initializeNpcValues() {
		Double attack = Math.random() * ((50 - 1) + 1);
		Double defense = Math.random() * ((10 - 1) + 1);
		Double hp = Math.random() * ((1000 - 1) + 1);
		NpcDB npcDB = new NpcDB();
		if (CountNpcs() == 0) {
			npcDB.setName("Frank");
			npcDB.setDescription(npc_0);
			npcDB.setLocation(1);
			npcDB.setAttack(75);
			npcDB.setDefense(75);
			npcDB.setHp(3000);
		} else {
			npcDB.setName(getMeAgoodName());
			npcDB.setDescription(npc_1);
			npcDB.setLocation(2);
			npcDB.setAttack(attack.intValue());
			npcDB.setDefense(defense.intValue());
			npcDB.setHp(hp.intValue());
		}

		npcRepos.save(npcDB);
		// npcCount++;
	}

	public Boolean createNewUser(String name) {
		try {
			UserDB result = userRepos.findByName(name);
			result.getName();
			result.getLvl();
			result.getMoney();
			result.getExp();
			result.getAttack();
			result.getDefense();
			result.getDescription();
			result.getLocation();
			result.getHp();
			String test = result.toString();
			System.out.println("record does exist:" + test);
			return false;
		} catch (Exception e) {
			System.out.println("record doesnt exist, creating it");
		}
		UserDB newEntry = new UserDB();
		// newEntry.setId(id);
		newEntry.setName(name);
		newEntry.setLvl(1);
		newEntry.setMoney(1);
		newEntry.setExp(1);
		newEntry.setAttack(1);
		newEntry.setDefense(1);
		newEntry.setDescription("A weak vagrant with no weapon");
		newEntry.setLocation(1);
		newEntry.setHp(1000);
		userRepos.save(newEntry);
		return true;
	}

	public HashMap<String, Integer> getStats(String name, Boolean user) {
		HashMap<String, Integer> stats = new HashMap<String, Integer>();
		if (user) {
			stats.put("ID", userRepos.findByName(name).getId());
			stats.put("attack", userRepos.findByName(name).getAttack());
			stats.put("defense", userRepos.findByName(name).getDefense());
			stats.put("exp", userRepos.findByName(name).getExp());
			stats.put("location", userRepos.findByName(name).getLocation());
			stats.put("lvl", userRepos.findByName(name).getLvl());
			stats.put("money", userRepos.findByName(name).getMoney());
		} else {
			stats.put("ID", npcRepos.findByName(name).getId());
			stats.put("attack", npcRepos.findByName(name).getAttack());
			stats.put("defense", npcRepos.findByName(name).getDefense());
			stats.put("hp", npcRepos.findByName(name).getHp());
			stats.put("location", npcRepos.findByName(name).getLocation());
			// stats.put("name", npcRepos.findByName(name).);
		}
		return stats;
	}

	// counters
	public Integer CountMaps() {
		// String result = "";
		Integer count = 0;
		for (MapDB mapDB : mapRepos.findAll()) {
			count++;
		}
		return count;
	}

	public Integer CountUsers() {
		Integer count = 0;
		for (UserDB userdb : userRepos.findAll()) {
			count++;
		}
		return count; // + "response" + response;
	}

	public Integer CountItems() {
		Integer count = 0;
		for (ItemsDB itemdb : itemsRepos.findAll()) {
			count++;
		}
		return count;
	}

	public Integer CountNpcs()
	{
		Integer count = 0;
		for(NpcDB itemdb : npcRepos.findAll())
		{
				count++;
		}
		return count;
	}

	public String CountNpcsByLocation(Integer location) {
		StringWriter npcs = new StringWriter();
		Integer count = 0;
		for (NpcDB npcDB : npcRepos.findAll()) {
			if (npcDB.getLocation() == location) {
				npcs.write(npcDB.getName() + ",");
				count++;
			}
		}
		return npcs.toString();
	}

	public String CountUsersByLocation(Integer location) {
		StringWriter users = new StringWriter();
		Integer count = 0;
		for (UserDB userDB : userRepos.findAll()) {
			if (userDB.getLocation() == location) {
				users.write(userDB.getName() + ",");
				count++;
			}
		}
		return users.toString();
	}

	public HashMap<Integer, String> ShowUsersInLocation(Integer index) {
		HashMap<Integer, String> users = new HashMap<Integer, String>();
		for (UserDB userDB : userRepos.findAll()) {
			if (userDB.getLocation() == index) {
				users.put(userDB.getId(), userDB.getName());
			}
		}
		return users; // + "response" + response;
	}

	public HashMap<Integer, String> ShowNpcsInLocation(Integer index) {
		HashMap<Integer, String> npcs = new HashMap<Integer, String>();
		for (NpcDB npcDB : npcRepos.findAll()) {
			if (npcDB.getLocation() == index) {
				npcs.put(npcDB.getId(), npcDB.getName());
			}
		}
		return npcs; // + "response" + response;

	}

	public Integer move(String name) {
		if (CountMaps() < 11) {
			initializeMapValues();
		}
		Double location = Math.random() * ((CountMaps()));
		// random NPC generation and movement
		Double npcToMove = Math.random() * ((CountNpcs()));
		int temp = npcToMove.intValue();
		npcRepos.findById(temp).get().setLocation(location.intValue());
		userRepos.findByName(name).setLocation(location.intValue());
		// Model model = null;
		// templateController.template_1(name, model);
		return location.intValue();
	}

	public Map mapStatus(Integer mapIndex) {
		HashMap mapObj = new HashMap();
		int count = 0;
		Iterator itUser = (ShowUsersInLocation(mapIndex)).entrySet().iterator();
		while (itUser.hasNext()) {
			Map.Entry pair = (Map.Entry) itUser.next();
			mapObj.put(count, pair.getValue());
			itUser.remove(); // avoids a ConcurrentModificationException
			count++;
		}
		Iterator itNpc = (ShowNpcsInLocation(mapIndex)).entrySet().iterator();
		while (itNpc.hasNext()) {
			Map.Entry pair = (Map.Entry) itNpc.next();
			mapObj.put(count, pair.getValue());
			itNpc.remove(); // avoids a ConcurrentModificationException
			count++;
		}
		for (CacheDB cacheDB : cacheRepos.findAll()) {
			mapObj.put(count, cacheDB.getCurrentStatis());
			count++;
		}

		return mapObj;
	}

	//// get individual user or npc
	public String getUserByName(String name) {
		return userRepos.findByName(name).getName();
	}

	public String getNpcByName(String name) {
		return npcRepos.findByName(name).getName();
	}

	public String getUserByIndex(Integer index) {
		return userRepos.findById(index).get().getName();
	}

	public String getNpcByIndex(Integer index) {
		return npcRepos.findById(index).get().getName();
	}

	public String getStatus(String where) {
		return where;
	}

	public Map findUserStatsByName(String name) throws JSONException {
		HashMap userObj = new HashMap();

		try {
			userObj.put("name", userRepos.findByName(name).getName());
			userObj.put("attack", userRepos.findByName(name).getAttack());
			userObj.put("defense", userRepos.findByName(name).getDefense());
			userObj.put("description", userRepos.findByName(name).getDescription());
			userObj.put("exp", userRepos.findByName(name).getExp());
			userObj.put("hp", userRepos.findByName(name).getHp());
			userObj.put("location", userRepos.findByName(name).getLocation());
			userObj.put("lvl", userRepos.findByName(name).getLvl());
			userObj.put("money", userRepos.findByName(name).getMoney());
			userObj.put("name", userRepos.findByName(name).getName());
		} catch (Exception e) {
			e.printStackTrace();
			return (HashMap) userObj.put("error", e.toString());
		}
		return userObj;
	}

	public static String getMeAgoodName() {
		Random rand = new Random();
		String vocals = "aeiou" + "ioaeu" + "ouaei";
		String cons = "bcdfghjklznpqrst" + "bcdfgjklmnprstvw" + "bcdfgjklmnprst";
		// String allchars = vocals + cons;
		int length = rand.nextInt(8);
		if (length < 3)
			length = 3;
		// int consnum = 1;
		int consnum = 1;
		String name = "";
		String touse;
		char c;

		for (int i = 0; i < length; i++) {
			if (consnum == 2) {
				touse = vocals;
				if (length != 2) {
					consnum = rand.nextInt(2);
				} else {
					consnum = 1;
				}
			} else
				touse = cons;
			// pick a random character from the set we are goin to use.
			c = touse.charAt(rand.nextInt(touse.length()));
			name = name + c;
			if (cons.indexOf(c) != -1)
				consnum++;
			if (vocals.indexOf(c) != -1)
				consnum = consnum - 1;
		}
		name = name.charAt(0) + name.substring(1, name.length());
		System.out.println(name);
		return name;

	}

	public void updateCache(Integer location, String msg) {
		CacheDB newCacheEntry = new CacheDB();
		newCacheEntry.setCurrentStatus(msg);
		newCacheEntry.setMapName("map_" + location);
		cacheRepos.save(newCacheEntry);
		// return Methods.getNpcByIndex(index);
	}
}
