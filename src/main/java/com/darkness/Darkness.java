package com.darkness;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.web.reactive.config.EnableWebFlux;

@EnableWebFlux
@SpringBootApplication
@EnableScheduling
public class Darkness {

	public static void main(String[] args) {
		SpringApplication app = new SpringApplication(Darkness.class);
		System.out.println("Starting Darkness MUD Server...");
		app.run(args);
	}
}