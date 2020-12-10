package com.darkness;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;;

//@SpringBootTest(classes = configApplication.class)
@SpringBootApplication
public class Darkness {

	public static void main(String[] args) {
		SpringApplication app = new SpringApplication(Darkness.class);
		System.out.print("Starting darkness with Args: [");
		for (String s : args) {
			System.out.print(s + " ");
		}
		System.out.println("]");
		app.run(args);
	}
}
