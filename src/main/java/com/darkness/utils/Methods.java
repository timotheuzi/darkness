package com.darkness.utils;

import com.darkness.db.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;

@Component
public class Methods {

	@Autowired UserRepo userRepos;
	@Autowired MapRepo mapRepos;
	@Autowired ItemsRepo itemsRepos;
	@Autowired NpcRepo npcRepos;
	@Autowired CacheRepo cacheRepos;

	private final Random rand = new Random();

	public void initializeMapValues() {
		MapDB mapDB = new MapDB();
		long count = mapRepos.count();
		mapDB.setName("map_" + (count + 1));
		if (count == 0) {
			mapDB.setDescription(DarknessConstants.map_0);
		} else if ((count % 2) == 0) {
			mapDB.setDescription(DarknessConstants.map_1);
		} else {
			mapDB.setDescription(DarknessConstants.map_2);
		}
		mapDB.setItems(0); mapDB.setNpcs(0); mapDB.setUsers(0);
		mapRepos.save(mapDB);
	}

	public void initializeNpcValues() {
		NpcDB npcDB = new NpcDB();
		if (npcRepos.count() == 0) {
			npcDB.setName("Frank");
			npcDB.setDescription(DarknessConstants.npc_0);
			npcDB.setLocation(1);
			npcDB.setAttack(75); npcDB.setDefense(75); npcDB.setHp(3000);
		} else {
			npcDB.setName(getMeAgoodName());
			npcDB.setDescription(DarknessConstants.npc_1);
			npcDB.setLocation(2);
			npcDB.setAttack(rand.nextInt(50));
			npcDB.setDefense(rand.nextInt(10));
			npcDB.setHp(rand.nextInt(1000));
		}
		npcRepos.save(npcDB);
	}

	public Boolean createNewUser(String name) {
		UserDB existing = userRepos.findByName(name);
		if (existing != null) return false;

		UserDB newEntry = new UserDB();
		newEntry.setName(name);
		newEntry.setLvl(1); newEntry.setMoney(1); newEntry.setExp(1);
		newEntry.setAttack(1); newEntry.setDefense(1);
		newEntry.setDescription("A weak vagrant with no weapon");
		newEntry.setLocation(1); newEntry.setHp(1000);
		userRepos.save(newEntry);
		return true;
	}

	public HashMap<String, Integer> getStats(String name) {
		UserDB u = userRepos.findByName(name);
		HashMap<String, Integer> stats = new HashMap<>();
		if (u != null) {
			stats.put("ID", u.getId());
			stats.put("attack", u.getAttack());
			stats.put("defense", u.getDefense());
			stats.put("exp", u.getExp());
			stats.put("location", u.getLocation());
			stats.put("lvl", u.getLvl());
			stats.put("money", u.getMoney());
		}
		return stats;
	}

	public Integer CountMaps() { return (int) mapRepos.count(); }
	public Integer CountUsers() { return (int) userRepos.count(); }
	public Integer CountNpcs() { return (int) npcRepos.count(); }

	public Map<Integer, String> ShowUsersInLocation(Integer location) {
		return userRepos.findByLocation(location).stream()
				.collect(Collectors.toMap(UserDB::getId, UserDB::getName));
	}

	public Map<Integer, String> ShowNpcsInLocation(Integer location) {
		return npcRepos.findByLocation(location).stream()
				.collect(Collectors.toMap(NpcDB::getId, NpcDB::getName));
	}

	public Map<Integer, String> mapStatus(Integer mapIndex) {
		Map<Integer, String> mapObj = new HashMap<>();
		int count = 0;
		for (String name : ShowUsersInLocation(mapIndex).values()) mapObj.put(count++, name);
		for (String name : ShowNpcsInLocation(mapIndex).values()) mapObj.put(count++, name);
		return mapObj;
	}

	public Integer move(String name) {
		long mapCount = mapRepos.count();
		if (mapCount < 11) initializeMapValues();
		int newLoc = rand.nextInt((int)mapCount + 1);
		
		UserDB u = userRepos.findByName(name);
		if (u != null) {
			u.setLocation(newLoc);
			userRepos.save(u);
		}
		return newLoc;
	}

	public String getMeAgoodName() {
		String vocals = "aeiou";
		String cons = "bcdfghjklmnpqrstvwxyz";
		StringBuilder name = new StringBuilder();
		int length = rand.nextInt(5) + 3;
		for (int i = 0; i < length; i++) {
			name.append(i % 2 == 0 ? cons.charAt(rand.nextInt(cons.length())) : vocals.charAt(rand.nextInt(vocals.length())));
		}
		return name.substring(0, 1).toUpperCase() + name.substring(1);
	}
}