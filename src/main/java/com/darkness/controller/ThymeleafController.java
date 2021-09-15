package com.darkness.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import com.darkness.db.MapRepo;
import com.darkness.db.UserDB;
import com.darkness.db.UserRepo;
import com.darkness.db.NpcRepo;
import com.darkness.utils.Methods;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;

@Controller
public class ThymeleafController {

	@Autowired
	UserRepo uRepo;
	
	@Autowired
	MapRepo mRepo;
	
	@Autowired
	NpcRepo nRepo;
	
	@Autowired
	Methods methods;

	//default index/user creation page
	@RequestMapping("/")
    public String index() 
	{
		methods.initializeMapValues();
		methods.initializeItemValues();
		methods.initializeNpcValues();
	    return "index";
	}
    // main home page template
    @GetMapping("/home")
    public String home(@RequestParam(name="name", required=false) String name, Model model) 
	{
    	//methods.randomNpcMove();
		Integer currentMap = null;
		//methods.initializeMapValues();
		//String userName = uRepo.findByName(name).getName();
		currentMap = mRepo.findById(1).get().getId();//Math.random() * ((methods.CountMaps() - 1) + 1);
		//uRepo.findByName(name).setLocation();
		model.addAttribute("name", uRepo.findByName(name).getName());
		return "home";
		/*model.addAttribute("mapName", mRepo.findById(currentMap.intValue()).get());
		model.addAttribute("description", mRepo.findById(currentMap.intValue()).get().());
		model.addAttribute("npcs", methods.ShowNpcsInLocation(currentMap));
		model.addAttribute("users", methods.ShowUsersInLocation(currentMap));   
		model.addAttribute("location", currentMap);   */
    }

    //todo administration thymeleaf template
    @GetMapping("/template_1")
    public String template_1(@RequestParam(name="name", required=true) String name, Model model) 
	{//methods.initializeNpcValues();
		model.addAttribute("name", uRepo.findByName(name).getName());
		/*model.addAttribute("mapName", mRepo.findById(currentMap.intValue()).get().getMapName());
		model.addAttribute("description", mRepo.findById(currentMap.intValue()).get().getDescription());
		///model.addAttribute("nps", mRepo.findById(currentMap.intValue()).getNpcs());
		//model.addAttribute("users", mRepo.findById(currentMap.intValue()).getUsers());   
		model.addAttribute("npcs", methods.ShowNpcsInLocation(currentMap.intValue()));
		model.addAttribute("users", methods.ShowUsersInLocation(currentMap.intValue()));
		model.addAttribute("location", currentMap); */
		return "template_1";
    }
}