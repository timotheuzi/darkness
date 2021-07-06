package com.darkness.controller;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.json.JSONException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.darkness.db.CacheRepo;
import com.darkness.db.MapDB;
import com.darkness.db.MapRepo;
import com.darkness.db.UserDB;
import com.darkness.db.UserRepo;
import com.darkness.utils.Methods;

/**
 * In game controller endpoints Author: Timotheuzi
 */

@RestController
public class ControllerClass {

	@Autowired
	UserRepo repository;
	@Autowired
	MapRepo maprepo;
	@Autowired
	Methods Methods;
	@Autowired
	CacheRepo cacheRepos;
	@Autowired
	TemplateController tempController;

	@RequestMapping(method = RequestMethod.GET, path = "/createNewUser", produces = MediaType.TEXT_HTML_VALUE)
	public String createNewUser(@RequestParam(name = "name", required = true) String name) {

		if (Methods.createNewUser(name)) {
			return "New User Created name " + name + " created....";
		} else {
			return "User already exists, logging in using " + name + " and redirect to home";
		}
	}

	@RequestMapping(method = RequestMethod.GET, path = "/setUser", produces = MediaType.APPLICATION_JSON_VALUE)
	public String setUser(@RequestParam(name = "name", required = true) String name,
						  @RequestParam(name = "lvl", required = false) Integer lvl,
						  @RequestParam(name = "money", required = false) Integer money,
						  @RequestParam(name = "exp", required = false) Integer exp,
						  @RequestParam(name = "attack", required = false) Integer attack,
						  @RequestParam(name = "defense", required = false) Integer defense,
						  @RequestParam(name = "description", required = false) String description,
						  @RequestParam(name = "location", required = false) Integer location,
						  @RequestParam(name = "hp", required = false) Integer hp) {

		repository.findByName(name);
		int id = repository.findByName(name).getId();

		UserDB newEntry = new UserDB();
		newEntry.setId(id);
		newEntry.setName(name);
		if (lvl != null) {
			newEntry.setLvl(lvl);
		} else {
			newEntry.setLvl(repository.findByName(name).getLvl());
		}

		if (money != null) {
			newEntry.setMoney(money);
		} else {
			newEntry.setMoney(repository.findByName(name).getMoney());
		}

		if (exp != null) {
			newEntry.setExp(exp);
		} else {
			newEntry.setExp(repository.findByName(name).getExp());
		}

		if (attack != null) {
			newEntry.setAttack(attack);
		} else {
			newEntry.setAttack(repository.findByName(name).getAttack());
		}

		if (defense != null) {
			newEntry.setDefense(defense);
		} else {
			newEntry.setDefense(repository.findByName(name).getDefense());
		}

		if (description != null) {
			newEntry.setDescription(description);
		} else {
			newEntry.setDescription(repository.findByName(name).getDescription());
		}

		if (location != null) {
			newEntry.setLocation(location);
		} else {
			newEntry.setDescription(repository.findByName(name).getDescription());
		}

		if (hp != null) {
			newEntry.setLocation(hp);
		} else {
			newEntry.setHp(repository.findByName(name).getHp());
		}

		repository.save(newEntry);
		return newEntry.toString();
	}

	@RequestMapping(method = RequestMethod.GET, path = "/getFullInformation", produces = MediaType.APPLICATION_JSON_VALUE)
	public Map getFullInformation(@RequestParam(name = "name", required = true) String name,
								  @RequestParam(name = "user", required = false, defaultValue = "user") String user) {
		Map<String, Integer> info = new HashMap<String, Integer>();
		Boolean userNpc = true;
		if (user.contains("npc")) {
			userNpc = false;
		}
		info = Methods.getStats(name, userNpc);
		return info;
	}

	/*
	 * @GetMapping("/CountUsers") public Integer findAll(){
	 *
	 * String result = ""; Integer count = 0; for(userDB userDB :
	 * repository.findAll()) { count++; result += userDB.getId() + "</br>"; }
	 * //Response response = new Response("Done", 1); return count; // + "response"
	 * + response; }
	 */
	@GetMapping("/CountMaps")
	public Integer CountMaps() {
		String result = "";
		// MapRepo = new MapRepo;
		// List<maprepo> = maprepo;
		Integer count = 0;
		for (MapDB mapDB : maprepo.findAll()) {
			count++;
		}
		return count;
	}

	@SuppressWarnings("static-access")
	// @GetMapping("/initializeMap")
	@RequestMapping(method = RequestMethod.GET, path = "/initializeMap", produces = MediaType.TEXT_HTML_VALUE)
	public String initializeMap() {
		// Response response =
		Methods.initializeMapValues();
		return "Success";
	}

	// @GetMapping("/initializeNpc")
	@RequestMapping(method = RequestMethod.GET, path = "/initializeNpc", produces = MediaType.TEXT_HTML_VALUE)
	public String initializeNpc() {
		Methods.initializeNpcValues();
		return "Success";
	}

	// @GetMapping("/initializeItem")
	@RequestMapping(method = RequestMethod.GET, path = "/initializeItem", produces = MediaType.TEXT_HTML_VALUE)
	public String initializeItem() {
		Methods.initializeItemValues();
		return "Success";
	}

	// @GetMapping("/various")
	@RequestMapping(method = RequestMethod.GET, path = "/various", produces = MediaType.APPLICATION_JSON_VALUE) // consumes
	// =
	// MediaType.APPLICATION_JSON_VALUE,
	// consumes
	// =
	// MediaType.APPLICATION_JSON_VALUE,
	public Map various(Integer location, String value, String name) throws JSONException {
		// Map<String, String> map = requestForm.get(arg0);
		// String loca = requestForms.get("location").toString();
		// String value = requestForms.get("value").toString();
		// String name = requestForms.get("name").toString();
		// Integer location = Integer.parseInt(loca);
		if (!value.isEmpty()) {
			value = value.replaceAll(",", "");
			Methods.updateCache(location, value);
		}
		Map<String, String> output = new HashMap<String, String>();
		// output.put("msg", value);
		// output.put("location", location.toString());
		// cacheRepos.save(output);
		if (value.toLowerCase().contains("move")) {
			Methods.move(name);
			// output.put("users", Methods.ShowUsersInLocation(location).toString());
			// output.put("npcs", Methods.ShowNpcsInLocation(location).toString());
			// output.put("description", maprepo.findById(location).get().getDescription());

			// Model model = null;
			// tempController.template_1(name, model);
			return output;
		} else if (value.toLowerCase().contains("inv")
				&& value.toLowerCase().contains(Methods.ShowNpcsInLocation(location).toString())) {
			Iterator it = Methods.ShowNpcsInLocation(location).entrySet().iterator();
			while (it.hasNext()) {
				Map.Entry pair = (Map.Entry) it.next();
				if (value.contains(pair.getValue().toString())) {
					return Methods.getStats(pair.getValue().toString(), false);
				}
				it.remove(); // avoids a ConcurrentModificationException
			}
		} else if (value.toLowerCase().contains("inv")
				&& value.toLowerCase().contains(Methods.ShowUsersInLocation(location).toString())) {
			Iterator it = Methods.ShowUsersInLocation(location).entrySet().iterator();
			while (it.hasNext()) {
				Map.Entry pair = (Map.Entry) it.next();
				if (value.contains(pair.getValue().toString())) {
					return Methods.getStats(pair.getValue().toString(), true);
				}
				it.remove(); // avoids a ConcurrentModificationException
			}
		} else if (value.toLowerCase().contains("inv")) {
			return Methods.getStats(name, true);
		} else {
			output.put("msg", "No implementation for that string yet");
			return output;
		}
		// Map error = (error, "error happened");
		return output;
	}

	// @GetMapping("/updateRoom")
	@RequestMapping(method = RequestMethod.GET, path = "/updateRoom", produces = MediaType.APPLICATION_JSON_VALUE)
	public Map updateRoom(@RequestParam(name = "mapIndex", required = false) Integer mapIndex) {
		if (mapIndex != null) {
			return Methods.mapStatus(mapIndex);
		} else {

			return Methods.mapStatus(mapIndex);
		}
	}

	// @GetMapping("/findUserName")
	@RequestMapping(method = RequestMethod.GET, path = "/findUserByIndex", produces = MediaType.APPLICATION_JSON_VALUE)
	public String findUserByIndex(@RequestParam(name = "index", required = true) Integer index) {
		// int[] updateRoom = Methods.mapStatus(location);
		return Methods.getUserByIndex(index);
	}

	// @GetMapping("/findNpcName")
	@RequestMapping(method = RequestMethod.GET, path = "/findNpcByIndex", produces = MediaType.APPLICATION_JSON_VALUE)
	public String findNpcByIndex(@RequestParam(name = "index", required = true) Integer index) {
		// int[] updateRoom = Methods.mapStatus(location);
		return Methods.getNpcByIndex(index);
	}

	// @GetMapping("/findNpcName")

	/*
	 * @RequestMapping(method = RequestMethod.GET, path = "/saveCookie", produces =
	 * MediaType.APPLICATION_JSON_VALUE) public String
	 * saveCookie(@RequestParam(name="user", required=true) String cookie)
	 *
	 * {
	 *
	 * //java.util.Map<String, String> values = (java.util.Map<String, String>)
	 * form; return cookie; }
	 */
}