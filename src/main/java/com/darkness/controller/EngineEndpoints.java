package com.darkness.controller;

import com.darkness.db.*;
import com.darkness.utils.DarknessConstants;
import com.darkness.utils.Methods;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.util.HashMap;
import java.util.Map;

/**
 * In game engine endpoints. 
 * Refactored for reactive execution to ensure high throughput.
 */
@RestController
public class EngineEndpoints {

	@Autowired
	UserRepo repository;
	@Autowired
	MapRepo maprepo;
	@Autowired
	Methods Methods;
	@Autowired
	CacheRepo cacheRepos;

	@GetMapping(path = "/createNewUser", produces = MediaType.TEXT_HTML_VALUE)
	public Mono<String> createNewUser(@RequestParam(name = "name") String name) {
		return Mono.fromCallable(() -> {
			if (Methods.createNewUser(name)) {
				return "New User Created name " + name + " created....";
			} else {
				return "User already exists, logging in using " + name;
			}
		}).subscribeOn(Schedulers.boundedElastic());
	}

	@GetMapping(path = "/getFullInformation", produces = MediaType.APPLICATION_JSON_VALUE)
	public Mono<Map<String, Integer>> getFullInformation(@RequestParam(name = "name") String name) {
		return Mono.fromCallable(() -> Methods.getStats(name))
				.subscribeOn(Schedulers.boundedElastic());
	}

	@GetMapping("/CountMaps")
	public Mono<Integer> CountMaps() {
		return Mono.fromCallable(() -> Methods.CountMaps())
				.subscribeOn(Schedulers.boundedElastic());
	}

	@GetMapping(path = "/initializeMap", produces = MediaType.TEXT_HTML_VALUE)
	public Mono<String> initializeMap() {
		return Mono.fromRunnable(() -> Methods.initializeMapValues())
				.subscribeOn(Schedulers.boundedElastic())
				.thenReturn("Success initializing map values");
	}

	@GetMapping(path = "/variousInput", produces = MediaType.APPLICATION_JSON_VALUE)
	public Mono<Map<String, String>> various(@RequestParam(name = "name") String name,
					   @RequestParam(name = "value", defaultValue = "") String value,
					   @RequestParam(name = "location", defaultValue = "0") Integer location) {
		return Mono.fromCallable(() -> {
			Map<String, String> output = new HashMap<>();
			String val = value.replaceAll(",", "").toLowerCase();
			
			if (val.contains("move")) {
				Methods.move(name);
				output.put("mapInfo", DarknessConstants.map_1);
				output.put("npcInfo", DarknessConstants.npc_1);
				return output;
			} else {
				output.put("msg", "No implementation for that string yet");
				return output;
			}
		}).subscribeOn(Schedulers.boundedElastic());
	}

	@GetMapping(path = "/updateRoom", produces = MediaType.APPLICATION_JSON_VALUE)
	public Mono<Map<Integer, String>> updateRoom(@RequestParam(name = "mapIndex", required = false) Integer mapIndex) {
		return Mono.fromCallable(() -> Methods.mapStatus(mapIndex))
				.subscribeOn(Schedulers.boundedElastic());
	}
}