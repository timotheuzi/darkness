package com.darkness.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.darkness.utils.Methods;
import org.springframework.context.annotation.Primary;

import javax.sql.DataSource;

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

	/*@Bean
	@Primary
	@ConfigurationProperties(prefix="spring.datasource")
	public DataSource primaryDataSource() {
		return DataSourceBuilder.create().build();
	}*/

	/*@Bean
	@ConfigurationProperties(prefix="spring.secondDatasource")
	public DataSource secondaryDataSource() {
		return DataSourceBuilder.create().build();
	}*/

}