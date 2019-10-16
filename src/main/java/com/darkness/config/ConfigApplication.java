package com.darkness.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.darkness.utils.methods;

@Configuration
public class ConfigApplication<config> {

	// ##################################################################################################
	// method Bean
	// ##################################################################################################

	@Bean
	public methods methods() {
		methods methods = new methods();

		return methods; // rtest
	}

}