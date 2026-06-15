package com.darkness.controller;

import com.darkness.db.UserDB;
import com.darkness.db.UserRepo;
import com.darkness.utils.DarknessConstants;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

@Controller
public class ThymeleafController {

    @Autowired
    UserRepo uRepo;

    @RequestMapping("/")
    public String index() {
        return "redirect:/game";
    }

    @GetMapping("/game")
    public String game() {
        return "game";
    }

    @GetMapping("/home")
    public Mono<String> home(@RequestParam(name = "name", required = false) String name, Model model) {
        return Mono.fromCallable(() -> {
            UserDB u = uRepo.findByName(name);
            if (u != null) {
                model.addAttribute("name", u.getName());
            }
            model.addAttribute("mapInfo", DarknessConstants.map_0);
            model.addAttribute("npcInfo", DarknessConstants.npc_0);
            return "home";
        }).subscribeOn(Schedulers.boundedElastic());
    }
}