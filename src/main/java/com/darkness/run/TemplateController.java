package com.darkness.run;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.darkness.db.MapRepo;
import com.darkness.db.NpcRepo;
import com.darkness.db.UserDB;
import com.darkness.db.UserRepo;
import com.darkness.utils.Methods;

@Controller
public class TemplateController {
	// @Autowiredtest
	// private methods Methods;
	// @Value("${hellodfsdf}")
	// this.msg;
	@Autowired
	UserRepo uRepo;

	@Autowired
	MapRepo mRepo;

	@Autowired
	NpcRepo nRepo;

	@Autowired
	Methods methods;

	@RequestMapping("/")
	public String index() {
		methods.initializeMapValues();
		methods.initializeItemValues();
		methods.initializeNpcValues();
		return "index";
	}

	@GetMapping("/greeting")
	public String greeting(@RequestParam(name = "name", required = false, defaultValue = "World") String name,
			Model model) {
		model.addAttribute("name", name);
		UserDB newEntry = new UserDB();
		// newEntry.setId(id);
		newEntry.setName(name);
		newEntry.setLvl(1);
		newEntry.setMoney(1);
		newEntry.setExp(1);
		newEntry.setAttack(1);
		newEntry.setDefense(1);
		newEntry.setDescription("A weak noob with no weapon");
		newEntry.setLocation(1);
		uRepo.save(newEntry);
		return "greeting";
	}

	// home map
	@GetMapping("/home")
	public String home(@RequestParam(name = "name", required = false) String name, Model model) {
		Integer currentMap = null;
		// methods.initializeMapValues();
		// String userName = uRepo.findByName(name).getName();
		currentMap = mRepo.findById(1).get().getId();// Math.random() * ((methods.CountMaps() - 1) + 1);
		// uRepo.findByName(name).setLocation();
		model.addAttribute("name", uRepo.findByName(name).getName());
		model.addAttribute("mapName", mRepo.findById(currentMap.intValue()).get().getMapName());
		model.addAttribute("description", mRepo.findById(currentMap.intValue()).get().getDescription());
		model.addAttribute("npcs", methods.ShowNpcsInLocation(currentMap));
		model.addAttribute("users", methods.ShowUsersInLocation(currentMap));
		model.addAttribute("location", currentMap);
		return "home";
	}

	@GetMapping("/template_1")
	public String template_1(@RequestParam(name = "name", required = true) String name, Model model) {
		// methods.initializeMapValues();
		Integer currentMap = methods.move(name);
		uRepo.findByName(name).setLocation(currentMap.intValue());
		// methods.initializeNpcValues();
		model.addAttribute("name", uRepo.findByName(name).getName());
		model.addAttribute("mapName", mRepo.findById(currentMap.intValue()).get().getMapName());
		model.addAttribute("description", mRepo.findById(currentMap.intValue()).get().getDescription());
		/// model.addAttribute("nps", mRepo.findById(currentMap.intValue()).getNpcs());
		// model.addAttribute("users",
		/// mRepo.findById(currentMap.intValue()).getUsers());
		model.addAttribute("npcs", methods.ShowNpcsInLocation(currentMap.intValue()));
		model.addAttribute("users", methods.ShowUsersInLocation(currentMap.intValue()));
		model.addAttribute("location", currentMap);
		return "template_1";
	}

}