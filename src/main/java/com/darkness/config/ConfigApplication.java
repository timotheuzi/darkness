package com.darkness.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.darkness.utils.Methods;

@Configuration
public class ConfigApplication<config> {

	// ##################################################################################################
	// method Bean
	// ##################################################################################################

	@Bean
	public Methods methods() {
		Methods methods = new Methods();

		return methods; // rtest
	}

}